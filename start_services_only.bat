@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo Quick Start - Services Only (CPU Mode)
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

echo Starting LLaMA.cpp Server in CPU mode...
echo Please update the LLaMA.cpp path in this script before running
echo.
echo Example command:
echo cd YOUR_LLAMA_CPP_PATH
echo .\llama-server.exe -m YOUR_MODEL_FILE -c 2048 --host 0.0.0.0 --port 8080
echo.
pause

echo Waiting for LLaMA.cpp server to start...
set "llama_started=false"
for /l %%i in (1,1,25) do (
    netstat -an | findstr ":8080" >nul
    if !errorlevel! equ 0 (
        echo LLaMA.cpp server started successfully!
        set "llama_started=true"
        goto :llama_ready
    )
    echo Waiting... %%i/25
    timeout /t 1 /nobreak >nul
)

:llama_ready
if "%llama_started%"=="false" (
    echo Warning: LLaMA.cpp server may not be fully ready
    echo Continuing anyway...
)
echo.

echo Starting Backend Service...
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

echo Starting Frontend Service...
start "Frontend Server" cmd /k "cd /d %~dp0\frontend && npm start"

echo Waiting for frontend service to start...
set "frontend_started=false"
for /l %%i in (1,1,20) do (
    netstat -an | findstr ":3000" >nul
    if !errorlevel! equ 0 (
        echo Frontend service started successfully!
        set "frontend_started=true"
        goto :frontend_ready
    )
    echo Waiting... %%i/20
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
echo All services started!
echo ========================================
echo.

echo Service URLs:
echo - Frontend: http://localhost:3000
echo - Backend: http://localhost:8000
echo - LLaMA.cpp: http://localhost:8080 (if started manually)
echo.

echo Service Status:
if "%llama_started%"=="true" (
    echo - LLaMA.cpp: RUNNING
) else (
    echo - LLaMA.cpp: MANUAL START REQUIRED
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
echo Note: LLaMA.cpp server needs to be started manually
echo Please update the paths in this script or use environment variables
echo Press any key to exit...
pause >nul
