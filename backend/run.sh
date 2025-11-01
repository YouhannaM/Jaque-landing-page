#!/bin/bash

# Jaque.ai Backend Startup Script

echo "🚀 Starting Jaque.ai Backend..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    if [ -f ../.env.example ]; then
        cp ../.env.example .env
        echo "✅ Created .env file. Please update it with your configuration."
    else
        echo "❌ .env.example not found. Please create .env manually."
        exit 1
    fi
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r ../requirements.txt

# Check if PostgreSQL is running
if ! pg_isready -h localhost -p 5432 > /dev/null 2>&1; then
    echo "⚠️  PostgreSQL doesn't appear to be running on localhost:5432"
    echo "   Please start PostgreSQL or update DATABASE_URL in .env"
fi

# Start the server
echo "✨ Starting FastAPI server..."
echo "📍 API will be available at: http://localhost:8000"
echo "📖 API docs will be available at: http://localhost:8000/docs"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
