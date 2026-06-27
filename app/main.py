import asyncio
import base64
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
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

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
    # Force UTF-8 encoding pour les accents
    import sys
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    
    try:
        _REFERENCE_TEXT = load_reference()
    except Exception:
        _REFERENCE_TEXT = ""
    asyncio.create_task(_export_loop())
    if not _GROQ_KEYS:
        logging.getLogger(__name__).warning("Aucune GROQ_API_KEY définie — les réponses IA seront dégradées.")
    else:
        logging.getLogger(__name__).info("%d clé(s) Groq chargée(s).", len(_GROQ_KEYS))
    
    # Vérifier que les fichiers MD existent
    if KNOWLEDGE_DIR.exists():
        md_files = list(KNOWLEDGE_DIR.glob("*.md"))
        logging.getLogger(__name__).info("Knowledge base: %d fichier(s) trouvé(s) dans %s", len(md_files), KNOWLEDGE_DIR)
        for mf in sorted(md_files):
            logging.getLogger(__name__).info("  - %s (%d octets)", mf.name, mf.stat().st_size)
    else:
        logging.getLogger(__name__).warning("Dossier knowledge introuvable: %s", KNOWLEDGE_DIR)


REPORT_DATA: list = []


class ChatRequest(BaseModel):
    message: str
    conversation_id: str = ""


# ── ElevenLabs TTS ─────────────────────────────────────────────────────────
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "zAvB1CA77BKeZMAepR7x")  # Lucie

@app.post("/tts")
async def text_to_speech(req: ChatRequest):
    """Convertir le texte en audio via ElevenLabs — voix française naturelle."""
    if not ELEVENLABS_API_KEY:
        raise HTTPException(503, "TTS non configuré (ELEVENLABS_API_KEY manquante)")

    text = req.message.strip()[:1000]
    if not text:
        raise HTTPException(400, "Texte vide")

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.3,
            "use_speaker_boost": True,
        },
    }

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                url,
                headers={
                    "xi-api-key": ELEVENLABS_API_KEY,
                    "Content-Type": "application/json",
                    "Accept": "audio/mpeg",
                },
                json=payload,
            )
            if resp.status_code != 200:
                logging.getLogger(__name__).error("ElevenLabs %d: %s", resp.status_code, resp.text[:300])
                raise HTTPException(resp.status_code, f"ElevenLabs erreur {resp.status_code}")

            audio_base64 = base64.b64encode(resp.content).decode("utf-8")
            return {"audio": f"data:audio/mpeg;base64,{audio_base64}", "success": True}

    except httpx.TimeoutException:
        raise HTTPException(504, "ElevenLabs timeout")
    except HTTPException:
        raise
    except Exception as e:
        logging.getLogger(__name__).error("TTS error: %s", e)
        raise HTTPException(500, str(e))

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
        "temperature": 0.7,
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
            text = resp.json()["choices"][0]["message"]["content"]
            # Réparer l'encoding UTF-8 si nécessaire
            try:
                # Si le texte a des caractères mal encodés (Ã© au lieu de é)
                text = text.encode('latin-1').decode('utf-8', errors='ignore')
            except (UnicodeDecodeError, UnicodeEncodeError):
                pass  # Si ça fail, garder le texte original
            return text

    raise RuntimeError("Toutes les clés Groq sont épuisées")


# ── Knowledge & Intent ───────────────────────────────────────────────────────

def search_knowledge(query: str, top_k: int = 3, intent: str = "QUESTION_INFO") -> list[str]:
    # Routage par intent — tous les fichiers disponibles sauf restrictions explicites
    INTENT_FILES = {
        "QUESTION_INFO": [
            "dify_01_calcul_tarification.md",
            "dify_02_garanties_produits.md",
            "dify_03_references_legales.md",
            "dify_05_culture_assurance.md"
        ],
        "GREETING":      [],
        "ORIENTATION":   [
            "dify_04_processus_commercial.md",
            "dify_02_garanties_produits.md"
        ],
        "QUOTE_AUTO": [
            "dify_01_calcul_tarification.md",
            "dify_02_garanties_produits.md",
            "dify_04_processus_commercial.md"
        ],
        "QUOTE_RD": [
            "dify_02_garanties_produits.md",
            "dify_04_processus_commercial.md"
        ],
    }
    
    allowed     = INTENT_FILES.get(intent)
    query_lower = query.lower()
    results     = []
    for md_file in sorted(KNOWLEDGE_DIR.glob("*.md")):
        if allowed is not None and md_file.name not in allowed:
            continue
        try:
            with open(md_file, encoding="utf-8") as f:
                content = f.read()
            # Récupère les sections pertinentes (simple recherche par mots-clés)
            lines = content.split("\n")
            matching_sections = []
            for i, line in enumerate(lines):
                if any(word in line.lower() for word in query_lower.split()):
                    start = max(0, i - 2)
                    end = min(len(lines), i + 10)
                    matching_sections.append("\n".join(lines[start:end]))
            if matching_sections:
                results.extend(matching_sections[:top_k])
        except Exception:
            pass
    
    return results[:top_k] if results else []


@app.get("/")
async def root():
    """Servir le fichier index.html à la racine"""
    index_file = STATIC / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file), media_type="text/html; charset=utf-8")
    return {"service": "AssurDevis", "version": "3.0", "status": "online"}


@app.post("/init")
async def init_conversation():
    conv_id = str(uuid.uuid4())
    conversations[conv_id] = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "history": [],
    }
    increment_counter("conversations")
    return {"conversation_id": conv_id}


@app.post("/chat")
async def chat(req: ChatRequest):
    if not req.conversation_id:
        raise HTTPException(400, "conversation_id requis")

    conv_id = req.conversation_id
    conv = conversations.get(conv_id)
    if not conv:
        raise HTTPException(404, "Conversation not found")

    # Détection d'intent simple
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

    # Contexte par intent
    intent_context = {
        "GREETING": (
            "Réponds chaleureusement et présente AssurDevis comme un assistant expert en assurance algérienne. "
            "Propose aide sur devis auto, habitation, RC pro, ou questions sur l'assurance. "
            "Sois amical et encourageant. Réponds en français ou en arabe (فصحى) selon la langue de l'utilisateur."
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
