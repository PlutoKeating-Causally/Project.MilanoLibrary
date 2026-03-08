#!/bin/bash
# Project.MilanoLibrary Backend Startup Script

set -e

echo "🚀 Starting Project.MilanoLibrary Backend..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Create necessary directories
mkdir -p /tmp/milano_library/uploads

# Load environment variables
if [ -f "../.env" ]; then
    export $(grep -v '^#' ../.env | xargs)
fi

# Start server
echo "✅ Starting FastAPI server on http://localhost:8000"
echo "📚 API docs available at http://localhost:8000/docs"
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
