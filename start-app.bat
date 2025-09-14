@echo off
echo ============================================
echo    Legal Perplexity 2.0 - Starting App
echo ============================================
echo.

REM Check if we're in the correct directory
if not exist "main.py" (
    echo Error: main.py not found. Please run this script from the project root directory.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist ".venv\Scripts\activate.bat" (
    echo Error: Virtual environment not found. Please create a virtual environment first.
    echo Run: python -m venv .venv
    pause
    exit /b 1
)

REM Check if frontend directory exists
if not exist "frontend\package.json" (
    echo Error: Frontend not found. Please ensure frontend directory exists.
    pause
    exit /b 1
)

echo [1/4] Activating virtual environment...
call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo Error: Failed to activate virtual environment
    pause
    exit /b 1
)

echo [2/4] Installing/updating Python dependencies...
pip install -r requirements-fastapi.txt --quiet
if %errorlevel% neq 0 (
    echo Warning: Some Python packages may not have installed correctly
)

echo [3/4] Installing/updating Node.js dependencies...
cd frontend
call npm install --silent
if %errorlevel% neq 0 (
    echo Error: Failed to install Node.js dependencies
    cd ..
    pause
    exit /b 1
)
cd ..

echo [4/4] Starting both servers...
echo.
echo Starting Backend Server (FastAPI)...
echo Starting Frontend Server (React + Vite)...
echo.
echo ============================================
echo   Servers will open in separate windows
echo ============================================
echo   Backend:  http://localhost:8000
echo   Frontend: http://localhost:5173 (or 5174)
echo   Docs:     http://localhost:8000/docs
echo ============================================
echo.
echo Press Ctrl+C in each window to stop servers
echo Close this window when done
echo.

REM Start backend in new window
start "Legal Perplexity - Backend Server" cmd /k "cd /d "%~dp0" && .venv\Scripts\activate.bat && uvicorn main:app --reload --host 0.0.0.0 --port 8000"

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend in new window
start "Legal Perplexity - Frontend Server" cmd /k "cd /d "%~dp0frontend" && npm run dev"

echo.
echo Both servers are starting...
echo Check the new command windows for server status.
echo.
pause