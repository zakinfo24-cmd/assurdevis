"""Tests fonctionnels complets AssurDevis."""
import httpx, asyncio, json, os
BASE = "http://localhost:5000"

async def test():
    c = httpx.AsyncClient(timeout=60)
    ok = ko = 0

    async def check(label, method, path, **kw):
        nonlocal ok, ko
        try:
            if method == "GET":
                r = await c.get(BASE + path, **kw)
            else:
                r = await c.post(BASE + path, **kw)
            status = "OK" if r.status_code < 400 else "FAIL"
            if r.status_code < 400:
                ok += 1
            else:
                ko += 1
            print(f"  [{status}] {label} ({r.status_code})")
            return r
        except Exception as e:
            print(f"  [ERROR] {label} -> {e}")
            ko += 1
            return None

    print("=== TESTS FONCTIONNELS ===")
    await check("Health", "GET", "/health")
    await check("Chat salam", "POST", "/chat", json={"message": "salam"})
    r1 = await check("Chat devis auto", "POST", "/chat", json={"message": "devis auto"})
    await check("Chat agence", "POST", "/chat", json={"message": "agence"})
    await check("Chat question", "POST", "/chat", json={"message": "c quoi RC?"})

    # Devis Auto avec conversation
    if r1:
        conv_id = r1.json()["conversation_id"]
        fields = {"valeur": 2000000, "puissance": 7, "usage": "personnel",
                  "garanties": ["RC", "VOL", "INC"], "duree_mois": 12, "age": 30}
        r = await check("Devis Auto", "POST", "/devis/auto",
                        json={"conversation_id": conv_id, "message": json.dumps(fields)})
        if r and r.status_code == 200:
            d = r.json().get("devis", {})
            print(f"      -> {d.get('total_ttc', '?')} DA TTC, id={d.get('_id', '?')}")

    # Devis RD
    r2 = await check("Chat devis maison", "POST", "/chat", json={"message": "devis maison"})
    if r2:
        conv_id2 = r2.json()["conversation_id"]
        r = await check("Devis RD", "POST", "/devis/rd",
                        json={"conversation_id": conv_id2,
                              "message": json.dumps({"branche_rd": "incendie", "valeur_bien": 5000000})})
        if r and r.status_code == 200:
            d = r.json().get("devis", {})
            print(f"      -> {d.get('total_ttc', '?')} DA TTC")

    # Analyse PDF
    pdf_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "reference_contrat.pdf")
    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            r = await check("Analyse PDF", "POST", "/analyse",
                            files={"file": ("test.pdf", f.read(), "application/pdf")})
    else:
        print("  [SKIP] Analyse PDF (fichier non trouve)")

    # Endpoints stats
    await check("Admin stats", "GET", "/admin/stats")
    await check("Rapport HTML", "GET", "/rapport")
    await check("Export JSON", "GET", "/admin/export/download")
    await check("Export CSV", "GET", "/admin/export/download/csv")
    await check("Rating submit", "POST", "/rating",
                json={"message": json.dumps({"devis_id": "t123", "stars": 4})})
    await check("Rating stats", "GET", "/rating/stats")
    await check("Scoring", "POST", "/scoring/devis",
                json={"message": json.dumps(
                    {"items": [{"type": "RO", "value": 5000}, {"type": "RNO", "value": 3000}],
                     "total_ttc": 20000, "garanties": ["RC", "VOL", "INC"]})})

    # Vérifier rapport régénéré
    report_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "saved", "report.html")
    if os.path.exists(report_path):
        print(f"\nreport.html: {os.path.getsize(report_path)} bytes")
    else:
        print("\nreport.html: NON TROUVE")

    print(f"\n=== RESULTAT: {ok} reussis, {ko} echecs ===")

asyncio.run(test())
