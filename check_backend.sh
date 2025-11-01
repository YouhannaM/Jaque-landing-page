#!/bin/bash

echo "🔍 Checking Backend Status..."
echo "================================"
echo ""

# Check if port 8000 is in use
echo "1. Checking if port 8000 is in use:"
if netstat -tuln 2>/dev/null | grep -q ":8000 " || ss -tuln 2>/dev/null | grep -q ":8000 "; then
    echo "✅ Port 8000 is OPEN and listening"
else
    echo "❌ Port 8000 is NOT listening"
    echo "   Start backend with: uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload"
    exit 1
fi
echo ""

# Check if backend responds
echo "2. Testing backend health endpoint:"
HEALTH=$(curl -s http://localhost:8000/health 2>&1)
if echo "$HEALTH" | grep -q "healthy"; then
    echo "✅ Backend is HEALTHY and responding"
    echo "$HEALTH" | python3 -m json.tool
else
    echo "❌ Backend is NOT responding"
    echo "Error: $HEALTH"
    exit 1
fi
echo ""

# Check docs endpoint
echo "3. Testing API docs endpoint:"
DOCS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/docs 2>&1)
if [ "$DOCS" = "200" ]; then
    echo "✅ API Docs are available at: http://localhost:8000/docs"
else
    echo "⚠️  API Docs returned status: $DOCS"
fi
echo ""

# List all endpoints
echo "4. Available endpoints:"
echo "   - Health: http://localhost:8000/health"
echo "   - API Docs: http://localhost:8000/docs"
echo "   - Demo Request: http://localhost:8000/api/demo/request"
echo "   - CAD Upload: http://localhost:8000/api/cad/upload"
echo ""

# Check if accessible from outside
echo "5. Backend is running on:"
echo "   - localhost:8000 (this computer only)"
echo "   - 0.0.0.0:8000 (accessible from network)"
echo ""

# Test a real endpoint
echo "6. Testing demo requests endpoint:"
REQUESTS=$(curl -s http://localhost:8000/api/demo/requests 2>&1)
if echo "$REQUESTS" | grep -q "id"; then
    COUNT=$(echo "$REQUESTS" | grep -o '"id"' | wc -l)
    echo "✅ Found $COUNT demo requests in database"
else
    echo "⚠️  No demo requests found (this is OK for a new installation)"
fi
echo ""

echo "================================"
echo "✅ Backend Status: WORKING!"
echo ""
echo "📖 To access the interactive API docs:"
echo "   1. Open a web browser (Chrome, Firefox, etc.)"
echo "   2. Go to: http://localhost:8000/docs"
echo "   3. Click around to test the API"
echo ""
echo "🌐 If accessing from another computer on the same network:"
echo "   - Find this computer's IP address with: hostname -I"
echo "   - Use: http://YOUR-IP:8000/docs"
