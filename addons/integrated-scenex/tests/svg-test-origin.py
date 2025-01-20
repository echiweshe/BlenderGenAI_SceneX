# File: /home/ernestc/.config/blender/4.3/scripts/addons/BelnderGenAI/tests/test_svg_generation.py

import bpy
import sys
import os
import math
from pathlib import Path

def print_separator(title: str = ""):
    print("\n" + "=" * 50)
    if title:
        print(title)
        print("=" * 50)

def setup_addon_path():
    addon_dir = Path("/home/ernestc/.config/blender/4.3/scripts/addons/BelnderGenAI").resolve()
    if str(addon_dir) not in sys.path:
        sys.path.append(str(addon_dir))
        print(f"Added to Python path: {addon_dir}")

def debug_svg_input(svg_content: str, source: str = "test"):
    print_separator("Original SVG Input")
    print(f"SVG Source: {source}")
    print("\nSVG Content:")
    print(svg_content)

def test_basic_svg():
    # Test SVG content - important to track if this gets modified
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

    print_separator("Test Configuration")
    print("Running SVG generation test...")
    debug_svg_input(test_svg, "test_case")

    try:
        from core.XV1_svg_converter import SVGToSceneConverter
        print("\nSuccessfully imported SVGToSceneConverter")
        
        # Clear scene
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
        print("\nCleared scene")

        # Test conversion
        print("\nStarting conversion...")
        converter = SVGToSceneConverter()
        result = converter.convert(test_svg)

        print_separator("Results")
        print(f"Components created: {len(result['components'])}")
        for comp in result['components']:
            print(f"- {comp.name} at {comp.location}")

        print(f"\nConnections created: {len(result['connections'])}")
        for conn in result['connections']:
            print(f"- {conn.name}")

        if not result['components'] and not result['connections']:
            print("\nERROR: No objects created")
            print("Please check:")
            print("1. SVG content is valid")
            print("2. XML namespace handling")
            print("3. Path parsing for connections")

    except Exception as e:
        print_separator("ERROR")
        print(f"Test failed: {str(e)}")
        raise

if __name__ == "__main__":
    setup_addon_path()
    test_basic_svg()
