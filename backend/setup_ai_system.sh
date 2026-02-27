#!/bin/bash

echo "=========================================="
echo "🤖 Manufacturing Operations Platform"
echo "   AI Setup Script"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo "📋 Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo ""
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${YELLOW}⚠ Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo ""
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install AI/ML requirements
echo ""
echo "📚 Installing AI/ML dependencies..."
echo "   (This may take several minutes...)"
pip install -r requirements_ai.txt

if [ $? -ne 0 ]; then
    echo ""
    echo -e "${YELLOW}⚠ Some packages failed to install${NC}"
    echo "   Installing minimal fallback requirements..."
    pip install fastapi uvicorn sqlalchemy pydantic python-multipart scikit-learn numpy
fi

# Create necessary directories
echo ""
echo "📁 Creating directory structure..."
mkdir -p database
mkdir -p ai
mkdir -p api
mkdir -p logs
echo -e "${GREEN}✓ Directories created${NC}"

# Initialize database
echo ""
echo "🗄️  Initializing database..."
cd database
python3 seed_data.py

if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠ Database seeding encountered issues${NC}"
    echo "   You may need to run it manually later"
fi

cd ..

# Train AI models
echo ""
echo "🤖 Training AI models on quality standards..."
cd ai
python3 quality_standards_trainer.py

if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠ AI training encountered issues${NC}"
    echo "   The system will use fallback models"
fi

cd ..

# Download sentence transformer model (if available)
echo ""
echo "⬇️  Downloading AI models..."
python3 << EOF
try:
    from sentence_transformers import SentenceTransformer
    print("Downloading all-MiniLM-L6-v2 model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("✓ Model downloaded successfully")
except Exception as e:
    print(f"⚠ Model download failed: {e}")
    print("  Will use fallback TF-IDF model")
EOF

# Create startup script
echo ""
echo "📝 Creating startup script..."
cat > start_api.sh << 'STARTSCRIPT'
#!/bin/bash
echo "🚀 Starting Manufacturing Operations API..."
source venv/bin/activate
cd api
python3 manufacturing_api.py
STARTSCRIPT

chmod +x start_api.sh
echo -e "${GREEN}✓ Startup script created${NC}"

# Summary
echo ""
echo "=========================================="
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo "=========================================="
echo ""
echo "📊 What was installed:"
echo "   • Database with machines and quality standards"
echo "   • AI models for quality plan generation"
echo "   • Machine recommendation engine"
echo "   • FastAPI backend server"
echo ""
echo "🚀 To start the API server:"
echo "   ./start_api.sh"
echo ""
echo "   or manually:"
echo "   source venv/bin/activate"
echo "   cd api && python3 manufacturing_api.py"
echo ""
echo "📖 API Documentation:"
echo "   http://localhost:8000/docs (once started)"
echo ""
echo "🔧 Test the system:"
echo "   curl http://localhost:8000/"
echo ""
echo "=========================================="
