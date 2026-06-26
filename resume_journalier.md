# Résumé session — AssurDevis AI

## 1. Analyse de contrat par upload PDF

Ajout du module **Scan & Analyse** : l'utilisateur upload un contrat PDF (via bouton 📄 ou suggestions), PyMuPDF extrait le texte, Ollama compare avec le PDF de référence (`reference_contrat.pdf`) et retourne un JSON structuré :
- Type de contrat (Auto / MRH / RC Pro…)
- Score de similarité (0–100%)
- Garanties, exclusions, franchises
- Résumé client en français/darija

**API** : `POST /analyse` — endpoint dédié, asynchrone.
**Frontend** : `addAnalyseCard()` — carte colorée avec barre de score, tags garanties/exclusions.

---

## 2. Nettoyage compagnies et ORASS

Retrait de toutes les références aux compagnies concurrentes (CAAT, SAA, Alliance) et au logiciel ORASS dans l'intention detection, le README, et le DEMO. Suppression de Tesseract des dépendances (PDF uniquement, pas d'image).

---

## 3. Module de sauvegarde silencieuse

**Principes** :
- 0 bouton visible pour l'utilisateur
- Sauvegarde automatique après chaque devis + chaque analyse
- Identifiant court (8 chars) + timestamp
- Dossier `saved/devis/` et `saved/analyses/`

**Fonctions** :
- `auto_save_devis()` — sauvegarde devis avec wilaya, garanties, montants
- `auto_save_analyse()` — sauvegarde résultat d'analyse PDF
- `_regenerate_report()` — régénère le rapport HTML à chaque sauvegarde

---

## 4. Scoring automatique des devis

Module `scoring.py` — note /100 pondérée :
- **Économie** 35% (basé sur le montant total TTC)
- **Couverture** 35% (basé sur le nombre de garanties souscrites)
- **Protection** 30% (basé sur le ratio RO / RNO)

Affiché en 🟢 (> 70) / 🟡 (40–70) / 🔴 (< 40) sur la carte devis.

**API** : `POST /scoring/devis`

---

## 5. Système de vote ⭐

5 étoiles cliquables sur chaque carte devis. 1 vote par devis. Moyenne globale affichée immédiatement.

**API** : `POST /rating` + `GET /rating/stats`
**Stockage** : `saved/ratings.json`

---

## 6. Export email automatisé

**Toutes les 24h** au démarrage + boucle horaire, l'IA consolide les données et les envoie par email :
- Corps HTML (tableau des indicateurs clés)
- Pièce jointe JSON (données brutes)
- Pièce jointe CSV (ouvrable dans Excel)

**Config** : `.env` — `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `SMTP_FROM`, `EXPORT_TO_EMAILS`
**Module** : `export_manager.py`

---

## 7. Rapport HTML live

Page autonome accessible via `/rapport` (URL bookmarkée par les responsables) :
- Stats : devis, analyses, montant total, orientations, consultations
- Garanties les plus demandées
- Votes : X votants · Y/5
- Top 10 Wilayas
- Liens exports JSON + CSV

Régénéré à chaque sauvegarde/vote. Optimisé pour impression Word (bordures, marges 1.5cm, polices pt).

---

## 8. Top 10 Wilayas + compteur orientation

- Champ `wilaya` extrait des `fields` et sauvegardé dans chaque devis
- Top 10 dans le rapport + CSV + JSON
- Intention `ORIENTATION` détectée dans `detect_intent()` (agence, orientation, bureau, rendez-vous, rdv…)
- `increment_counter("orientation")` thread-safe via `threading.Lock`
- `increment_counter("total_consultations")` à chaque message chat

---

## 9. Validation des champs frontend

Ajout de la validation côté client pour la collecte des champs Auto :
- Valeur véhicule ≥ 100 000 DA
- Puissance CV entre 3 et 15
- Âge entre 16 et 99 ans
- Durée : 1, 3, 6, 9 ou 12 mois
- Usage : personnel ou professionnel
- RC obligatoire dans les garanties
- Messages d'erreur + ré-posage de la question

---

## 10. Correctifs bugs (crédibilité)

| Problème | Correctif |
|---|---|
| `import logging` manquant | Ajouté dans `main.py` |
| Cache `_ollama_available` permanent | Supprimé — vérification à chaque appel |
| Race condition `increment_counter` | `threading.Lock` |
| Aucune limite upload PDF | Limite 50 Mo + HTTP 413 |
| `run.bat` échoue via `from engine import` | `start_assurdevis.bat` lance depuis `app/` |

---

## 11. `start_assurdevis.bat`

Lanceur unique pour la clé USB :
- Détection Python (système → portable)
- Installation automatique des dépendances
- Détection et lancement d'Ollama si présent
- Mode complet (avec IA) ou Lite (devis uniquement) selon disponibilité
- Ouverture navigateur sur `http://localhost:5000`

---

## Philosophie du projet

AssurDevis n'est **pas un portail client** (contrairement à CAAT E-Pack qui ignore l'assurance auto). C'est un **générateur de leads qualifiés** : l'IA qualifie, estime, collecte → le commercial finalise avec visite de risque. Les données sont exportées toutes les 24h vers les équipes métier (marketing, commercial, analyse).

> Prochaine étape envisagée : **renouvellement contrat auto** via upload du contrat en cours (sans bonus-malus), puis extension avec bonus-malus réel si la compagnie livre les contrats avant échéance.
