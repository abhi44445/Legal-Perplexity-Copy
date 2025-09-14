@echo off
title Legal Perplexity - Quick Start

REM Quick start without dependency checks
echo Starting Legal Perplexity 2.0...
echo.

REM Start backend
echo Starting Backend...
start "Backend - FastAPI" cmd /k "cd /d "%~dp0" && .venv\Scripts\activate.bat && uvicorn main:app --reload --host 0.0.0.0 --port 8000"

REM Wait a moment
timeout /t 2 /nobreak >nul

REM Start frontend
echo Starting Frontend...
start "Frontend - React" cmd /k "cd /d "%~dp0frontend" && npm run dev"

echo.
echo ✅ Both servers are starting...
echo 🌐 Backend: http://localhost:8000
echo 🎨 Frontend: http://localhost:5173
echo 📚 API Docs: http://localhost:8000/docs
echo.
echo Close this window when done.
pause