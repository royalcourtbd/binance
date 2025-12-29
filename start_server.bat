@echo off
REM Binance P2P Orders API - Startup Script (Windows)
REM This script starts the FastAPI backend server

echo 🚀 Starting Binance P2P Orders API Server...
echo.

REM Check if virtual environment exists
if not exist ".venv" (
    echo ⚠️  Virtual environment not found!
    echo Creating virtual environment...
    python -m venv .venv
    echo ✅ Virtual environment created
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Check if dependencies are installed
python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo ⚠️  Dependencies not installed!
    echo Installing dependencies...
    pip install -r requirements.txt
    echo ✅ Dependencies installed
    echo.
)

REM Check if .env file exists
if not exist ".env" (
    echo ❌ Error: .env file not found!
    echo.
    echo Please create a .env file with your Binance API credentials:
    echo   copy .env.example .env
    echo   # Then edit .env with your actual API keys
    echo.
    pause
    exit /b 1
)

REM Start the server
echo ✅ Starting server...
echo 📡 Server will be available at:
echo    - API: http://localhost:8000
echo    - Docs: http://localhost:8000/docs
echo    - ReDoc: http://localhost:8000/redoc
echo.
echo Press CTRL+C to stop the server
echo.

REM Run with auto-reload for development
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
