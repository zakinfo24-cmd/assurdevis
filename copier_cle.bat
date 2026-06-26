@echo off
title Copie AssurDevis vers clé USB
echo ===========================================
echo   Copie AssurDevis AI vers clé USB
echo ===========================================
echo.
echo Lecteurs disponibles :
echo.
wmic logicaldisk where drivetype=2 get DeviceID,VolumeName,Size 2>nul
echo.
set /p DEST="Entrez la lettre du lecteur USB (ex: E:) : "
if "%DEST%"=="" exit /b

set SRC=%~dp0
echo.
echo Copie de "%SRC%" vers "%DEST%\AssurDevis\" ...
xcopy "%SRC%" "%DEST%\AssurDevis\" /E /I /H /Y
echo.
echo [OK] Copie terminée vers %DEST%\AssurDevis\
echo.
echo Pour lancer :
echo   %DEST%\AssurDevis\run.bat      (mode complet)
echo   %DEST%\AssurDevis\run_lite.bat (mode devis seul)
echo.
pause
