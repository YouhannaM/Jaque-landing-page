#!/bin/bash

echo "🧪 Testing Complete End-to-End Workflow"
echo "========================================"
echo ""

# Step 1: Submit demo request
echo "📝 Step 1: Submitting demo request..."
DEMO_RESPONSE=$(curl -s -X POST http://localhost:8000/api/demo/request \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Smith",
    "email": "john.smith@manufacturing.com",
    "company": "Advanced Manufacturing Inc",
    "role": "Quality Manager",
    "message": "We need help with predictive quality control for our CNC machining operations. Attached is a sample part drawing."
  }')

echo "$DEMO_RESPONSE" | python3 -m json.tool
echo ""

# Step 2: Upload CAD file
echo "📁 Step 2: Uploading CAD file..."
CAD_RESPONSE=$(curl -s -X POST http://localhost:8000/api/cad/upload \
  -F "file=@test_simple_part.dxf")

echo "$CAD_RESPONSE" | python3 -m json.tool
echo ""

# Step 3: Verify demo request was saved
echo "✅ Step 3: Verifying demo request in database..."
curl -s http://localhost:8000/api/demo/requests | python3 -m json.tool
echo ""

# Step 4: Check uploaded files
echo "📂 Step 4: Checking uploaded CAD files..."
curl -s http://localhost:8000/api/cad/uploads | python3 -m json.tool
echo ""

echo "✨ Complete workflow test finished!"
