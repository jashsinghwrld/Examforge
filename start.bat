@echo off
title RGPV Physics AI - Startup
color 0A

setlocal EnableExtensions EnableDelayedExpansion

:: Prefer a stable Python for compiled deps (pydantic-core wheels)
set "PY_CMD=python"
py -3.11 --version >nul 2>&1
if %errorlevel%==0 (
    set "PY_CMD=py -3.11"
)
py -3.12 --version >nul 2>&1
if %errorlevel%==0 (
    set "PY_CMD=py -3.12"
)

echo.
echo ============================================================
echo        RGPV Engineering Physics AI - Startup Script
echo ============================================================
echo.

:: Check Python
echo [1/5] Checking Python installation...
%PY_CMD% --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install from https://www.python.org/downloads
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)
%PY_CMD% --version
echo Python OK.
echo.

:: Check Node.js
echo [2/5] Checking Node.js installation...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js is not installed or not in PATH.
    echo Please install from https://nodejs.org
    pause
    exit /b 1
)
node --version
echo Node.js OK.
echo.

:: Check .env file
echo [3/5] Checking backend configuration...
if not exist "physics_backend\.env" (
    echo .env file not found. Creating from template...
    if exist "physics_backend\.env.example" (
        copy "physics_backend\.env.example" "physics_backend\.env" >nul
    ) else (
        echo ERROR: physics_backend\.env.example not found.
        echo Please create physics_backend\.env with at least GEMINI_API_KEY=...
        pause
        exit /b 1
    )
    echo.
    echo ============================================================
    echo  ACTION REQUIRED:
    echo  Open physics_backend\.env in Notepad and replace:
    echo  GEMINI_API_KEY=your_gemini_api_key_here
    echo  with your actual key from aistudio.google.com/app/apikey
    echo ============================================================
    echo.
    pause
)
echo Config OK.
echo.

:: Setup Backend
echo [4/5] Setting up backend...
cd physics_backend

if not exist "venv" (
    echo Creating virtual environment...
    %PY_CMD% -m venv venv
    echo Virtual environment created.
)

echo Installing backend dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt --quiet
echo Backend dependencies installed.
cd ..
echo.

:: Setup Frontend
echo [5/5] Setting up frontend...
cd physics_frontend

if not exist "node_modules" (
    echo Installing frontend dependencies, please wait...
    call npm install
    echo Frontend dependencies installed.
) else (
    echo Frontend dependencies already installed.
)

cd ..
echo.

:: Launch Both Servers
echo ============================================================
echo  All checks passed. Starting servers...
echo ============================================================
echo.
echo  Backend  - http://localhost:8000
echo  Frontend - http://localhost:5173
echo  API Docs - http://localhost:8000/docs
echo.
echo  Keep both server windows open while using the app.
echo ============================================================
echo.

:: Start backend in new window
start "RGPV Physics - Backend" cmd /k "cd /d %~dp0physics_backend && call venv\Scripts\activate.bat && uvicorn main:app --reload --port 8000"

:: Wait for backend to start
timeout /t 4 /nobreak >nul

:: Start frontend in new window
start "RGPV Physics - Frontend" cmd /k "cd /d %~dp0physics_frontend && npm run dev"

:: Wait then open browser
timeout /t 4 /nobreak >nul
start http://localhost:5173

echo.
echo Both servers are starting in separate windows.
echo Your browser will open automatically.
echo.
pause
