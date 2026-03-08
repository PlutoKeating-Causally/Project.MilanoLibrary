#!/bin/bash
# Project.MilanoLibrary Backend Test Runner

set -e

echo "🧪 Running Project.MilanoLibrary Backend Tests..."

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

# Run tests
echo "🚀 Running tests..."
python3 -m pytest tests/ -v --tb=short

echo "✅ Tests completed!"
