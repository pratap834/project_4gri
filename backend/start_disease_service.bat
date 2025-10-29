@echo off
echo ========================================
echo  Disease Detection Service Launcher
echo ========================================
echo.
echo Starting Disease Detection Service on Port 8002...
echo.

cd /d "%~dp0api"

REM Activate virtual environment if it exists
if exist "..\disease_env\Scripts\activate.bat" (
    echo Activating virtual environment...
    call ..\disease_env\Scripts\activate.bat
)

REM Start the disease detection service
python disease_detection_service.py

pause
