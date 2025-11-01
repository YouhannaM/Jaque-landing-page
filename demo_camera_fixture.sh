#!/bin/bash

echo "🎯 Complete Workflow: Camera Fixture Analysis"
echo "=============================================="
echo ""

# Step 1: Submit demo request
echo "📝 Step 1: Submitting demo request for camera fixture..."
DEMO=$(curl -s -X POST http://localhost:8000/api/demo/request \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Camera Systems Engineer",
    "email": "engineer@cameraco.com",
    "company": "Camera Manufacturing Inc",
    "role": "Engineering",
    "message": "Need quality analysis for camera fixture part. STL file attached - looking for dimensional accuracy and manufacturing feasibility assessment."
  }')

echo "$DEMO" | python3 -m json.tool
echo ""

# Step 2: Upload STL file (if it exists)
if [ -f "camera Fixture-part1.STL" ]; then
    echo "📁 Step 2: Uploading camera Fixture-part1.STL..."
    echo ""

    UPLOAD=$(curl -s -X POST http://localhost:8000/api/cad/upload \
      -F "file=@camera Fixture-part1.STL")

    echo "$UPLOAD" | python3 -m json.tool
    echo ""

    # Extract and display key metrics
    echo "🔍 Camera Fixture Analysis Summary:"
    echo "-----------------------------------"
    echo "$UPLOAD" | python3 -c "
import sys, json
data = json.load(sys.stdin)
if data.get('success'):
    a = data.get('analysis', {})
    print(f\"✅ File analyzed successfully\")
    print(f\"📊 Mesh Quality:\")
    print(f\"   • Vertices: {a.get('vertices', 0):,}\")
    print(f\"   • Faces: {a.get('faces', 0):,}\")
    print(f\"   • Watertight: {'✅ Yes' if a.get('is_watertight') else '⚠️ No (has holes)'}\")
    if a.get('volume'):
        print(f\"📐 Dimensions:\")
        print(f\"   • Volume: {a.get('volume', 0):.2f} mm³\")
        print(f\"   • Surface Area: {a.get('surface_area', 0):.2f} mm²\")
        bounds = a.get('bounds', {})
        if bounds:
            min_b = bounds.get('min', [0,0,0])
            max_b = bounds.get('max', [0,0,0])
            print(f\"   • Size: {max_b[0]-min_b[0]:.1f} x {max_b[1]-min_b[1]:.1f} x {max_b[2]-min_b[2]:.1f} mm\")
else:
    print('❌ Analysis failed')
"
else
    echo "⚠️  File 'camera Fixture-part1.STL' not found"
    echo "   Please copy it to: /home/user/Jaque-landing-page/"
    echo ""
    echo "   Or use the API docs at: http://localhost:8000/docs"
fi

echo ""
echo "✅ Workflow complete!"
