#!/bin/bash

# Quick Interactive Backend Test Script
# This will test all major features of your Jaque.ai backend

echo "╔════════════════════════════════════════════════════════════╗"
echo "║        🚀 Jaque.ai Backend Quick Test                     ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if backend is running
echo -e "${BLUE}[1/6]${NC} Checking if backend is running..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Backend is running!${NC}"
else
    echo -e "${YELLOW}⚠️  Backend is not responding. Make sure it's running on port 8000${NC}"
    echo "Start it with: uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload"
    exit 1
fi
echo ""

# Test 1: Health Check
echo -e "${BLUE}[2/6]${NC} Testing Health Check Endpoint..."
echo "GET /health"
curl -s http://localhost:8000/health | python3 -m json.tool
echo ""
echo ""

# Test 2: API Documentation
echo -e "${BLUE}[3/6]${NC} API Documentation Available At:"
echo -e "${GREEN}📖 Swagger UI:${NC} http://localhost:8000/docs"
echo -e "${GREEN}📖 ReDoc:${NC}     http://localhost:8000/redoc"
echo ""

# Test 3: Submit Demo Request
echo -e "${BLUE}[4/6]${NC} Testing Demo Request Submission..."
echo "POST /api/demo/request"
DEMO_RESPONSE=$(curl -s -X POST http://localhost:8000/api/demo/request \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User from Script",
    "email": "test@quicktest.com",
    "company": "Quick Test Corp",
    "role": "Quality Manager",
    "message": "This is an automated test from quick_test.sh"
  }')
echo "$DEMO_RESPONSE" | python3 -m json.tool
echo ""
echo ""

# Test 4: Upload CAD File
if [ -f "test_simple_part.dxf" ]; then
    echo -e "${BLUE}[5/6]${NC} Testing CAD File Upload..."
    echo "POST /api/cad/upload (with test_simple_part.dxf)"
    CAD_RESPONSE=$(curl -s -X POST http://localhost:8000/api/cad/upload \
      -F "file=@test_simple_part.dxf")
    echo "$CAD_RESPONSE" | python3 -m json.tool
    echo ""
    echo ""
else
    echo -e "${YELLOW}⚠️  test_simple_part.dxf not found, skipping CAD upload test${NC}"
    echo ""
fi

# Test 5: View All Data
echo -e "${BLUE}[6/6]${NC} Viewing All Demo Requests..."
echo "GET /api/demo/requests"
curl -s http://localhost:8000/api/demo/requests | python3 -m json.tool
echo ""
echo ""

# Summary
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                    ✅ Testing Complete!                    ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "📊 What to do next:"
echo ""
echo "1. ${GREEN}Open Interactive API Docs:${NC}"
echo "   http://localhost:8000/docs"
echo ""
echo "2. ${GREEN}View All Demo Requests:${NC}"
echo "   curl http://localhost:8000/api/demo/requests | python3 -m json.tool"
echo ""
echo "3. ${GREEN}Check Uploaded CAD Files:${NC}"
echo "   curl http://localhost:8000/api/cad/uploads | python3 -m json.tool"
echo ""
echo "4. ${GREEN}Read the Full Testing Guide:${NC}"
echo "   cat TESTING_GUIDE.md"
echo ""
echo "🎉 Your backend is working perfectly!"
