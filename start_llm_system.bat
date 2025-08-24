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
if not exist "C:\Users\cyq12\llama.cpp\qwen-7b-chat-f16.gguf" (
    echo Error: Model file not found!
    echo Please download qwen-7b-chat-f16.gguf to C:\Users\cyq12\llama.cpp\
    pause
    exit /b 1
)
echo Model file found!
echo.

echo Checking LLaMA.cpp executable...
if not exist "C:\Users\cyq12\llama.cpp\build\bin\Release\llama-server.exe" (
    echo Error: LLaMA.cpp not compiled!
    echo Please compile LLaMA.cpp first
    pause
    exit /b 1
)
echo LLaMA.cpp executable found!
echo.

echo Step 1: Starting LLaMA.cpp Server (CPU Mode)...
start "LLaMA.cpp Server" cmd /k "cd /d C:\Users\cyq12\llama.cpp\build\bin\Release && llama-server.exe -m ..\..\..\qwen-7b-chat-f16.gguf -c 2048 --host 0.0.0.0 --port 8080"

echo Waiting for LLaMA.cpp server to start...
set "llama_started=false"
for /l %%i in (1,1,30) do (
    netstat -an | findstr ":8080" >nul
    if !errorlevel! equ 0 (
        echo LLaMA.cpp server started successfully!
        set "llama_started=true"
        goto :llama_ready
    )
    echo Waiting... %%i/30
    timeout /t 1 /nobreak >nul
)

:llama_ready
if "%llama_started%"=="false" (
    echo Warning: LLaMA.cpp server may not be fully ready
    echo Continuing anyway...
)
echo.

echo Step 2: Starting Backend Service...
start "Backend Server" cmd /k "cd /d c:\project\test_2 && python run_backend.py"

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
start "Frontend Server" cmd /k "cd /d c:\project\test_2\frontend && npm start"

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
echo - LLaMA.cpp: http://localhost:8080
echo.

echo Service Status:
if "%llama_started%"=="true" (
    echo - LLaMA.cpp: RUNNING
) else (
    echo - LLaMA.cpp: UNKNOWN
)

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
echo Note: Running in CPU mode for stability
echo Please wait for all services to fully start before using
echo.
echo Press any key to exit this script...
pause >nul
