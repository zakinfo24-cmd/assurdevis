@echo off
title AssurDevis AI — Mode Devis (Lite)
cd /d "%~dp0"
echo ===========================================
echo   AssurDevis AI v2.0 — Mode Devis (Lite)
echo ===========================================
echo.
echo [INFO] Mode sans LLM. Devis auto + RD disponibles.
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

%PYTHON% -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo [INSTALL] Dependances Python...
    %PYTHON% -m pip install fastapi uvicorn httpx PyMuPDF --quiet 2>nul
)

echo [LANCEMENT] Serveur AssurDevis sur http://localhost:5000
echo [INFO] Ouvrez http://localhost:5000 dans votre navigateur
echo [INFO] Pas d'IA conversationnelle. Tapez "devis auto" pour estimer.
echo.
start "" http://localhost:5000
%PYTHON% -m uvicorn app.main:app --host 0.0.0.0 --port 5000
pause
