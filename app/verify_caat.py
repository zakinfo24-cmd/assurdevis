with open("static/index_CAAT.html", "r", encoding="utf-8") as f:
    c = f.read()

checks = {
    "CAAT avatar in header": '<div class="header-avatar">CAAT</div>',
    "Header name": "CAAT &mdash; Assistant IA",
    "Bot avatar JS": "avatar.textContent = 'CAAT'",
    "User avatar JS": "avatar.textContent = 'U'",
    "Gold accent": "--gold:",
    "Blue color var": "--caat-800:",
    "Suggestions remain": "suggestions",
    "Devis card": "devis-card",
    "Rating": "devis-rating",
    "Scoring": "calculateScore",
    "No AssurDevis": "AssurDevis",
    "No Sana": "Sana",
    "No bdx": "bdx-",
}
for label, term in checks.items():
    present = term in c
    ok_bad = "OK" if (present and "No " not in label) or (not present and "No " in label) else "ISSUE"
    print(f"{ok_bad}: {label} ({'found' if present else 'not found'})")

print(f"\nSize: {len(c)} bytes")
