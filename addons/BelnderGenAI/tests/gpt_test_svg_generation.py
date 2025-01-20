import bpy
import sys
import os
import math  # Ensure math is imported
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

# Import module from core
try:
    from core.XV1_svg_converter import SVGToSceneConverter
    print("Successfully imported SVGToSceneConverter")
except ImportError as e:
    print(f"Error importing SVGToSceneConverter: {e}")
    print(f"Current directory: {addon_dir}")
    print(f"Python path: {sys.path}")
    raise

def setup_test_scene():
    """Setup a clean test scene."""
    print("Setting up test scene...")
    
    # Clear existing scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Set render engine
    bpy.context.scene.render.engine = 'CYCLES'  # Use Cycles for Blender 4.3
    
    # Set up camera
    bpy.ops.object.camera_add(location=(0, -10, 5))
    camera = bpy.context.active_object
    camera.rotation_euler = (math.radians(30), 0, 0)  # Use math.radians correctly
    
    print("Test scene setup complete")

def test_basic_svg():
    """Test basic SVG generation and conversion."""
    print("Starting SVG test...")
    setup_test_scene()

    # Test SVG content
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
        # Create converter instance
        print("Creating SVG converter...")
        converter = SVGToSceneConverter()

        # Convert SVG to scene data
        print("Converting SVG to scene data...")
        scene_data = converter.convert(test_svg)

        # Print conversion results
        print("\nScene Data:")
        print("-----------")
        for key, value in scene_data.items():
            print(f"{key}: {value}")

        # Verify objects were created
        print("\nVerifying created objects:")
        component_count = len([obj for obj in bpy.data.objects if 'component' in obj.name])
        connection_count = len([obj for obj in bpy.data.objects if 'connection' in obj.name])

        print(f"Components created: {component_count}")
        print(f"Connections created: {connection_count}")

        if component_count == 2 and connection_count == 1:
            print("\nTest completed successfully!")
        else:
            print("\nTest completed with unexpected object counts")
            
    except Exception as e:
        print(f"\nError during test: {str(e)}")
        raise

if __name__ == "__main__":
    test_basic_svg()
