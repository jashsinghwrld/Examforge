@echo off
title RGPV Physics AI — Stop Servers
color 0C

echo.
echo ============================================================
echo        RGPV Physics AI — Stopping Servers
echo ============================================================
echo.

echo Stopping backend server (port 8000)...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8000"') do (
    taskkill /F /PID %%a >nul 2>&1
)
echo  Backend stopped.

echo Stopping frontend server (port 5173)...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":5173"') do (
    taskkill /F /PID %%a >nul 2>&1
)
echo  Frontend stopped.

echo.
echo  All servers stopped.
echo.
pause
