#!/bin/bash
# Quick start script for the backend API

echo "Starting EMS Call Analysis API..."
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Set PYTHONPATH
export PYTHONPATH=.

# Run the server
echo ""
echo "✅ Starting Flask server..."
python api/app.py

