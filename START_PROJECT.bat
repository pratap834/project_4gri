@echo off
echo ========================================
echo   FarmWise Agricultural AI - Launcher
echo ========================================
echo.
cd /d "d:\cap\leaf-disease-proj\farmwise-agricultural-ai"

echo [1/3] Starting Backend API Server (Port 8001)...
start "FarmWise Backend API - Port 8001" powershell -NoExit -Command "cd 'd:\cap\leaf-disease-proj\farmwise-agricultural-ai\backend\api' ; Write-Host '========================================' -ForegroundColor Green ; Write-Host '  Backend API Server Starting...' -ForegroundColor Green ; Write-Host '  Port: 8001' -ForegroundColor Green ; Write-Host '========================================' -ForegroundColor Green ; Write-Host '' ; python api_server_mongodb.py"
timeout /t 6 /nobreak >nul

echo [2/3] Starting Disease Detection Service (Port 8002)...
start "FarmWise Disease Detection - Port 8002" powershell -NoExit -Command "cd 'd:\cap\leaf-disease-proj\farmwise-agricultural-ai\backend\api' ; Write-Host '========================================' -ForegroundColor Yellow ; Write-Host '  Disease Detection Service Starting...' -ForegroundColor Yellow ; Write-Host '  Port: 8002' -ForegroundColor Yellow ; Write-Host '========================================' -ForegroundColor Yellow ; Write-Host '' ; python disease_detection_service.py"
timeout /t 6 /nobreak >nul

echo [3/3] Starting Frontend Next.js Server (Port 3000)...
start "FarmWise Frontend - Port 3000" powershell -NoExit -Command "cd 'd:\cap\leaf-disease-proj\farmwise-agricultural-ai\frontend' ; Write-Host '========================================' -ForegroundColor Cyan ; Write-Host '  Frontend Server Starting...' -ForegroundColor Cyan ; Write-Host '  Port: 3000 (or 3001 if busy)' -ForegroundColor Cyan ; Write-Host '========================================' -ForegroundColor Cyan ; Write-Host '' ; npm run dev"
timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo   Servers Starting...
echo ========================================
echo.
echo Three PowerShell windows will open:
echo   1. GREEN  - Backend API (Port 8001)
echo   2. YELLOW - Disease Detection (Port 8002)
echo   3. CYAN   - Frontend App (Port 3000)
echo.
echo Backend API:       http://localhost:8001
echo Disease Detection: http://localhost:8002
echo Frontend:          http://localhost:3000
echo.
echo Waiting for servers to initialize...
timeout /t 10 /nobreak >nul

echo Opening browser...
start http://localhost:3000

echo.
echo ========================================
echo   Project is Running!
echo ========================================
echo.
echo To STOP servers: Close the PowerShell windows
echo                  or press Ctrl+C in each window
echo.
echo Press any key to close this launcher...
pause >nul
