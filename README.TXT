═══════════════════════════════════════════
  AssurDevis AI v2.0 — Kit Portable USB
═══════════════════════════════════════════

CONTENU :

  app/main.py         → Serveur FastAPI
  app/engine.py       → Moteur de calcul devis
  static/index.html   → Interface chat (frontend)
  instructions_sana.txt → Prompt système Sana
  knowledge/          → Base documentaire (RAG)
  ollama_models/      → Copier ici le modèle GGUF (optionnel)

  run.bat             → Lancement complet (Ollama + devis)
  run_lite.bat        → Lancement devis uniquement (sans IA)
  copier_cle.bat      → Copie le kit vers une clé USB

PRÉREQUIS :

  • Python 3.12+ installé sur le PC de démo
  • Pour le mode complet : Ollama + modèle qwen2.5:7b

LANCEMENT RAPIDE (mode devis uniquement, sans IA) :

  1. Insérez la clé USB
  2. Lancez run_lite.bat
  3. Le navigateur s'ouvre sur http://localhost:5000
  4. Tapez "devis auto" → suivez les questions

LANCEMENT COMPLET (avec IA conversationnelle) :

  1. Téléchargez Ollama depuis https://ollama.com
  2. Tirez le modèle : ollama pull qwen2.5:7b
     (ou copiez le .gguf dans ollama_models/)
  3. Lancez run.bat

STRUCTURE DU PORTEFEUILLE CLIENT :

  Pour un nouveau client :
  • Copier le dossier portable/
  • Renommer
  • Déployer sur le serveur dédié
  • Changer le port si nécessaire dans .env

Contact : AssurDevis — support@assurdevis.dz
