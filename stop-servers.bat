@echo off
title Legal Perplexity - Stop Servers

echo ============================================
echo   Legal Perplexity 2.0 - Stopping Servers
echo ============================================
echo.

REM Kill processes running on ports 8000 and 5173/5174
echo Stopping backend server (port 8000)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000') do (
    taskkill /f /pid %%a >nul 2>&1
)

echo Stopping frontend server (port 5173)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5173') do (
    taskkill /f /pid %%a >nul 2>&1
)

echo Stopping frontend server (port 5174)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5174') do (
    taskkill /f /pid %%a >nul 2>&1
)

REM Kill any node processes that might be related to Vite
echo Cleaning up Node.js processes...
taskkill /f /im node.exe >nul 2>&1

REM Kill any Python processes that might be related to uvicorn
echo Cleaning up Python processes...
wmic process where "commandline like '%%uvicorn%%main:app%%'" delete >nul 2>&1

echo.
echo ✅ Servers stopped successfully!
echo.
pause