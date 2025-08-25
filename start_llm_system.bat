@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo Philosophy Concept Explorer System
echo ========================================
echo.

echo Checking port availability...
netstat -an | findstr ":8000" >nul
if %errorlevel% equ 0 (
    echo Port 8000 is already in use. Stopping existing service...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000"') do (
        taskkill /f /pid %%a >nul 2>&1
    )
    timeout /t 2 /nobreak >nul
)

netstat -an | findstr ":8080" >nul
if %errorlevel% equ 0 (
    echo Port 8080 is already in use. Stopping existing service...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8080"') do (
        taskkill /f /pid %%a >nul 2>&1
    )
    timeout /t 2 /nobreak >nul
)

netstat -an | findstr ":3000" >nul
if %errorlevel% equ 0 (
    echo Port 3000 is already in use. Stopping existing service...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":3000"') do (
        taskkill /f /pid %%a >nul 2>&1
    )
    timeout /t 2 /nobreak >nul
)

echo Ports cleared successfully!
echo.

echo Checking dependencies...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python not found! Please install Python 3.8+
    pause
    exit /b 1
)

node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Node.js not found! Please install Node.js 16+
    pause
    exit /b 1
)

echo Dependencies check passed!
echo.

echo Checking model file...
echo Please ensure you have downloaded a GGUF model file
echo and updated the path in backend/config.py
echo.
echo Example model files:
echo - qwen-7b-chat-f16.gguf
echo - qwen-7b-chat-q4_0.gguf
echo - llama-2-7b-chat.gguf
echo.
pause

echo Checking LLaMA.cpp executable...
echo Please ensure LLaMA.cpp is compiled and the path is correct
echo You can update the path in this script or use environment variables
echo.
pause

echo Step 1: Starting LLaMA.cpp Server (CPU Mode)...
echo Please update the LLaMA.cpp path in this script before running
echo.
echo Example command:
echo cd YOUR_LLAMA_CPP_PATH
echo .\llama-server.exe -m YOUR_MODEL_FILE -c 2048 --host 0.0.0.0 --port 8080
echo.
pause

echo Step 2: Starting Backend Service...
start "Backend Server" cmd /k "cd /d %~dp0 && python run_backend.py"

echo Waiting for backend service to start...
set "backend_started=false"
for /l %%i in (1,1,20) do (
    netstat -an | findstr ":8000" >nul
    if !errorlevel! equ 0 (
        echo Backend service started successfully!
        set "backend_started=true"
        goto :backend_ready
    )
    echo Waiting... %%i/20
    timeout /t 1 /nobreak >nul
)

:backend_ready
if "%backend_started%"=="false" (
    echo Warning: Backend service may not be fully ready
    echo Continuing anyway...
)
echo.

echo Step 3: Starting Frontend Service...
start "Frontend Server" cmd /k "cd /d %~dp0\frontend && npm start"

echo Waiting for frontend service to start...
set "frontend_started=false"
for /l %%i in (1,1,25) do (
    netstat -an | findstr ":3000" >nul
    if !errorlevel! equ 0 (
        echo Frontend service started successfully!
        set "frontend_started=true"
        goto :frontend_ready
    )
    echo Waiting... %%i/25
    timeout /t 1 /nobreak >nul
)

:frontend_ready
if "%frontend_started%"=="false" (
    echo Warning: Frontend service may not be fully ready
    echo Continuing anyway...
)
echo.

echo Final status check...
echo.
echo ========================================
echo All services have been started!
echo ========================================
echo.

echo Service URLs:
echo - Frontend: http://localhost:3000
echo - Backend: http://localhost:8000
echo - LLaMA.cpp: http://localhost:8080 (if started manually)
echo.

echo Service Status:
echo - LLaMA.cpp: MANUAL START REQUIRED
if "%backend_started%"=="true" (
    echo - Backend: RUNNING
) else (
    echo - Backend: UNKNOWN
)

if "%frontend_started%"=="true" (
    echo - Frontend: RUNNING
) else (
    echo - Frontend: UNKNOWN
)

echo.
echo Note: LLaMA.cpp server needs to be started manually
echo Please update the paths in this script or use environment variables
echo.
echo Press any key to exit this script...
pause >nul
