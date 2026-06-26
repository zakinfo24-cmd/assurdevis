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
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .engine import calc_auto, calc_rd
from .contract_analyser import load_reference, analyse_contract, extract_text
from .save_manager import auto_save_devis, auto_save_analyse, get_stats, export_data, save_rating, get_rating_stats, increment_counter
from .export_manager import send_export_mail
from .report_generator import devis_csv, analyses_csv, ratings_csv, full_csv, html_report
from .scoring import score_devis

app = FastAPI(title="AssurDevis")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

BASE = Path(__file__).parent.parent

# Servir le frontend statique
STATIC = BASE / "static"
if STATIC.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC)), name="static")

# ── Groq API (remplace Ollama) ──────────────────────────────────────────────
GROQ_URL   = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

# Rotation automatique des clés Groq
_GROQ_KEYS = [
    k for k in [
        os.getenv("GROQ_API_KEY"),
        os.getenv("GROQ_API_KEY_2"),
        os.getenv("GROQ_API_KEY_3"),
        os.getenv("GROQ_API_KEY_4"),
        os.getenv("GROQ_API_KEY_5"),
    ] if k
]
_groq_key_index = 0

def get_groq_key() -> str:
    return _GROQ_KEYS[_groq_key_index] if _GROQ_KEYS else ""

def rotate_groq_key():
    global _groq_key_index
    _groq_key_index = (_groq_key_index + 1) % len(_GROQ_KEYS)
    logging.getLogger(__name__).warning(
        "Rotation clé Groq → clé %d/%d", _groq_key_index + 1, len(_GROQ_KEYS)
    )

KNOWLEDGE_DIR     = BASE / "knowledge"
INSTRUCTIONS_PATH = BASE / "app" / "instructions_assurdevis.txt"

SYSTEM_PROMPT = ""
if INSTRUCTIONS_PATH.exists():
    with open(INSTRUCTIONS_PATH, encoding="utf-8") as f:
        SYSTEM_PROMPT = f.read()

conversations: dict[str, dict] = {}
_REFERENCE_TEXT: str = ""

LAST_EXPORT_FILE   = BASE / "saved" / "last_export.json"
EXPORT_EMAILS      = os.getenv("EXPORT_TO_EMAILS", "").strip()
EXPORT_INTERVAL_H  = 24


# ── Export programmé ────────────────────────────────────────────────────────

def _check_export_due() -> bool:
    if not EXPORT_EMAILS:
        return False
    if not LAST_EXPORT_FILE.exists():
        return True
    try:
        with open(LAST_EXPORT_FILE, encoding="utf-8") as f:
            data = json.load(f)
        last    = datetime.fromisoformat(data.get("exported_at", ""))
        elapsed = (datetime.now(timezone.utc) - last).total_seconds()
        return elapsed >= EXPORT_INTERVAL_H * 3600
    except Exception:
        return True


def _mark_export_done(success: bool, msg: str = ""):
    LAST_EXPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LAST_EXPORT_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "exported_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "success": success,
            "message": msg,
        }, f, ensure_ascii=False)


async def _run_scheduled_export():
    if not EXPORT_EMAILS:
        return
    if not _check_export_due():
        return
    logger = logging.getLogger(__name__)
    logger.info("Export programmé : consolidating data...")
    try:
        data       = export_data()
        recipients = [e.strip() for e in EXPORT_EMAILS.split(",") if e.strip()]
        subject    = f"AssurDevis Export — {data['exported_at']}"
        all_ok     = True
        for to in recipients:
            ok = await send_export_mail(to, subject, data)
            if not ok:
                logger.warning("Export échoué vers %s", to)
                all_ok = False
        if all_ok:
            logger.info("Export envoyé avec succès à %d destinataire(s)", len(recipients))
            _mark_export_done(True, f"Envoyé à {len(recipients)} destinataire(s)")
        else:
            _mark_export_done(False, "Échec partiel ou total")
    except Exception as e:
        logger.error("Erreur export programmé : %s", e)
        _mark_export_done(False, str(e))


async def _export_loop():
    while True:
        await _run_scheduled_export()
        await asyncio.sleep(3600)


# ── Startup ─────────────────────────────────────────────────────────────────

@app.on_event("startup")
async def _startup():
    global _REFERENCE_TEXT
    try:
        _REFERENCE_TEXT = load_reference()
    except Exception:
        _REFERENCE_TEXT = ""
    asyncio.create_task(_export_loop())
    if not _GROQ_KEYS:
        logging.getLogger(__name__).warning("Aucune GROQ_API_KEY définie — les réponses IA seront dégradées.")
    else:
        logging.getLogger(__name__).info("%d clé(s) Groq chargée(s).", len(_GROQ_KEYS))


REPORT_DATA: list = []


class ChatRequest(BaseModel):
    message: str
    conversation_id: str = ""


# ── Groq API helpers ────────────────────────────────────────────────────────

async def check_groq() -> bool:
    """Vérifie que la clé Groq active est valide."""
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
    """Appelle Groq avec rotation automatique si limite atteinte (429)."""
    if not _GROQ_KEYS:
        raise RuntimeError("Aucune clé Groq configurée")

    headers = {"Content-Type": "application/json"}
    payload = {
        "model": GROQ_MODEL,
        "messages": messages,
        "temperature": 0.3,
        "max_tokens": 800,
    }

    attempts = len(_GROQ_KEYS)
    for _ in range(attempts):
        headers["Authorization"] = f"Bearer {get_groq_key()}"
        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(GROQ_URL, json=payload, headers=headers)
            if resp.status_code == 429:
                rotate_groq_key()
                continue
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"]

    raise RuntimeError("Toutes les clés Groq sont épuisées")


# ── Knowledge & Intent ───────────────────────────────────────────────────────

def search_knowledge(query: str, top_k: int = 3, intent: str = "QUESTION_INFO") -> list[str]:
    INTENT_FILES = {
        "QUESTION_INFO": ["dify_03_references_legales.md", "dify_05_culture_assurance.md"],
        "GREETING":      [],
        "ORIENTATION":   ["dify_04_processus_commercial.md"],
        "QUOTE_AUTO":    None,
        "QUOTE_RD":      None,
    }
    allowed     = INTENT_FILES.get(intent)
    query_lower = query.lower()
    results     = []
    for md_file in sorted(KNOWLEDGE_DIR.glob("*.md")):
        if allowed is not None and md_file.name not in allowed:
            continue
        with open(md_file, encoding="utf-8") as f:
            content = f.read()
        sections = re.split(r"\n#{1,3}\s+", content)
        for section in sections:
            score = sum(1 for word in query_lower.split() if word in section.lower())
            if score > 0:
                name = md_file.name.replace("dify_", "").replace(".md", "").replace("_", " ")
                results.append((score, f"[{name}] {section.strip()[:1500]}"))
    results.sort(key=lambda x: -x[0])
    return [r[1] for r in results[:top_k]]


def detect_intent(msg: str) -> str:
    msg_lower = msg.lower()
    if any(w in msg_lower for w in ["devis", "tarif", "prix", "combien", "estimation", "assurance auto", "assurance voiture", "cotation"]):
        if any(w in msg_lower for w in ["maison", "habitation", "mrh", "villa", "appartement", "mr"]):
            return "QUOTE_RD"
        return "QUOTE_AUTO"
    if any(w in msg_lower for w in ["agence", "orientation", "bureau", "rencontrer", "rendez-vous", "rdv", "ou se trouve", "adresse"]):
        return "ORIENTATION"
    if any(w in msg_lower for w in ["salut", "bonjour", "salam", "bonsoir"]):
        return "GREETING"
    return "QUESTION_INFO"


# ── Routes ───────────────────────────────────────────────────────────────────

@app.get("/")
async def root():
    index = STATIC / "index.html"
    if index.exists():
        return FileResponse(str(index))
    return {"status": "AssurDevis API", "message": "Frontend non trouvé. Utilisez /docs pour l'API."}


@app.post("/chat")
async def chat(req: ChatRequest):
    conv_id = req.conversation_id or str(uuid.uuid4())
    if conv_id not in conversations:
        conversations[conv_id] = {"history": [], "fields": {}}
    conv = conversations[conv_id]
    conv["history"].append({"role": "user", "content": req.message})

    intent = detect_intent(req.message)

    try:
        increment_counter("total_consultations")
    except Exception:
        pass

    # Vérifier Groq — fallback dégradé si indisponible
    groq_on = await check_groq()
    if not groq_on:
        fallback = {
            "GREETING":      "Bienvenue sur AssurDevis ! / أهلاً بك في AssurDevis ! En quoi puis-je vous aider ?",
            "QUOTE_AUTO":    "Pour un devis auto, tapez « devis auto » et je vous guide étape par étape.",
            "QUOTE_RD":      "Pour un devis habitation, tapez « devis maison » et je vous guide.",
            "ORIENTATION":   "Précisez votre wilaya et je vous orienterai vers l'agence la plus proche.",
            "QUESTION_INFO": "Je suis AssurDevis, votre assistant en assurance. Posez votre question, je vous réponds.",
        }
        return {
            "response": fallback.get(intent, "Je suis temporairement en mode dégradé. Tapez « devis auto » pour commencer."),
            "conversation_id": conv_id,
            "intent": intent,
        }

    intent_context = {
        "GREETING": (
            "L'utilisateur salue. Réponds avec chaleur et bonne humeur en te présentant comme "
            "AssurDevis, l'assistant virtuel intelligent spécialisé en assurance en Algérie. "
            "Ta phrase d'accueil est exactement : 'Bienvenue sur AssurDevis ! En quoi puis-je vous aider ?' "
            "Tu peux ajouter une touche légère et sympathique — une petite blague douce ou un mot "
            "chaleureux — pour mettre l'utilisateur à l'aise, mais reste professionnel. "
            "Propose-lui : devis auto, questions sur les garanties, analyse de contrat, ou orientation. "
            "Tu réponds en français par défaut, mais si l'utilisateur écrit en arabe classique (فصحى), "
            "réponds-lui en arabe classique avec la même qualité et le même ton."
        ),
        "QUOTE_AUTO": (
            "L'utilisateur veut un devis assurance auto. Guide-le de façon conversationnelle et chaleureuse, "
            "comme un conseiller expert qui connaît bien son métier. "
            "Collecte naturellement : marque et modèle, année, valeur vénale en DA, puissance fiscale (CV), "
            "wilaya, usage (personnel ou professionnel), garanties souhaitées (RC obligatoire, "
            "dommages collision, vol/incendie, tous risques). "
            "Pose une question à la fois. Tu peux glisser un commentaire léger et bienveillant "
            "('Excellent choix !', 'Bonne question !'). "
            "Réponds en français ou en arabe classique selon la langue de l'utilisateur."
        ),
        "QUOTE_RD": (
            "L'utilisateur veut un devis pour une autre branche (habitation, RC pro, incendie, etc.). "
            "Guide-le avec expertise et chaleur pour identifier la branche exacte "
            "et collecter les informations nécessaires. "
            "Réponds en français ou en arabe classique selon la langue de l'utilisateur."
        ),
        "ORIENTATION": (
            "L'utilisateur cherche une agence ou un bureau d'assurance. "
            "Demande-lui sa wilaya avec gentillesse pour l'orienter vers l'agence la plus proche. "
            "Réponds en français ou en arabe classique selon la langue de l'utilisateur."
        ),
        "QUESTION_INFO": (
            "L'utilisateur pose une question sur l'assurance. "
            "Réponds avec précision, expertise et une touche de chaleur humaine. "
            "Base-toi sur la réglementation algérienne en vigueur : "
            "Ordonnance 95-07, circulaires CNA, grilles ORASS 2026. "
            "Si la question est légère ou amusante, tu peux répondre avec un peu d'humour bienveillant. "
            "Réponds en français ou en arabe classique (فصحى) selon la langue utilisée par l'interlocuteur."
        ),
    }

    system = SYSTEM_PROMPT
    system += f"\n\nContexte de cette interaction : {intent_context.get(intent, intent_context['QUESTION_INFO'])}"

    context = search_knowledge(req.message, intent=intent)
    if context:
        system += "\n\nInformations de référence :\n" + "\n---\n".join(context)

    messages = [{"role": "system", "content": system}]
    for h in conv["history"][-10:]:
        messages.append(h)

    try:
        answer = await query_groq(messages)
    except Exception as e:
        logging.getLogger(__name__).error("Groq query failed: %s", e)
        answer = "Le moteur IA est temporairement indisponible. Tapez « devis auto » pour une estimation rapide."

    conv["history"].append({"role": "assistant", "content": answer})
    return {"response": answer, "conversation_id": conv_id, "intent": intent}


@app.post("/devis/auto")
async def devis_auto(req: ChatRequest):
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
            except Exception:
                pass
    except Exception as e:
        result = {"error": str(e)}
    return {"devis": result} if result else {"error": "Impossible de calculer le devis"}


@app.post("/devis/rd")
async def devis_rd_endpoint(req: ChatRequest):
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
            except Exception:
                pass
    except Exception as e:
        result = {"error": str(e)}
    return {"devis": result} if result else {"error": "Impossible de calculer le devis"}


@app.post("/analyse")
async def analyse_contrat(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(400, "Fichier requis")
    contents = await file.read()
    if len(contents) == 0:
        raise HTTPException(400, "Fichier vide")
    if len(contents) > 50 * 1024 * 1024:
        raise HTTPException(413, "Fichier trop volumineux (max 50 Mo)")
    text = extract_text(contents, file.filename)
    if not text:
        return {"error": "Impossible d'extraire le texte", "filename": file.filename}

    groq_on = await check_groq()
    if not groq_on:
        return {
            "texte_extrait": text[:2000],
            "note": "Mode dégradé — Groq indisponible. Analyse non réalisée.",
            "filename": file.filename,
        }

    # Analyse du contrat via Groq directement
    analyse_prompt = [
        {"role": "system", "content": (
            "Tu es AssurDevis, expert en assurance algérienne (Ordonnance 95-07). "
            "Analyse ce contrat d'assurance et fournis : "
            "1) Résumé des garanties couvertes, "
            "2) Montant des primes et franchises, "
            "3) Exclusions importantes, "
            "4) Date d'échéance si mentionnée, "
            "5) Points d'attention pour l'assuré. "
            "Réponds en français, de façon claire et structurée."
        )},
        {"role": "user", "content": f"Voici le contrat à analyser :\n\n{text[:8000]}"},
    ]
    try:
        result = await query_groq(analyse_prompt)
    except Exception as e:
        result = f"Erreur lors de l'analyse : {e}"

    try:
        auto_save_analyse({"filename": file.filename, "resultat": result})
    except Exception:
        pass
    return {"filename": file.filename, "resultat": result}


@app.get("/admin/stats")
async def admin_stats():
    return {"stats": get_stats()}


@app.get("/admin/export/download")
async def admin_export_download():
    return export_data()


@app.get("/admin/export/download/csv")
async def admin_export_csv():
    from fastapi.responses import PlainTextResponse
    return PlainTextResponse(
        content=full_csv(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=assurdevis_export.csv"},
    )


@app.get("/admin/report")
async def admin_report():
    from fastapi.responses import HTMLResponse
    return HTMLResponse(content=html_report(), status_code=200)


@app.get("/rapport")
async def rapport():
    from fastapi.responses import HTMLResponse, FileResponse
    report_path = BASE / "saved" / "report.html"
    if report_path.exists():
        return FileResponse(str(report_path))
    return HTMLResponse(content=html_report(), status_code=200)


@app.post("/admin/export/mail")
async def admin_export_mail(req: ChatRequest):
    try:
        fields    = json.loads(req.message) if isinstance(req.message, str) else req.message
        recipient = fields.get("to", "")
        if not recipient:
            raise HTTPException(400, "Destinataire requis")
        data    = export_data()
        subject = fields.get("subject", f"AssurDevis Export — {data['exported_at']}")
        ok      = await send_export_mail(recipient, subject, data)
        return {"sent": ok, "to": recipient}
    except Exception as e:
        raise HTTPException(400, str(e))


@app.post("/rating")
async def submit_rating(req: ChatRequest):
    try:
        fields   = json.loads(req.message) if isinstance(req.message, str) else req.message
        devis_id = fields.get("devis_id", "")
        stars    = int(fields.get("stars", 0))
        if not devis_id or stars < 1 or stars > 5:
            raise HTTPException(400, "devis_id requis et stars entre 1 et 5")
        stats = save_rating(devis_id, stars)
        return {"stats": stats}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(400, str(e))


@app.get("/rating/stats")
async def rating_stats():
    return {"stats": get_rating_stats()}


@app.post("/scoring/devis")
async def scoring_devis_endpoint(req: ChatRequest):
    try:
        fields = json.loads(req.message) if isinstance(req.message, str) else req.message
        score  = score_devis(fields)
        return {"score": score}
    except Exception as e:
        raise HTTPException(400, str(e))


@app.get("/health")
async def health():
    groq = await check_groq()
    return {"status": "ok", "groq": groq, "model": GROQ_MODEL, "keys_loaded": len(_GROQ_KEYS), "active_key": _groq_key_index + 1, "version": "3.0"}
