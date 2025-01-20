# File: /home/ernestc/.config/blender/4.3/scripts/addons/BelnderGenAI/tests/test_svg_generation.py

import bpy
import sys
import os
import math
from pathlib import Path

# Set the addon directory path
addon_dir = Path("/home/ernestc/.config/blender/4.3/scripts/addons/BelnderGenAI").resolve()

# Add addon_dir to sys.path if not already added
if str(addon_dir) not in sys.path:
    sys.path.append(str(addon_dir))
    print(f"Added to Python path: {addon_dir}")

# Debugging paths
print(f"Addon directory: {addon_dir}")
print(f"Current Python path: {sys.path}")

# Import our converter
try:
    from core.XV1_svg_converter import SVGToSceneConverter
    print("Successfully imported SVGToSceneConverter")
except ImportError as e:
    print(f"Error importing SVGToSceneConverter: {e}")
    print(f"Current directory: {os.getcwd()}")
    raise

def clear_scene():
    """Clear all objects from the scene."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
def setup_viewport():
    """Configure viewport for better visualization."""
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'MATERIAL'
                    space.shading.use_scene_lights = True
                    # Set a nice default view
                    space.region_3d.view_perspective = 'PERSP'
                    space.region_3d.view_distance = 15

def setup_scene():
    """Setup test scene with camera and light."""
    print("Setting up test scene...")
    
    # Clear scene
    clear_scene()
    
    # Set up camera
    bpy.ops.object.camera_add(location=(10, -10, 10))
    camera = bpy.context.active_object
    camera.rotation_euler = (math.radians(45), 0, math.radians(45))
    bpy.context.scene.camera = camera  # Set as active camera
    
    # Set up light
    bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
    light = bpy.context.active_object
    light.data.energy = 5.0
    
    # Configure viewport
    setup_viewport()
    
    print("Test scene setup complete")

def test_basic_svg():
    """Test SVG to scene conversion."""
    print("\nStarting SVG conversion test...")
    
    # Setup clean scene
    setup_scene()
    
    # Test SVG
    test_svg = '''<?xml version="1.0" encoding="UTF-8"?>
    <svg width="800" height="600" xmlns="http://www.w3.org/2000/svg">
        <g class="component aws-component" data-service="lambda" id="lambda1">
            <rect x="100" y="100" width="64" height="64" class="component"/>
            <text x="132" y="180">Lambda Function</text>
        </g>
        <g class="component aws-component" data-service="s3" id="s3bucket">
            <rect x="300" y="100" width="64" height="64" class="component"/>
            <text x="332" y="180">S3 Bucket</text>
        </g>
        <path class="connection" id="lambda_to_s3" d="M 164 132 L 300 132"/>
    </svg>'''

    try:
        # Create converter
        print("\nCreating SVG converter...")
        converter = SVGToSceneConverter()

        # Convert SVG
        print("Converting SVG to scene data...")
        scene_data = converter.convert(test_svg)

        # Print conversion results
        print("\nScene Data:")
        print("-----------")
        for key, value in scene_data.items():
            print(f"{key}: {value}")

        # Verify objects
        print("\nVerifying created objects:")
        components = [obj for obj in bpy.data.objects if 'component' in obj.name]
        connections = [obj for obj in bpy.data.objects if 'connection' in obj.name]
        
        print(f"Components created ({len(components)}):")
        for comp in components:
            print(f"- {comp.name} at location {comp.location}")
            
        print(f"\nConnections created ({len(connections)}):")
        for conn in connections:
            print(f"- {conn.name}")

        # Switch to camera view for better visualization
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                area.spaces[0].region_3d.view_perspective = 'CAMERA'

        if len(components) == 2 and len(connections) == 1:
            print("\nTest completed successfully!")
            return True
        else:
            print("\nTest completed with unexpected object counts")
            return False
            
    except Exception as e:
        print(f"\nError during test: {str(e)}")
        raise

if __name__ == "__main__":
    test_basic_svg()
