#!/bin/bash

echo "🎯 Testing CAD File Upload: camera Fixture-part1.STL"
echo "====================================================="
echo ""

# Check if file exists
if [ ! -f "camera Fixture-part1.STL" ]; then
    echo "❌ File 'camera Fixture-part1.STL' not found in current directory"
    echo ""
    echo "Please either:"
    echo "  1. Copy the file to: /home/user/Jaque-landing-page/"
    echo "  2. Update the path in this script"
    echo "  3. Use the API docs at: http://localhost:8000/docs"
    exit 1
fi

echo "📁 File found! Uploading to backend..."
echo ""

# Upload the file
RESPONSE=$(curl -s -X POST http://localhost:8000/api/cad/upload \
  -F "file=@camera Fixture-part1.STL")

echo "📊 Analysis Results:"
echo "===================="
echo "$RESPONSE" | python3 -m json.tool
echo ""
echo ""

# Extract key information
echo "🔍 Key Information:"
echo "-------------------"
echo "$RESPONSE" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    if data.get('success'):
        print(f\"✅ Upload: Success\")
        print(f\"📄 Filename: {data.get('filename')}\")
        print(f\"💾 File Size: {data.get('file_size'):,} bytes\")
        print(f\"📐 Format: {data.get('file_type')}\")
        print()
        analysis = data.get('analysis', {})
        if 'vertices' in analysis:
            print(f\"3D Mesh Analysis:\")
            print(f\"  • Vertices: {analysis.get('vertices'):,}\")
            print(f\"  • Faces: {analysis.get('faces'):,}\")
            print(f\"  • Watertight: {analysis.get('is_watertight')}\")
            if analysis.get('volume'):
                print(f\"  • Volume: {analysis.get('volume'):.2f} cubic units\")
            print(f\"  • Surface Area: {analysis.get('surface_area'):.2f} square units\")
    else:
        print(f\"❌ Upload failed: {data.get('message')}\")
except Exception as e:
    print(f\"Error parsing response: {e}\")
"

echo ""
echo "✅ Complete! Your CAD file has been analyzed."
