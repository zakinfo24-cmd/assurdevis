from .engine import GARANTIES


def score_devis(devis: dict) -> dict:
    items = devis.get("items", [])
    total_ttc = devis.get("total_ttc", 0)
    garanties = devis.get("garanties", [])

    total_ro = sum(
        i.get("value", 0) for i in items if i.get("type") == "RO"
    )
    total_rno = sum(
        i.get("value", 0) for i in items if i.get("type") == "RNO"
    )

    eco_score = _economy_score(total_ttc)
    cov_score = _coverage_score(garanties)
    prot_score = _protection_score(total_ro, total_rno)

    overall = round(eco_score * 0.35 + cov_score * 0.35 + prot_score * 0.30)

    return {
        "overall": min(overall, 100),
        "economy": eco_score,
        "coverage": cov_score,
        "protection": prot_score,
        "details": {
            "total_ttc": total_ttc,
            "garanties_count": len(garanties),
            "total_ro": total_ro,
            "total_rno": total_rno,
        },
    }


def _economy_score(total_ttc: int) -> int:
    if total_ttc <= 0:
        return 50
    if total_ttc <= 10000:
        return 90
    if total_ttc <= 20000:
        return 75
    if total_ttc <= 40000:
        return 60
    if total_ttc <= 70000:
        return 40
    return 20


def _coverage_score(garanties: list) -> int:
    total_options = len(GARANTIES) + 1
    selected = len([g for g in garanties if g in GARANTIES or g == "RC"])
    return round(min(selected / total_options * 100, 100))


def _protection_score(total_ro: int, total_rno: int) -> int:
    total = total_ro + total_rno
    if total == 0:
        return 30
    ratio = total_ro / total
    if ratio >= 0.5:
        return 90
    if ratio >= 0.3:
        return 70
    if ratio >= 0.15:
        return 50
    return 30
