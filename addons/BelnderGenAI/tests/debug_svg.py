# File: /home/ernestc/.config/blender/4.3/scripts/addons/BelnderGenAI/tests/debug_svg.py

import xml.etree.ElementTree as ET

def debug_svg_parsing(svg_content: str):
    """Debug SVG parsing issues."""
    print("\nDEBUG SVG PARSING")
    print("=" * 50)
    
    try:
        # Parse SVG
        root = ET.fromstring(svg_content)
        print("\n1. Basic SVG Info:")
        print(f"Root tag: {root.tag}")
        print(f"Root attributes: {root.attrib}")
        
        # Debug namespace
        ns = {'svg': 'http://www.w3.org/2000/svg'}
        print("\n2. Checking for components with namespace:")
        components = root.findall(".//svg:g[@class='component aws-component']", ns)
        print(f"Found {len(components)} components with namespace")
        
        print("\n3. Checking for components without namespace:")
        components = root.findall(".//g[@class='component aws-component']")
        print(f"Found {len(components)} components without namespace")
        
        # Print all groups
        print("\n4. All group elements found:")
        all_groups = root.findall(".//g")
        for i, group in enumerate(all_groups):
            print(f"\nGroup {i + 1}:")
            print(f"  Class: {group.get('class')}")
            print(f"  ID: {group.get('id')}")
            print(f"  Children: {[child.tag for child in group]}")
            
        # Print all path elements
        print("\n5. All path elements:")
        paths = root.findall(".//path")
        for i, path in enumerate(paths):
            print(f"\nPath {i + 1}:")
            print(f"  Class: {path.get('class')}")
            print(f"  ID: {path.get('id')}")
            print(f"  Data: {path.get('d')}")
            
    except Exception as e:
        print(f"\nError during debug: {str(e)}")

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

if __name__ == "__main__":
    debug_svg_parsing(test_svg)
