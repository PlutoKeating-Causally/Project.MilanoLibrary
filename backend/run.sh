#!/bin/bash
# Project.MilanoLibrary Backend Startup Script (Updated)

set -e

echo "🚀 Starting Project.MilanoLibrary Backend..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q fastapi uvicorn python-multipart httpx

# Create necessary directories
mkdir -p /tmp/milano_library/uploads

# Load environment variables
if [ -f "../.env" ]; then
    export $(grep -v '^#' ../.env | xargs)
fi

# Test import
echo "🧪 Testing backend import..."
python3 -c "from app.main import app; print('✅ Backend imports successfully')"

# Start server
echo "✅ Starting FastAPI server on http://localhost:8000"
echo "📚 API docs available at http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
