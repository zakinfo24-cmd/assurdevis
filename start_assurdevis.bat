@echo off
title AssurDevis AI
cd /d "%~dp0"
setlocal enabledelayedexpansion
set OLLAMA_MODELS=%~dp0ollama_models
echo =======================================
echo   AssurDevis AI v2.0
echo =======================================
echo.

REM --- Detection Python ---
set PYTHON=python
where python >nul 2>&1
if errorlevel 1 (
    if exist "python_portable\python.exe" (
        set PYTHON=python_portable\python.exe
    ) else (
        echo [ERR] Python introuvable.
        echo Installez Python 3.12+ depuis python.org
        pause
        exit /b 1
    )
)
echo [OK] Python : %PYTHON%

REM --- Installer les dependances ---
%PYTHON% -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo [INSTALL] Dependances Python...
    %PYTHON% -m pip install fastapi uvicorn httpx PyMuPDF pytesseract Pillow python-dotenv --quiet 2>nul
)

REM --- Detecter Ollama ---
set OLLAMA_AVAIL=0
where ollama >nul 2>&1
if %errorlevel% equ 0 (
    set OLLAMA_AVAIL=1
) else (
    if exist "ollama\ollama.exe" set OLLAMA_AVAIL=1
)

REM --- Lancer Ollama si disponible ---
if %OLLAMA_AVAIL% equ 1 (
    tasklist /fi "imagename eq ollama.exe" 2>nul | find /i "ollama.exe" >nul
    if errorlevel 1 (
        echo [LANCEMENT] Ollama...
        if exist "ollama\ollama.exe" (
            start "" /B "ollama\ollama.exe" serve
        ) else (
            start "" /B ollama serve
        )
        timeout /t 3 /nobreak >nul
    )
    if exist "ollama_models\*.gguf" (
        echo [RESTAURATION] Modele depuis cle USB...
        if not exist "%USERPROFILE%\.ollama\models" mkdir "%USERPROFILE%\.ollama\models"
        copy /Y "ollama_models\*.gguf" "%USERPROFILE%\.ollama\models\" >nul 2>&1
    )
    echo [MODE] Complet (Ollama + IA conversationnelle)
) else (
    echo [MODE] Lite (devis uniquement, sans IA)
)

echo.
echo [LANCEMENT] Serveur sur http://localhost:5000
echo.
start "" http://localhost:5000
cd app
%PYTHON% -m uvicorn main:app --host 0.0.0.0 --port 5000
pause
