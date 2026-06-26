---
fichier: 02_garanties_produits.md
domaine: Assurances Algériennes — Garanties & Produits
version: 2026
---

# 02 — Garanties, Produits et Risques Divers

---

# PARTIE A — Référentiel des Garanties Auto

---
fichier: referentiel_garanties.md
domaine: Assurances Algériennes
lois: [Ordonnance 95-07, Loi 03-12, Code Civil Art. 175, Loi 88-31]
version: 1.1
statut: PRODUCTION
enrichi_depuis: Chatbot HTML v2 + DMP ORASS + Compagnie (Mai 2026)
---

================================================================================
# RÉFÉRENTIEL DES GARANTIES — STANDARD ALGÉRIEN
# Catalogue complet des produits d'assurance commercialisables en Algérie
================================================================================

---

# [PRODUITS::CATALOGUE::INDEX]

> TYPE: index_general
> CHUNK_ID: GARAN-CAT-INDEX

| Branche | Section |
|---|---|
| I. Assurances Automobiles | 23 garanties + 7 Packs Compagnie |
| II. Assurances Habitation (MRH) | 12 garanties |
| III. Assurances de Personnes | 10 garanties |
| IV. Assurance Vie & Emprunteur | 5 garanties |
| V. Assurances Professionnelles & Techniques | 7 garanties |
| VI. Assurances Spécifiques & Transport | 5 garanties |

================================================================================
# I. ASSURANCES AUTOMOBILES
================================================================================

---

# [PRODUITS::AUTO::GARANTIE::RC_OBLIGATOIRE]

> TYPE: garantie
> STATUT: OBLIGATOIRE
> LOI: ORDONNANCE_95-07
> CHUNK_ID: GARAN-AUTO-RC_OBLIGATOIRE

NOM : Responsabilité Civile (RC)
STATUT LÉGAL : Obligatoire — minimum légal
OBJET : Couvrir les dommages matériels et corporels causés aux tiers.
BASE LÉGALE : Ordonnance 95-07
NOTE : Toute autre garantie auto est optionnelle sauf CAT-NAT.

---

# [PRODUITS::AUTO::GARANTIE::TOUS_RISQUES]

> TYPE: garantie
> STATUT: OPTIONNELLE
> CONTRAT: TOUS_RISQUES
> CODE: TR
> CHUNK_ID: GARAN-AUTO-TOUS_RISQUES

NOM : Dommages Tous Accidents (Tous Risques)
OBJET : Indemnise les dommages au véhicule quel que soit le responsable,
        même sans tiers identifié.
CAS COUVERTS :
  - Choc contre corps fixe
  - Renversement
  - Accident sans tiers identifié
  - Accident dont l'assuré est responsable
AVANTAGE CLÉ : Pas besoin d'identifier un tiers pour être indemnisé.

---

# [PRODUITS::AUTO::GARANTIE::COLLISION_VALEUR_VENALE]

> TYPE: garantie
> STATUT: OPTIONNELLE
> CONDITION: tiers_identifie_obligatoire
> CHUNK_ID: GARAN-AUTO-COLLISION_VALE

NOM : Dommages Collision (Garantie Valeur Vénale)
OBJET : Indemnisation jusqu'à la valeur marchande du véhicule.
CONDITION IMPÉRATIVE : Exige un tiers identifié.
PARTICULARITÉ : Fonctionne même si l'assuré est responsable.
LIMITE : Pas d'indemnisation si le tiers n'est pas identifié.

---

# [PRODUITS::AUTO::GARANTIE::BRIS_DE_GLACE]

> TYPE: garantie
> STATUT: OPTIONNELLE
> CODE: BDG
> CHUNK_ID: GARAN-AUTO-BRIS_DE_GLACE

NOM : Bris de Glace (BDG)
ÉLÉMENTS COUVERTS :
  - Pare-brise
  - Lunette arrière
  - Vitres latérales
NOTE ALGÉRIENNE : Souvent sans franchise si réparation (non remplacement).
ATTENTION : Les phares et rétroviseurs NE sont PAS couverts ici
            → voir garantie Optiques & Rétroviseurs.

---

# [PRODUITS::AUTO::GARANTIE::OPTIQUES_RETROVISEURS]

> TYPE: garantie
> STATUT: OPTIONNELLE
> CODE: OPT
> SPECIFICITE: droit_algerien
> CHUNK_ID: GARAN-AUTO-OPTIQUES_RETRO

NOM : Dommages Collision (Optiques & Rétroviseurs)
SPÉCIFICITÉ ALGÉRIENNE : En Algérie, les phares et rétroviseurs sont
                          gérés dans cette garantie distincte et NON dans le BDG.
ÉLÉMENTS COUVERTS :
  - Phares avant et arrière
  - Rétroviseurs extérieurs

---

# [PRODUITS::AUTO::GARANTIE::INCENDIE_EXPLOSION]

> TYPE: garantie
> STATUT: OPTIONNELLE
> CODE: ICTM
> CHUNK_ID: GARAN-AUTO-INCENDIE_EXPLO

NOM : Incendie & Explosion
OBJET : Dégâts causés par le feu ou explosion du véhicule.
ORIGINES COUVERTES :
  - Incendie d'origine interne (court-circuit, moteur)
  - Incendie d'origine externe (feu venant de l'extérieur)
  - Explosion

---

# [PRODUITS::AUTO::GARANTIE::VOL]

> TYPE: garantie
> STATUT: OPTIONNELLE
> CODE: VIV
> CHUNK_ID: GARAN-AUTO-VOL

NOM : Vol et Tentative de Vol
OBJET : Remboursement de la valeur vénale ou des dégâts liés à l'effraction.
ÉLÉMENTS COUVERTS :
  - Vol total du véhicule → remboursement valeur vénale
  - Tentative de vol avec effraction → dégâts serrures, neiman
FRANCHISE : 25 000 DA minimum (voir Module_Indemnisation)

---

# [PRODUITS::AUTO::GARANTIE::VANDALISME]

> TYPE: garantie
> STATUT: OPTIONNELLE
> CODE: VAN
> CHUNK_ID: GARAN-AUTO-VANDALISME

NOM : Vandalisme
OBJET : Dommages causés par des actes de malveillance gratuits.
DISTINCTION : Acte volontaire sans but de vol (rayures, bris intentionnel, etc.)

---

# [PRODUITS::AUTO::GARANTIE::CATNAT]

> TYPE: garantie
> STATUT: OBLIGATOIRE
> LOI: LOI_03-12
> CHUNK_ID: GARAN-AUTO-CATNAT

NOM : Catastrophes Naturelles (CAT-NAT)
STATUT LÉGAL : Obligatoire en Algérie
LOI : Loi 03-12
ÉVÉNEMENTS COUVERTS :
  - Inondations
  - Séismes
  - Coulées de boue

---

# [PRODUITS::AUTO::GARANTIE::TEMPETE_CLIMATIQUE]

> TYPE: garantie
> STATUT: OPTIONNELLE
> CODE: TMP
> CHUNK_ID: GARAN-AUTO-TEMPETE_CLIMAT

NOM : Tempête / Événements Climatiques
OBJET : Phénomènes violents sans besoin d'arrêté officiel.
ÉVÉNEMENTS COUVERTS :
  - Grêle
  - Vent violent
  - Autres événements climatiques extrêmes
DIFFÉRENCE AVEC CAT-NAT : Pas besoin d'arrêté de catastrophe naturelle.

---

# [PRODUITS::AUTO::GARANTIE::CORPOREL_CONDUCTEUR]

> TYPE: renvoi_module
> STATUT: HORS_PERIMETRE_AUTO
> CHUNK_ID: GARAN-AUTO-CORPOREL_CONDU
> MODULE_SOURCE: Module_Personnes.md

NOM : Dommages Corporels du Conducteur
PÉRIMÈTRE : Cette garantie relève du Module Personnes (M4) — non traitée ici.
RENVOI : → Voir [Module_Personnes.md] — Section SECTION-PERS-GAV et SECTION-PERS-IPP
NOTE : Bien que souscrite en option sur un contrat auto, la tarification
       et la gestion des dommages corporels conducteur sont régies
       exclusivement par les règles du Module Personnes.

---

# [PRODUITS::AUTO::GARANTIE::ASSISTANCE_DEPANNAGE]

> TYPE: garantie
> STATUT: OPTIONNELLE
> CODE: AST, ASTP
> CHUNK_ID: GARAN-AUTO-ASSISTANCE_DEP

NOM : Assistance / Dépannage
PRESTATIONS :
  - Remorquage 24h/24
  - Rapatriement du véhicule et des occupants
  - Véhicule de remplacement (selon contrat)

---

# [PRODUITS::AUTO::GARANTIE::VALEUR_A_NEUF]

> TYPE: garantie
> STATUT: OPTIONNELLE
> CODE: EVNA, VN
> CHUNK_ID: GARAN-AUTO-VALEUR_A_NEUF

NOM : Valeur à Neuf / Valeur Majorée
OBJET : Remboursement au prix d'achat sans déduire la vétusté.
DURÉE : Généralement pendant 12 à 36 mois après l'achat du véhicule.
AVANTAGE : Évite la dépréciation lors d'un sinistre total en début de vie du véhicule.

---

# [PRODUITS::AUTO::GARANTIE::DEFENSE_RECOURS]

> TYPE: garantie
> STATUT: OPTIONNELLE
> CODE: DR, DRG
> SOURCE: DMP_REFERENCE_GARANTIE
> CHUNK_ID: GARAN-AUTO-DEFENSE_RECOURS

NOM : Defense et Recours (DR / DRG)
OBJET : Prise en charge des frais de justice et de la defense penale.
DR : Defense & Recours payant (protection juridique complete)
DRG : Defense & Recours gratuit (protection juridique de base)

---

# [PRODUITS::AUTO::GARANTIE::RC_FRONTIERE]

> TYPE: garantie
> STATUT: OPTIONNELLE
> CODE: RC1M, RC2M
> SOURCE: DMP_REFERENCE_GARANTIE
> CHUNK_ID: GARAN-AUTO-RC_FRONTIERE

NOM : RC Frontiere (1 ou 2 Mois)
OBJET : Extension de la RC pour deplacements a l'etranger.
RC1M : 1 mois de couverture frontiere
RC2M : 2 mois de couverture frontiere

---

# [PRODUITS::AUTO::GARANTIE::EXT_RC_PAYS_ARABES]

> TYPE: garantie
> STATUT: OPTIONNELLE
> CODE: EXTRC
> SOURCE: DMP_REFERENCE_GARANTIE
> CHUNK_ID: GARAN-AUTO-EXT_RC_PAYS_ARAB

NOM : Extension RC Pays Arabes
OBJET : Extension geographique de la RC aux pays arabes.

---

# [PRODUITS::AUTO::GARANTIE::COLLISION_FRANCHISE]

> TYPE: garantie
> STATUT: OPTIONNELLE
> CODE: DC10 a DC50
> SOURCE: Compagnie + DMP_REFERENCE_GARANTIE
> CHUNK_ID: GARAN-AUTO-COLLISION_FRAN

NOM : Dommages Collision avec Franchise
FRANCHISES : DC10=10000, DC20=20000, DC30=30000, DC40=40000, DC50=50000 DA

---

# [PRODUITS::AUTO::GARANTIE::AVEC_SANS_COLLISION]

> TYPE: garantie
> STATUT: OPTIONNELLE
> CODE: ASC2, ASC3, ASC5
> SOURCE: Compagnie
> CHUNK_ID: GARAN-AUTO-AVEC_SANS_COLL

NOM : Dommages Avec ou Sans Collision
PLAFONDS : ASC2=200000, ASC3=300000, ASC5=500000 DA

---

# [PRODUITS::AUTO::GARANTIE::PERTE_JOUISSANCE]

> TYPE: garantie
> STATUT: OPTIONNELLE
> CODE: PJX
> SOURCE: Compagnie
> CHUNK_ID: GARAN-AUTO-PERTE_JOUISSAN

NOM : Perte de Jouissance
OBJET : Indemnite journaliere en cas d'immobilisation du vehicule.

---

# [PRODUITS::AUTO::GARANTIE::TOP_REPARATEUR]

> TYPE: garantie
> STATUT: OPTIONNELLE
> CODE: TOP2
> SOURCE: Compagnie
> CHUNK_ID: GARAN-AUTO-TOP_REPARATEUR

NOM : Top Reparateur
OBJET : Reparation en reseau agree sans avance de frais.

---

# [PRODUITS::AUTO::GARANTIE::RACHAT_VETUSTE]

> TYPE: garantie
> STATUT: OPTIONNELLE
> CODE: RVF
> SOURCE: Compagnie
> CHUNK_ID: GARAN-AUTO-RACHAT_VETUSTE

NOM : Rachat Vetuste et Franchise
OBJET : Suppression de la vetuste et de la franchise en cas de sinistre.

---

# [PRODUITS::AUTO::GARANTIE::BDG_PANORAMIQUE]

> TYPE: garantie
> STATUT: OPTIONNELLE
> CODE: BGP
> SOURCE: Compagnie
> CHUNK_ID: GARAN-AUTO-BDG_PANORAMIQU

NOM : Bris de Glace Panoramique
OBJET : Extension du BDG aux toits panoramiques et vitres feuilletées.

---

# [PRODUITS::AUTO::GARANTIE::VOL_INCENDIE]

> TYPE: garantie
> STATUT: OPTIONNELLE
> CODE: VIV, VOL, ICTM, IRCC
> SOURCE: DMP_CODEGARA_TAXE
> CHUNK_ID: GARAN-AUTO-VOL_INCENDIE

NOM : Vol et Incendie
FORMULES : VIV (Vol+Incendie combine), VOL (Vol seul), ICTM (Incendie/Tempete), IRCC (Incendie+CAT-NAT)

---

# [PRODUITS::AUTO::PACKS::Compagnie]

> TYPE: pack
> STATUT: OPTIONNEL
> SOURCE: Compagnie
> CHUNK_ID: GARAN-AUTO-PACKS_Compagnie

NOM : Packs Remise Compagnie
REMISES : ECO=10%, CLASSIC=20%, ESSENTIEL=25%, ESSENTIEL+=30%, PREMIUM=40%, SILVER=45%, GOLD=50%

================================================================================
# II. ASSURANCES HABITATION (Multirisque Habitation — MRH)
================================================================================

---

# [PRODUITS::HABITATION::GARANTIE::INCENDIE_BASE]

> TYPE: garantie
> STATUT: GARANTIE_DE_BASE_MRH
> CHUNK_ID: GARAN-HAB-INCENDIE_BASE

NOM : Incendie, Explosion, Foudre
OBJET : Garantie de base du contrat MRH.
BIENS COUVERTS :
  - Bâtiment (structure)
  - Mobilier (contenu)

---

# [PRODUITS::HABITATION::GARANTIE::DEGATS_EAUX]

> TYPE: garantie
> STATUT: STANDARD_MRH
> CHUNK_ID: GARAN-HAB-DEGATS_EAUX

NOM : Dégâts des Eaux
CAUSES COUVERTES :
  - Fuites de canalisations
  - Ruptures de canalisations
  - Infiltrations par la toiture

---

# [PRODUITS::HABITATION::GARANTIE::VOL_VANDALISME]

> TYPE: garantie
> STATUT: OPTIONNELLE_MRH
> CHUNK_ID: GARAN-HAB-VOL_VANDALISME

NOM : Vol & Vandalisme (Habitation)
OBJET : Vol des biens meubles et dégradations des accès.
BIENS COUVERTS : Mobilier, appareils, effets personnels.

---

# [PRODUITS::HABITATION::GARANTIE::RC_LOCATAIRE]

> TYPE: garantie
> STATUT: STANDARD_MRH
> CIBLE: locataires
> CHUNK_ID: GARAN-HAB-RC_LOCATAIRE
> MODULE_DETAIL: Module_Risques_Divers.md — RD-MRH

NOM : RC Locataire
OBJET : Couvre les dommages causés par le locataire à l'immeuble du bailleur.
RISQUES COUVERTS :
  - Incendie accidentel se propageant à l'immeuble
  - Dégâts des eaux causés à l'immeuble
  - Dégradations involontaires des parties communes
DISTINCTION : Distincte de la RC Vie Privée (propriétaire occupant).
NOTE LÉGALE : Obligatoire dans tout bail d'habitation — usage constant marché algérien.

---

# [PRODUITS::HABITATION::GARANTIE::BRIS_GLACE_HABITAT]

> TYPE: garantie
> STATUT: OPTIONNELLE_MRH
> CHUNK_ID: GARAN-HAB-BRIS_GLACE_HAB
> MODULE_DETAIL: Module_Risques_Divers.md — RD-MRH

NOM : Bris de Glace Habitation
OBJET : Couvre la casse accidentelle des vitrages du logement.
ÉLÉMENTS COUVERTS :
  - Fenêtres et baies vitrées
  - Portes vitrées intérieures et extérieures
  - Véranda et verrière
  - Miroirs fixes (selon contrat)
DISTINCTION : NE couvre PAS les vitres de véhicule → voir GARAN-AUTO-BRIS_DE_GLACE.
FRANCHISE : Généralement 0 DA si casse accidentelle sans bris volontaire.

---



> TYPE: garantie
> STATUT: OBLIGATOIRE
> LOI: LOI_03-12
> CHUNK_ID: GARAN-HAB-CATNAT

NOM : CAT-NAT (Habitation)
STATUT LÉGAL : Obligation légale algérienne distincte pour les propriétaires.
NOTE : Obligation différente de la CAT-NAT automobile.

---

# [PRODUITS::HABITATION::GARANTIE::TEMPETE_GRELE]

> TYPE: garantie
> STATUT: OPTIONNELLE_MRH
> CHUNK_ID: GARAN-HAB-TEMPETE_GRELE

NOM : Tempête / Grêle / Neige
OBJET : Dommages atmosphériques à la structure du bâtiment.

---

# [PRODUITS::HABITATION::GARANTIE::RC_VIE_PRIVEE]

> TYPE: garantie
> STATUT: STANDARD_MRH
> CHUNK_ID: GARAN-HAB-RC_VIE_PRIVEE

NOM : RC Vie Privée (Chef de Famille)
OBJET : Dommages causés aux tiers par les membres du foyer ou animaux.
BÉNÉFICIAIRES : Chef de famille et tous membres du foyer.

---

# [PRODUITS::HABITATION::GARANTIE::DOMMAGES_ELECTRIQUES]

> TYPE: garantie
> STATUT: OPTIONNELLE_MRH
> CHUNK_ID: GARAN-HAB-DOMMAGES_ELECT

NOM : Dommages Électriques
OBJET : Surtensions sur les appareils électroménagers et informatiques.

---

# [PRODUITS::HABITATION::GARANTIE::OBJETS_VALEUR]

> TYPE: garantie
> STATUT: OPTIONNELLE_MRH
> CONDITION: expertise_requise
> CHUNK_ID: GARAN-HAB-OBJETS_VALEUR

NOM : Objets de Valeur / Collections
OBJET : Protection renforcée pour bijoux et œuvres d'art.
CONDITION : Sur expertise préalable obligatoire.

---

# [PRODUITS::HABITATION::GARANTIE::LOYERS_IMPAYES]

> TYPE: garantie
> STATUT: OPTIONNELLE_MRH
> CIBLE: proprietaires_bailleurs
> CHUNK_ID: GARAN-HAB-LOYERS_IMPAYES

NOM : Loyers Impayés
OBJET : Protection du bailleur contre les défauts de paiement du locataire.

---

# [PRODUITS::HABITATION::GARANTIE::PROTECTION_JURIDIQUE]

> TYPE: garantie
> STATUT: OPTIONNELLE_MRH
> CHUNK_ID: GARAN-HAB-PROTECTION_JUR

NOM : Protection Juridique Habitation
OBJET : Litiges de voisinage, syndic de copropriété ou artisans.

================================================================================
# III. ASSURANCES DE PERSONNES (Santé & Prévoyance)
================================================================================

---

# [PRODUITS::PERSONNES::GARANTIE::COMPLEMENTAIRE_SANTE]

> TYPE: garantie
> STATUT: COLLECTIVE_OU_INDIVIDUELLE
> ORGANISMES_REF: CNAS, CASNOS
> CHUNK_ID: GARAN-PERS-COMPLEMENTAIRE

NOM : Complémentaire Santé (Santé Collective)
OBJET : Remboursement des frais médicaux en sus de la sécurité sociale.
ORGANISMES DE BASE ALGÉRIENS : CNAS (salariés) / CASNOS (non-salariés)

---

# [PRODUITS::PERSONNES::GARANTIE::DECES]

> TYPE: garantie
> STATUT: PREVOYANCE
> CHUNK_ID: GARAN-PERS-DECES

NOM : Garantie Décès
OBJET : Capital versé aux bénéficiaires désignés en cas de décès de l'assuré.

---

# [PRODUITS::PERSONNES::GARANTIE::PTIA]

> TYPE: garantie
> STATUT: PREVOYANCE
> CODE: PTIA
> CHUNK_ID: GARAN-PERS-PTIA

NOM : Perte Totale et Irréversible d'Autonomie (PTIA)
OBJET : Versement anticipé du capital si l'assuré nécessite une aide constante
        pour les actes essentiels de la vie quotidienne.

---

# [PRODUITS::PERSONNES::GARANTIE::ITT]

> TYPE: garantie
> STATUT: PREVOYANCE
> CODE: ITT
> CHUNK_ID: GARAN-PERS-ITT

NOM : Incapacité Temporaire de Travail (ITT)
OBJET : Indemnités journalières pour compenser la perte de salaire
        pendant l'arrêt de travail.

---

# [PRODUITS::PERSONNES::GARANTIE::INVALIDITE_PERMANENTE]

> TYPE: garantie
> STATUT: PREVOYANCE
> CODES: IPT, IPP
> CHUNK_ID: GARAN-PERS-INVALIDITE_PER

NOM : Invalidité Permanente (IPT / IPP)
OBJET : Rente ou capital selon le taux d'invalidité après consolidation.
IPT : Invalidité Permanente Totale
IPP : Invalidité Permanente Partielle

---

# [PRODUITS::PERSONNES::GARANTIE::GAV]

> TYPE: garantie
> STATUT: INDIVIDUELLE
> CODE: GAV
> CHUNK_ID: GARAN-PERS-GAV

NOM : Garantie des Accidents de la Vie (GAV)
OBJET : Indemnisation des accidents domestiques, de loisirs ou médicaux
        sans responsable identifié.

---

# [PRODUITS::PERSONNES::GARANTIE::DEPENDANCE]

> TYPE: garantie
> STATUT: PREVOYANCE_LONG_TERME
> CHUNK_ID: GARAN-PERS-DEPENDANCE

NOM : Garantie Dépendance
OBJET : Rente pour financer la perte d'autonomie liée à l'âge ou à la maladie.

---

# [PRODUITS::PERSONNES::GARANTIE::OBSEQUES]

> TYPE: garantie
> STATUT: PREVOYANCE
> CHUNK_ID: GARAN-PERS-OBSEQUES

NOM : Garantie Obsèques
OBJET : Financement et/ou organisation des funérailles.

---

# [PRODUITS::PERSONNES::GARANTIE::MALADIES_GRAVES]

> TYPE: garantie
> STATUT: PREVOYANCE
> CHUNK_ID: GARAN-PERS-MALADIES_GRAVE

NOM : Maladies Graves / Redoutées
OBJET : Capital immédiat versé au diagnostic d'une maladie grave.
MALADIES CONCERNÉES : Cancer, AVC, infarctus, et autres maladies redoutées.

---

# [PRODUITS::PERSONNES::GARANTIE::INDEMNITES_HOSPITALISATION]

> TYPE: garantie
> STATUT: COMPLEMENTAIRE_SANTE
> CHUNK_ID: GARAN-PERS-INDEMNITES_HOS

NOM : Indemnités Journalières d'Hospitalisation
OBJET : Somme forfaitaire versée par jour d'hospitalisation.

================================================================================
# IV. ASSURANCE VIE & EMPRUNTEUR
================================================================================

---

# [PRODUITS::VIE::GARANTIE::ASSURANCE_VIE]

> TYPE: garantie
> BRANCHE: VIE_CAPITALISATION
> CHUNK_ID: GARAN-VIE-ASSURANCE_VIE

NOM : Assurance Vie (Fonds Euros / UC)
OBJET : Épargne, capitalisation et transmission de patrimoine.
TYPES : Fonds en euros (capital garanti) / Unités de compte (UC, liées aux marchés).

---

# [PRODUITS::VIE::GARANTIE::DECES_EMPRUNTEUR]

> TYPE: garantie
> BRANCHE: EMPRUNTEUR
> CODE: ADE
> CHUNK_ID: GARAN-VIE-DECES_EMPRUNTE

NOM : Assurance Décès Emprunteur (ADE)
OBJET : Remboursement du crédit bancaire à la banque en cas de décès de l'emprunteur.
BÉNÉFICIAIRE : La banque prêteuse.

---

# [PRODUITS::VIE::GARANTIE::PTIA_EMPRUNTEUR]

> TYPE: garantie
> BRANCHE: EMPRUNTEUR
> CHUNK_ID: GARAN-VIE-PTIA_EMPRUNTEU

NOM : PTIA Emprunteur
OBJET : Solde du prêt en cas d'invalidité totale et irréversible de l'emprunteur.

---

# [PRODUITS::VIE::GARANTIE::ITT_EMPRUNTEUR]

> TYPE: garantie
> BRANCHE: EMPRUNTEUR
> CHUNK_ID: GARAN-VIE-ITT_EMPRUNTEUR

NOM : ITT Emprunteur
OBJET : Prise en charge des mensualités du crédit pendant l'arrêt de travail.

---

# [PRODUITS::VIE::GARANTIE::PERTE_EMPLOI_EMPRUNTEUR]

> TYPE: garantie
> BRANCHE: EMPRUNTEUR
> CHUNK_ID: GARAN-VIE-PERTE_EMPLOI_E

NOM : Perte d'Emploi Emprunteur
OBJET : Relais du paiement des mensualités en cas de licenciement.
CONDITION : Licenciement involontaire uniquement.

================================================================================
# V. ASSURANCES PROFESSIONNELLES & TECHNIQUES
================================================================================

---

# [PRODUITS::PRO::GARANTIE::RC_PRO]

> TYPE: garantie
> STATUT: OPTIONNELLE_OU_OBLIGATOIRE_SELON_PROFESSION
> CHUNK_ID: GARAN-PRO-RC_PRO

NOM : RC Professionnelle (RC Pro)
OBJET : Erreurs, fautes ou omissions commises dans l'exercice de l'activité.
PROFESSIONS CIBLES : Médecins, Avocats, Comptables, Architectes, etc.

---

# [PRODUITS::PRO::GARANTIE::DECENNALE]

> TYPE: garantie
> STATUT: OBLIGATOIRE
> LOI: CODE_CIVIL_ART175
> DUREE: 10_ans
> CHUNK_ID: GARAN-PRO-DECENNALE

NOM : Garantie Décennale
STATUT LÉGAL : Obligatoire (Article 175 du Code Civil algérien)
OBJET : Solidité des ouvrages de construction pendant 10 ans.
CIBLES : Entrepreneurs, constructeurs, architectes.

---

# [PRODUITS::PRO::GARANTIE::DOMMAGES_BIENS_PROS]

> TYPE: garantie
> STATUT: OPTIONNELLE_PRO
> CHUNK_ID: GARAN-PRO-DOMMAGES_BIENS

NOM : Dommages aux Biens Professionnels
OBJET : Protection des locaux et équipements professionnels.
RISQUES COUVERTS : Incendie, vol, bris de machines.
CIBLES : Usines, commerces, entrepôts.

---

# [PRODUITS::PRO::GARANTIE::PERTES_EXPLOITATION]

> TYPE: garantie
> STATUT: OPTIONNELLE_PRO
> CHUNK_ID: GARAN-PRO-PERTES_EXPLOIT

NOM : Pertes d'Exploitation
OBJET : Compensation de la perte de marge après un sinistre matériel.
NOTE : Complément indispensable des dommages aux biens professionnels.

---

# [PRODUITS::PRO::GARANTIE::RC_DIRIGEANTS]

> TYPE: garantie
> STATUT: OPTIONNELLE_PRO
> CHUNK_ID: GARAN-PRO-RC_DIRIGEANTS

NOM : RC des Dirigeants
OBJET : Protection du patrimoine personnel du dirigeant contre les fautes de gestion.
CIBLES : PDG, DG, membres de conseil d'administration.

---

# [PRODUITS::PRO::GARANTIE::PROTECTION_JURIDIQUE_PRO]

> TYPE: garantie
> STATUT: OPTIONNELLE_PRO
> CHUNK_ID: GARAN-PRO-PROTECTION_JUR

NOM : Protection Juridique Professionnelle
OBJET : Frais de justice pour litiges avec clients, fournisseurs ou administration fiscale.

---

# [PRODUITS::PRO::GARANTIE::CYBER_RISQUES]

> TYPE: garantie
> STATUT: OPTIONNELLE_PRO
> DOMAINE: NOUVELLES_TECHNOLOGIES
> CHUNK_ID: GARAN-PRO-CYBER_RISQUES

NOM : Cyber-Risques
OBJET : Protection contre les attaques informatiques.
RISQUES COUVERTS :
  - Piratage informatique
  - Vol de données
  - Ransomwares (rançongiciels)

================================================================================
# VI. ASSURANCES SPÉCIFIQUES & TRANSPORT
================================================================================

---

# [PRODUITS::SPECIFIQUES::GARANTIE::VOYAGE]

> TYPE: garantie
> STATUT: INDIVIDUELLE_OU_COLLECTIVE
> CHUNK_ID: GARAN-SPEC-VOYAGE

NOM : Assurance Voyage
OBJET : Couverture lors des déplacements à l'étranger.
PRESTATIONS :
  - Assistance médicale internationale (obligatoire visa Schengen)
  - Rapatriement sanitaire

---

# [PRODUITS::SPECIFIQUES::GARANTIE::SCOLAIRE]

> TYPE: garantie
> STATUT: INDIVIDUELLE
> CIBLE: eleves
> CHUNK_ID: GARAN-SPEC-SCOLAIRE

NOM : Assurance Scolaire
OBJET : Couverture des élèves durant l'année scolaire.
GARANTIES INCLUSES :
  - Responsabilité civile
  - Accident individuel

---

# [PRODUITS::SPECIFIQUES::GARANTIE::TRANSPORT_FACULTES]

> TYPE: garantie
> BRANCHE: TRANSPORT
> CHUNK_ID: GARAN-SPEC-TRANSPORT_FACU

NOM : Transport de Facultés (Maritime / Terrestre)
FORMULES :
  - Tous Risques → couverture maximale
  - FAP Sauf (Franc d'Avaries Particulières Sauf) → couverture limitée aux sinistres majeurs

---

# [PRODUITS::SPECIFIQUES::GARANTIE::RISQUES_GUERRE]

> TYPE: garantie
> BRANCHE: TRANSPORT
> CODE: RGA
> CHUNK_ID: GARAN-SPEC-RISQUES_GUERRE

NOM : Risques de Guerre et Assimilés (RGA)
OBJET : Rachat de l'exclusion terrorisme / sabotage pour les marchandises transportées.

---

# [PRODUITS::SPECIFIQUES::GARANTIE::ANIMAUX]

> TYPE: garantie
> STATUT: INDIVIDUELLE
> CHUNK_ID: GARAN-SPEC-ANIMAUX

NOM : Assurance Animaux
OBJET : Frais vétérinaires en cas de maladie ou accident de l'animal.

================================================================================
# FIN RÉFÉRENTIEL GARANTIES — v1.0 — STANDARD_DZ
================================================================================
## Procédure de Gestion des Garanties

**Référence Légale** : Ordonnance 95-07, Art. 2 — Loi 03-12, Art. 1.

### Procédure de Gestion des Garanties
1. **Étape 1 — Identification** : Identifier le type de garantie demandée (automobile, habitation, personnes, vie, transport).
2. **Étape 2 — Vérification d'éligibilité** : Contrôler les conditions de souscription et les exclusions légales selon l'Ordonnance 95-07.
3. **Étape 3 — Tarification** : Appliquer les barèmes officiels du référentiel technique ; se référer à [Référentiel Technique](./referentiel_technique_assurance.md).
4. **Étape 4 — Émission** : Générer le certificat d'assurance ou avenant selon les formulaires agréés par le CNA.
5. **Étape 5 — Archivage** : Enregistrer le dossier dans le [Registre Souverain Master](./REGISTRE_SOUVERAIN_MASTER.md).

## Liens Connexes

- [Module Devis](./Module_Devis.md)
- [Module Gestion Sinistres](./Module_Gestion_Sinistres.md)
- [Module Indemnisation](./Module_Indemnisation.md)
- [Module Personnes](./Module_Personnes.md)
- [Module Vie](./Module_Vie.md)

---

# PARTIE B — Module Risques Divers (RD)

---
fichier: Module_Risques_Divers.md
domaine: Assurances Algériennes
lois: [Ordonnance 95-07, Ordonnance 03-12, Décret 95-413, Décret 95-414, Décret 95-415, Code Civil Art. 175, Loi Finances 2026]
version: 1.0
statut: PRODUCTION
date: 2026-05-12
usage: BASE_CONNAISSANCE_SOUVERAINE | MOTEUR_DEVIS | WORKFLOW_INTERNE
langue: FR
classification: CONFIDENTIEL — Usage Interne
chunk_strategy: 1_concept_par_section
alias_rag: MODULE_RISQUES_DIVERS_v1
module_id: MODULE_RD
lien_devis: Module_Devis.md
lien_garanties: referentiel_garanties.md
lien_params: PARAMETRES_EXPERTS_ALERTE.md
lien_registre: REGISTRE_SOUVERAIN_MASTER.md
---

================================================================================
# MODULE RISQUES DIVERS — STANDARD ALGÉRIEN
# MRH | RC Professionnelle | Décennale | TRC | Incendie Entreprise | Transport
================================================================================

---

## TABLE DES MATIÈRES

1. [RD-CADRE] — Cadre Légal & Classification
2. [RD-MRH] — Multirisque Habitation (MRH)
3. [RD-RC-PRO] — Responsabilité Civile Professionnelle
4. [RD-DECENNALE] — Garantie Décennale
5. [RD-TRC] — Tous Risques Chantier (TRC)
6. [RD-INCENDIE] — Incendie & Risques Entreprise
7. [RD-TRANSPORT] — Transport de Marchandises
8. [RD-TAXES] — Taxes & Formule TTC par Branche
9. [RD-ALERTES] — Alertes & Anomalies

---

# ══════════════════════════════════════════════════════════════════
# SECTION I — CADRE LÉGAL & CLASSIFICATION
# ══════════════════════════════════════════════════════════════════

---

# [RD::CADRE_LEGAL::REFERENCES]

> TYPE: references_legislatives
> CHUNK_ID: RD-CADRE-LEGAL

| Texte | Objet |
|---|---|
| Ordonnance 95-07 | Loi cadre assurances — régit tous les contrats |
| Ordonnance 03-12 | CAT-NAT obligatoire — s'applique MRH et Entreprise |
| Décret 95-413 | RC entreprises obligatoire |
| Décret 95-414 | RC construction obligatoire |
| Décret 95-415 | Incendie entreprises obligatoire |
| Code Civil Art. 175 | Garantie décennale obligatoire — ouvrages de construction |
| Loi Finances 2026 | Taux TCA et taxes en vigueur |

---

# [RD::CLASSIFICATION::BRANCHES]

> TYPE: classification_produits
> CHUNK_ID: RD-CLASSIFICATION

| Branche | Code | Statut légal | Module source |
|---|---|---|---|
| Multirisque Habitation | MRH | Recommandée / CAT-NAT obligatoire | RD-MRH |
| RC Professionnelle | RCP | Obligatoire selon profession | RD-RC-PRO |
| Garantie Décennale | DEC | Obligatoire — Art. 175 Code Civil | RD-DECENNALE |
| Tous Risques Chantier | TRC | Obligatoire grands chantiers | RD-TRC |
| Incendie Entreprise | INC | Obligatoire — Décret 95-415 | RD-INCENDIE |
| Transport Marchandises | TMD | Obligatoire import/export | RD-TRANSPORT |

---

# ══════════════════════════════════════════════════════════════════
# SECTION II — MULTIRISQUE HABITATION (MRH)
# ══════════════════════════════════════════════════════════════════

---

# [RD::MRH::GARANTIES::CATALOGUE]

> TYPE: catalogue_garanties
> CHUNK_ID: RD-MRH-GARANTIES

GARANTIES MRH — CATALOGUE COMPLET :

GARANTIES DE BASE (incluses systématiquement) :
  ✅ Incendie, Explosion, Foudre          → Bâtiment + Mobilier
  ✅ Dégâts des Eaux                      → Fuites, ruptures, infiltrations toiture
  ✅ CAT-NAT                              → Obligatoire Loi 03-12
  ✅ RC Vie Privée (Chef de Famille)      → Dommages tiers causés par le foyer ou animaux

GARANTIES OPTIONNELLES :
  ⭕ Vol & Vandalisme                     → Mobilier, effets personnels, accès
  ⭕ Tempête / Grêle / Neige             → Dommages atmosphériques structure bâtiment
  ⭕ Dommages Électriques                → Surtensions appareils électroménagers/informatiques
  ⭕ Bris de Glace Habitation            → Vitres, vitrages, véranda (distinct du BDG auto)
  ⭕ RC Locataire                        → Dommages causés au bailleur (incendie, dégâts eaux)
  ⭕ Objets de Valeur / Collections      → Sur expertise préalable obligatoire
  ⭕ Loyers Impayés                      → Protection bailleur — locataire défaillant
  ⭕ Protection Juridique Habitation     → Litiges voisinage, syndic, artisans

NOTE RC LOCATAIRE :
  Distincte de la RC Vie Privée (propriétaire).
  Le locataire est responsable des dommages causés à l'immeuble du bailleur.
  Obligatoire dans tout bail d'habitation (usage courant marché algérien).

NOTE BRIS DE GLACE HABITATION :
  Couvre les vitrages du logement (fenêtres, portes vitrées, véranda).
  NE couvre PAS les pare-brises ou vitres de véhicule → voir GARAN-AUTO-BRIS_DE_GLACE.

---

# [RD::MRH::VARIABLES::TARIFICATION]

> TYPE: variables_calcul
> CHUNK_ID: RD-MRH-VARIABLES

VARIABLES ENTRANT DANS LE CALCUL DE LA PRIME MRH :

  V1 — Surface habitable (m²)          : Détermine le capital bâtiment de base
  V2 — Type de bien                    : Appartement / Villa / Maison individuelle
  V3 — Statut occupant                 : Propriétaire occupant / Locataire / Propriétaire bailleur
  V4 — Capital Bâtiment (DA)           : Valeur de reconstruction (non valeur vénale)
  V5 — Capital Mobilier (DA)           : Estimation inventaire assuré
  V6 — Étage / Niveau                  : Influence risque dégâts des eaux
  V7 — Zone géographique               : Impact CAT-NAT (zone sismique, inondable)
  V8 — Garanties optionnelles choisies : Cumul des extensions souscrites

---

# [RD::MRH::FORMULES::CALCUL_CAPITAUX]

> TYPE: formule_calcul
> CHUNK_ID: RD-MRH-CALCUL-CAPITAUX

ÉTAPE 1 — CALCUL DES CAPITAUX À ASSURER :

  A. CAPITAL BÂTIMENT (propriétaires uniquement) :
     Capital_Bâtiment = Surface_m² × Coût_Reconstruction_m²
     Coût_Reconstruction_m² standard Algérie 2026 : 60 000 DA à 90 000 DA/m²
     (selon standing : économique / moyen / haut de gamme)

     Exemple : Appartement 80 m² standing moyen
     Capital_Bâtiment = 80 × 75 000 = 6 000 000 DA

  B. CAPITAL MOBILIER :
     Méthode 1 : Inventaire pièce par pièce (précis)
     Méthode 2 : Règle pratique = Capital_Bâtiment × 35% (standard)

     Exemple : 6 000 000 × 35% = 2 100 000 DA

  C. RÈGLE PROPORTIONNELLE (sous-assurance) :
     Si Capital_Assuré < Valeur_Réelle :
       Indemnité = Sinistre × (Capital_Assuré / Valeur_Réelle)
     → Toujours déclarer la valeur réelle pour éviter la réduction d'indemnité.

---

# [RD::MRH::FORMULES::PRIME]

> TYPE: formule_calcul
> CHUNK_ID: RD-MRH-FORMULE-PRIME

ÉTAPE 2 — CALCUL DE LA PRIME NETTE MRH :

  BARÈME DE BASE 2026 (taux sur capitaux assurés) :

  | Garantie               | Taux annuel           | Base de calcul        |
  |---|---|---|
  | Incendie + Explosion   | 0,08‰ à 0,15‰         | Capital Bâtiment      |
  | Dégâts des Eaux        | 0,10‰ à 0,20‰         | Capital Bâtiment      |
  | CAT-NAT                | 0,05‰ (plancher légal)| Capital Bâtiment      |
  | RC Vie Privée          | Forfait 3 000 DA/an   | —                     |
  | Vol & Vandalisme       | 0,20‰ à 0,35‰         | Capital Mobilier      |
  | Tempête / Grêle        | 0,05‰ à 0,10‰         | Capital Bâtiment      |
  | Dommages Électriques   | 0,15‰ à 0,25‰         | Capital Mobilier      |
  | Bris de Glace Habitat  | Forfait 2 000 DA/an   | —                     |
  | RC Locataire           | Forfait 4 000 DA/an   | —                     |

  FORMULE PRIME NETTE TOTALE MRH :
  ```
  Prime_Nette_MRH = (Capital_Bâtiment × Taux_Bâtiment)
                  + (Capital_Mobilier × Taux_Mobilier)
                  + Σ Forfaits_Garanties_Optionnelles
  ```

  Exemple complet (propriétaire occupant, appartement 80 m²) :
    Capital Bâtiment  : 6 000 000 DA × 0,12‰  =   720 DA
    Capital Mobilier  : 2 100 000 DA × 0,25‰  =   525 DA
    CAT-NAT           : 6 000 000 DA × 0,05‰  =   300 DA
    RC Vie Privée     : Forfait               = 3 000 DA
    RC Locataire      : Forfait               = 4 000 DA
    Bris de Glace     : Forfait               = 2 000 DA
    ─────────────────────────────────────────────────────
    PRIME NETTE       :                       = 10 545 DA

ÉTAPE 3 — FORMULE TTC MRH :
  ```
  Prime_TTC_MRH = Prime_Nette_MRH × (1 + 0,19 + 0,02 + 0,01)
                = Prime_Nette_MRH × 1,22
  ```
  Exemple : 10 545 × 1,22 = 12 865 DA TTC/an

---

# ══════════════════════════════════════════════════════════════════
# SECTION III — RC PROFESSIONNELLE
# ══════════════════════════════════════════════════════════════════

---

# [RD::RC_PRO::DEFINITION]

> TYPE: description_produit
> CHUNK_ID: RD-RCP-DEFINITION
> LOI: DECRET_95-413

NOM : Responsabilité Civile Professionnelle (RC Pro)
STATUT LÉGAL : Obligatoire selon secteur (Décret 95-413)
OBJET : Couvre les dommages causés aux tiers dans l'exercice de l'activité professionnelle.

PROFESSIONS À RC OBLIGATOIRE EN ALGÉRIE :
  - Médecins, dentistes, pharmaciens
  - Avocats, notaires, huissiers
  - Architectes, bureaux d'études, géomètres
  - Experts-comptables, commissaires aux comptes
  - Agents et courtiers d'assurance
  - Entrepreneurs BTP, promoteurs immobiliers
  - Établissements d'enseignement privés

---

# [RD::RC_PRO::VARIABLES::TARIFICATION]

> TYPE: variables_calcul
> CHUNK_ID: RD-RCP-VARIABLES

VARIABLES ENTRANT DANS LE CALCUL DE LA PRIME RC PRO :

  V1 — Secteur d'activité (code APE/NACE)   : Détermine le taux de base
  V2 — Chiffre d'affaires annuel HT (DA)    : Base de calcul principale
  V3 — Nombre de salariés                   : Facteur aggravant/atténuant
  V4 — Nature des prestations               : Conseil / Exécution / Production
  V5 — Limite de garantie choisie (plafond) : Capital maximum indemnisable
  V6 — Franchise choisie                    : Atténue la prime
  V7 — Historique sinistres RC (3 ans)      : CRM professionnel

---

# [RD::RC_PRO::FORMULES::PRIME]

> TYPE: formule_calcul
> CHUNK_ID: RD-RCP-FORMULE-PRIME

BARÈME PAR SECTEUR D'ACTIVITÉ 2026 :

  | Secteur                        | Taux sur CA HT  | Prime min. annuelle |
  |---|---|---|
  | Professions médicales          | 0,8‰ à 1,5‰     | 25 000 DA           |
  | Professions juridiques         | 0,5‰ à 1,0‰     | 20 000 DA           |
  | Architecture / BET             | 1,0‰ à 2,0‰     | 30 000 DA           |
  | Expertise comptable            | 0,5‰ à 0,8‰     | 15 000 DA           |
  | Commerce / Distribution        | 0,3‰ à 0,6‰     | 10 000 DA           |
  | Informatique / Conseil         | 0,6‰ à 1,2‰     | 18 000 DA           |
  | Enseignement privé             | 0,4‰ à 0,7‰     | 12 000 DA           |
  | Autres activités de service    | 0,5‰ à 1,0‰     | 15 000 DA           |

FORMULE PRIME NETTE RC PRO :
  ```
  Prime_Nette_RCP = MAX(CA_Annuel_HT × Taux_Secteur ; Prime_Minimum_Secteur)
                  × Coefficient_Limite_Garantie
                  × CRM_Pro
  ```

  COEFFICIENT LIMITE DE GARANTIE :
    Plafond 5 000 000 DA   → Coefficient 1,00 (base)
    Plafond 10 000 000 DA  → Coefficient 1,25
    Plafond 20 000 000 DA  → Coefficient 1,50
    Plafond 50 000 000 DA  → Coefficient 2,00

  Exemple (architecte, CA = 15 000 000 DA, plafond 10 M DA, CRM = 1,00) :
    Prime_Nette = 15 000 000 × 1,5‰ × 1,25 × 1,00
               = 22 500 × 1,25
               = 28 125 DA

FORMULE TTC RC PRO :
  ```
  Prime_TTC_RCP = Prime_Nette_RCP × (1 + 0,19 + 0,01)
                = Prime_Nette_RCP × 1,20
  ```
  Exemple : 28 125 × 1,20 = 33 750 DA TTC/an

---

# ══════════════════════════════════════════════════════════════════
# SECTION IV — GARANTIE DÉCENNALE
# ══════════════════════════════════════════════════════════════════

---

# [RD::DECENNALE::DEFINITION]

> TYPE: description_produit
> CHUNK_ID: RD-DEC-DEFINITION
> LOI: CODE_CIVIL_ART_175

NOM : Garantie Décennale (Responsabilité Civile Décennale)
STATUT LÉGAL : Obligatoire — Article 175 du Code Civil algérien
DURÉE : 10 ans à compter de la réception de l'ouvrage
OBJET : Couvre la solidité et la conformité des ouvrages de construction.

CIBLES :
  - Entrepreneurs BTP
  - Constructeurs
  - Architectes maîtres d'œuvre
  - Promoteurs immobiliers

DOMMAGES COUVERTS :
  ✅ Effondrement total ou partiel de l'ouvrage
  ✅ Vices affectant la solidité (fissures structurelles, affaissements)
  ✅ Vices rendant l'ouvrage impropre à sa destination
  ✅ Dommages aux éléments d'équipement indissociables

DOMMAGES EXCLUS :
  ❌ Usure normale
  ❌ Dommages esthétiques sans impact sur solidité
  ❌ Sinistres provenant d'un mauvais entretien du maître d'ouvrage

---

# [RD::DECENNALE::VARIABLES::TARIFICATION]

> TYPE: variables_calcul
> CHUNK_ID: RD-DEC-VARIABLES

VARIABLES ENTRANT DANS LE CALCUL DE LA PRIME DÉCENNALE :

  V1 — Valeur totale des travaux HT (DA)    : Base de calcul principale
  V2 — Nature de l'ouvrage                  : Résidentiel / Commercial / Industriel / Infrastructure
  V3 — Durée du chantier (mois)             : Impact sur l'exposition
  V4 — Qualifications de l'entreprise       : Agrément, certifications techniques
  V5 — Historique sinistres décennaux       : 5 dernières années
  V6 — Zone géographique                    : Zone sismique → majoration

---

# [RD::DECENNALE::FORMULES::PRIME]

> TYPE: formule_calcul
> CHUNK_ID: RD-DEC-FORMULE-PRIME

BARÈME PAR NATURE D'OUVRAGE 2026 :

  | Nature ouvrage                 | Taux sur valeur travaux HT | Prime min. |
  |---|---|---|
  | Résidentiel collectif (R+3+)   | 1,5% à 2,5%               | 80 000 DA  |
  | Résidentiel individuel         | 1,0% à 1,8%               | 40 000 DA  |
  | Commercial / Tertiaire         | 2,0% à 3,0%               | 100 000 DA |
  | Industriel / Entrepôt          | 2,5% à 4,0%               | 150 000 DA |
  | Infrastructure (voirie, VRD)   | 1,5% à 2,5%               | 80 000 DA  |
  | Réhabilitation / Rénovation    | 1,8% à 3,0%               | 60 000 DA  |

  MAJORATION ZONE SISMIQUE (Algérie — zones I à III) :
    Zone I (faible)   → +0%
    Zone II (modérée) → +15%
    Zone III (forte)  → +30%

FORMULE PRIME NETTE DÉCENNALE :
  ```
  Prime_Nette_DEC = MAX(Valeur_Travaux_HT × Taux_Nature ; Prime_Minimum)
                  × Coefficient_Zone_Sismique
  ```

  Exemple (immeuble R+5 résidentiel, travaux 50 000 000 DA, zone II) :
    Prime_Nette = MAX(50 000 000 × 2,0% ; 80 000) × 1,15
               = 1 000 000 × 1,15
               = 1 150 000 DA

FORMULE TTC DÉCENNALE :
  ```
  Prime_TTC_DEC = Prime_Nette_DEC × (1 + 0,19 + 0,01)
                = Prime_Nette_DEC × 1,20
  ```
  Exemple : 1 150 000 × 1,20 = 1 380 000 DA TTC

---

# ══════════════════════════════════════════════════════════════════
# SECTION V — TOUS RISQUES CHANTIER (TRC)
# ══════════════════════════════════════════════════════════════════

---

# [RD::TRC::DEFINITION]

> TYPE: description_produit
> CHUNK_ID: RD-TRC-DEFINITION
> LOI: DECRET_95-414, ORDONNANCE_95-07

NOM : Tous Risques Chantier (TRC)
STATUT LÉGAL : Obligatoire pour grands chantiers (Décret 95-414)
OBJET : Couvre les dommages matériels accidentels aux ouvrages en cours de construction.
DURÉE : Durée du chantier + période de garantie de bon fonctionnement (12 mois standard)

DISTINCTION DÉCENNALE / TRC :
  TRC       → Dommages PENDANT la construction (chantier en cours)
  DÉCENNALE → Dommages APRÈS réception (10 ans post-livraison)
  Ces deux garanties sont COMPLÉMENTAIRES et souvent souscrites ensemble.

GARANTIES INCLUSES TRC :
  ✅ Dommages aux ouvrages en construction (intempéries, erreurs d'exécution)
  ✅ Dommages aux matériaux et équipements sur chantier
  ✅ Effondrement partiel pendant les travaux
  ✅ Actes de vandalisme sur chantier
  ✅ Dommages aux existants (biens du maître d'ouvrage adjacents au chantier)
  ✅ RC chantier — dommages causés aux tiers riverains

GARANTIES OPTIONNELLES TRC :
  ⭕ Bris de machines et engins de chantier
  ⭕ Dommages aux installations de chantier (baraquements, grues)
  ⭕ Pertes indirectes (pénalités de retard)

---

# [RD::TRC::VARIABLES::TARIFICATION]

> TYPE: variables_calcul
> CHUNK_ID: RD-TRC-VARIABLES

VARIABLES ENTRANT DANS LE CALCUL DE LA PRIME TRC :

  V1 — Valeur totale du marché TTC (DA)     : Base de calcul principale
  V2 — Nature des travaux                   : Génie civil / Bâtiment / Infrastructures
  V3 — Durée du chantier (mois)             : Facteur d'exposition temporelle
  V4 — Présence d'engins lourds             : Grues, pelleteuses → majoration
  V5 — Zone géographique                    : Risque sismique, inondation
  V6 — Valeur des existants à protéger (DA) : Biens du maître d'ouvrage adjacents
  V7 — Qualifications entrepreneur          : Agrément, références chantiers similaires

---

# [RD::TRC::FORMULES::PRIME]

> TYPE: formule_calcul
> CHUNK_ID: RD-TRC-FORMULE-PRIME

BARÈME PAR NATURE DE TRAVAUX 2026 :

  | Nature travaux                  | Taux sur valeur marché | Prime min.  |
  |---|---|---|
  | Bâtiment résidentiel            | 0,8% à 1,5%           | 60 000 DA   |
  | Bâtiment commercial / tertiaire | 1,0% à 1,8%           | 80 000 DA   |
  | Génie civil / Infrastructure    | 1,2% à 2,5%           | 120 000 DA  |
  | Travaux de réhabilitation       | 1,0% à 2,0%           | 70 000 DA   |
  | Ouvrages hydrauliques / barrages| 2,0% à 3,5%           | 200 000 DA  |

  COEFFICIENT DURÉE CHANTIER :
    Durée ≤ 6 mois   → Coefficient 0,80 (chantier court)
    Durée 6-12 mois  → Coefficient 1,00 (base)
    Durée 12-24 mois → Coefficient 1,20
    Durée > 24 mois  → Coefficient 1,40

  MAJORATION ENGINS LOURDS :
    Présence grues / excavateurs → +10% sur prime nette

FORMULE PRIME NETTE TRC :
  ```
  Prime_Nette_TRC = MAX(Valeur_Marché × Taux_Nature ; Prime_Minimum)
                  × Coeff_Durée
                  × Coeff_Engins
  ```

  Exemple (bâtiment R+4 commercial, marché 80 000 000 DA, 18 mois, sans engins lourds) :
    Prime_Nette = MAX(80 000 000 × 1,3% ; 80 000) × 1,20 × 1,00
               = 1 040 000 × 1,20
               = 1 248 000 DA

FORMULE TTC TRC :
  ```
  Prime_TTC_TRC = Prime_Nette_TRC × (1 + 0,19 + 0,01)
                = Prime_Nette_TRC × 1,20
  ```
  Exemple : 1 248 000 × 1,20 = 1 497 600 DA TTC

---

# ══════════════════════════════════════════════════════════════════
# SECTION VI — INCENDIE & RISQUES ENTREPRISE
# ══════════════════════════════════════════════════════════════════

---

# [RD::INCENDIE::DEFINITION]

> TYPE: description_produit
> CHUNK_ID: RD-INC-DEFINITION
> LOI: DECRET_95-415

NOM : Assurance Incendie & Risques Entreprise
STATUT LÉGAL : Obligatoire — Décret 95-415
OBJET : Protection des biens professionnels contre les dommages matériels.

GARANTIES DE BASE :
  ✅ Incendie, Explosion, Foudre          → Bâtiment + Contenu professionnel
  ✅ CAT-NAT                              → Obligatoire Loi 03-12
  ✅ Dégâts des Eaux                      → Dommages aux biens et équipements

GARANTIES OPTIONNELLES :
  ⭕ Vol & Vandalisme                     → Stocks, matériel, caisse
  ⭕ Bris de Machines                     → Pannes accidentelles équipements industriels
  ⭕ Dommages Électriques                → Surtensions matériel professionnel
  ⭕ Pertes d'Exploitation               → Compensation perte de marge post-sinistre
  ⭕ Marchandises Transportées           → En transit depuis/vers l'entreprise
  ⭕ RC Exploitation                     → Dommages causés aux tiers dans l'exercice

NOTE PERTES D'EXPLOITATION :
  Complément INDISPENSABLE des dommages aux biens.
  Sans cette garantie, l'entreprise supporte seule la perte de revenus
  pendant la reconstruction ou réparation.
  Base de calcul : Marge Brute annuelle × Période d'indemnisation (mois).

---

# [RD::INCENDIE::VARIABLES::TARIFICATION]

> TYPE: variables_calcul
> CHUNK_ID: RD-INC-VARIABLES

VARIABLES ENTRANT DANS LE CALCUL DE LA PRIME INCENDIE ENTREPRISE :

  V1 — Valeur bâtiment professionnel (DA)   : Capital construction
  V2 — Valeur contenu / équipements (DA)    : Matériel, mobilier, outils
  V3 — Valeur stocks (DA)                   : Matières premières + produits finis
  V4 — Activité / Secteur                   : Détermine le taux de risque incendie
  V5 — Construction du bâtiment             : Béton / Métal / Bois → impact taux
  V6 — Systèmes de protection               : Sprinklers, alarme → réduction prime
  V7 — Marge brute annuelle (DA)            : Base calcul pertes d'exploitation
  V8 — Période max indemnisation PE (mois)  : 6 / 12 / 24 mois

---

# [RD::INCENDIE::FORMULES::PRIME]

> TYPE: formule_calcul
> CHUNK_ID: RD-INC-FORMULE-PRIME

BARÈME PAR ACTIVITÉ 2026 :

  | Activité                         | Taux bâtiment + contenu | Taux stocks  |
  |---|---|---|
  | Commerce / Négoce                | 1,0‰ à 2,0‰            | 1,5‰ à 2,5‰  |
  | Industrie légère (agroalim, tex) | 1,5‰ à 2,5‰            | 2,0‰ à 3,0‰  |
  | Industrie lourde (métal, chimie) | 2,0‰ à 4,0‰            | 2,5‰ à 4,0‰  |
  | Entrepôt / Logistique            | 1,5‰ à 3,0‰            | 2,0‰ à 3,5‰  |
  | Bureaux / Services               | 0,5‰ à 1,0‰            | 0,5‰ à 1,0‰  |
  | Hôtellerie / Restauration        | 1,5‰ à 2,5‰            | 1,0‰ à 2,0‰  |

  RÉDUCTION SYSTÈMES DE PROTECTION :
    Alarme incendie certifiée   → -10% sur prime nette
    Sprinklers installés        → -20% sur prime nette
    Les deux                    → -25% sur prime nette

FORMULE PRIME NETTE INCENDIE ENTREPRISE :
  ```
  Prime_Nette_INC = (Capital_Bâtiment × Taux_Bâtiment)
                  + (Capital_Contenu × Taux_Contenu)
                  + (Capital_Stocks × Taux_Stocks)
                  + Prime_PE (si garantie pertes exploitation souscrite)
                  × (1 - Réduction_Protection)
  ```

  FORMULE PERTES D'EXPLOITATION :
  ```
  Prime_PE = Marge_Brute_Annuelle × Taux_PE × (Période_Indemnisation_mois / 12)

  Taux_PE standard : 1,5‰ à 3,0‰ selon activité
  ```

  Exemple (entrepôt logistique) :
    Bâtiment  : 30 000 000 DA × 2,0‰  =  60 000 DA
    Contenu   : 10 000 000 DA × 2,0‰  =  20 000 DA
    Stocks    : 20 000 000 DA × 2,5‰  =  50 000 DA
    PE 12 mois: 15 000 000 DA × 2,0‰  =  30 000 DA
    Alarme    : -10%
    ──────────────────────────────────────────────
    Sous-total: 160 000 DA × 0,90     = 144 000 DA

FORMULE TTC INCENDIE ENTREPRISE :
  ```
  Prime_TTC_INC = Prime_Nette_INC × (1 + 0,19 + 0,02 + 0,01)
                = Prime_Nette_INC × 1,22
  ```
  Exemple : 144 000 × 1,22 = 175 680 DA TTC/an

---

# ══════════════════════════════════════════════════════════════════
# SECTION VII — TRANSPORT DE MARCHANDISES
# ══════════════════════════════════════════════════════════════════

---

# [RD::TRANSPORT::DEFINITION]

> TYPE: description_produit
> CHUNK_ID: RD-TMD-DEFINITION

NOM : Assurance Transport de Marchandises (Facultés)
OBJET : Couvre les marchandises transportées contre les dommages ou pertes en transit.

FORMULES DISPONIBLES :
  - Tous Risques      → Couverture maximale — tous dommages accidentels
  - FAP Sauf          → Franc d'Avaries Particulières Sauf — sinistres majeurs uniquement
  - FAP Absolue       → Couverture minimale — perte totale uniquement

TYPES DE TRANSPORT COUVERTS :
  ✅ Transport terrestre (camion, train)
  ✅ Transport maritime (importations/exportations)
  ✅ Transport aérien (fret)
  ✅ Transport multimodal

GARANTIES OPTIONNELLES :
  ⭕ Risques de Guerre et Assimilés (RGA)   → Rachat exclusion terrorisme/sabotage
  ⭕ Avaries particulières                 → Dommages partiels marchandise
  ⭕ Retard de livraison                   → Pertes financières consécutives

---

# [RD::TRANSPORT::FORMULES::PRIME]

> TYPE: formule_calcul
> CHUNK_ID: RD-TMD-FORMULE-PRIME

VARIABLES PRINCIPALES :
  V1 — Valeur des marchandises (DA ou devise)
  V2 — Type de marchandise (alimentaire / industrielle / périssable / dangereuse)
  V3 — Mode de transport (terrestre / maritime / aérien)
  V4 — Destination / Origine (national / international)
  V5 — Fréquence expéditions (polices au voyage ou contrat annuel)

BARÈME PAR MODE ET FORMULE 2026 :

  | Mode          | Formule        | Taux sur valeur marchandise |
  |---|---|---|
  | Terrestre DZ  | Tous Risques   | 0,5‰ à 1,0‰ par voyage      |
  | Terrestre DZ  | FAP Sauf       | 0,2‰ à 0,5‰ par voyage      |
  | Maritime      | Tous Risques   | 1,0‰ à 2,5‰ par voyage      |
  | Maritime      | FAP Sauf       | 0,5‰ à 1,0‰ par voyage      |
  | Aérien        | Tous Risques   | 0,3‰ à 0,8‰ par voyage      |
  | RGA (option)  | Tous modes     | +0,05‰ à +0,15‰             |

FORMULE PRIME NETTE TRANSPORT (police au voyage) :
  ```
  Prime_Nette_TMD = Valeur_Marchandise × Taux_Mode_Formule
                  + Option_RGA (si souscrite)
  ```

  Exemple (conteneur maritime 5 000 000 DA, Tous Risques, avec RGA) :
    Prime = 5 000 000 × 1,5‰ + 5 000 000 × 0,10‰
          = 7 500 + 500
          = 8 000 DA par voyage

CONTRAT ANNUEL (abonnement) :
  ```
  Prime_Annuelle_TMD = CA_Expéditions_Annuel × Taux_Moyen_Pondéré × 0,85
  ```
  (Coefficient 0,85 = remise contrat annuel vs polices au voyage)

FORMULE TTC TRANSPORT :
  ```
  Prime_TTC_TMD = Prime_Nette_TMD × (1 + 0,19 + 0,015)
                = Prime_Nette_TMD × 1,205
  ```

---

# ══════════════════════════════════════════════════════════════════
# SECTION VIII — SYNTHÈSE TAXES PAR BRANCHE
# ══════════════════════════════════════════════════════════════════

---

# [RD::TAXES::SYNTHESE]

> TYPE: parametre_systeme
> CHUNK_ID: RD-TAXES-SYNTHESE
> SOURCE: PARAMETRES_EXPERTS_ALERTE.md — PARAM-TARIF-001

RAPPEL TAUX FISCAUX RISQUES DIVERS 2026 :

| Branche                | TVA   | TCA  | Fonds CatNat | Total   | Multiplicateur TTC |
|---|---|---|---|---|---|
| MRH                    | 19%   | 2%   | 1%           | 22%     | × 1,22             |
| RC Professionnelle     | 19%   | 1%   | —            | 20%     | × 1,20             |
| Garantie Décennale     | 19%   | 1%   | —            | 20%     | × 1,20             |
| TRC                    | 19%   | 1%   | —            | 20%     | × 1,20             |
| Incendie Entreprise    | 19%   | 2%   | 1%           | 22%     | × 1,22             |
| Transport Marchandises | 19%   | 1,5% | —            | 20,5%   | × 1,205            |

BASE LÉGALE : PARAMETRES_EXPERTS_ALERTE.md — [PARAM-TARIF-001]
Loi de Finances 2026, art. 58 — Décret 17-191.

---

# ══════════════════════════════════════════════════════════════════
# SECTION IX — ALERTES & ANOMALIES RISQUES DIVERS
# ══════════════════════════════════════════════════════════════════

---

# [RD::ALERTES::CATALOGUE]

> TYPE: alertes_systeme
> CHUNK_ID: RD-ALERTES

| Code Alerte         | Niveau   | Déclencheur | Action |
|---|---|---|---|
| `[ALERTE-RD-001]`   | HAUTE    | Capital MRH déclaré < 50% valeur reconstruction estimée | Signaler sous-assurance — demander justificatif |
| `[ALERTE-RD-002]`   | CRITIQUE | RC Pro souscrite sans vérification activité réglementée | Contrôler agrément professionnel obligatoire |
| `[ALERTE-RD-003]`   | HAUTE    | Décennale souscrite < 10 ans après réception ouvrage | Vérifier date réception — attestation maître d'ouvrage |
| `[ALERTE-RD-004]`   | HAUTE    | TRC souscrit après démarrage chantier (rétroactif) | Refus ou majoration 30% — sinistres antérieurs exclus |
| `[ALERTE-RD-005]`   | CRITIQUE | Incendie entreprise sans CAT-NAT intégré | Ajout obligatoire CAT-NAT — Décret 03-12 |
| `[ALERTE-RD-006]`   | MOYENNE  | Stocks déclarés inférieurs à stocks réels connus | Risque sous-assurance stocks — règle proportionnelle |
| `[ALERTE-RD-007]`   | HAUTE    | Transport maritime sans RGA pour destinations à risque | Recommander option RGA si zone conflictuelle |
| `[ANO-RD-001]`      | CRITIQUE | Prime calculée < Prime minimum réglementaire | Blocage émission — corriger avant validation |
| `[ANO-RD-002]`      | HAUTE    | Taux TTC appliqué incorrect par branche | Vérifier table RD-TAXES-SYNTHESE |

---

## Liens Connexes

- [Module Devis](./Module_Devis.md)
- [Référentiel Garanties](./referentiel_garanties.md)
- [Paramètres Experts & Alertes](./PARAMETRES_EXPERTS_ALERTE.md)
- [Référentiel Technique](./referentiel_technique_assurance.md)
- [Registre Souverain Master](./REGISTRE_SOUVERAIN_MASTER.md)

================================================================================
# FIN MODULE RISQUES DIVERS — v1.0 — STANDARD_DZ — 2026-05-12
================================================================================


---

# PARTIE C — Référentiel Technique

---
fichier: referentiel_technique_assurance.md
domaine: Assurances Algériennes
lois: [Ordonnance 95-07, Loi 88-31, Ordonnance 03-12, Décret 95-413]
version: 1.2
statut: PRODUCTION
enrichi_depuis: DMP Assur (TARIF_AUTO, TAXE, COMMISSION, FRAIS_GESTION, BONUS_MALUS) + 50 contrats + SAA (Mai 2026)
---

# RÉFÉRENTIEL TECHNIQUE DES SEUILS D'ALERTE & LOGIQUES DE CONTRÔLE
## Assur — Ingénierie Risques & Audit
### v1.1 — Mars 2026 | Confidentiel — Usage Interne

---

> **PRÉAMBULE**
> Ce référentiel définit les règles de gestion, seuils d'alerte et logiques de contrôle applicables aux 8 modules de la plateforme Assur. Les tags `[ALERTE-XXX]` sont formatés pour être reconnus nativement par le moteur Système Expert. Toute règle déclenchant une alerte doit générer un ticket dans le système de workflow.

---

## TABLE DES MATIÈRES

1. [Référentiel Tarification "Marché" — Modules 1 & 3](#module-1-3)
2. [Logique Anti-Fraude & Agence — Module 3](#module-3-fraude)
3. [Protocole Croisement Inter-Compagnies — Module 4](#module-4)
4. [Référentiel Audit Comptable DC/DMP — Module 6](#module-6)
5. [Indicateurs de Performance DG — Module 8](#module-8)
6. [Annexes & Paramétrage Système Expert](#annexes)

---

<a name="module-1-3"></a>
## SECTION 1 — RÉFÉRENTIEL TARIFICATION "MARCHÉ"
### Modules 1 (Émission) & 3 (Contrôle Qualité Portefeuille)

---

### 1.1 Grille des Primes de Référence — Moyenne Algérie 2026

> **Base légale** : Ordonnance 95-07 | Décrets 17-191 & 17-192
> **Mise à jour** : Annuelle — Sourçage L'Autorité de Régulation + relevés portefeuilles agences

#### 1.1.1 Assurance Automobile

| Catégorie | Puissance | Usage | Prime RC Nette (DA) | Prime Tous Risques Nette (DA) | Prime Totale Référence HT |
|---|---|---|---|---|---|
| Tourisme — 4CV | ≤ 4 CV | Personnel | 10 000 | 16 000 | **26 000** |
| **Tourisme — 6CV** | **5–6 CV** | **Personnel** | **14 000** | **20 000** | **34 000** |
| Tourisme — 7CV | 7 CV | Personnel | 18 000 | 24 000 | **42 000** |
| Tourisme — 8CV+ | ≥ 8 CV | Personnel | 22 000 | 30 000 | **52 000** |
| **Utilitaire léger** | **≤ 3,5T** | **Commercial** | **28 000** | **35 000** | **63 000** |

---
### 1.1.A Taux Réels Extrait du DMP (TARIF_AUTO — MONTFIXE RC)

> SOURCE: Base Assur — Table TARIF_AUTO — 10 lignes extraites
> CHUNK_ID: TECH-11A_TAUX_RÉELS_EXTRAIT_DU_DMP_
