@echo off
echo ========================================
echo   Stopping FarmWise Servers...
echo ========================================
echo.

REM Kill processes on port 8001 (Backend API)
echo [1/6] Stopping Backend API (Port 8001)...
powershell -Command "$conn = Get-NetTCPConnection -LocalPort 8001 -ErrorAction SilentlyContinue; if($conn) { $conn | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue } }"
timeout /t 1 /nobreak >nul

REM Kill processes on port 8002 (Disease Detection)
echo [2/6] Stopping Disease Detection Service (Port 8002)...
powershell -Command "$conn = Get-NetTCPConnection -LocalPort 8002 -ErrorAction SilentlyContinue; if($conn) { $conn | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue } }"
timeout /t 1 /nobreak >nul

REM Kill processes on port 3000 (Frontend)
echo [3/6] Stopping Frontend (Port 3000)...
powershell -Command "$conn = Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue; if($conn) { $conn | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue } }"
timeout /t 1 /nobreak >nul

REM Kill processes on port 3001 (Frontend alternate)
echo [4/6] Stopping Frontend (Port 3001 if used)...
powershell -Command "$conn = Get-NetTCPConnection -LocalPort 3001 -ErrorAction SilentlyContinue; if($conn) { $conn | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue } }"
timeout /t 1 /nobreak >nul

REM Kill any remaining node processes (for frontend)
echo [5/6] Cleaning up Node.js processes...
taskkill /F /IM node.exe >nul 2>&1
timeout /t 1 /nobreak >nul

REM Kill any remaining python API server processes
echo [6/6] Cleaning up Python API processes...
powershell -Command "Get-Process python -ErrorAction SilentlyContinue | Where-Object {$_.CommandLine -like '*api_server_mongodb*' -or $_.CommandLine -like '*disease_detection_service*'} | Stop-Process -Force -ErrorAction SilentlyContinue"
timeout /t 1 /nobreak >nul

echo.
echo ========================================
echo   All servers stopped successfully!
echo ========================================
echo.
echo You can now run START_PROJECT.bat again
echo.
pause
