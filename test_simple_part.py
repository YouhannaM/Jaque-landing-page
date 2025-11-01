#!/usr/bin/env python3
"""
Create a simple DXF file for testing the CAD upload functionality
This creates a simple rectangular part with a circular hole
"""

import ezdxf

# Create a new DXF document
doc = ezdxf.new('R2010')

# Get the modelspace
msp = doc.modelspace()

# Add a rectangle (outer boundary)
# Starting from (0, 0), width=100, height=50
msp.add_lwpolyline([
    (0, 0),
    (100, 0),
    (100, 50),
    (0, 50),
    (0, 0)  # Close the polyline
])

# Add a circle (hole in the center)
# Center at (50, 25), radius=10
msp.add_circle((50, 25), radius=10)

# Add some dimension lines
msp.add_line((0, -10), (100, -10))  # Bottom dimension line
msp.add_text(
    '100mm',
    dxfattribs={'height': 3}
).set_placement((45, -15))

# Add layer information
doc.layers.new('Outline', dxfattribs={'color': 1})  # Red
doc.layers.new('Holes', dxfattribs={'color': 3})    # Green

# Save the DXF file
doc.saveas('test_simple_part.dxf')

print("✅ Created test_simple_part.dxf")
print("   - Rectangular part: 100mm x 50mm")
print("   - Circular hole: diameter 20mm at center")
print("   - 2 layers: Outline, Holes")
