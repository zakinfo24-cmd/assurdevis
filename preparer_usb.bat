@echo off
title Préparation clé USB AssurDevis
cd /d "%~dp0"
echo ===========================================
echo   Préparation clé USB AssurDevis AI
echo ===========================================
echo.

REM ─── 1. Python embeddable ─────────────────
echo [1/5] Téléchargement Python embeddable...
curl -L -o python_embed.zip "https://www.python.org/ftp/python/3.12.9/python-3.12.9-embed-amd64.zip"
if exist python_embed.zip (
    echo [OK] Python téléchargé.
    move /Y python_embed.zip python_portable\ >nul 2>&1
) else (
    echo [WARN] Échec téléchargement Python. Téléchargez manuellement depuis python.org
    echo        → python-3.12.9-embed-amd64.zip → coller dans portable\python_portable\
)

REM ─── 2. Packages Python ────────────────────
echo [2/5] Installation des dépendances...
python -m pip install fastapi uvicorn httpx -t python_portable\site-packages 2>nul
echo [OK] Dépendances installées.

REM ─── 3. Ollama ─────────────────────────────
echo [3/5] Téléchargement Ollama...
curl -L -o ollama_setup.exe "https://ollama.com/download/OllamaSetup.exe"
if exist ollama_setup.exe (
    echo [OK] Ollama téléchargé (ollama_setup.exe).
    move /Y ollama_setup.exe ollama_models\ >nul 2>&1
) else (
    echo [WARN] Échec téléchargement Ollama. Téléchargez depuis ollama.com/download
)

REM ─── 4. Modèle ─────────────────────────────
echo [4/5] Téléchargement du modèle qwen2.5:7b...
echo      (Cette étape peut prendre 5-10 minutes selon votre connexion)
ollama pull qwen2.5:7b
if %errorlevel% equ 0 (
    echo [OK] Modèle téléchargé.
    REM Copier le modèle dans le dossier portable
    mkdir "%USERPROFILE%\.ollama\models" 2>nul
    xcopy "%USERPROFILE%\.ollama\models\*" "ollama_models\" /E /I /Y 2>nul
) else (
    echo [WARN] Ollama pas encore installé. Installez puis : ollama pull qwen2.5:7b
)

REM ─── 5. Référence contrat ────────────────────
echo [5/5] Préparation dossier contrat type...
echo.
echo ⚠ Placez votre contrat type de la compagnie au format PDF uniquement :
echo   portable\reference_contrat.pdf
echo.
echo Ce fichier servira de référence pour le module Scan & Analyse.

echo.
echo ──────── RÉSUMÉ ────────
dir /B /S portable\ 2>nul
echo.
echo Copiez tout le dossier portable\ sur la clé USB.
echo Sur le PC de démo :
echo   run_lite.bat  → mode devis uniquement
echo   run.bat       → mode complet
echo.
echo 📄 NOUVEAU : Scanner un contrat → cliquez sur 📄 dans la barre de saisie
echo.
pause
