# 🚀 Legal Perplexity 2.0 - Batch Scripts

This folder contains convenient batch scripts to manage your Legal Perplexity application.

## 📁 Available Scripts

### 🌟 `start-app.bat` (Recommended)
**Full setup and start script with error checking**

- ✅ Checks all prerequisites (virtual environment, dependencies)
- 🔧 Installs/updates Python and Node.js dependencies
- 🚀 Starts both backend and frontend servers
- 📊 Provides detailed status information
- ⚠️ Comprehensive error handling

**Usage:**
```bash
# Double-click the file or run from command line
start-app.bat
```

### ⚡ `quick-start.bat`
**Fast start without dependency checks**

- 🏃‍♂️ Quick startup for development
- 🚀 Assumes all dependencies are already installed
- 💨 Minimal setup time
- 🎯 Perfect for regular development sessions

**Usage:**
```bash
# For quick development starts
quick-start.bat
```

### 🛑 `stop-servers.bat`
**Clean shutdown of all servers**

- 🔌 Stops backend server (port 8000)
- 🔌 Stops frontend server (ports 5173/5174)
- 🧹 Cleans up background processes
- ✅ Ensures clean shutdown

**Usage:**
```bash
# Stop all running servers
stop-servers.bat
```

## 🎯 Quick Start Guide

### First Time Setup:
1. Run `start-app.bat` - it will handle all setup
2. Wait for both servers to start
3. Open http://localhost:5173 in your browser

### Daily Development:
1. Use `quick-start.bat` for faster startup
2. Develop your features
3. Use `stop-servers.bat` when done

## 🌐 Server URLs

After running the start scripts, access your application at:

- **Frontend (React)**: http://localhost:5173 or http://localhost:5174
- **Backend (FastAPI)**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

## 🔧 Prerequisites

Before using these scripts, ensure you have:

- ✅ Python 3.8+ installed
- ✅ Node.js 16+ installed
- ✅ Virtual environment created (`.venv` folder)
- ✅ All dependencies listed in `requirements-fastapi.txt`
- ✅ Frontend dependencies in `frontend/package.json`

## 🚨 Troubleshooting

### Port Already in Use:
- Frontend will automatically try port 5174 if 5173 is busy
- Use `stop-servers.bat` to clean up any stuck processes

### Virtual Environment Issues:
- Ensure `.venv` folder exists in project root
- Recreate with: `python -m venv .venv`

### Permission Errors:
- Run Command Prompt as Administrator
- Check Windows Defender/Antivirus settings

### Backend Won't Start:
- Check if all Python dependencies are installed
- Verify `main.py` exists in project root
- Check `requirements-fastapi.txt` file

### Frontend Won't Start:
- Ensure Node.js is installed
- Check if `frontend/package.json` exists
- Try deleting `frontend/node_modules` and running `npm install`

## 📝 Manual Commands

If batch scripts don't work, you can run manually:

### Backend:
```bash
cd "path/to/project"
.venv\Scripts\activate.bat
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend:
```bash
cd "path/to/project/frontend"
npm run dev
```

## 🎉 Features

Your Legal Perplexity app includes:
- 🤖 AI-powered constitutional law analysis
- 📚 Constitutional document search
- 💬 Interactive chat interface
- 📖 Citation and reasoning display
- 🎨 Modern, responsive UI
- ⚖️ Legal article formatting

Happy coding! 🚀