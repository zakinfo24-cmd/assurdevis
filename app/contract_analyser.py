"""
Module d'analyse de contrats d'assurance.
100% offline — OCR + classification + parsing via Ollama.
"""
import json
import os
import io
import logging
import pytesseract
from PIL import Image
import shutil

# Try multiple Tesseract locations for portability
_tesseract_candidates = [
    shutil.which("tesseract"),                          # PATH
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",    # default install
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
]
for _p in _tesseract_candidates:
    if _p and os.path.exists(_p):
        pytesseract.pytesseract.tesseract_cmd = _p
        break

logger = logging.getLogger(__name__)

# ── Référence ────────────────────────────────────────────────────────────
REFERENCE_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), ".."
)
REFERENCE_NAMES = ["reference_contrat.pdf"]
_REFERENCE_TEXT: str | None = None


def load_reference() -> str:
    """Charge et extrait le texte du PDF de référence."""
    global _REFERENCE_TEXT
    if _REFERENCE_TEXT is not None:
        return _REFERENCE_TEXT
    path = os.path.join(REFERENCE_DIR, "reference_contrat.pdf")
    if not os.path.exists(path):
        _REFERENCE_TEXT = ""
        logger.warning("Aucun PDF de référence trouvé : %s", path)
        return _REFERENCE_TEXT
    try:
        import fitz
        doc = fitz.open(path)
        parts = [page.get_text() for page in doc]
        doc.close()
        _REFERENCE_TEXT = "\n".join(parts).strip()
        logger.info("Référence chargée : %s (%d pages, %d caractères)",
                     path, len(doc), len(_REFERENCE_TEXT))
    except Exception as e:
        _REFERENCE_TEXT = ""
        logger.error("Erreur chargement référence : %s", e)
    return _REFERENCE_TEXT


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extrait le texte d'un PDF via PyMuPDF, avec fallback OCR."""
    try:
        import fitz
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        parts = []
        for page in doc:
            parts.append(page.get_text())
        doc.close()
        text = "\n".join(parts).strip()
        if text:
            return text
    except Exception as e:
        logger.error("Erreur extraction PDF : %s", e)

    # Fallback OCR pour PDF scannés
    logger.info("Texte vide — tentative OCR...")
    return _ocr_pdf(file_bytes)


def _ocr_pdf(file_bytes: bytes, lang: str = "fra") -> str:
    """Extrait le texte d'un PDF scanné via Tesseract OCR."""
    try:
        import fitz
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        parts = []
        for page in doc:
            pix = page.get_pixmap(dpi=300)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            text = pytesseract.image_to_string(img, lang=lang)
            parts.append(text.strip())
        doc.close()
        return "\n".join(parts).strip()
    except Exception as e:
        logger.error("Erreur OCR PDF : %s", e)
        return ""


def extract_text(file_bytes: bytes, filename: str = "") -> str:
    """Extrait le texte d'un PDF."""
    return extract_text_from_pdf(file_bytes)


# ── Analyse via Ollama ──────────────────────────────────────────────────

ANALYSE_SYSTEM = """Tu es un expert en analyse de contrats d'assurance.

Tu reçois :
1. Le texte de RÉFÉRENCE — le contrat type de la compagnie.
2. Le texte du CONTRAT SCANNÉ — le document à analyser.

Ta mission :
1. Compare le contrat scanné avec le modèle de référence.
2. Détermine le TYPE de contrat et le SCORE de similarité (0-100%).
3. Extrais les informations structurées suivantes :

Réponds UNIQUEMENT en JSON valide, sans texte avant/après :
{
  "type_contrat": "Auto / MRH / RC Pro / ...",
  "score_similarite": 85,
  "reconnu": true,
  "garanties": ["RC", "Vol", "Incendie", ...],
  "exclusions": ["Guerre", "Émeute", ...],
  "prime_annuelle_ht": 45000,
  "franchises": {"RC": 0, "Vol": "10%", ...},
  "clauses_importantes": ["Clause 1...", "Clause 2..."],
  "resume_client": "Résumé simple en français ou darija."
}

Si le contrat n'est pas reconnu (hors périmètre), mets "reconnu": false.
Si une info n'est pas trouvée, mets null."""


async def analyse_contract(
    text: str,
    reference_text: str,
    ollama_host: str = "http://localhost:11434",
    ollama_model: str = "qwen2.5:7b",
) -> dict:
    """Envoie le texte extrait + référence à Ollama pour analyse."""
    if not text:
        return {"error": "Texte vide — impossible d'analyser"}

    system = ANALYSE_SYSTEM
    if reference_text:
        system += f"\n\n## TEXTE DE RÉFÉRENCE\n{reference_text[:8000]}"

    import httpx
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": f"## CONTRAT SCANNÉ\n{text[:12000]}"},
    ]

    try:
        async with httpx.AsyncClient(timeout=180) as client:
            prompt_parts = []
            for m in messages:
                role = m.get("role", "user")
                content = m.get("content", "")
                if role == "system":
                    prompt_parts.append(f"[System]\n{content}")
                elif role == "user":
                    prompt_parts.append(f"[User]\n{content}")
                elif role == "assistant":
                    prompt_parts.append(f"[Assistant]\n{content}")
            prompt_parts.append("[Assistant]\n")
            prompt = "\n\n".join(prompt_parts)
            resp = await client.post(f"{ollama_host}/api/generate", json={
                "model": ollama_model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.1, "num_predict": 2048},
            })
            resp.raise_for_status()
            raw = resp.json()["response"]
            # Extraction du JSON depuis la réponse
            json_match = raw.strip()
            if "```json" in json_match:
                json_match = json_match.split("```json")[1].split("```")[0]
            elif "```" in json_match:
                json_match = json_match.split("```")[1].split("```")[0]
            result = json.loads(json_match.strip())
            return result
    except json.JSONDecodeError:
        return {"error": "Réponse Ollama invalide", "raw": raw[:500]}
    except Exception as e:
        return {"error": str(e)}
