"""Génération de rapports CSV/HTML exploitables par les équipes métier."""

import csv
import io
import json
import os
from datetime import datetime

from .save_manager import DEVIS_DIR, ANALYSES_DIR, _load_ratings


def devis_csv() -> str:
    """CSV devis : chaque ligne = 1 devis, colonnes = indicateurs clés."""
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow([
        "ID", "Date", "Type", "Wilaya", "Total TTC (DA)", "Mensualité (DA)",
        "Durée (mois)", "Nb Garanties", "Garanties",
        "TVA (DA)", "FGA (DA)", "Total HT (DA)", "Réduction (%)",
    ])
    files = sorted([f for f in os.listdir(DEVIS_DIR) if f.endswith(".json")])
    for fname in files:
        path = os.path.join(DEVIS_DIR, fname)
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
        w.writerow([
            d.get("id", ""),
            d.get("saved_at", ""),
            d.get("type", "auto"),
            d.get("wilaya", ""),
            d.get("total_ttc", 0),
            d.get("monthly", 0),
            d.get("duree_mois", 12),
            len(d.get("garanties", [])),
            ", ".join(d.get("garanties", [])),
            d.get("tva", 0),
            d.get("fga", 0),
            d.get("total_ht", 0),
            d.get("reduction", 0),
        ])
    return out.getvalue()


def analyses_csv() -> str:
    """CSV analyses : chaque ligne = 1 contrat analysé."""
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow([
        "ID", "Date", "Fichier", "Type Contrat",
        "Score Similarité (%)", "Reconnu",
    ])
    files = sorted([f for f in os.listdir(ANALYSES_DIR) if f.endswith(".json")])
    for fname in files:
        path = os.path.join(ANALYSES_DIR, fname)
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
        w.writerow([
            d.get("id", ""),
            d.get("saved_at", ""),
            d.get("filename", ""),
            d.get("type_contrat", ""),
            d.get("score_similarite", ""),
            "Oui" if d.get("reconnu") else "Non",
        ])
    return out.getvalue()


def ratings_csv() -> str:
    """CSV votes : chaque ligne = 1 vote client."""
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(["Date", "ID Devis", "Étoiles"])
    ratings = _load_ratings()
    for r in ratings:
        w.writerow([
            r.get("rated_at", ""),
            r.get("devis_id", ""),
            r.get("stars", ""),
        ])
    return out.getvalue()


def full_csv() -> str:
    """CSV complet avec en-tête de section et résumé."""
    from save_manager import get_stats, get_rating_stats
    stats = get_stats()
    rstats = get_rating_stats()
    parts = []
    parts.append("=== RÉSUMÉ ===")
    parts.append(f"Devis,{stats['total_devis']}")
    parts.append(f"Analyses,{stats['total_analyses']}")
    votes_avg = f"{rstats['average']:.2f}" if rstats['average'] else "-"
    parts.append(f"Votes,{rstats['count']},{votes_avg}/5")
    parts.append(f"Orientation,{stats['orientation_count']}")
    parts.append(f"Consultations totales,{stats['total_consultations']}")
    parts.append(f"Montant TTC total,{stats['total_ttc_sum']} DA")
    parts.append("")
    parts.append("=== TOP WILAYAS ===")
    parts.append("Rang,Wilaya,Nb consultations")
    for i, w in enumerate(stats.get("top_wilayas", []), 1):
        parts.append(f"{i},{w['wilaya']},{w['count']}")
    parts.append("")
    parts.append("=== DEVIS ===")
    parts.append(devis_csv().strip())
    parts.append("\n=== ANALYSES ===")
    parts.append(analyses_csv().strip())
    parts.append("")
    return "\n".join(parts)


def html_report() -> str:
    """Rapport HTML autonome, lisible dans un navigateur."""
    from save_manager import get_stats, get_rating_stats
    stats = get_stats()
    rstats = get_rating_stats()

    garanties_rows = "".join(
        f"<tr><td>{g}</td><td>{c}</td></tr>"
        for g, c in sorted(stats.get("garanties_breakdown", {}).items(),
                           key=lambda x: -x[1])
    )

    votes_count = rstats["count"]
    votes_avg = f"{rstats['average']:.2f}" if rstats["average"] else "—"

    wilaya_rows = "".join(
        f"<tr><td>{i+1}</td><td>{w['wilaya']}</td><td>{w['count']}</td></tr>"
        for i, w in enumerate(stats.get("top_wilayas", []))
    )

    return f"""<!DOCTYPE html>
<html lang="fr">
<head><meta charset="UTF-8"><title>AssurDevis — Rapport</title>
<style>
* {{ box-sizing: border-box; }}
body {{ font-family: 'Segoe UI', Arial, sans-serif; max-width: 880px; margin: 20px auto; padding: 0 16px; color: #1a1a1a; font-size: 14px; line-height: 1.5; }}
h1 {{ color: #6B1226; font-size: 22px; margin: 0 0 4px 0; }}
h2 {{ color: #4A0A1A; font-size: 17px; margin: 20px 0 8px 0; border-bottom: 2px solid #6B1226; padding-bottom: 4px; }}
table {{ width: 100%; border-collapse: collapse; margin: 8px 0; }}
th, td {{ text-align: left; padding: 6px 10px; border: 1px solid #999; font-size: 13px; }}
th {{ background: #e0d6d9; font-weight: 700; }}
.stats-table {{ width: 100%; margin: 12px 0; }}
.stats-table td {{ width: 20%; text-align: center; border: 1px solid #ccc; padding: 10px 6px; background: #f7f2ee; }}
.stat-val {{ font-size: 24px; font-weight: 700; color: #6B1226; display: block; }}
.stat-lbl {{ font-size: 10px; color: #555; text-transform: uppercase; letter-spacing: .3px; }}
.vote-big {{ font-size: 26px; font-weight: 700; color: #6B1226; margin: 4px 0; }}
a {{ color: #6B1226; }}
</style>
<style media="print">
@page {{ margin: 1.5cm; }}
body {{ margin: 0; padding: 0; font-size: 12pt; }}
h1 {{ font-size: 18pt; }}
h2 {{ font-size: 14pt; }}
th, td {{ border-color: #333; padding: 4pt 8pt; font-size: 11pt; }}
.stats-table td {{ padding: 6pt; }}
.stat-val {{ font-size: 16pt; }}
.stat-lbl {{ font-size: 8pt; }}
.vote-big {{ font-size: 18pt; }}
a {{ color: #333; text-decoration: none; }}
</style>
</head>
<body>
<h1>AssurDevis — Rapport de données</h1>
<p style="color:#888;font-size:12px;margin:0 0 12px 0;">Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}</p>
<table class="stats-table">
<tr>
  <td><span class="stat-val">{stats["total_devis"]}</span><span class="stat-lbl">Devis</span></td>
  <td><span class="stat-val">{stats["total_analyses"]}</span><span class="stat-lbl">Analyses</span></td>
  <td><span class="stat-val">{stats["total_ttc_sum"]:,}</span><span class="stat-lbl">Montant TTC (DA)</span></td>
  <td><span class="stat-val">{stats["orientation_count"]}</span><span class="stat-lbl">Demandes orientation</span></td>
  <td><span class="stat-val">{stats["total_consultations"]}</span><span class="stat-lbl">Consultations</span></td>
</tr>
</table>
<h2>Garanties les plus demandées</h2>
<table>{"".join(garanties_rows) if garanties_rows else "<tr><td>Aucune donnée</td></tr>"}</table>
<h2>Votes</h2>
<p class="vote-big">{votes_count} votants · {votes_avg}/5</p>
<h2>Top 10 Wilayas</h2>
<table>{"".join(wilaya_rows) if wilaya_rows else "<tr><td>Aucune donnée</td></tr>"}</table>
<h2>Fichiers</h2>
<p>Export JSON : <a href="/admin/export/download">telecharger</a><br>Export CSV (Excel) : <a href="/admin/export/download/csv">telecharger</a></p>
</body></html>"""
