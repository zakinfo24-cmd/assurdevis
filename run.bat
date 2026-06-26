@echo off
title AssurDevis AI — Mode Complet
cd /d "%~dp0"
setlocal
set OLLAMA_MODELS=%~dp0ollama_models
echo =======================================
echo   AssurDevis AI v2.0 — Mode Complet
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

REM --- Installer les dependances si besoin ---
%PYTHON% -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo [INSTALL] Dependances Python...
    %PYTHON% -m pip install fastapi uvicorn httpx PyMuPDF python-multipart --quiet 2>nul
)

REM --- Verifier / lancer Ollama ---
echo [CHECK] Ollama...
where ollama >nul 2>&1
set OLLAMA_OK=%errorlevel%
if %OLLAMA_OK% neq 0 (
    if exist "ollama\ollama.exe" set OLLAMA_OK=0
)

if %OLLAMA_OK% equ 0 (
    tasklist /fi "imagename eq ollama.exe" 2>nul | find /i "ollama.exe" >nul
    if errorlevel 1 (
        echo [LANCEMENT] Ollama...
        if exist "ollama\ollama.exe" (
            start "" /B "ollama\ollama.exe" serve
        ) else (
            start "" /B ollama serve
        )
        timeout /t 3 /nobreak >nul
    ) else (
        echo [OK] Ollama deja lance.
    )
    if exist "ollama_models\blobs\" (
        echo [RESTAURATION] Modele gemma3:4b depuis cle USB...
        if not exist "%USERPROFILE%\.ollama\models\blobs" mkdir "%USERPROFILE%\.ollama\models\blobs"
        if not exist "%USERPROFILE%\.ollama\models\manifests" mkdir "%USERPROFILE%\.ollama\models\manifests"
        xcopy /E /Y "ollama_models\blobs\*" "%USERPROFILE%\.ollama\models\blobs\" >nul
        xcopy /E /Y "ollama_models\manifests\*" "%USERPROFILE%\.ollama\models\manifests\" >nul
    )
) else (
    echo [MODE DEGRADE] Ollama introuvable. Devis uniquement.
)

REM --- Lancer le serveur ---
echo.
echo [LANCEMENT] Serveur AssurDevis sur http://localhost:5000
echo [INFO] Ouvrez http://localhost:5000 dans votre navigateur
echo.
start "" http://localhost:5000
%PYTHON% -m uvicorn app.main:app --host 0.0.0.0 --port 5000
pause
