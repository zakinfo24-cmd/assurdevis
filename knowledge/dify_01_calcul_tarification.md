---
fichier: dify_01_calcul_tarification-v2.md
domaine: Assurances Algériennes — Calcul & Tarification
source: Tables officielles (TARIF_AUTO, TARIF, TAXE, TAXE_ACCESSOIRE, COMMISSION, TIMBRE_GRADUE, TIMBRE_GRADUE_EXCEPTION, TARIF_IND_AUTO, REDUCTION_AUTOMOBILE, DETAIL_REDUCTION_AUTOMOBILE, GENRE_AUTO, BRANCHE, CATEGORIE, CONVENTION)
version: 2025-07 (barème effectif 2025/07/01) — Révision complète v2
statut: PRODUCTION
audit: Vérification complète sur tables CSV (Toutes_les_tables.zip — juin 2026)
---

## ⚠️ RÈGLES DE VERROUILLAGE DONNÉES (Prévention hallucination IA)

Toutes les valeurs ci-dessous proviennent **exclusivement** des tables officielles. Aucun taux, montant ou coefficient ne doit être inventé. Les sources de données permises sont :
- **TARIF** / **TARIF_AUTO** : taux et montants forfaitaires
- **TAXE** / **TAXE_ACCESSOIRE** : taux et bases de taxe (par CODECATE et CODTYPTA)
- **CONVENTION** : réductions par convention (CODEREDU → REDUCTION_AUTOMOBILE)
- **REDUCTION_AUTOMOBILE** / **DETAIL_REDUCTION_AUTOMOBILE** : codes de réduction
- **TIMBRE_GRADUE** / **TIMBRE_GRADUE_EXCEPTION** : timbres gradués
- **TARIF_IND_AUTO** : indemnités conducteur
- **GENRE_AUTO** : dictionnaire officiel des genres véhicule
- **COMMISSION** : taux de commission par catégorie et type d'intermédiaire

**Interdiction absolue :** Aucune mention de noms de compagnies d'assurance ou systèmes propriétaires.

---

# ⚡ AUDIT DE COHÉRENCE — CORRECTIONS APPLIQUÉES EN V2

## ANOMALIE A — Codes GENRE_AUTO (CRITIQUE)

**Source : table GENRE_AUTO.csv**

Le document v1 utilisait CODGENAU=03 pour désigner les « VP Tourisme » dans les barèmes RC. Cette association est **INCORRECTE**.

**Dictionnaire officiel GENRE_AUTO (extrait des tables)** :

| CODGENAU | Libellé officiel |
|---|---|
| 00 | Véhicules particuliers sans remorque |
| 01 | Remorques véhicules particuliers |
| 02 | Motocyclettes sans side-car jusqu'à 125 cm³ |
| **03** | **Side-car, tricycles, triporteurs** |
| 04 | TPM dont CU n'excède pas 2T sans mat. inflammable |
| 05 | Cyclomoteurs jusqu'à 50 cm³ |
| 06 | Scooter jusqu'à 125 cm³ |
| 07 | Scooter jusqu'à 175 cm³ |
| 08 | Triporteurs, tricycles jusqu'à 125 cm³ |
| 09 | Vélomoteurs sans side-car jusqu'à 125 cm³ |
| 10 | Voiture d'ambulance |
| 11 | Voiture de défilé & exhibitions |
| 12 | Corbillards et fourgons funéraires |
| 13 | Chasse-neige |
| 14 | Camions et bennes d'ordures ménagères |
| 15 | Camions de salubrité |
| 17 | Véhicules moteur indépendant remorque camping |
| 18 | Véhicules de sapeurs-pompiers |
| 19 | Véhicule particulier attelé d'une remorque |
| 30 | Véhicules dont le poids total excède 3,5T |
| 32 | TPM dont CU excède 2T sans mat. inflammable |
| 34 | TPV |
| 35 | Tracteurs routiers attelés de semi-remorque |
| 36 | Tracteurs routiers seuls |
| 47 | Garagistes Automobiles (plaques) |
| 48 | Garagistes Cyclomoteurs (plaques) |

**Règle corrigée pour Sana (devis VP Tourisme) :**
- CODGENAU = **00** = VP sans remorque (standard Auto Tourisme)
- CODGENAU = **03** = Side-car / Tricycle / Triporteur (≠ VP Tourisme)

**Dans TARIF_AUTO, le genre 03 correspond effectivement à Side-car/Tricycle/Triporteur** (usage 01/02/03, zones N/S). Pour les VP standard, utiliser CODGENAU=00.

---

## ANOMALIE B — Timbre Gradué Genre 03 (CONFIRMÉ)

**Source : table TIMBRE_GRADUE.csv**

Il n'existe **aucune ligne** TIMBRE_GRADUE avec CODGENAU=03 (Side-car) pour prime ≥ 10 000 DA ayant un palier distinct. Les données réelles pour le genre numérique 3 (03) sont :

**TIMBRE_GRADUE Genre 03 (Side-car / Tricycle / Triporteur) — table officielle :**

| PUIVEHMI | PUIVEHMA | TRANCHE PRIME | Valeur fixe | Taux | Date effet |
|---|---|---|---|---|---|
| 1 | 10 | Prime < 2 500 DA | **300 DA** | — | 2006/01/01 |
| 1 | 10 | 2 500 ≤ Prime < 10 000 DA | — | **5%** | 2006/01/01 |
| 1 | 10 | 10 000 ≤ Prime < 50 000 DA | — | **10%** | 2006/01/01 |
| 1 | 10 | Prime ≥ 50 000 DA | — | **15%** | 2006/01/01 |
| 11 | 999 | Prime < 2 500 DA | **600 DA** | — | 2006/01/01 |
| 11 | 999 | 2 500 ≤ Prime < 10 000 DA | — | **10%** | 2006/01/01 |
| 11 | 999 | 10 000 ≤ Prime < 50 000 DA | — | **20%** | 2006/01/01 |
| 11 | 999 | Prime ≥ 50 000 DA | — | **30%** | 2006/01/01 |
| 0 | 99 | Prime < 2 500 DA | **300 DA** | — | 2009/04/01 |
| 0 | 99 | 2 500 ≤ Prime < 10 000 DA | — | **5%** | 2009/04/01 |
| 0 | 99 | 10 000 ≤ Prime < 50 000 DA | — | **3%** | 2009/04/01 |
| 0 | 99 | Prime ≥ 50 000 DA | — | **2%** | 2009/04/01 |

**Note :** La table utilise des valeurs entières sans zéro de tête. CODGENAU=3 = Genre 03. Le barème 2009/04/01 (PUIVEHMI=0, PUIVEHMA=99) est plus récent et prévaut.

**Conclusion :** La v1 affirmait un palier unique à 5% pour prime ≥ 10 000 DA Genre 03. C'est incorrect. Le barème réel distingue quatre tranches avec descente des taux après 2009.

---

## ANOMALIE C — Réductions Paiement (Chèque, Virement, TPE) INEXISTANTES EN TABLE

**Source : tables REDUCTION_AUTOMOBILE, DETAIL_REDUCTION_AUTOMOBILE, TYPE_TARIF_TPV**

Après audit exhaustif de toutes les tables :
- **Aucune table** ne contient de réduction spécifique pour mode de paiement Chèque, Virement, ou TPE pour la branche Auto standard (CODECATE=1110/1111).
- La table `REDUCTION_TPV` concerne uniquement les flottes TPV (catégorie 1111) avec des réductions par nombre de véhicules (NBRMINRI/NBRMAXRI).

**Conséquence :** Les réductions Chèque (3%), Virement (2%), TPE (0%) mentionnées en v1 sont des valeurs **documentaires sans source table officielle**. Elles sont supprimées du moteur de calcul.

**Règle corrigée :** Dans l'algorithme de sélection de réduction (ÉTAPE 6), supprimer l'option « Réduction Paiement » :
1. Convention (priorité 1)
2. Pack Combiné (priorité 2)
3. Réduction Commerciale REDUCTION_AUTOMOBILE (priorité 3)

Si aucune des 3 : réduction = 0%.

---

## ANOMALIE D — Pack Combiné Auto + RD (TAUX ABSENTS EN TABLE)

**Source : toutes les tables disponibles (audit complet)**

Aucune table du jeu de données ne contient de taux pour un « Pack Combiné Auto + RD ». La structure CONVENTION référence des codes de réduction (CODEREDU) existant dans REDUCTION_AUTOMOBILE, mais aucun code spécifique « Pack Combiné » n'est détecté.

**Conséquence :** Le Pack Combiné est supprimé comme catégorie de réduction calculable dans l'algorithme. Il peut exister comme concept commercial mais son taux n'est pas définissable à partir des tables disponibles.

---

## ANOMALIE E — Partie J (RD/IARDT) — État réel

**Constat après audit :** La Partie J v1 contenait uniquement des statistiques observées (prime médiane MRH = 3 241 DA, prime médiane Incendie = 777 000 DA), sans aucune formule de calcul. Ces données sont des moyennes empiriques non calculables.

**La Partie J est reconstruite en Section J ci-dessous** à partir des tables réelles.

---

================================================================================
# PARTIE A — STRUCTURE UNIVERSELLE DE LA PRIME
================================================================================

---

## [DEVIS::STRUCTURE_PRIME::FORMULE_COEFFICIENTS_ENCADRES]

> TYPE: définition_coefficients
> APPLICABLE: tous_produits_auto

**COEFFICIENTS PERMIS (liste exhaustive) :**
```
Les SEULS coefficients autorisés sont :
  1. coef_zone    → CODEZONE (N = Nord, S = Sud)
  2. coef_usage   → CODUSAAU (01=Personnel, 02=Commerce, 03=Taxi, etc.)
  3. coef_durée   → MAJORATION_DUREE (selon durée souscrite)

AUCUN AUTRE COEFFICIENT NE PEUT ÊTRE INVENTÉ OU AJOUTÉ.

⚠️ La CONVENTION n'est PAS un coefficient global. C'est une réduction appliquée
exclusivement sur le Total_RNO_brut (cf. ÉTAPE 6 / PARTIE F), sélectionnée
parmi les réductions disponibles selon hiérarchie de priorité.
```

---

## [DEVIS::STRUCTURE_PRIME::FORMULE_GENERALE]

> TYPE: formule_calcul
> APPLICABLE: tous_produits_auto

```
PRIME TTC = PRIME_NETTE + TAXES + TIMBRE_GRADUE
```

Décomposition complète :

```
1. PRIME NETTE = Somme des primes ajustées :

   a) Partie Obligatoire :
   - RC_brute = TARIF_AUTO[CODEGARA='RC', CODGENAU, CODUSAAU, CODEZONE,
                            PUISMINI ≤ cv ≤ PUISMAXI].MONTFIXE
               × coef_durée
   - Garanties RO hors RC (DR, DRG, AST, ASTP) :
     Prime_g = TARIF_AUTO[CODEGARA=g, ...].MONTFIXE × coef_durée

   Total_RO = RC_brute + Σ(garanties RO hors RC)

   b) Parties Optionnelles (RNO) :
   - Pour chaque garantie optionnelle g :
     SI TARIF_AUTO[g].TAUXCAPI ≠ NULL (garantie proportionnelle au capital) :
        Prime_g = TARIF_AUTO[g].TAUXCAPI × VALEUR_VENALE × coef_durée

     SINON SI TARIF_AUTO[g].MONTFIXE ≠ NULL (garantie forfaitaire) :
        Prime_g = TARIF_AUTO[g].MONTFIXE × coef_durée
        [Le coefficient de zone et d'usage sont déjà reflétés dans le MONTFIXE
        retourné par la requête TARIF_AUTO filtrée sur CODEZONE et CODUSAAU]

   Total_RNO_brut = Σ(Prime_g pour g ∈ RNO)

   c) Réduction RNO (une seule, selon hiérarchie ÉTAPE 6 — v2 : 3 options) :
   - Total_RNO_net = Total_RNO_brut × (1 − réduction_sélectionnée)

   d) Indemnité Conducteur (jamais soumise à réduction) :
   - Ind = TARIF_IND_AUTO[FORMULE, NOMPLAIN].PRIM_PTA × coef_durée

   e) Surprimes réglementaires (jeune conducteur, permis récent),
      calculées sur (Total_RO + Total_RNO_net + Ind)

   PRIME_NETTE = Total_RO + Total_RNO_net + Ind + Surprimes

2. TAXES = ∑ (BASE_TAXE_i × TAUX_TAXE_i)
   Source : TAXE[CODTYPTA, CODECATE, CODEGARA, DATEEFFE la plus récente ≤ date émission]
   - CODTYPTA=1 (TVA compagnie) : TAUXPRIM=19% depuis 2017/01/01, base='R' (prime nette)
   - CODTYPTA=2 (FGA réassurance) : TAUXPRIM=3%, base='R'
   Source complémentaire : TAXE_ACCESSOIRE[CODTYPTA, CODECATE, DATEEFFE]

3. TIMBRE_GRADUE = cf. PARTIE E — barème par CODGENAU, PUIVEHMI/MA, tranches de prime

4. PRIME TTC = PRIME_NETTE + TAXES + TIMBRE_GRADUE
```

**Commission intermédiaire** (table COMMISSION — ne s'applique pas au calcul client) :
- Source : COMMISSION[CODTYPIN, CODECATE, CODEGARA, DATEEFFE]
- TAUCOMAP = taux d'apport (pour l'intermédiaire)
- TAUCOMGE = taux de gestion (pour la compagnie)
- Ces taux sont comptables, ils n'entrent pas dans la prime client.

---

================================================================================
# PARTIE B — BARÈME RC AUTO (TARIF_AUTO, effectif 2025/07/01)
================================================================================

---

## [DEVIS::AUTO::BAREME_RC::VP_TOURISME]

> TYPE: bareme_tarifaire
> SOURCE: TARIF_AUTO — CODEGARA='RC', CODGENAU=03, date 2025/07/01
> APPLICABLE: Side-car/Tricycle/Triporteur (Genre 03)
> ⚠️ ATTENTION : CODGENAU=03 = Side-car/Tricycle selon GENRE_AUTO

### Règle de lecture :
- **MONTFIXE** = prime RC annuelle brute en DA (avant durée et taxes)
- **PRIMMINI** = prime minimale perçue (plancher réglementaire)
- La prime applicable = **max(MONTFIXE × coef_durée, PRIMMINI)**

---

### B.1 — RC Genre 03 — Usage 01 (Personnel)

| Tranche CV | Zone N (DA/an) | Zone S (DA/an) | Prime mini |
|---|---|---|---|
| 1–2 CV | 1 109,42 | 876,39 | 114,75 |
| 3–4 CV | 1 463,54 | 1 167,77 | 114,75 |
| 5–6 CV | 1 827,71 | 1 463,54 | 114,75 |
| 7–10 CV | 2 217,77 | 1 756,27 | 114,75 |
| 11–14 CV | 2 576,91 | 2 056,24 | 128,86 |
| 15–23 CV | 2 824,35 | 2 340,06 | 141,23 |

> Source : DATEEFFE = 2025/07/01

---

### B.2 — RC Genre 03 — Usage 02 (Commerce)

| Tranche CV | Zone N (DA/an) | Zone S (DA/an) |
|---|---|---|
| 1–2 CV | 1 438,54 | 1 135,83 |
| 3–4 CV | 1 898,77 | 1 514,42 |
| 5–6 CV | 2 370,48 | 1 898,80 |
| 7–10 CV | 2 877,52 | 2 277,39 |
| 11–14 CV | 3 343,48 | 2 667,91 |
| 15–23 CV | 3 663,89 | 3 034,61 |

---

### B.3 — RC Genre 03 — Usage 00 (Affaire)

| Tranche CV | Zone N (DA/an) | Zone S (DA/an) |
|---|---|---|
| 1–2 CV | 1 307,92 | 1 032,59 |
| 3–4 CV | 1 726,22 | 1 376,75 |
| 5–6 CV | 2 155,17 | 1 726,24 |
| 7–10 CV | 2 615,85 | 2 070,41 |
| 11–14 CV | 3 039,47 | 2 425,21 |
| 15–23 CV | 3 330,69 | 2 758,82 |

---

### B.4 — RC Genre 03 — Usage 03 (Taxi)

| Tranche CV | Zone N (DA/an) | Zone S (DA/an) |
|---|---|---|
| 1–2 CV | 2 163,99 | 1 492,82 |
| 3–4 CV | 3 095,06 | 2 173,27 |
| 5–6 CV | 3 543,82 | 2 616,73 |
| 7–10 CV | 4 003,16 | 3 048,72 |
| 11–14 CV | 4 688,91 | 3 730,47 |
| 15–23 CV | 5 035,76 | 4 108,21 |
| 24–99 CV | 5 270,07 | 4 354,89 |

---

### B.5 — Zones géographiques

- **Zone N** = Nord (Alger, Oran, Constantine, Annaba, Blida, Tizi-Ouzou, Béjaïa…)
- **Zone S** = Sud / Hauts Plateaux (Biskra, Laghouat, Ghardaïa, Ouargla, Tamanrasset…)

**Règle pratique :** si la wilaya n'est pas classée explicitement, appliquer Zone N.

---

### B.6 — Identification du genre pour VP standard

Pour un véhicule particulier touristique standard (berline, SUV, citadine…) :
- Utiliser CODGENAU=**00** (VP sans remorque) dans la requête TARIF_AUTO.
- Utiliser CODGENAU=**03** uniquement pour side-car, tricycle, triporteur réel.

---

================================================================================
# PARTIE C — COEFFICIENTS DE DURÉE
================================================================================

---

## [DEVIS::AUTO::COEFFICIENTS_DUREE]

> TYPE: barème_durée
> SOURCE: MAJORATION_DUREE — CODECATE=1110, effectif permanent depuis 1988

| Code | Durée | Coefficient (% de la prime annuelle) |
|---|---|---|
| A | 12 mois (annuel) | **100%** |
| S | 6 mois | **55%** |
| T | 3 mois | **35%** |
| M | 1 mois | **25%** |
| DJ | 10 jours | **10%** |
| TJ | 3 jours | **5%** |
| VJ | 20 jours | **18%** |

**Durées spéciales 1114 (Transport Public Voyageurs) :**
- M (1 mois) = 50%
- BM (2 mois) = 63%
- T (3 mois) = 75%

**Formule d'application :**
```
Prime_durée = MONTFIXE × (coef_durée / 100)
Prime_durée = max(Prime_durée, PRIMMINI)
```

---

================================================================================
# PARTIE D — GARANTIES OPTIONNELLES (RNO)
================================================================================

---

## [DEVIS::AUTO::GARANTIES_LISTE]

> TYPE: catalogue_garanties
> SOURCE: TARIF_AUTO — codes CODEGARA
> APPLICABLE: catégorie 1110/1111 (Auto VP Tourisme)

### D.1 — Garanties Responsabilité Obligatoire (RO)
Ne sont pas soumises à réduction commerciale.

| Code | Libellé | Mode de calcul | Source |
|---|---|---|---|
| RC | Responsabilité Civile | **FORFAITAIRE** : MONTFIXE × coef_durée (filtré zone/usage) | TARIF_AUTO.MONTFIXE |
| DR | Défense et Recours | **FORFAITAIRE** : MONTFIXE × coef_durée | TARIF_AUTO.MONTFIXE |
| DRG | Défense et Recours Garnissage | **FORFAITAIRE** : MONTFIXE × coef_durée | TARIF_AUTO.MONTFIXE |
| AST / ASTP | Assistance | **FORFAITAIRE** : MONTFIXE × coef_durée | TARIF_AUTO.MONTFIXE |

### D.2 — Garanties Facultatives (RNO)
Soumises à réduction commerciale.

| Code | Libellé | Mode de calcul | Source |
|---|---|---|---|
| VIV | Vol, Incendie, Vandalisme | **PROPORTIONNEL** : TAUXCAPI × valeur_venale × coef_durée | TARIF_AUTO.TAUXCAPI |
| VOL | Vol seul | **PROPORTIONNEL** : TAUXCAPI × valeur_venale × coef_durée | TARIF_AUTO.TAUXCAPI |
| TR | Tous Risques | **PROPORTIONNEL** : TAUXCAPI × valeur_venale × coef_durée | TARIF_AUTO.TAUXCAPI |
| BDG | Bris de Glaces | **FORFAITAIRE** : MONTFIXE × coef_durée | TARIF_AUTO.MONTFIXE |
| EVNA | Événements Naturels (hors CAT-NAT) | **PROPORTIONNEL** : TAUXCAPI × valeur_venale × coef_durée | TARIF_AUTO.TAUXCAPI |
| DCA–DCG | Dommages Collision (niveaux) | **FORFAITAIRE** : MONTFIXE × coef_durée | TARIF_AUTO.MONTFIXE |
| ASC2–ASC5 | Dommages Avec/Sans Collision (plafonds : ASC2=200 000 DA, ASC3=300 000 DA, ASC5=500 000 DA) | **FORFAITAIRE** : MONTFIXE × coef_durée | TARIF_AUTO.MONTFIXE |
| ASV1–ASV4 | Assistance Voyageur niveaux 1–4 | **FORFAITAIRE** : MONTFIXE × coef_durée | TARIF_AUTO.MONTFIXE |
| PEA | Protection Équipements Audio | **FORFAITAIRE** : MONTFIXE × coef_durée | TARIF_AUTO.MONTFIXE |
| EXTB / EXTRC | Extension RC Frontière / Branche | **FORFAITAIRE** : MONTFIXE × coef_durée | TARIF_AUTO.MONTFIXE |
| INCD | Incapacité | **FORFAITAIRE** : MONTFIXE × coef_durée | TARIF_AUTO.MONTFIXE |

**⚠️ RÈGLE CRITIQUE :**
- **PROPORTIONNEL** → TAUXCAPI × VALEUR_VENALE × coef_durée (jamais MONTFIXE)
- **FORFAITAIRE** → MONTFIXE × coef_durée uniquement (jamais TAUXCAPI ou capital)

> Les taux exacts (TAUXCAPI / MONTFIXE) se trouvent dans TARIF_AUTO filtré par
> CODEGARA, CODGENAU, CODUSAAU, CODEZONE, DATEEFFE la plus récente ≤ date émission.

---

### D.3 — Garanties Corporelles — Indemnité Conducteur

> SOURCE: TARIF_IND_AUTO

| Formule | Capital Décès | Capital Invalidité | Frais Médicaux | Prime (5 CV) |
|---|---|---|---|---|
| A | 10 000 DA | 20 000 DA | 2 000 DA | 107–221 DA selon places |
| B | 20 000 DA | 40 000 DA | 4 000 DA | 164–392 DA |
| C | 30 000 DA | 30 000 DA | 2 500 DA | 172–415 DA |
| D | 50 000 DA | 50 000 DA | 5 000 DA | 260–680 DA |
| E | 100 000 DA | 100 000 DA | 6 000 DA | 398–1 094 DA |
| F | 200 000 DA | 200 000 DA | 8 000 DA | 680–1 940 DA |

Formule : `PRIM_PTA` (prime annuelle directe issue de TARIF_IND_AUTO).
L'Indemnité Conducteur n'est **jamais** soumise à réduction.

---

================================================================================
# PARTIE E — TIMBRE GRADUÉ (CORRIGÉ)
================================================================================

---

## [DEVIS::AUTO::TIMBRE_GRADUE]

> TYPE: taxe_parafiscale
> SOURCE: TIMBRE_GRADUE — barèmes effectifs 2009/04/01 (NUME_LOT=5, le plus récent)
> et TIMBRE_GRADUE_EXCEPTION pour genres particuliers

### Logique de sélection :
1. Chercher dans TIMBRE_GRADUE_EXCEPTION si le genre a une règle spéciale
2. Sinon consulter TIMBRE_GRADUE avec filtres : CODGENAU, PUIVEHMI ≤ puissance ≤ PUIVEHMA, PRIMMINI ≤ prime_nette ≤ PRIMMAXI
3. Appliquer : si VALTIMGR > 0 → timbre fixe = VALTIMGR ; si TAUTIMGR > 0 → timbre = prime_nette × (TAUTIMGR/100)

### TIMBRE_GRADUE_EXCEPTION (genres spéciaux — valeur forfaitaire) :

Les genres suivants ont un timbre forfaitaire indépendant de la prime :

**Barème 1988 (ancien) :**

| Genre | Valeur Timbre |
|---|---|
| 04, 14, 15, 16, 18, 30, 31, 32, 33, 35, 36, 38, 45, 46, 49 | 1 200 DA |

**Barème 2006 (en vigueur depuis 2006/01/01) :**

| Genre | Valeur | Taux |
|---|---|---|
| 14, 15, 16, 18, 30, 31, 32, 33, 35, 36, 38, 45, 46, 49 | 0 | **100% de la prime** |

---

### Genre 00 (VP sans remorque) — PUIVEHMI=11, PUIVEHMA=999 (puissance ≥ 11CV) :

| Tranche de prime nette | Valeur fixe | Taux |
|---|---|---|
| Prime < 2 500 DA | **600 DA** | — |
| 2 500 ≤ Prime < 10 000 DA | — | **10%** |
| 10 000 ≤ Prime < 50 000 DA | — | **6%** *(barème 2009)* |
| Prime ≥ 50 000 DA | — | **4%** *(barème 2009)* |

> Source : TIMBRE_GRADUE PUIVEHMI=11, PUIVEHMA=99, CODGENAU=0, DATEEFFE=2009/04/01, NUME_LOT=5

### Genre 00 (VP sans remorque) — PUIVEHMI=0, PUIVEHMA=10 (puissance ≤ 10CV) :

| Tranche de prime nette | Valeur fixe | Taux |
|---|---|---|
| Prime < 2 500 DA | **300 DA** | — |
| 2 500 ≤ Prime < 10 000 DA | — | **5%** |
| 10 000 ≤ Prime < 50 000 DA | — | **3%** |
| Prime ≥ 50 000 DA | — | **2%** |

> Source : TIMBRE_GRADUE PUIVEHMI=0, PUIVEHMA=10, CODGENAU=0, DATEEFFE=2009/04/01, NUME_LOT=5

---

### Genre 03 (Side-car / Tricycle / Triporteur) — PUIVEHMI=0, PUIVEHMA=99 :

| Tranche de prime nette | Valeur fixe | Taux |
|---|---|---|
| Prime < 2 500 DA | **300 DA** | — |
| 2 500 ≤ Prime < 10 000 DA | — | **5%** |
| 10 000 ≤ Prime < 50 000 DA | — | **3%** |
| Prime ≥ 50 000 DA | — | **2%** |

> Source : TIMBRE_GRADUE PUIVEHMI=0, PUIVEHMA=99, CODGENAU=3, DATEEFFE=2009/04/01, NUME_LOT=5

**⚠️ NOTE CRITIQUE (correction v2) :** Le taux unique à 5% pour prime ≥ 10 000 DA Genre 03 de la v1 était **incorrect**. Le barème réel 2009 distingue 3% (10k–50k) et 2% (≥50k).

---

### Genre 34 (TPV) — PUIVEHMI=11, PUIVEHMA=999 :

| Tranche de prime nette | Valeur fixe | Taux |
|---|---|---|
| Prime < 2 500 DA | **600 DA** | — |
| 2 500 ≤ Prime < 10 000 DA | — | **10%** |
| 10 000 ≤ Prime < 50 000 DA | — | **20%** |
| Prime ≥ 50 000 DA | — | **30%** |

> Source : TIMBRE_GRADUE PUIVEHMI=11, PUIVEHMA=999, CODGENAU=34, DATEEFFE=2006/01/01

---

**Application :** Le timbre est calculé sur la prime nette HT avant taxes.

---

================================================================================
# PARTIE F — RÉDUCTIONS ET MAJORATIONS (CORRIGÉE)
================================================================================

---

## [DEVIS::AUTO::REDUCTIONS_CATALOGUE]

> SOURCE: REDUCTION_AUTOMOBILE — liste des codes de réduction autorisés

### F.1 — Réductions sur la partie RNO uniquement

| Code | Libellé | Taux |
|---|---|---|
| R1 | Auto 5% sur RNO | 5% |
| R2 | Auto 10% sur RNO | 10% |
| RA | Auto 15% sur RNO | 15% |
| RB | Auto 25% sur RNO | 25% |
| R3 | Réduction 30% | 30% |
| M5 | Réduction 20% | 20% |
| R7 | Auto 35% sur RNO | 35% |
| R6 | Auto 40% sur RNO | 40% |
| M1 | Réduction 40% | 40% |
| RD | Auto 45% sur RNO | 45% |
| R4 / R5 / N1 / N2 | Auto 50% sur RNO | 50% |
| RI / 01 | Réduction 50% | 50% |
| AS | Réduction 55% | 55% |
| M6 | Réduction 60% | 60% |
| RF | Auto 60% sur RNO (Flottes convention) | 60% |

### F.2 — Réductions Flottes (code F*)

| Code | Libellé | Taux |
|---|---|---|
| FA | Auto Flotte 10% sur RNO | 10% |
| FB | Auto Flotte 15% sur RNO | 15% |
| FD | Auto Flotte 30% sur RNO | 30% |
| FE | Auto Flotte 35% sur RNO | 35% |
| F1–F6 | Auto Flotte 40%–50% sur RNO | 40–50% |
| FK | Auto Flotte 72% sur RNO | 72% |
| FL | Auto Flotte 77% sur RNO | 77% |

### F.3 — Majorations

| Code | Libellé | Taux |
|---|---|---|
| A1 | Majoration 10% | +10% |
| A2 | Majoration 20% | +20% |
| A3 | Majoration 30% | +30% |

### F.4 — RÉDUCTIONS DE PAIEMENT (SUPPRIMÉES en v2)

**⚠️ CORRECTION v2 :** Les réductions Chèque (3%), Virement (2%), TPE (0%) sont supprimées.
Elles n'existent pas dans les tables officielles pour les branches Auto standard.
Ces valeurs étaient documentaires. Ne pas les intégrer dans l'algorithme de calcul.

### F.5 — PACK COMBINÉ Auto + RD (SUPPRIMÉ en v2)

**⚠️ CORRECTION v2 :** Aucun taux de Pack Combiné n'est présent dans les tables.
Le concept peut exister commercialement mais le taux n'est pas calculable.
Ne pas inclure dans l'algorithme.

---

## [DEVIS::AUTO::SURPRIMES_REGLEMENTAIRES]

| Condition | Surprime |
|---|---|
| Conducteur < 21 ans | +25% sur prime totale |
| Conducteur 21–24 ans | +15% sur prime totale |
| Permis < 1 an | +10% sur prime totale |

---

================================================================================
# PARTIE G — ALGORITHME DE CALCUL COMPLET (v2)
================================================================================

---

## [DEVIS::AUTO::ALGORITHME_CALCUL]

> TYPE: algorithme_sequentiel
> APPLICABLE: Auto tous genres

```
ÉTAPE 1 — IDENTIFIER LES PARAMÈTRES
  - puissance_cv    ∈ {1-2, 3-4, 5-6, 7-10, 11-14, 15-23, 24+}
  - genre_auto      → CODGENAU (voir tableau GENRE_AUTO officiel)
  - usage           ∈ {00=Affaire, 01=Fonctionnaire, 02=Commerce, 03=Taxi, ...}
  - zone            ∈ {N=Nord, S=Sud}
  - durée_code      ∈ {A, S, T, M, DJ, TJ, VJ}
  - garanties[]     = liste des codes garantie souhaités
  - valeur_venale   = valeur marchande du véhicule (DA)
  - conducteur_age  = âge du conducteur principal
  - anciennete_permis = années depuis l'obtention du permis
  - code_reduction  = code réduction commerciale REDUCTION_AUTOMOBILE (peut être nul)
  - code_convention = code convention CONVENTION (peut être nul)

⚠️ SÉLECTION CODGENAU — RÈGLE OBLIGATOIRE :
  - VP Tourisme standard (berline, SUV...) → CODGENAU = 00
  - Side-car, tricycle, triporteur → CODGENAU = 03
  - TPV → CODGENAU = 34
  Cf. table GENRE_AUTO pour tous les autres genres.

ÉTAPE 2 — CALCUL RC OBLIGATOIRE
  RC_annuel = TARIF_AUTO[
    CODEGARA='RC',
    CODGENAU = genre_auto,
    CODUSAAU = usage,
    CODEZONE = zone,
    PUISMINI ≤ cv ≤ PUISMAXI,
    DATEEFFE la plus récente ≤ date_émission
  ].MONTFIXE
  RC_annuel = max(RC_annuel, PRIMMINI)
  RC_période = RC_annuel × coef_durée[durée_code]
  RC_période = max(RC_période, PRIMMINI)

ÉTAPE 3 — CALCUL GARANTIES RO HORS RC (DR, AST, etc.)
  Pour chaque garantie g ∈ {DR, DRG, AST, ASTP} :
    Prime_g = TARIF_AUTO[CODEGARA=g, même filtres].MONTFIXE × coef_durée

ÉTAPE 4 — TOTAL RO
  Total_RO = RC_période + Σ(Prime_g pour g∈RO_hors_RC)

ÉTAPE 5 — CALCUL GARANTIES RNO (facultatives)
  Pour chaque garantie g ∈ garanties_optionnelles :
    SI TARIF_AUTO[CODEGARA=g, ...].TAUXCAPI ≠ NULL :
      Prime_g = TARIF_AUTO[g].TAUXCAPI × valeur_venale × coef_durée
    SINON SI TARIF_AUTO[CODEGARA=g, ...].MONTFIXE ≠ NULL :
      Prime_g = TARIF_AUTO[g].MONTFIXE × coef_durée
    Prime_g = max(Prime_g, PRIMMINI_g)

  Total_RNO_brut = Σ(Prime_g pour g∈RNO)

ÉTAPE 6 — SÉLECTION RÉDUCTION (une seule, 3 options en v2)

  ⚠️ RÈGLE CORRIGÉE v2 : Réductions paiement et Pack Combiné SUPPRIMÉS.

  1. SI code_convention fourni ET existe dans CONVENTION (DATEEFFE ≤ date ET DATERESI ≥ date) :
       code_reduction_effectif = CONVENTION[code_convention].CODEREDU
       réduction_sélectionnée = REDUCTION_AUTOMOBILE[code_reduction_effectif].taux
       → APPLIQUER cette réduction ✓ → ARRÊTER

  2. SINON SI code_reduction fourni ET existe dans REDUCTION_AUTOMOBILE :
       réduction_sélectionnée = REDUCTION_AUTOMOBILE[code_reduction].taux
       → APPLIQUER cette réduction ✓ → ARRÊTER

  3. SINON :
       réduction_sélectionnée = 0%

  Application :
    Total_RNO_net = Total_RNO_brut × (1 - réduction_sélectionnée / 100)

ÉTAPE 7 — INDEMNITÉ CONDUCTEUR
  Ind_conducteur = TARIF_IND_AUTO[FORMINDI=formule, NOMPLAIN=places].PRIM_PTA × coef_durée
  ⚠️ Jamais soumise à réduction.

ÉTAPE 8 — SURPRIMES
  Prime_intermédiaire = Total_RO + Total_RNO_net + Ind_conducteur

  Si conducteur_age < 21 :
    Surprime_jeune = Prime_intermédiaire × 0,25
  Sinon si conducteur_age < 25 :
    Surprime_jeune = Prime_intermédiaire × 0,15
  Sinon : Surprime_jeune = 0

  Si anciennete_permis < 1 :
    Surprime_permis = Prime_intermédiaire × 0,10
  Sinon : Surprime_permis = 0

ÉTAPE 9 — PRIME NETTE HT
  Prime_Nette = Prime_intermédiaire + Surprime_jeune + Surprime_permis

ÉTAPE 10 — TIMBRE GRADUÉ
  Requête : TIMBRE_GRADUE[CODGENAU, PUIVEHMI ≤ cv ≤ PUIVEHMA, PRIMMINI ≤ Prime_Nette ≤ PRIMMAXI]
  Prendre la ligne DATEEFFE la plus récente ≤ date_émission.
  Si VALTIMGR > 0 : Timbre = VALTIMGR (forfait)
  Si TAUTIMGR > 0 : Timbre = Prime_Nette × (TAUTIMGR / 100)
  Vérifier d'abord TIMBRE_GRADUE_EXCEPTION pour les genres spéciaux.

ÉTAPE 11 — TAXES
  Source principale : TAXE[CODECATE, CODEGARA, CODTYPTA, DATEEFFE la plus récente ≤ date_émission]
  Source complémentaire : TAXE_ACCESSOIRE[CODECATE, CODTYPTA, DATEEFFE]

  Pour chaque ligne taxe applicable :
    Si BASETAXE = 'R' (ou champ vide = base prime nette) :
      Taxe_i = Prime_Nette × (TAUXPRIM_i / 100)
    TYPE_TAXE : CODTYPTA=1 → TVA (19%), CODTYPTA=2 → FGA (3%)

  TAXES_TOTALES = Σ Taxe_i

  Pratiquement pour catégorie 1110 Auto VP :
    TVA = Prime_Nette × 19%   [CODTYPTA=1, TAUXPRIM=19% depuis 2017]
    FGA = Prime_Nette × 3%    [CODTYPTA=2, TAUXPRIM=3%]
    TAXES_TOTALES ≈ Prime_Nette × 22%

ÉTAPE 12 — PRIME TTC
  Prime_TTC = Prime_Nette + TAXES_TOTALES + Timbre

ÉTAPE 13 — MENSUALITÉ (si paiement échelonné)
  Mensualité = Prime_TTC / durée_en_mois
```

---

================================================================================
# PARTIE H — RÈGLES MÉTIER
================================================================================

---

## [DEVIS::AUTO::REGLES_METIER]

**H.1 — Prime minimale absolue :**
La prime de chaque garantie ne peut jamais être inférieure à PRIMMINI (TARIF_AUTO).

**H.2 — Unicité de réduction :**
Une seule réduction commerciale s'applique par contrat (v2 : 2 types disponibles).
La réduction s'applique **uniquement sur la partie RNO**, jamais sur RC, DR, timbre, TVA.

**H.3 — Hiérarchie réductions (v2 — 2 niveaux) :**
```
1. Convention → code de réduction via CONVENTION.CODEREDU → REDUCTION_AUTOMOBILE
2. Commerciale → code REDUCTION_AUTOMOBILE direct
3. (Pas de réduction) → 0%
```

**H.4 — Durée et prorata :**
Le coef_durée s'applique à MONTFIXE avant application des réductions.

**H.5 — Zone géographique :**
Déterminée par la wilaya d'immatriculation. En cas de doute, Zone N.

**H.6 — Genre véhicule :**
Le CODGENAU doit être déterminé à partir de la table GENRE_AUTO officielle.
Ne jamais assimiler CODGENAU=03 à « VP Tourisme » : c'est Side-car/Tricycle.

**H.7 — Convention :**
La CONVENTION est un accord professionnel/collectif. Elle se traduit par un CODEREDU
qui pointe vers un code de réduction REDUCTION_AUTOMOBILE. Ce taux s'applique sur
Total_RNO_brut uniquement. Source : CONVENTION[CODECONV, DATEEFFE, DATERESI, CODEREDU].

Exemples de conventions actives (historiques, à vérifier date de résiliation) :
- Code 011 (Grp Avicol) → CODEREDU=RF → réduction 60%
- Code N1 (Personnel NAFTAL) → CODEREDU=R5 → réduction 50%
- Code CPA (CPA Flotte) → CODEREDU=R9 → réduction à vérifier

**H.8 — Surprimes non réductibles :**
Les surprimes jeune conducteur et permis récent ne sont pas soumises à réduction.

**H.9 — Indemnité Conducteur (exclusion des réductions) :**
L'Indemnité Conducteur n'entre pas dans Total_RNO_brut. Elle reste incluse dans
la base de calcul des surprimes :
```
Prime_intermédiaire = Total_RO + Total_RNO_net + Indemnité_Conducteur
```

**H.10 — Taxes : base de calcul correcte :**
Consulter TAXE et TAXE_ACCESSOIRE par CODECATE et DATEEFFE. La base est toujours
la prime nette HT. Ne jamais appliquer la même taxe deux fois.

**H.11 — Commission (ne pas inclure dans le devis client) :**
Source : COMMISSION[CODTYPIN, CODECATE, CODEGARA]. Ces taux sont exclusivement
comptables (TAUCOMAP = apport, TAUCOMGE = gestion) et n'entrent pas dans la prime
affichée au client.

---

================================================================================
# PARTIE I — EXEMPLES DE CALCUL COMPLETS (v2)
================================================================================

---

## [DEVIS::AUTO::EXEMPLES_CALCUL]

### Exemple 1 — VP Tourisme 6CV, Usage Personnel, Zone N, 12 mois, RC seule

```
Genre : VP standard → CODGENAU=00
Paramètres : cv=6, usage=01, zone=N, durée=A (12 mois)

ÉTAPE 2 — RC :
  Requête TARIF_AUTO[CODEGARA='RC', CODGENAU=00, CODUSAAU=01, CODEZONE=N,
                      PUISMINI≤6≤PUISMAXI, DATEEFFE=2025/07/01]
  RC_annuel = MONTFIXE (à récupérer en table)
  [Nota : les barèmes Genre 00 sont distincts de Genre 03]

ÉTAPE 10 — Timbre (CODGENAU=0, puissance 6CV → PUIVEHMI=0, PUIVEHMA=10) :
  Prime < 2 500 → Timbre = 300 DA
  Prime 2 500–10 000 → Timbre = 5% × Prime_Nette
  Prime 10 000–50 000 → Timbre = 3% × Prime_Nette
  Prime ≥ 50 000 → Timbre = 2% × Prime_Nette

ÉTAPE 11 — TVA = Prime_Nette × 19%

ÉTAPE 12 — Prime TTC = Prime_Nette + TVA + Timbre
```

---

### Exemple 2 — Side-car 6CV, Zone N, 12 mois, RC + TR

```
Genre : Side-car → CODGENAU=03
cv=6, usage=01, zone=N, durée=A

ÉTAPE 2 — RC :
  RC_annuel = TARIF_AUTO[CODEGARA='RC', CODGENAU=03, CODUSAAU=01, CODEZONE=N, 5≤cv≤6]
  → RC_annuel = 1 827,71 DA (barème 2025/07/01)

ÉTAPE 5 — TR (optionnelle) :
  TR = TARIF_AUTO[CODEGARA='TR', CODGENAU=03, ...].TAUXCAPI × valeur_venale × 1.0

ÉTAPE 10 — Timbre (CODGENAU=3, PUIVEHMI=0, PUIVEHMA=99, barème 2009/04/01) :
  Prime < 2 500 → 300 DA
  2 500–10 000 → 5%
  10 000–50 000 → 3%   ← CORRECTION v2 (était 5% en v1)
  ≥ 50 000 → 2%        ← CORRECTION v2

ÉTAPE 11 — TVA = Prime_Nette × 19%
ÉTAPE 12 — Prime TTC = Prime_Nette + TVA + Timbre
```

---

### Exemple 3 — VP 6CV, 6 mois, RC seule

```
RC annuel = MONTFIXE (table TARIF_AUTO CODGENAU=00)
RC 6 mois = RC_annuel × 55%
RC 6 mois = max(RC_6mois, PRIMMINI)

Timbre = barème CODGENAU=00, PUIVEHMI=0, PUIVEHMA=10
TVA = Prime_Nette × 19%
Prime TTC = Prime_Nette + TVA + Timbre
```

---

### Exemple 4 — ERREUR COURANTE : Garantie Forfaitaire vs Proportionnelle

❌ **CALCUL FAUX :**
```
DR (Défense et Recours) = 1 500 000 × 0.5% = 7 500 DA   ❌ FAUX
```

✅ **CALCUL CORRECT :**
```
DR est une garantie FORFAITAIRE.
DR = TARIF_AUTO[CODEGARA='DR', ...].MONTFIXE × coef_durée
```

---

### Exemple 5 — Convention (CORRECTION v2 : sans réduction paiement)

```
Client N1 (Personnel NAFTAL) — code convention : N1
Véhicule VP, RC + VOL + TR, zone N, 12 mois

ÉTAPE 6 — Sélection réduction :
  1. Convention N1 → CONVENTION[N1].CODEREDU = R5 → REDUCTION_AUTOMOBILE[R5] = 50%
  réduction_sélectionnée = 50%
  Total_RNO_net = Total_RNO_brut × (1 - 0.50) = Total_RNO_brut × 50%

⚠️ NOTE v2 : Il n'existe plus d'étape "Réduction Paiement" dans l'algorithme.
Si le client paie par virement ou chèque, aucune réduction supplémentaire n'est appliquée
(source manquante en table). La Convention reste la réduction maximale applicable.
```

---

================================================================================
# PARTIE J — RISQUES DIVERS (RD / IARDT) — RECONSTRUCTION COMPLÈTE
================================================================================

---

## J.1 — Produits RD identifiés dans les tables

> SOURCE: BRANCHE.csv, CATEGORIE.csv, TARIF.csv, TAXE.csv, TAXE_ACCESSOIRE.csv, COMMISSION.csv

### Produits calculables (table TARIF présente) :

| Code catégorie | Branche | Description | Tables présentes | Statut |
|---|---|---|---|---|
| **1221** | 12 — Incendie | Multirisque Habitation (MRH) | TARIF (67 règles), TAXE, COMMISSION | **Calculable** |
| **1222** | 12 — Incendie | Multirisque Immeuble (MRP) | TARIF (26 règles), TAXE, COMMISSION | **Calculable** |
| **1223** | 12 — Incendie | Multirisque Professionnelle | TARIF (330 règles), TAXE, COMMISSION | **Calculable** |
| **1212** | 12 — Incendie | Incendie Risques Annexes (RS) | TARIF (43 règles), TAXE, COMMISSION | **Calculable** |
| **1213** | 12 — Incendie | Incendie Risques Annexes (RI) | TARIF (90 règles), TAXE, COMMISSION | **Calculable** |
| **14111** | 14 — RC Générale | RC Générale/Professionnelle (RS) | TARIF (552 règles), TAXE, COMMISSION | **Calculable** |
| **1511** | 15 — Autres dommages | Dégâts des Eaux (RS) | TARIF (640 règles), TAXE, COMMISSION | **Calculable** |
| **1531** | 15 — Autres dommages | Vol sur la Personne (RS) | TARIF (3 règles), TAXE, COMMISSION | Partiellement calculable |
| **3122** | 31 — Transport terrestre | Facultés Terrestres Privées | TARIF (12 règles), TAXE, COMMISSION | **Calculable** |
| **3431** | 34 — Transport maritime | Facultés Maritimes | TARIF (85 règles), TAXE, COMMISSION | **Calculable** |

### Branches identifiées mais sans tables de tarif directes :

| Code | Description | Statut calcul |
|---|---|---|
| 1200/1201 | Catastrophes Naturelles (CAT-NAT) Immobilier | Tables TAXE présentes, tarif paramétrique |
| 14181–14189 | RC Propriétaires (immeubles, chiens, ruches…) | COMMISSION présente, TARIF à vérifier |
| 1553 | Tous Risques Engins de Chantier | COMMISSION présente, tarif à reconstruire |
| 1611 | Pertes d'Exploitation après Incendie | COMMISSION présente, tarif à reconstruire |

---

## J.2 — Tables tarifaires RD identifiées

| Table | Rôle | Champs de calcul clés |
|---|---|---|
| **TARIF** | Règles de calcul par garantie et catégorie | COEFMULT, RAPPDIVI, CODNATTA, NUMEORDR |
| **CONDITION_TARIF** | Conditions de sélection de règles | CODRUBCA, VALEMINI, VALEMAXI |
| **TAXE** | Taux de taxe par catégorie/garantie | TAUXPRIM, BASETAXE, CODTYPTA |
| **TAXE_ACCESSOIRE** | Taux complémentaires par catégorie | TAUXACCE |
| **COMMISSION** | Taux commission intermédiaire | TAUCOMAP, TAUCOMGE |

**Structure TARIF (moteur de calcul interne) :**
- CODNATTA = 'T' (Taux) ou 'L' (Limite) ou autre
- COEFMULT × variable_source / RAPPDIVI = résultat rubrique
- CODEGARA = code garantie (INC, DDE, VOL, RC, BDG, ATS, TTER, TGN…)
- CODRUBTA = code rubrique résultat (PB, PN, CA, etc.)
- Les règles sont ordonnées par NUMEORDR et enchaînées

---

## J.3 — Formule générale RD

La structure de calcul RD suit le même schéma qu'Auto :

```
Prime_TTC_RD = Prime_Nette_RD + TAXES_RD + TIMBRE_RD

Prime_Nette_RD = Σ(Prime_Garantie_g pour g ∈ garanties_souscrites)
               − Réductions

TAXES_RD = Prime_Nette_RD × Taux_TVA[CODECATE]
         où Taux_TVA = 19% depuis 2017/01/01 (CODTYPTA=1)

TIMBRE_RD = TIMBRE_DIMENSION[CODECATE] ou VALEUR_TIMBRE_DIMENSION[CODECATE]
         (timbres fixes par catégorie — non gradués comme en Auto)
```

**Source TIMBRE pour RD :**
- Table TIMBRE_DIMENSION contient les dimensions de timbre par produit
- Table VALEUR_TIMBRE_DIMENSION contient les montants correspondants
- Pour la plupart des produits RD : timbre forfaitaire fixe (non proportionnel)

---

## J.4 — Produit MRH (Catégorie 1221)

### J.4.1 — Identification des garanties disponibles

**Source : TARIF.csv filtré sur CODECATE=1221 — garanties présentes :**

| Code garantie | Description |
|---|---|
| INC | Incendie |
| DDE | Dégâts des Eaux |
| VOL | Vol |
| VOLB | Vol Bijoux |
| RC | Responsabilité Civile Locataire |
| BDG | Bris de Glaces |
| ATS | Assistance |
| TTER | Terrorisme |
| TGN | Tempête/Grêle/Neige |
| DEPD | Dépendances |
| EMTE | Émeutes |
| EVNA | Événements Naturels |
| INAG | Incendie Agricole |
| INFD | Infidélité Domestique |
| PRSC | Prévoyance Scolaire |

### J.4.2 — Structure de calcul MRH (moteur TARIF)

La table TARIF contient pour chaque garantie MRH des règles ordonnées de type :
- **PBI** (Prime Base Immeuble) = Capital_Bâtiment × Taux_INC / 1000
- **PB** (Prime Brute) = Base × Coefficient / Diviseur
- **PN** (Prime Nette) = PB − Franchise_Minimum
- **CA** (Capital Assuré) = valeur du bien

**Exemple de structure INC (Incendie) — règles clés détectées :**
```
Règle 1 : PBI2 = Capital_Immeuble × 0,40 / 1000
Règle 2 : PB = PBI × 0,16 / 100  (taux Incendie ~0.16‰)
Règle 3 : PN = PB (prime nette)
```

**Exemple de structure DDE (Dégâts des Eaux) :**
```
ATS.PB = Capital × 0.15 / 1000
DDE.PB = DDE_taux × capital_couvert
```

**Exemple de structure VOL :**
```
VOL.PB = Capital_Contenu × 0.9 / 10000   (taux ~0.09%)
```

### J.4.3 — Taxes MRH

**Source : TAXE et TAXE_ACCESSOIRE pour CODECATE=1221**

| Type | CODTYPTA | Taux | Base | Effectif |
|---|---|---|---|---|
| TVA | 1 | 17% → 19% | R (Prime nette) | 1988 → 2017/01/01 |
| FGA | 2 | — | — | Non renseigné pour 1221 |

```
TVA_MRH = Prime_Nette_MRH × 19%   [depuis 2017/01/01]
```

### J.4.4 — Commission MRH

**Source : COMMISSION[CODECATE=1221]**

| Type intermédiaire | TAUCOMAP (apport) | TAUCOMGE (gestion) |
|---|---|---|
| G (Agent général) | 20% | 10% |
| T (Courtier) | 20% | 10% |
| A (Apporteur) | 20% | 10% |

> Commission uniquement comptable — ne s'applique pas au calcul client.

---

## J.5 — Produit RC Générale/Professionnelle RS (Catégorie 14111)

### J.5.1 — Garanties disponibles

| Code | Description |
|---|---|
| RMG1 | Responsabilité Civile Matérielle Générale 1 |
| RCP | RC Corporelle |
| RCE | RC Étendue |
| RCOC | RC Objets Confiés |
| RCSC | RC Sous-Contractants |
| RMEX | RC Matérielle Étendue |
| RMG2 | RC Matérielle Générale 2 |
| RCVL | RC Vie et Liberté |
| MINA | Minimum d'Assurance |
| RCPA | RC Patronale |

### J.5.2 — Structure de calcul RC Générale

```
Prime_RCG = f(Chiffre_d_Affaire, Plafond_Garantie, Taux_Activité)

Principales rubriques TARIF pour 14111 :
- LIGA = Limite de Garantie (capital assuré)
- PB   = Prime Brute = LIGA × Taux / 1000
- PN   = Prime Nette = PB × Coef_Application
- MINA = Prime minimum = 25% × PB
```

### J.5.3 — Taxes RC Générale

| Type | Taux effectif |
|---|---|
| TVA (CODTYPTA=1) | 19% depuis 2017/01/01 |

```
TVA_RCG = Prime_Nette_RCG × 19%
```

### J.5.4 — Commission RC Générale

| Type | TAUCOMAP | TAUCOMGE |
|---|---|---|
| G / T | 10% | 4% |

---

## J.6 — Produit Dégâts des Eaux RS (Catégorie 1511)

### J.6.1 — Garanties disponibles

| Code | Description |
|---|---|
| DDEC | Dégâts des Eaux Contenu |
| IDTT | Indemnités Diverses Tiers Tiers |

### J.6.2 — Structure de calcul

```
Variables d'entrée :
- VA  = Valeur Assurée (capital)
- TRP = Taux de Prime (% ou ‰)
- TRT = Taux base 10 000

Prime_DDEC = VA × TRP (ou TRT / 10000)
```

### J.6.3 — Taxes DDE

| Taux effectif |
|---|
| TVA 19% sur prime nette |

---

## J.7 — Taxes RD — Récapitulatif par produit

**Source : TAXE_ACCESSOIRE (par CODECATE, CODTYPTA=1)**

| Catégorie | Produit | Taux TVA actuel (depuis 2017/01/01) |
|---|---|---|
| 1221 | MRH | **19%** |
| 1222 | MRP | **19%** |
| 1223 | Multirisque Pro | **19%** |
| 1212 | Incendie RS | **19%** |
| 1213 | Incendie RI | **19%** |
| 14111 | RC Générale RS | **19%** |
| 1411 | RC Générale (base) | **19%** |
| 1511 | DDE RS | **19%** |
| 1521 | Bris de Glaces RS | **19%** |
| 1531 | Vol sur la Personne | **19%** |
| 3122 | Facultés Terrestres | **19%** |
| 3431 | Facultés Maritimes | **19%** |

> Référence : TAXE_ACCESSOIRE[CODTYPTA=1, CODECATE, DATEEFFE=2017/01/01, TAUXACCE=19]

---

## J.8 — Commissions RD — Récapitulatif

**Source : COMMISSION[CODECATE, CODTYPIN IN (G,T)]**

| Catégorie | Produit | TAUCOMAP (apport) | TAUCOMGE (gestion) |
|---|---|---|---|
| 1221 | MRH | 20% | 10% |
| 1222 | MRP | 20% | 10% |
| 1223 | Multirisque Pro | 20% | 10% |
| 1212/1213 | Incendie RS/RI | 8% | 4% |
| 14111 | RC Générale RS | 10% | 4% |
| 1411 | RC Générale | 10% | 4% |
| 1511 | DDE RS | — | — |
| 1531 | Vol Personne | 10% | 4% |
| 3122 | Facultés Terrestres | 9% | 4% |
| 3431 | Facultés Maritimes | 5% | 4% |

> Commission uniquement comptable — ne s'applique pas au calcul client.

---

## J.9 — Algorithme de calcul RD générique

```
Pour tout produit RD (CODECATE ∈ branches 12, 13, 14, 15, 16, 31, 34) :

ÉTAPE 1 — IDENTIFIER CODECATE et garanties souscrites

ÉTAPE 2 — CALCUL DES PRIMES GARANTIES
  Pour chaque garantie g :
    Récupérer règles de TARIF[CODTYPTA, CODECATE, CODEGARA=g, DATEEFFE la plus récente]
    Appliquer les règles ordonnées (NUMEORDR) pour calculer PB, PN, CA
    La formule dépend du type CODNATTA :
      'T' (Taux) : Rubrique = Base × COEFMULT / RAPPDIVI
      'L' (Limite) : Rubrique = Limite plafonnée
    Conditions de sélection : CONDITION_TARIF[même clé]

  Total_Primes_Brutes = Σ(PB_g)
  Total_Primes_Nettes = Σ(PN_g)

ÉTAPE 3 — RÉDUCTIONS RD
  Appliquer REDUCTION_AUTOMOBILE si code réduction fourni
  (mêmes codes que branche Auto — applicable sur partie optionnelle)

ÉTAPE 4 — PRIME NETTE RD
  Prime_Nette_RD = Total_Primes_Nettes − Réductions

ÉTAPE 5 — TAXES RD
  TVA_RD = Prime_Nette_RD × 19%   [CODTYPTA=1, depuis 2017]
  TAXES_RD = TVA_RD

ÉTAPE 6 — TIMBRE RD
  Consulter TIMBRE_DIMENSION et VALEUR_TIMBRE_DIMENSION pour CODECATE
  Timbre = valeur forfaitaire ou proportionnelle selon table

ÉTAPE 7 — PRIME TTC RD
  Prime_TTC_RD = Prime_Nette_RD + TAXES_RD + Timbre
```

---

## J.10 — Règles métier RD

**J.10.1 — Durée :** Coefficients identiques à l'Auto (A=100%, S=55%, T=35%, M=25%)

**J.10.2 — Prime minimale :** Respecter PRIMMINI de chaque garantie si présent en TARIF

**J.10.3 — CAT-NAT :** Branche indépendante (catégories 1200/1201). Ne jamais inclure
dans le calcul Auto ou dans un autre produit RD. Taxes spécifiques (TAXE_ACCESSOIRE[1200,1201] = 0% depuis 2017/04/01).

**J.10.4 — Garanties interdites :** Vérifier GARANTIE_INTERDITE pour les combinaisons non autorisées

---

## J.11 — Conclusion d'audit — Cas B (Partie J partiellement reconstructible)

**Ce qui est calculable à partir des tables disponibles :**
- Taxes : 100% calculables (TAXE + TAXE_ACCESSOIRE)
- Commissions : 100% identifiables (COMMISSION) — comptable seulement
- Structure de formule : présente dans TARIF (règles ordonnées)
- Produits MRH (1221), RC Générale (14111), DDE (1511), Facultés (3122, 3431) : formules partiellement décodables

**Ce qui manque pour une reconstruction complète :**
- Les rubriques métier ($TATS, $TASI, $VALC, $GEM, $QUAS…) sont des variables dynamiques
  dont les valeurs sont saisies à l'émission — elles ne sont pas dans les tables statiques
- Les CONDITION_TARIF requièrent une connaissance des variables contextuelles (ancienneté, localisation, activité…)
- Pour MRH/MRP : les taux ‰ exacts par type de construction et zone ne sont pas dans une table de barème simple mais encodés dans les règles TARIF COEFMULT/RAPPDIVI

**Recommandation :**
Pour déployer un vrai moteur de devis RD exploitable par Sana, il faut soit :
1. Reconstruire les rubriques métier à partir de cas réels (CALCUL_RUBRIQUE)
2. Implémenter un sous-moteur capable d'exécuter la table TARIF avec ses règles ordonnées
3. Commencer par les produits à barème simple (RC Générale — taux sur capital/CA)

---

================================================================================
# PARTIE K — TABLEAU DE BORD SANA (ASSISTANT)
================================================================================

---

## [SANA::REGLES_CALCUL_DEVIS]

> TYPE: regles_assistant_ia
> APPLICABLE: AssurDevis.AI — Sana

### K.1 — Collecte d'information obligatoire avant tout calcul Auto :

```
INFORMATIONS REQUISES :
1. Type de véhicule → détermine CODGENAU (VP=00, Side-car=03, TPV=34, etc.)
2. Usage du véhicule → détermine CODUSAAU (01=personnel, 02=commerce, 03=taxi...)
3. Puissance fiscale (CV) → détermine la tranche dans TARIF_AUTO
4. Zone géographique (wilaya) → détermine CODEZONE (N ou S)
5. Durée souhaitée → détermine coef_durée
6. Garanties souhaitées → liste des CODEGARA à inclure
7. Valeur vénale → nécessaire pour garanties en % (VIV, TR, TOPR...)
8. Âge conducteur et ancienneté permis → pour surprimes éventuelles
9. Convention éventuelle → code CONVENTION si applicable
```

### K.2 — Collecte d'information pour devis RD :

```
INFORMATIONS REQUISES (MRH) :
1. Type de bien (habitation principale / résidence secondaire / maison individuelle)
2. Surface habitable (m²)
3. Type de construction (dur / semi-dur / autre)
4. Valeur du bâtiment estimée (DA)
5. Valeur du contenu (mobilier, électroménager, bijoux)
6. Garanties choisies (Incendie, Vol, RC locataire, DDE, BDG, TGN, Terrorisme)
7. Durée souhaitée

INFORMATIONS REQUISES (RC Générale) :
1. Activité professionnelle (code ACTIVITE ou libellé)
2. Chiffre d'affaires annuel (DA)
3. Plafond de garantie souhaité
4. Garanties choisies
```

### K.3 — Règles de présentation du devis :

```
PRÉSENTER :
- Prime RC (obligatoire, non négociable)
- Chaque garantie optionnelle avec son montant
- Réduction appliquée (code et montant économisé)
- Sous-total Prime Nette HT
- TVA (19%)
- Timbre gradué (montant calculé selon barème)
- Prime TTC annuelle
- Prime TTC pour la durée choisie

NE PAS PRÉSENTER :
- Les codes internes (CODEGARA, CODGENAU, etc.)
- Les détails comptables (commission, réassurance)
- Les noms de compagnies ou systèmes propriétaires
```

### K.4 — Messages d'erreur :

| Condition | Message |
|---|---|
| CV non fourni | "Quelle est la puissance fiscale de votre véhicule (en CV) ?" |
| Type véhicule ambigu | "S'agit-il d'un VP standard, d'un side-car, d'un camion ou d'un autre type ?" |
| Valeur vénale = 0 pour VIV/TR | "La valeur vénale est nécessaire pour calculer la garantie Vol/Incendie/Tous Risques." |
| Garanties incompatibles | "Ces deux garanties ne peuvent pas être souscrites ensemble." |
| Usage Taxi sans zone | "Pour un taxi, la zone géographique (nord/sud) est indispensable." |
| Produit RD sans données suffisantes | "Ce produit nécessite des informations complémentaires (valeur assurée, activité…)." |

### K.5 — Règle CODGENAU pour Sana (CORRECTION v2) :

```
SI véhicule = "voiture / berline / SUV / citadine / utilitaire léger" :
  CODGENAU = 00 (VP sans remorque)

SI véhicule = "side-car / tricycle / triporteur" :
  CODGENAU = 03

SI véhicule = "moto / scooter ≤ 125cm³" :
  CODGENAU = 02

SI véhicule = "bus / minibus / taxi-collectif" :
  CODGENAU = 34 (TPV)

SI véhicule = "camion / poids lourd > 3.5T" :
  CODGENAU = 30

⚠️ NE JAMAIS utiliser CODGENAU=03 pour un VP Tourisme standard.
```

---

================================================================================
# ANNEXES
================================================================================

---

## [ANNEXE::CODES_USAGE]

| Code CODUSAAU | Libellé |
|---|---|
| 00 | Affaire (usage professionnel général) |
| 01 | Fonctionnaire / Personnel |
| 02 | Commerce |
| 03 | Taxi |
| 04 | Commerce C.Bis |
| 05 | Transport Public Marchandises (TPM) |
| 06 | Transport Public Voyageurs (TPV) |
| 07 | Véhicules Spéciaux |
| 08 | Besoins propres du propriétaire |
| 09 | Travaux chez les Tiers |
| 10 | Auto-École |
| 11 | Location |

---

## [ANNEXE::CODES_GENRE_OFFICIEL]

**Source : GENRE_AUTO.csv (table officielle)**

| Code CODGENAU | Libellé officiel | Usage Sana |
|---|---|---|
| 00 | VP sans remorque | ✅ VP Tourisme standard |
| 01 | Remorques VP | — |
| 02 | Motocyclettes sans side-car ≤ 125 cm³ | Moto |
| 03 | Side-car, tricycles, triporteurs | ≠ VP Tourisme |
| 04 | TPM CU ≤ 2T | Fourgon léger |
| 05 | Cyclomoteurs ≤ 50 cm³ | — |
| 06 | Scooter ≤ 125 cm³ | Scooter |
| 07 | Scooter ≤ 175 cm³ | Scooter |
| 08 | Triporteurs/tricycles ≤ 125 cm³ | — |
| 09 | Vélomoteurs ≤ 125 cm³ | — |
| 10 | Voiture ambulance | — |
| 19 | VP avec remorque | — |
| 30 | Poids lourd > 3,5T | PL |
| 32 | TPM CU > 2T | — |
| 34 | TPV | Bus/Taxi collectif |
| 35 | Tracteur + semi-remorque | — |
| 36 | Tracteur routier seul | — |
| 45 | Engins chantier voie publique | — |
| 46 | Engins chantier hors voie publique | — |
| 47 | Garagistes (plaques Auto) | — |
| 49 | Dépannage | — |
| 50 | Tracteur pneumatique + remorque | — |
| 54 | Tracteur pneumatique sans remorque | — |

---

## [ANNEXE::BRANCHES_IARDT]

**Source : BRANCHE.csv**

| CODEBRAN | Libellé | Famille |
|---|---|---|
| 11 | Automobile | Auto |
| 12 | Incendie & éléments naturels | RD |
| 13 | Risques Construction | RD |
| 14 | Responsabilité Civile Générale | RD |
| 15 | Autres dommages aux biens | RD |
| 16 | Pertes Pécuniaires Diverses | RD |
| 18 | Assistance | RD |
| 21 | Assurance des récoltes | Agricole |
| 22 | Assurance Mortalité Animaux | Agricole |
| 31 | Transport voie terrestre | Transport |
| 32 | Transport ferroviaire | Transport |
| 33 | Transport voie aérienne | Transport |
| 34 | Transport voie maritime | Transport |
| 51 | Assurance Crédit | Financier |
| 52 | Caution | Financier |

---

## [ANNEXE::DATES_BAREME]

| Date | Événement |
|---|---|
| 1988/01/01 | Barème originel |
| 2006/01/01 | Révision timbres gradués |
| 2009/04/01 | Nouveau barème timbre (NUME_LOT=5) |
| 2017/01/01 | Passage TVA 17% → 19% |
| 2025/01/01 | Barème RC 2025 H1 |
| 2025/07/01 | **Barème RC 2025 H2 (barème actuel)** |

**Règle d'application :**
Utiliser toujours la date d'effet la plus récente **inférieure ou égale** à la date d'émission.

---

## [ANNEXE::TYPE_TAXE]

**Source : TYPE_TAXE.csv**

| CODTYPTA | Libellé | Taux standard |
|---|---|---|
| 1 | TVA | 19% (depuis 2017) |
| 2 | FGA | 3% |
| 3 | TVR | 0% (exonération) |

---

===============================================================================
# PARTIE L — FORMULES D'ESTIMATION RAPIDE (ORDRE DE GRANDEUR)
===============================================================================

---

## [DEVIS::ESTIMATION::RC_PRO]

> TYPE: estimation_formules
> APPLICABLE: devis_RC_Professionnelle

### L.1 — RC Professionnelle — Estimation rapide

| Type garantie | Formule d'estimation |
|---|---|
| RC Exploitation | CA_annuel × 0.3% à 0.8% |
| Incendie contenu | Valeur_contenu × 0.15% à 0.3% |
| Multirisque complète | (CA × 0.012) + (contenu × 0.0025) |

**TVA :** 19% — **FGA :** 3% (sur prime nette)

---

### L.2 — MRH — Estimation rapide

| Type garantie | Formule d'estimation |
|---|---|
| Incendie | valeur_bâtiment × 1.5‰ |
| MRH complète (Incendie + Vol + DDE + RC) | (valeur_bâtiment + mobilier) × 2.5‰ |

**TVA :** 19% — **FGA :** 3% (sur prime nette)
