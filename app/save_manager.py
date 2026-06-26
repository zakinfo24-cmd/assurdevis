import json
import os
import threading
import uuid
from datetime import datetime, timezone

SAVE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "saved"
)
DEVIS_DIR = os.path.join(SAVE_DIR, "devis")
ANALYSES_DIR = os.path.join(SAVE_DIR, "analyses")

for d in [DEVIS_DIR, ANALYSES_DIR]:
    os.makedirs(d, exist_ok=True)

_COUNTER_LOCK = threading.Lock()


def _ts() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _regenerate_report():
    """Regénère saved/report.html après chaque sauvegarde."""
    try:
        from report_generator import html_report
        path = os.path.join(SAVE_DIR, "report.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(html_report())
    except Exception:
        pass


def auto_save_devis(devis_data: dict) -> dict:
    fields = devis_data.get("fields", {})
    wilaya = fields.get("wilaya", fields.get("region", ""))
    entry = {
        "id": str(uuid.uuid4())[:8],
        "type": devis_data.get("type", "auto"),
        "saved_at": _ts(),
        "wilaya": str(wilaya).strip() if wilaya else "",
        "garanties": devis_data.get("garanties", []),
        "total_ttc": devis_data.get("total_ttc", 0),
        "monthly": devis_data.get("monthly", 0),
        "duree_mois": devis_data.get("duree_mois", 12),
        "items": devis_data.get("items", []),
        "tva": devis_data.get("tva", 0),
        "fga": devis_data.get("fga", 0),
        "total_ht": devis_data.get("total_ht", 0),
        "reduction": devis_data.get("reduction_applied", 0),
        "fields": fields,
    }
    path = os.path.join(DEVIS_DIR, f"{entry['id']}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(entry, f, ensure_ascii=False, indent=2)
    _regenerate_report()
    return entry


def auto_save_analyse(analyse_data: dict) -> dict:
    entry = {
        "id": str(uuid.uuid4())[:8],
        "saved_at": _ts(),
        "filename": analyse_data.get("filename", ""),
        "type_contrat": analyse_data.get("resultat", {}).get("type_contrat"),
        "score_similarite": analyse_data.get("resultat", {}).get("score_similarite"),
        "reconnu": analyse_data.get("resultat", {}).get("reconnu"),
        "resultat": analyse_data.get("resultat", {}),
    }
    path = os.path.join(ANALYSES_DIR, f"{entry['id']}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(entry, f, ensure_ascii=False, indent=2)
    _regenerate_report()
    return entry


def get_stats() -> dict:
    devis_files = [f for f in os.listdir(DEVIS_DIR) if f.endswith(".json")]
    analyse_files = [f for f in os.listdir(ANALYSES_DIR) if f.endswith(".json")]

    total_ttc_sum = 0
    garanties_count = {}
    type_count = {}
    wilaya_count = {}

    for fname in devis_files:
        path = os.path.join(DEVIS_DIR, fname)
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        total_ttc_sum += data.get("total_ttc", 0)
        for g in data.get("garanties", []):
            garanties_count[g] = garanties_count.get(g, 0) + 1
        t = data.get("type", "auto")
        type_count[t] = type_count.get(t, 0) + 1
        w = data.get("wilaya", "").strip()
        if w:
            wilaya_count[w] = wilaya_count.get(w, 0) + 1

    top_wilayas = sorted(wilaya_count.items(), key=lambda x: -x[1])[:10]
    counters = _load_counters()

    return {
        "total_devis": len(devis_files),
        "total_analyses": len(analyse_files),
        "total_collected": len(devis_files) + len(analyse_files),
        "total_ttc_sum": total_ttc_sum,
        "garanties_breakdown": garanties_count,
        "type_breakdown": type_count,
        "top_wilayas": [{"wilaya": w, "count": c} for w, c in top_wilayas],
        "orientation_count": counters.get("orientation", 0),
        "total_consultations": counters.get("total_consultations", 0),
    }


RATINGS_FILE = os.path.join(SAVE_DIR, "ratings.json")
COUNTERS_FILE = os.path.join(SAVE_DIR, "counters.json")


def _load_counters() -> dict:
    if not os.path.exists(COUNTERS_FILE):
        return {"orientation": 0, "total_consultations": 0}
    with open(COUNTERS_FILE, encoding="utf-8") as f:
        return json.load(f)


def _save_counters(counters: dict):
    with open(COUNTERS_FILE, "w", encoding="utf-8") as f:
        json.dump(counters, f, ensure_ascii=False, indent=2)


def increment_counter(name: str, amount: int = 1):
    with _COUNTER_LOCK:
        counters = _load_counters()
        counters[name] = counters.get(name, 0) + amount
        _save_counters(counters)
    _regenerate_report()
    return counters[name]


def _load_ratings() -> list:
    if not os.path.exists(RATINGS_FILE):
        return []
    with open(RATINGS_FILE, encoding="utf-8") as f:
        return json.load(f)


def _save_ratings(ratings: list):
    with open(RATINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(ratings, f, ensure_ascii=False, indent=2)


def save_rating(devis_id: str, stars: int) -> dict:
    stars = max(1, min(5, stars))
    ratings = _load_ratings()
    rating = {
        "devis_id": devis_id,
        "stars": stars,
        "rated_at": _ts(),
    }
    ratings.append(rating)
    _save_ratings(ratings)
    _regenerate_report()
    return get_rating_stats(ratings)


def get_rating_stats(ratings: list = None) -> dict:
    if ratings is None:
        ratings = _load_ratings()
    count = len(ratings)
    if count == 0:
        return {"average": 0, "count": 0, "distribution": {str(i): 0 for i in range(1, 6)}}
    total = sum(r["stars"] for r in ratings)
    dist = {str(i): 0 for i in range(1, 6)}
    for r in ratings:
        dist[str(r["stars"])] += 1
    return {
        "average": round(total / count, 1),
        "count": count,
        "distribution": dist,
    }


def export_data() -> dict:
    devis_all = []
    for fname in sorted(os.listdir(DEVIS_DIR)):
        if not fname.endswith(".json"):
            continue
        path = os.path.join(DEVIS_DIR, fname)
        with open(path, encoding="utf-8") as f:
            devis_all.append(json.load(f))

    analyses_all = []
    for fname in sorted(os.listdir(ANALYSES_DIR)):
        if not fname.endswith(".json"):
            continue
        path = os.path.join(ANALYSES_DIR, fname)
        with open(path, encoding="utf-8") as f:
            analyses_all.append(json.load(f))

    return {
        "exported_at": _ts(),
        "devis": devis_all,
        "analyses": analyses_all,
        "ratings": _load_ratings(),
        "rating_stats": get_rating_stats(),
        "stats": get_stats(),
    }
