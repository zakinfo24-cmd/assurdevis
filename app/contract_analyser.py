"""
Module for analyzing insurance contracts.
Supports PDF text extraction with OCR fallback.
"""
import json
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# ── Reference ────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.parent
REFERENCE_PATH = BASE_DIR / "reference_contrat.pdf"
_REFERENCE_TEXT: str | None = None


def load_reference() -> str:
    """Load and extract text from reference PDF."""
    global _REFERENCE_TEXT
    if _REFERENCE_TEXT is not None:
        return _REFERENCE_TEXT

    if not REFERENCE_PATH.exists():
        _REFERENCE_TEXT = ""
        logger.warning("Reference PDF not found: %s", REFERENCE_PATH)
        return _REFERENCE_TEXT

    try:
        import fitz
        doc = fitz.open(str(REFERENCE_PATH))
        parts = [page.get_text() for page in doc]
        doc.close()
        _REFERENCE_TEXT = "\n".join(parts).strip()
        logger.info(
            "Reference loaded: %s (%d pages, %d chars)",
            REFERENCE_PATH.name,
            len(doc),
            len(_REFERENCE_TEXT),
        )
    except ImportError:
        logger.warning("PyMuPDF not installed — reference extraction skipped")
        _REFERENCE_TEXT = ""
    except Exception as e:
        logger.error("Failed to load reference: %s", e)
        _REFERENCE_TEXT = ""

    return _REFERENCE_TEXT


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from PDF using PyMuPDF, with OCR fallback."""
    try:
        import fitz
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        parts = [page.get_text() for page in doc]
        doc.close()
        text = "\n".join(parts).strip()
        if text:
            return text
    except ImportError:
        logger.warning("PyMuPDF not installed — OCR fallback attempted")
    except Exception as e:
        logger.error("PDF text extraction failed: %s", e)

    # OCR fallback for scanned PDFs
    logger.info("Empty text — attempting OCR...")
    return _ocr_pdf(file_bytes)


def _ocr_pdf(file_bytes: bytes, lang: str = "fra") -> str:
    """Extract text from scanned PDF using Tesseract OCR."""
    try:
        import fitz
        from PIL import Image
        import pytesseract

        doc = fitz.open(stream=file_bytes, filetype="pdf")
        parts = []
        for page in doc:
            pix = page.get_pixmap(dpi=300)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            text = pytesseract.image_to_string(img, lang=lang)
            parts.append(text.strip())
        doc.close()
        return "\n".join(parts).strip()
    except ImportError:
        logger.warning("Tesseract or PIL not installed — OCR skipped")
        return ""
    except Exception as e:
        logger.error("OCR failed: %s", e)
        return ""


def extract_text(file_bytes: bytes, filename: str = "") -> str:
    """Extract text from PDF file."""
    if not file_bytes:
        return ""
    return extract_text_from_pdf(file_bytes)

