#!/usr/bin/env python3
"""
Create a simple test STL file to demonstrate the workflow
This creates a simple cube
"""

import trimesh
import numpy as np

# Create a simple cube
vertices = np.array([
    [0, 0, 0],
    [1, 0, 0],
    [1, 1, 0],
    [0, 1, 0],
    [0, 0, 1],
    [1, 0, 1],
    [1, 1, 1],
    [0, 1, 1]
])

faces = np.array([
    [0, 1, 2], [0, 2, 3],  # bottom
    [4, 5, 6], [4, 6, 7],  # top
    [0, 1, 5], [0, 5, 4],  # front
    [2, 3, 7], [2, 7, 6],  # back
    [0, 3, 7], [0, 7, 4],  # left
    [1, 2, 6], [1, 6, 5]   # right
])

# Create mesh
mesh = trimesh.Trimesh(vertices=vertices, faces=faces)

# Save as STL
mesh.export('test_cube.stl')

print("✅ Created test_cube.stl")
print(f"   - Vertices: {len(mesh.vertices)}")
print(f"   - Faces: {len(mesh.faces)}")
print(f"   - Watertight: {mesh.is_watertight}")
print(f"   - Volume: {mesh.volume:.2f}")
print(f"   - Surface Area: {mesh.area:.2f}")
