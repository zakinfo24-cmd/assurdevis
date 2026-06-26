---
fichier: 04_processus_commercial.md
domaine: Assurances Algériennes — Processus & Guide
version: 2026
---

# 04 — Processus, Souscription et Guide Commercial

---

# PARTIE A — Processus d'Acheminement du Contrat

# Processus d'Acheminement d'un Contrat d'Assurance — v5

> Système de gestion Assur — Base Oracle reconstituée à partir du schéma `base_v5.dmp`

---

## 1. Identification des Acteurs
> CHUNK_ID: PROCESSUS::ACTEURS

| Acteur | Table(s) associée(s) | Rôle |
|---|---|---|
| Intermédiaire (agent/courtier) | `INTERMEDIAIRE`, `USER_INTERMEDIAIRE` | Apporteur d'affaires, point d'entrée du contrat |
| Apporteur | `APPORTEUR` | Entité apportant la souscription |
| Assuré | `ASSURE`, `ASSURE_BIS` | Titulaire du contrat |
| Société d'assurance | `SOCIETE`, `INTERMEDIAIRE` | Souscripteur principal |
| Coassureur | `COASSURANCE` | Partage de risque sur la police |
| Réassureur | `BRANCHE_REASS`, `CONDITION_SOUS_REASS` | Couverture en réassurance |

---

## 2. Phase 1 — Saisie et Initialisation du Contrat
> CHUNK_ID: PROCESSUS::SAISIE_INIT

### 2.1 Identification de l'assuré
- Création ou recherche de l'assuré dans la table `ASSURE` (code, raison sociale, adresse, pièce d'identité, coordonnées bancaires).
- Complétion du profil étendu dans `ASSURE_BIS` (KYC : situation familiale, professionnelle, revenus, bénéficiaires effectifs).
- Vérification dans `ASSURE_INTERDIT` (liste noire).

### 2.2 Paramétrage de la branche et de la catégorie
- Sélection de la **branche** (`BRANCHE`) : ex. Automobile, Vie, IARD.
- Sélection de la **catégorie** (`CATEGORIE`) avec ses plages de risques (`MINIRISQ` / `MAXIRISQ`), son registre de production (`CODREGPR`) et son registre sinistre (`CODREGSI`).
- Application des **caractéristiques de catégorie** (`CARACTERISTIQUE_CATEGORIE`, `CATEGORIE_CARACT_RUBRIQUE`).

### 2.3 Création de la police
- Génération du numéro de police via le registre `REGISTRE_PRODUCTION` (préfixe + plage numérique).
- Insertion dans la table `POLICE` avec :
  - Code intermédiaire (`CODEINTE`)
  - Code assuré (`CODEASSU`)
  - Catégorie (`CODECATE`)
  - Dates d'effet et d'échéance (`DATEEFFE`, `DATEECHE`)
  - Type de contrat (`TYPECONT`), régime bonus-malus (`CODREGBM`)
  - Date de souscription (`DATESOUS`) et de saisie (`DATESAIS`)
  - Utilisateur créateur (`NOMUTICR`)
- Verrouillage de la police en cours de saisie via `VERROUILLAGE_POLICE` (`TYPEVERR`, `UTILVERR`).

---

## 3. Phase 2 — Constitution des Risques et Garanties

### 3.1 Déclaration des risques
- Création des risques attachés à la police dans la table `RISQUE`.
- Renseignement des caractéristiques du risque dans `RISQUE_CARACT` et `RISQUE_FAMILLE`.
- Pour l'automobile : `DETAIL_RISQUE_AUTO`, `CARACTERISTIQUE_AUTO`, `NATURE_VEHICULE`, `USAGE_AUTO`, `GENRE_AUTO`, `REFERENCE_VEHICULE`.

### 3.2 Attribution des garanties
- Sélection des garanties dans le catalogue `GARANTIE` par catégorie.
- Enregistrement des garanties accordées dans `GARANTIE_ACCORDEE` (montants, dates d'effet/échéance).
- Vérification des `GARANTIE_INTERDITE` et `GARANTIE_DEPENDANTE`.
- Constitution des groupes de garanties via `GROUPE`, `GROUPE_GARANTIE`, `GROUPE_CARACT`.
- Application des plafonds dans `MODELE_PLAFOND`, `DETAIL_MODELE_PLAFOND`, `GROUPE_PLAFOND`.

### 3.3 Calcul des capitaux et primes
- Calcul des capitaux garantis (`CAPITAL_GARANTIE`).
- Application du tarif selon `TARIF`, `TARIF_AUTO`, `TYPE_TARIF`, `CONDITION_TARIF`.
- Calcul des rubriques de prime (`RUBRIQUE`, `RUBRIQUE_GARANTIE`, `CALCUL_RUBRIQUE`).
- Application des réductions (`REDUCTION_AUTOMOBILE`, `DETAIL_REDUCTION_AUTOMOBILE`, `REDUCTION_PAR_DEFAUT`).
- Application des majorations (`MAJORATION`, `MAJORATION_DUREE`).
- Application du bonus-malus (`BONUS_MALUS`, `BONUS_MALUS_GARANTIE`, `REGIME_BONUS_MALUS`).
- Application des taxes et accessoires (`TAXE`, `TAXE_ACCESSOIRE`, `TAXE_COMMISSION`, `EXONERATION_TAXE`).
- Application des commissions intermédiaire et gestion (`COMMISSION`, `COMMISSION_ACCESSOIRE`).

---

## 4. Phase 3 — Avenant de Souscription (Avenant 0)

- Création de l'**avenant initial** (numéro 0) dans la table `AVENANT` :
  - Type d'avenant (`CODTYPAV`) référencé dans `TYPE_AVENANT`
  - Date d'avenant (`DATEAVEN`), date d'effet (`DATEFFAV`), date d'échéance (`DATECHAV`)
  - Date de souscription (`DATESOUS`), date de saisie (`DATESAIS`)
  - Titre et commentaires (`TITRAVEN`, `COMMAVEN`)
- L'avenant génère une **quittance de souscription** dans la table `QUITTANCE` :
  - Type de quittance (`CODTYPQU`)
  - Prime nette (`PRIMNETT`), taxes, accessoires, commissions, timbres
  - Numéro de pièce comptable (`NUMEPIEC`)
- Génération du numéro de quittance via `NUMERO_QUITTANCE`.
- Impression de l'**attestation de risque** (`ATTESTATION_RISQUE`) si applicable (automobile).

---

## 5. Phase 4 — Validation et Émission

### 5.1 Contrôle et validation
- Vérification de l'habilitation utilisateur (`HABILITATION`, `ROLES_UTILISATEUR`, `Assur_ROLES`).
- Vérification du verrouillage (`VERROUILLAGE_POLICE`).
- Contrôle des caractéristiques obligatoires (`POLICE_CARACT`, `CARACTERISTIQUE`).
- Date de validation renseignée (`DATEVALI`) sur la police et l'avenant.

### 5.2 Enregistrement au registre
- Numéro attribué au registre de production (`NUMERO_REGISTRE_PRODUCTION`) selon la catégorie.
- Mise à jour du flag de sortie de la quittance (`SORTQUIT`, `DATSORQU`).

### 5.3 Émission des documents
- Génération du **contrat** via le modèle `MODELE_CONTRAT`.
- Émission de la **quittance** et de l'**avis d'échéance** (`AVIS_ECHEANCE`).
- Impression de l'attestation risque si la catégorie l'exige (`FLAG__PV` dans `CATEGORIE`).

---

## 6. Phase 5 — Encaissement de la Prime

- Saisie de l'encaissement dans `ENCAISSEMENT_QUITTANCE` :
  - Mode de paiement (`MODEPAIE`) : chèque, virement, espèces
  - Montant encaissé (`MONTENCA`), date d'encaissement (`DATEENCA`)
  - Référence de l'encaissement (`REFEENCA`)
  - Lien vers le bordereau d'opérations bancaires (`BORDEREAU_OPER_BANCAIRE`)
- Rapprochement bancaire via `RAPPROCHEMENT_BANCAIRE`, `DETAIL_RAPPROCHEMENT_BANCAIRE`.
- Génération des **mouvements comptables** dans `MOUVEMENT_COMPTABLE`, `JOURNAL_COMPTABLE`, `JOURNAL_TERME` selon les schémas `SCHEMA_COMPTABLE_PRODUCTION`.
- Intégration comptable via `ENVOI_COMPTABILITE`, `DETAIL_ENVOI_COMPTABILITE`.

---

## 7. Phase 6 — Gestion de la Vie du Contrat (Avenants)
> CHUNK_ID: PROCESSUS::ARCHIVAGE

Tout événement modificatif génère un nouvel avenant dans `AVENANT` :

| Type d'opération | Nature avenant (`NATUAVEN`) | Exemples |
|---|---|---|
| Modification | M | Changement de garanties, de véhicule, d'assuré |
| Renouvellement | R | Reconduction annuelle (`TYPE_AVENANT` avec `COTYAVRE` dans `CATEGORIE`) |
| Résiliation | S | Fin de contrat (`AGENCEMENT_SORT`, `TYPE_SORT`) |
| Adjonction | A | Ajout d'un risque, d'une garantie |
| Suspension | — | Suspension temporaire de garanties |

- Chaque avenant génère une nouvelle quittance (régularisation, ristourne, ou complément de prime).
- Historique des quittances conservé dans `HISTO_QUITTANCE` et `HISTO_ENCAISSE_QUITTANCE`.
- Images des états intermédiaires stockées dans `IMAGE_POLICE`, `IMAGE_RISQUE`, `IMAGE_GROUPE`, `IMAGE_GARANTIE_ACCORDEE`.

---

## 8. Phase 7 — Gestion des Sinistres

### 8.1 Déclaration du sinistre
- Création dans la table `SINISTRE` :
  - Exercice sinistre (`EXERSINI`), numéro sinistre (`NUMESINI`)
  - Date de survenance (`DATESURV`), date de déclaration (`DATEDECL`)
  - Nature sinistre (`NATUSINI`), cause (`CODCAUSI`), taux de responsabilité (`TAUXRESP`)
  - Police et risque concernés (`NUMEPOLI`, `CODERISQ`)
- Numéro attribué au registre sinistre (`REGISTRE_SINISTRE`, `NUMERO_REGISTRE_SINISTRE`).
- Enregistrement des éléments complémentaires : `SINISTRE_CAUSE`, `SINISTRE_RISQUE`, `SINISTRE_PV`.

### 8.2 Instruction et évaluation
- Enregistrement des ayants droit (`AYANT_DROIT_SINISTRE`) et bénéficiaires (`BENEFICIAIRE_SINISTRE`, `BENEFICIAIRE_TIERS`).
- Évaluation du sinistre dans `EVALUATION_SINISTRE`, `EVALUATION_GENERALE`.
- Constitution des provisions dans `PROVISION_SINISTRE`.
- Calcul des prestations via `PRESTATION`, `PRESTATION_RUBRIQUE`, `CALCUL_RUBRIQUE_SINISTRE_AUTO`.
- Gestion des garanties accordées sur sinistre (`DETAIL_GARANTIE_ACCORDEE`, `GARANTIE_ACCORDEE`).
- Suivi des événements (`EVENEMENT_SINISTRE`, `EVENEMENT_GARANTI_SINISTRE`).

### 8.3 Règlement du sinistre
- Création du règlement dans `REGLEMENT` :
  - Type de règlement (`CODTYPRE`), mode de paiement (`MODEPAIE`)
  - Montant réglé (`MONTREGL`), bénéficiaire (`NOM_BENE`)
  - Numéro de chèque ou virement, banque
  - Visa de règlement (`NUMEVISA`)
- Vérification du `POUVOIR_REGLEMENT` de l'utilisateur.
- Détail des rubriques de règlement dans `RUBRIQUE_REGLEMENT`, `DETAIL_SINISTRE_REGLE`.
- Clôture du sinistre via `SORT_SINISTRE` (type de sortie : `CODTYPSO`, date : `DATSORSI`).
- Génération des mouvements comptables selon `SCHEMA_COMPTABLE_REGLEMENT`, `SCHEMA_COMPTABLE_SINISTRE`.
- Liaison possible avec une instance judiciaire (`INSTANCE_JUDICIAIRE`, `CONVENTION_SINISTRE`).

---

## 9. Phase 8 — Clôture et Arrêtés Comptables

- Arrêté périodique par agence dans `ARRETE_AGENCE` et `ARRETE_COMPTABLE`.
- Clôture de l'exercice dans `ARRETE_COMPTABLE` (`CLOTEXER`).
- Génération de la **balance comptable** (`BALANCE_COMPTABLE`, `BALANCE_COMPTABLE_PLUS`).
- Édition des tableaux comptables (`TABLEAU_COMPTABLE`, `CELLULE_TABLEAU_COMPTABLE`, `DATA_TABLEAU_COMPTABLE`).
- Production des créances assurés (`CREANCE_ASSURE`, `GENERATION_CREANCE`, `DETAIL_GENERATION_CREANCE`).
- Soldage comptable via `SOLDAGE_COMPTABLE`.

---

## 10. Schéma de Flux Global

```
Prospect / Assuré
       │
       ▼
[1] SAISIE ASSURE ──────────────────── ASSURE / ASSURE_BIS / KYC
       │
       ▼
[2] CRÉATION POLICE ─────────────────── POLICE + REGISTRE_PRODUCTION
       │
       ▼
[3] RISQUES & GARANTIES ─────────────── RISQUE / GARANTIE_ACCORDEE / GROUPE
       │
       ▼
[4] CALCUL DE PRIME ─────────────────── TARIF / RUBRIQUE / TAXE / COMMISSION
       │
       ▼
[5] AVENANT 0 — SOUSCRIPTION ────────── AVENANT / QUITTANCE
       │
       ▼
[6] VALIDATION & ÉMISSION ───────────── HABILITATION / ATTESTATION_RISQUE
       │
       ▼
[7] ENCAISSEMENT ────────────────────── ENCAISSEMENT_QUITTANCE / BORDEREAU
       │
       ▼
[8] COMPTABILISATION ────────────────── MOUVEMENT_COMPTABLE / JOURNAL
       │
    ┌──┴──────────────────────────┐
    │                             │
    ▼                             ▼
[9] VIE DU CONTRAT           [10] SINISTRE
  Avenants successifs           Déclaration → Instruction
  AVENANT / QUITTANCE           SINISTRE → EVALUATION
  Renouvellement / Résiliation  → REGLEMENT → SORT_SINISTRE
    │                             │
    └──────────┬──────────────────┘
               ▼
          [11] ARRÊTÉS & CLÔTURE
          ARRETE_COMPTABLE / BALANCE_COMPTABLE
```

---

## 11. Tables Clés — Référentiel Rapide

| Domaine | Tables principales |
|---|---|
| **Contrat** | `POLICE`, `AVENANT`, `TYPE_AVENANT`, `MODELE_CONTRAT` |
| **Risque** | `RISQUE`, `RISQUE_CARACT`, `DETAIL_RISQUE_AUTO` |
| **Garantie** | `GARANTIE`, `GARANTIE_ACCORDEE`, `GROUPE`, `GROUPE_GARANTIE` |
| **Tarification** | `TARIF`, `RUBRIQUE`, `TAXE`, `COMMISSION`, `BONUS_MALUS` |
| **Production** | `QUITTANCE`, `ENCAISSEMENT_QUITTANCE`, `REGISTRE_PRODUCTION` |
| **Sinistre** | `SINISTRE`, `EVALUATION_SINISTRE`, `REGLEMENT`, `SORT_SINISTRE` |
| **Comptabilité** | `MOUVEMENT_COMPTABLE`, `JOURNAL_COMPTABLE`, `BALANCE_COMPTABLE` |
| **Acteurs** | `ASSURE`, `INTERMEDIAIRE`, `APPORTEUR`, `COASSURANCE` |
| **Paramétrage** | `BRANCHE`, `CATEGORIE`, `CARACTERISTIQUE`, `HABILITATION` |

---

*Document généré à partir de l'analyse du schéma Oracle v5 (`base_v5.dmp`) — Mai 2026*


---

# PARTIE B — Guide de Vente et Objections Commerciales

## Réponses aux objections fréquentes

### "C'est trop cher"
Proposer une garantie inférieure :
- Tous Risques → RC+Vol : économie de 30 à 40% / an
- RC+Vol → RC seule : économie supplémentaire, couverture minimale légale
Rappeler que la prime se paie mensuellement : ramener au montant mensuel.

### "J'ai vu moins cher ailleurs (CAAT, SAA, Trésor, MAATEC...)"
Ne pas dénigrer la concurrence. Valoriser :
- Les plafonds d'indemnisation
- Les délais de remboursement
- La qualité du réseau d'agences
- La réactivité en cas de sinistre

### "J'ai eu un accident l'année dernière"
Rassurer : c'est le rôle de l'assurance.
Le CRM (coefficient malus) est pris en compte dans le calcul.
Un sinistre responsable = +25% de prime environ.
Après 2 ans sans sinistre, retour au taux de base.

### "Je veux juste un prix rapide"
Aller directement aux 3 questions clés : wilaya, puissance CV, valeur vénale.
Donner une fourchette RC / TR immédiatement.

## Remises disponibles (une seule au choix)
- Pack multi-produit (auto + habitation + autre) : réduction combinée
- Formule Tous Risques complète : tarif préférentiel sur certaines garanties
- Paiement annuel (chèque / TPE / virement) : évite les frais de fractionnement

## Clôture commerciale
Quand le client dit "je veux souscrire" :
→ Féliciter chaleureusement
→ Inviter en agence pour le contrat définitif
→ Rappeler les documents nécessaires : carte grise, permis, CIN, photos véhicule
→ Préciser que le devis est une estimation — la prime définitive est établie en agence

## Véhicules non-assurables par AssurDevis
Avion, hélicoptère, bateau, train, vélo, trottinette, animaux.
Réponse : "Notre spécialité c'est l'assurance automobile. Pour [véhicule], 
il faudra voir une compagnie spécialisée."
