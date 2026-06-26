import asyncio
import json
import logging
import os
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import httpx
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .engine import calc_auto, calc_rd
from .contract_analyser import load_reference, extract_text
from .save_manager import auto_save_devis, auto_save_analyse, get_stats, export_data, save_rating, get_rating_stats, increment_counter
from .export_manager import send_export_mail
from .report_generator import full_csv, html_report
from .scoring import score_devis

# ── Configuration ────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AssurDevis", version="3.0")

# CORS — restreint en production
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE = Path(__file__).parent.parent

# ── Servir le frontend statique ──────────────────────────────────────────────
STATIC = BASE / "static"
if STATIC.exists():
    try:
        app.mount("/static", StaticFiles(directory=str(STATIC)), name="static")
        logger.info("Static files mounted: %s", STATIC)
    except Exception as e:
        logger.warning("Failed to mount static files: %s", e)

# ── Groq API Configuration ───────────────────────────────────────────────────
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

_GROQ_KEYS = [
    k for k in [
        os.getenv("GROQ_API_KEY"),
        os.getenv("GROQ_API_KEY_2"),
        os.getenv("GROQ_API_KEY_3"),
        os.getenv("GROQ_API_KEY_4"),
        os.getenv("GROQ_API_KEY_5"),
    ]
    if k
]
_groq_key_index = 0


def get_groq_key() -> str:
    return _GROQ_KEYS[_groq_key_index] if _GROQ_KEYS else ""


def rotate_groq_key():
    global _groq_key_index
    if not _GROQ_KEYS:
        return
    _groq_key_index = (_groq_key_index + 1) % len(_GROQ_KEYS)
    logger.warning(
        "Groq key rotated → key %d/%d", _groq_key_index + 1, len(_GROQ_KEYS)
    )


# ── Knowledge Base ───────────────────────────────────────────────────────────
KNOWLEDGE_DIR = BASE / "knowledge"
INSTRUCTIONS_PATH = BASE / "app" / "instructions_assurdevis.txt"

SYSTEM_PROMPT = ""
if INSTRUCTIONS_PATH.exists():
    try:
        with open(INSTRUCTIONS_PATH, encoding="utf-8") as f:
            SYSTEM_PROMPT = f.read()
        logger.info("System prompt loaded: %d chars", len(SYSTEM_PROMPT))
    except Exception as e:
        logger.warning("Failed to load system prompt: %s", e)

conversations: dict[str, dict] = {}
_REFERENCE_TEXT: str = ""

# ── Export Configuration ─────────────────────────────────────────────────────
LAST_EXPORT_FILE = BASE / "saved" / "last_export.json"
EXPORT_EMAILS = os.getenv("EXPORT_TO_EMAILS", "").strip()
EXPORT_INTERVAL_H = 24


def _check_export_due() -> bool:
    if not EXPORT_EMAILS:
        return False
    if not LAST_EXPORT_FILE.exists():
        return True
    try:
        with open(LAST_EXPORT_FILE, encoding="utf-8") as f:
            data = json.load(f)
        last = datetime.fromisoformat(data.get("exported_at", ""))
        elapsed = (datetime.now(timezone.utc) - last).total_seconds()
        return elapsed >= EXPORT_INTERVAL_H * 3600
    except Exception:
        return True


def _mark_export_done(success: bool, msg: str = ""):
    LAST_EXPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LAST_EXPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(
            {
                "exported_at": datetime.now(timezone.utc).isoformat(
                    timespec="seconds"
                ),
                "success": success,
                "message": msg,
            },
            f,
            ensure_ascii=False,
        )


async def _run_scheduled_export():
    if not EXPORT_EMAILS:
        return
    if not _check_export_due():
        return
    logger.info("Scheduled export: consolidating data...")
    try:
        data = export_data()
        recipients = [e.strip() for e in EXPORT_EMAILS.split(",") if e.strip()]
        subject = f"AssurDevis Export — {data['exported_at']}"
        all_ok = True
        for to in recipients:
            ok = await send_export_mail(to, subject, data)
            if not ok:
                logger.warning("Export failed to %s", to)
                all_ok = False
        if all_ok:
            logger.info("Export sent successfully to %d recipient(s)", len(recipients))
            _mark_export_done(True, f"Sent to {len(recipients)} recipient(s)")
        else:
            _mark_export_done(False, "Partial or total failure")
    except Exception as e:
        logger.error("Scheduled export error: %s", e)
        _mark_export_done(False, str(e))


async def _export_loop():
    while True:
        await _run_scheduled_export()
        await asyncio.sleep(3600)


# ── Startup ──────────────────────────────────────────────────────────────────
@app.on_event("startup")
async def _startup():
    global _REFERENCE_TEXT
    import sys

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    try:
        _REFERENCE_TEXT = load_reference()
    except Exception as e:
        logger.warning("Failed to load reference: %s", e)
        _REFERENCE_TEXT = ""

    asyncio.create_task(_export_loop())

    if not _GROQ_KEYS:
        logger.warning("No GROQ_API_KEY configured — AI responses will be degraded")
    else:
        logger.info("%d Groq key(s) loaded", len(_GROQ_KEYS))

    if KNOWLEDGE_DIR.exists():
        md_files = list(KNOWLEDGE_DIR.glob("*.md"))
        logger.info("Knowledge base: %d file(s) found in %s", len(md_files), KNOWLEDGE_DIR)
    else:
        logger.warning("Knowledge directory not found: %s", KNOWLEDGE_DIR)


# ── Models ───────────────────────────────────────────────────────────────────
class ChatRequest(BaseModel):
    message: str
    conversation_id: str = ""


# ── Groq API Helpers ─────────────────────────────────────────────────────────
async def check_groq() -> bool:
    """Check if active Groq key is valid."""
    if not _GROQ_KEYS:
        return False
    try:
        async with httpx.AsyncClient(timeout=8) as client:
            resp = await client.get(
                "https://api.groq.com/openai/v1/models",
                headers={"Authorization": f"Bearer {get_groq_key()}"},
            )
            return resp.status_code == 200
    except Exception:
        return False


async def query_groq(messages: list[dict]) -> str:
    """Call Groq with automatic key rotation on rate limit."""
    if not _GROQ_KEYS:
        raise RuntimeError("No Groq key configured")

    headers = {"Content-Type": "application/json"}
    payload = {
        "model": GROQ_MODEL,
        "messages": messages,
        "temperature": 0.3,
        "max_tokens": 800,
    }

    attempts = len(_GROQ_KEYS)
    for attempt in range(attempts):
        headers["Authorization"] = f"Bearer {get_groq_key()}"
        try:
            async with httpx.AsyncClient(timeout=60) as client:
                resp = await client.post(GROQ_URL, json=payload, headers=headers)
                if resp.status_code == 429:
                    rotate_groq_key()
                    continue
                resp.raise_for_status()
                text = resp.json()["choices"][0]["message"]["content"]
                try:
                    text = text.encode("latin-1").decode("utf-8", errors="ignore")
                except (UnicodeDecodeError, UnicodeEncodeError):
                    pass
                return text
        except Exception as e:
            logger.warning("Groq attempt %d failed: %s", attempt + 1, e)
            if attempt < attempts - 1:
                rotate_groq_key()
            continue

    raise RuntimeError("All Groq keys exhausted")


# ── Knowledge Search ─────────────────────────────────────────────────────────
def search_knowledge(query: str, top_k: int = 3, intent: str = "QUESTION_INFO") -> list[str]:
    """Search knowledge base by intent."""
    INTENT_FILES = {
        "QUESTION_INFO": [
            "dify_01_calcul_tarification.md",
            "dify_02_garanties_produits.md",
            "dify_03_references_legales.md",
            "dify_05_culture_assurance.md",
        ],
        "GREETING": [],
        "ORIENTATION": [
            "dify_04_processus_commercial.md",
            "dify_02_garanties_produits.md",
        ],
        "QUOTE_AUTO": [
            "dify_01_calcul_tarification.md",
            "dify_02_garanties_produits.md",
            "dify_04_processus_commercial.md",
        ],
        "QUOTE_RD": [
            "dify_02_garanties_produits.md",
            "dify_04_processus_commercial.md",
        ],
    }

    if not KNOWLEDGE_DIR.exists():
        return []

    allowed = INTENT_FILES.get(intent)
    query_lower = query.lower()
    results = []

    for md_file in sorted(KNOWLEDGE_DIR.glob("*.md")):
        if allowed is not None and md_file.name not in allowed:
            continue
        try:
            with open(md_file, encoding="utf-8") as f:
                content = f.read()
            lines = content.split("\n")
            matching_sections = []
            for i, line in enumerate(lines):
                if any(word in line.lower() for word in query_lower.split()):
                    start = max(0, i - 2)
                    end = min(len(lines), i + 10)
                    matching_sections.append("\n".join(lines[start:end]))
            if matching_sections:
                results.extend(matching_sections[:top_k])
        except Exception as e:
            logger.warning("Error reading %s: %s", md_file.name, e)

    return results[:top_k] if results else []


# ── Routes ───────────────────────────────────────────────────────────────────
@app.get("/")
async def root():
    """Serve index.html or status JSON."""
    index_file = STATIC / "index.html"
    if index_file.exists():
        try:
            return FileResponse(
                str(index_file), media_type="text/html; charset=utf-8"
            )
        except Exception as e:
            logger.error("Failed to serve index.html: %s", e)
            return HTMLResponse(
                content="<h1>AssurDevis</h1><p>Interface not available</p>",
                status_code=500,
            )
    return {"service": "AssurDevis", "version": "3.0", "status": "online"}


@app.post("/init")
async def init_conversation():
    """Initialize a new conversation."""
    conv_id = str(uuid.uuid4())
    conversations[conv_id] = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "history": [],
    }
    increment_counter("conversations")
    return {"conversation_id": conv_id}


@app.post("/chat")
async def chat(req: ChatRequest):
    """Chat endpoint with intent detection."""
    if not req.conversation_id:
        raise HTTPException(400, "conversation_id required")

    conv_id = req.conversation_id
    conv = conversations.get(conv_id)
    if not conv:
        raise HTTPException(404, "Conversation not found")

    # Intent detection
    msg_lower = req.message.lower()
    if any(w in msg_lower for w in ["devis auto", "assurance auto", "voiture"]):
        intent = "QUOTE_AUTO"
    elif any(w in msg_lower for w in ["devis", "habitation", "maison", "pro", "rc", "décennale"]):
        intent = "QUOTE_RD"
    elif any(w in msg_lower for w in ["agence", "bureau", "où"]):
        intent = "ORIENTATION"
    elif any(w in msg_lower for w in ["bonjour", "salut", "hello", "hi", "salam"]):
        intent = "GREETING"
    else:
        intent = "QUESTION_INFO"

    increment_counter(f"intent_{intent}")
    conv["history"].append({"role": "user", "content": req.message})

    # Intent context
    intent_context = {
        "GREETING": (
            "Respond warmly and present AssurDevis as an expert assistant in Algerian insurance. "
            "Offer help with auto quotes, home insurance, professional liability, or insurance questions. "
            "Be friendly and encouraging. Respond in French or Arabic (فصحى) based on user language."
        ),
        "QUOTE_AUTO": (
            "User wants an auto insurance quote. Guide them conversationally and warmly, "
            "like an expert advisor. Collect naturally: brand/model, year, value in DA, fiscal power (CV), "
            "wilaya, usage (personal/professional), desired guarantees (mandatory RC, collision, theft/fire, all-risk). "
            "Ask one question at a time. Add light, kind comments ('Great choice!', 'Good question!'). "
            "Respond in French or classical Arabic based on user language."
        ),
        "QUOTE_RD": (
            "User wants a quote for another branch (home, professional liability, fire, etc.). "
            "Guide with expertise and warmth to identify exact branch and collect necessary info. "
            "Respond in French or classical Arabic based on user language."
        ),
        "ORIENTATION": (
            "User seeks an insurance agency or office. Ask their wilaya kindly to direct them to nearest agency. "
            "Respond in French or classical Arabic based on user language."
        ),
        "QUESTION_INFO": (
            "User asks about insurance. Respond with precision, expertise, and human warmth. "
            "Base on current Algerian regulations: Ordinance 95-07, CNA circulars, ORASS 2026 grids. "
            "If question is light or amusing, respond with kind humor. "
            "Respond in French or classical Arabic (فصحى) based on user language."
        ),
    }

    system = SYSTEM_PROMPT
    system += f"\n\nContext: {intent_context.get(intent, intent_context['QUESTION_INFO'])}"

    context = search_knowledge(req.message, intent=intent)
    if context:
        system += "\n\nReference information:\n" + "\n---\n".join(context)

    messages = [{"role": "system", "content": system}]
    for h in conv["history"][-10:]:
        messages.append(h)

    try:
        answer = await query_groq(messages)
    except Exception as e:
        logger.error("Groq query failed: %s", e)
        answer = "AI engine temporarily unavailable. Type 'auto quote' for quick estimate."

    conv["history"].append({"role": "assistant", "content": answer})
    return {"response": answer, "conversation_id": conv_id, "intent": intent}


@app.post("/devis/auto")
async def devis_auto(req: ChatRequest):
    """Calculate auto insurance quote."""
    conv = conversations.get(req.conversation_id)
    if not conv:
        raise HTTPException(404, "Conversation not found")
    try:
        fields = json.loads(req.message) if isinstance(req.message, str) else req.message
        result = calc_auto(fields)
        if result:
            result["fields"] = fields
            try:
                saved = auto_save_devis(result)
                result["_id"] = saved["id"]
            except Exception as e:
                logger.warning("Failed to save devis: %s", e)
    except Exception as e:
        result = {"error": str(e)}
    return {"devis": result} if result else {"error": "Failed to calculate quote"}


@app.post("/devis/rd")
async def devis_rd_endpoint(req: ChatRequest):
    """Calculate other insurance quote."""
    conv = conversations.get(req.conversation_id)
    if not conv:
        raise HTTPException(404, "Conversation not found")
    try:
        fields = json.loads(req.message) if isinstance(req.message, str) else {}
        result = calc_rd(fields)
        if result:
            result["fields"] = fields
            try:
                saved = auto_save_devis(result)
                result["_id"] = saved["id"]
            except Exception as e:
                logger.warning("Failed to save devis: %s", e)
    except Exception as e:
        result = {"error": str(e)}
    return {"devis": result} if result else {"error": "Failed to calculate quote"}


@app.post("/analyse")
async def analyse_contrat(file: UploadFile = File(...)):
    """Analyze insurance contract."""
    if not file.filename:
        raise HTTPException(400, "File required")
    contents = await file.read()
    if len(contents) == 0:
        raise HTTPException(400, "Empty file")
    if len(contents) > 50 * 1024 * 1024:
        raise HTTPException(413, "File too large (max 50 MB)")

    try:
        text = extract_text(contents, file.filename)
    except Exception as e:
        logger.error("Text extraction failed: %s", e)
        return {"error": "Failed to extract text", "filename": file.filename}

    if not text:
        return {"error": "No text extracted", "filename": file.filename}

    groq_on = await check_groq()
    if not groq_on:
        return {
            "texte_extrait": text[:2000],
            "note": "Degraded mode — Groq unavailable. Analysis not performed.",
            "filename": file.filename,
        }

    # Contract analysis via Groq
    analyse_prompt = [
        {
            "role": "system",
            "content": (
                "You are AssurDevis, expert in Algerian insurance (Ordinance 95-07). "
                "Analyze this insurance contract and provide: "
                "1) Summary of covered guarantees, "
                "2) Premium and deductible amounts, "
                "3) Important exclusions, "
                "4) Expiration date if mentioned, "
                "5) Points of attention for insured. "
                "Respond in French, clearly and structured."
            ),
        },
        {"role": "user", "content": f"Contract to analyze:\n\n{text[:8000]}"},
    ]
    try:
        result = await query_groq(analyse_prompt)
    except Exception as e:
        result = f"Analysis error: {e}"

    try:
        auto_save_analyse({"filename": file.filename, "resultat": result})
    except Exception as e:
        logger.warning("Failed to save analysis: %s", e)

    return {"filename": file.filename, "resultat": result}


@app.get("/admin/stats")
async def admin_stats():
    """Get statistics."""
    return {"stats": get_stats()}


@app.get("/admin/export/download")
async def admin_export_download():
    """Download export data."""
    return export_data()


@app.get("/admin/export/download/csv")
async def admin_export_csv():
    """Download export as CSV."""
    from fastapi.responses import PlainTextResponse

    return PlainTextResponse(
        content=full_csv(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=assurdevis_export.csv"},
    )


@app.get("/admin/report")
async def admin_report():
    """Get HTML report."""
    return HTMLResponse(content=html_report(), status_code=200)


@app.get("/rapport")
async def rapport():
    """Get saved report or generate new one."""
    report_path = BASE / "saved" / "report.html"
    if report_path.exists():
        return FileResponse(str(report_path))
    return HTMLResponse(content=html_report(), status_code=200)


@app.post("/admin/export/mail")
async def admin_export_mail(req: ChatRequest):
    """Send export by email."""
    try:
        fields = json.loads(req.message) if isinstance(req.message, str) else req.message
        recipient = fields.get("to", "")
        if not recipient:
            raise HTTPException(400, "Recipient required")
        data = export_data()
        subject = fields.get("subject", f"AssurDevis Export — {data['exported_at']}")
        ok = await send_export_mail(recipient, subject, data)
        return {"sent": ok, "to": recipient}
    except Exception as e:
        raise HTTPException(400, str(e))


@app.post("/rating")
async def submit_rating(req: ChatRequest):
    """Submit quote rating."""
    try:
        fields = json.loads(req.message) if isinstance(req.message, str) else req.message
        devis_id = fields.get("devis_id", "")
        stars = int(fields.get("stars", 0))
        if not devis_id or stars < 1 or stars > 5:
            raise HTTPException(400, "devis_id required and stars between 1-5")
        stats = save_rating(devis_id, stars)
        return {"stats": stats}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(400, str(e))


@app.get("/rating/stats")
async def rating_stats():
    """Get rating statistics."""
    return {"stats": get_rating_stats()}


@app.post("/scoring/devis")
async def scoring_devis_endpoint(req: ChatRequest):
    """Score a quote."""
    try:
        fields = json.loads(req.message) if isinstance(req.message, str) else req.message
        score = score_devis(fields)
        return {"score": score}
    except Exception as e:
        raise HTTPException(400, str(e))


@app.get("/health")
async def health():
    """Health check endpoint."""
    groq = await check_groq()
    return {
        "status": "ok",
        "groq": groq,
        "model": GROQ_MODEL,
        "keys_loaded": len(_GROQ_KEYS),
        "active_key": _groq_key_index + 1,
        "version": "3.0",
    }

