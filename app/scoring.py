from .engine import GARANTIES

# Garanties de base recommandées pour un bon score
GARANTIES_BASE    = {'RC', 'DR', 'AST'}
GARANTIES_CONFORT = {'VIV', 'BDG', 'EVNA'}
GARANTIES_PREMIUM = {'TOPR', 'TR', 'VAN', 'VN'}

def score_devis(devis: dict) -> dict:
    items     = devis.get("items", [])
    total_ttc = devis.get("total_ttc", 0)
    garanties = set(devis.get("garanties", []))

    total_ro  = sum(i.get("value", 0) for i in items if i.get("type") == "RO")
    total_rno = sum(i.get("value", 0) for i in items if i.get("type") == "RNO")
    has_dc    = any(i.get("code") in ("DC", "DC10") for i in items)

    eco_score  = _economy_score(total_ttc)
    cov_score  = _coverage_score(garanties, has_dc)
    prot_score = _protection_score(total_ro, total_rno)

    overall = round(eco_score * 0.35 + cov_score * 0.35 + prot_score * 0.30)

    return {
        "overall":    min(overall, 100),
        "economy":    eco_score,
        "coverage":   cov_score,
        "protection": prot_score,
        "details": {
            "total_ttc":       total_ttc,
            "garanties_count": len(garanties),
            "total_ro":        total_ro,
            "total_rno":       total_rno,
        },
    }


def _economy_score(total_ttc: int) -> int:
    """Score économie : une prime raisonnable = bon score."""
    if total_ttc <= 0:
        return 50
    if total_ttc <= 30_000:
        return 95
    if total_ttc <= 60_000:
        return 85
    if total_ttc <= 100_000:
        return 72
    if total_ttc <= 150_000:
        return 60
    if total_ttc <= 250_000:
        return 48
    return 35


def _coverage_score(garanties: set, has_dc: bool) -> int:
    """
    Score couverture : basé sur les garanties utiles, pas le catalogue complet.
    RC seule = 30. Chaque garantie utile ajoute des points.
    """
    score = 30  # RC obligatoire = base

    if has_dc:
        score += 25  # Dommages collision = grosse valeur ajoutée

    if garanties & {'VIV', 'VOL'}:
        score += 15  # Vol/Incendie
    if garanties & {'TOPR', 'TR'}:
        score += 20  # Tous Risques
    if garanties & {'BDG'}:
        score += 5
    if garanties & {'AST', 'ASTP'}:
        score += 5
    if garanties & {'DR', 'DRG'}:
        score += 5
    if garanties & {'EVNA', 'ICTM'}:
        score += 5

    return min(score, 100)


def _protection_score(total_ro: int, total_rno: int) -> int:
    """Score protection : équilibre entre garanties obligatoires et optionnelles."""
    total = total_ro + total_rno
    if total == 0:
        return 40
    # Un bon mix RO/RNO donne un bon score
    if total_rno > 0:
        ratio_rno = total_rno / total
        if ratio_rno >= 0.4:
            return 90
        if ratio_rno >= 0.2:
            return 75
        return 60
    return 50  # RC seule
