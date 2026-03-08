#!/bin/bash
# Project.MilanoLibrary Frontend Startup Script

set -e

echo "🚀 Starting Project.MilanoLibrary Frontend..."

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Load environment variables
if [ -f "../.env" ]; then
    export $(grep -v '^#' ../.env | xargs)
fi

# Start development server
echo "✅ Starting React development server on http://localhost:3000"
npm start
