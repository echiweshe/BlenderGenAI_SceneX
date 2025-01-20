import bpy
import sys
import math
from pathlib import Path

addon_dir = Path("/home/ernestc/.config/blender/4.3/scripts/addons/BelnderGenAI").resolve()

if str(addon_dir) not in sys.path:
    sys.path.append(str(addon_dir))
    print(f"Added to Python path: {addon_dir}")

try:
    from core.XV1_svg_converter import SVGToSceneConverter
    print("Successfully imported SVGToSceneConverter")
except ImportError as e:
    print(f"Error importing SVGToSceneConverter: {e}")
    raise

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def setup_scene():
    clear_scene()
    bpy.ops.object.camera_add(location=(10, -10, 10))
    camera = bpy.context.active_object
    camera.rotation_euler = (math.radians(45), 0, math.radians(45))
    bpy.context.scene.camera = camera
    bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
    light = bpy.context.active_object
    light.data.energy = 5.0

def test_basic_svg():
    setup_scene()
    test_svg = '''<?xml version="1.0"?>
    <svg width="800" height="600" xmlns="http://www.w3.org/2000/svg">
        <g class="component aws-component" data-service="lambda" id="lambda1">
            <rect x="100" y="100" width="64" height="64"/>
            <text x="132" y="180">Lambda Function</text>
        </g>
        <g class="component aws-component" data-service="s3" id="s3bucket">
            <rect x="300" y="100" width="64" height="64"/>
            <text x="332" y="180">S3 Bucket</text>
        </g>
        <path class="connection" id="lambda_to_s3" d="M 164 132 L 300 132"/>
    </svg>'''
    converter = SVGToSceneConverter()
    scene_data = converter.convert(test_svg)
    print("Scene Data:", scene_data)
    components = [obj for obj in bpy.data.objects if 'component' in obj.name]
    connections = [obj for obj in bpy.data.objects if 'connection' in obj.name]
    print(f"Components created ({len(components)}): {components}")
    print(f"Connections created ({len(connections)}): {connections}")

if __name__ == "__main__":
    test_basic_svg()
