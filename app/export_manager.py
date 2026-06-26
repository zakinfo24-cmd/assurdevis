import json
import os
import smtplib
import ssl
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .report_generator import full_csv, html_report


def _load_config() -> dict:
    return {
        "smtp_host": os.getenv("SMTP_HOST", ""),
        "smtp_port": int(os.getenv("SMTP_PORT", "587")),
        "smtp_user": os.getenv("SMTP_USER", ""),
        "smtp_pass": os.getenv("SMTP_PASS", ""),
        "smtp_from": os.getenv("SMTP_FROM", ""),
    }


async def send_export_mail(recipient: str, subject: str, data: dict) -> bool:
    cfg = _load_config()
    if not cfg["smtp_host"] or not cfg["smtp_user"] or not cfg["smtp_pass"]:
        return False

    ts = data["exported_at"].replace(":", "-")
    rstats = data.get("rating_stats", {})
    garanties = data["stats"].get("garanties_breakdown", {})

    body_html = f"""<!DOCTYPE html>
<html lang="fr">
<head><meta charset="UTF-8"><style>
body {{ font-family: system-ui, sans-serif; max-width: 600px; }}
h1 {{ color: #6B1226; font-size: 18px; }}
table {{ width: 100%; border-collapse: collapse; margin: 8px 0; }}
th, td {{ padding: 6px 10px; text-align: left; border-bottom: 1px solid #ddd; font-size: 13px; }}
th {{ background: #f0e6e9; }}
.sum {{ font-size: 22px; font-weight: 700; color: #6B1226; }}
</style></head>
<body>
<h1>📊 AssurDevis — Rapport d'activité</h1>
<p>Export du {data['exported_at']}</p>
<table>
<tr><th>Indicateur</th><th>Valeur</th></tr>
<tr><td>Devis réalisés</td><td class="sum">{data['stats']['total_devis']}</td></tr>
<tr><td>Analyses de contrats</td><td class="sum">{data['stats']['total_analyses']}</td></tr>
<tr><td>Votes clients</td><td class="sum">{rstats.get('count', 0)}</td></tr>
<tr><td>Note moyenne</td><td class="sum">{rstats.get('average', 0)}/5</td></tr>
<tr><td>Montant total TTC</td><td class="sum">{data['stats']['total_ttc_sum']:,} DA</td></tr>
</table>
<h2>✅ Garanties les plus demandées</h2>
<table>{"".join(f"<tr><td>{g}</td><td>{c}</td></tr>" for g, c in sorted(garanties.items(), key=lambda x: -x[1])) if garanties else "<tr><td>Aucune donnée</td></tr>"}</table>
<h2>⭐ Distribution des votes</h2>
<table>{"".join(f"<tr><td>{s} étoile(s)</td><td>{c}</td></tr>" for s, c in sorted(rstats.get('distribution', {}).items())) if rstats.get('count') else "<tr><td>Aucun vote</td></tr>"}</table>
<h2>📁 Fichiers joints</h2>
<p>Ce message contient 2 fichiers :</p>
<ul>
<li><strong>assurdevis_export_{ts}.json</strong> — données brutes (intégration système)</li>
<li><strong>assurdevis_export_{ts}.csv</strong> — tableau Excel (ouvrable directement)</li>
</ul>
</body></html>"""

    msg = MIMEMultipart("alternative")
    msg["From"] = cfg["smtp_from"]
    msg["To"] = recipient
    msg["Subject"] = subject

    msg.attach(MIMEText(body_html, "html"))

    # Pièce jointe JSON
    json_att = MIMEApplication(
        json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8"),
        _subtype="json",
    )
    json_att.add_header("Content-Disposition", "attachment",
                        filename=f"assurdevis_export_{ts}.json")
    msg.attach(json_att)

    # Pièce jointe CSV
    csv_data = full_csv()
    csv_att = MIMEApplication(csv_data.encode("utf-8"), _subtype="csv")
    csv_att.add_header("Content-Disposition", "attachment",
                       filename=f"assurdevis_export_{ts}.csv")
    msg.attach(csv_att)

    try:
        ctx = ssl.create_default_context()
        with smtplib.SMTP(cfg["smtp_host"], cfg["smtp_port"]) as server:
            server.ehlo()
            server.starttls(context=ctx)
            server.login(cfg["smtp_user"], cfg["smtp_pass"])
            server.sendmail(cfg["smtp_from"], [recipient], msg.as_string())
        return True
    except Exception:
        return False
