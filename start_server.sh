#!/bin/bash

# Binance P2P Orders API - Startup Script
# This script starts the FastAPI backend server

echo "🚀 Starting Binance P2P Orders API Server..."
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "⚠️  Virtual environment not found!"
    echo "Creating virtual environment..."
    python3 -m venv .venv
    echo "✅ Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Check if dependencies are installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "⚠️  Dependencies not installed!"
    echo "Installing dependencies..."
    pip install -r requirements.txt
    echo "✅ Dependencies installed"
    echo ""
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found!"
    echo ""
    echo "Please create a .env file with your Binance API credentials:"
    echo "  cp .env.example .env"
    echo "  # Then edit .env with your actual API keys"
    echo ""
    exit 1
fi

# Start the server
echo "✅ Starting server..."
echo "📡 Server will be available at:"
echo "   - API: http://localhost:8000"
echo "   - Docs: http://localhost:8000/docs"
echo "   - ReDoc: http://localhost:8000/redoc"
echo ""
echo "Press CTRL+C to stop the server"
echo ""

# Run with auto-reload for development
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
