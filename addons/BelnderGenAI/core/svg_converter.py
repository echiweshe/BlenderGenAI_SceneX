# File: /home/ernestc/.config/blender/4.3/scripts/addons/BelnderGenAI/core/svg_converter.py

import bpy
import xml.etree.ElementTree as ET
from typing import Dict, List, Union, Optional, Tuple
import re

class SVGToSceneConverter:
    """Converts SVG content to Blender scene objects."""

    def __init__(self):
        """Initialize the SVG converter."""
        self.components = []
        self.connections = []

    def debug_print_element(self, element: ET.Element, level: int = 0):
        """Print debug info about an XML element."""
        indent = "  " * level
        print(f"{indent}Tag: {element.tag}")
        print(f"{indent}Attributes: {element.attrib}")
        print(f"{indent}Text: {element.text.strip() if element.text else ''}")
        for child in element:
            self.debug_print_element(child, level + 1)

    def parse_svg_path(self, d: str) -> List[Tuple[float, float]]:
        """Parse SVG path data into points."""
        try:
            # Remove any extra whitespace and split into commands
            d = re.sub(r'\s+', ' ', d.strip())
            commands = re.findall(r'([MLHVCSQTAZmlhvcsqtaz])([^MLHVCSQTAZmlhvcsqtaz]*)', d)
            
            points = []
            current_point = (0, 0)
            
            for cmd, params in commands:
                # Split parameters into numbers
                params = [float(x) for x in params.strip().split()]
                
                if cmd == 'M':  # Move to
                    current_point = (params[0], params[1])
                    points.append(current_point)
                elif cmd == 'L':  # Line to
                    current_point = (params[0], params[1])
                    points.append(current_point)
                    
            print(f"Parsed path points: {points}")
            return points
            
        except Exception as e:
            print(f"Error parsing path data '{d}': {str(e)}")
            return []

    def create_component(self, element: ET.Element) -> Optional[bpy.types.Object]:
        """Create a Blender object from an SVG component."""
        print("\nProcessing component element:")
        self.debug_print_element(element)
        
        try:
            # Find rect in component group
            rect = element.find(".//rect")
            if rect is None:
                print("No rect element found in component")
                return None

            print(f"Found rect element: {rect.attrib}")
                
            # Get component info
            service_type = element.get('data-service', 'unknown')
            component_id = element.get('id', 'unknown')
            
            # Get position and size
            x = float(rect.get('x', 0)) / 100.0  # Scale down SVG coordinates
            y = -float(rect.get('y', 0)) / 100.0  # Invert Y for Blender
            width = float(rect.get('width', 1)) / 100.0
            height = float(rect.get('height', 1)) / 100.0
            
            # Create cube
            bpy.ops.mesh.primitive_cube_add(location=(x, y, 0))
            obj = bpy.context.active_object
            obj.name = f"{service_type}_{component_id}"
            
            # Scale cube
            obj.scale.x = width / 2  # Divide by 2 since cube is 2 units wide
            obj.scale.y = height / 2
            obj.scale.z = 0.1  # Make it thin
            
            print(f"Created component: {obj.name} at ({x}, {y})")
            self.components.append(obj)
            return obj
            
        except Exception as e:
            print(f"Error creating component: {str(e)}")
            return None

    def create_connection(self, element: ET.Element) -> Optional[bpy.types.Object]:
        """Create a Blender curve from an SVG path."""
        print("\nProcessing connection element:")
        self.debug_print_element(element)
        
        try:
            # Get path data
            path_data = element.get('d', '')
            if not path_data:
                print("No path data found")
                return None
                
            print(f"Path data: {path_data}")
                
            # Parse path into points
            points = self.parse_svg_path(path_data)
            if not points:
                print("No points parsed from path")
                return None
                
            # Create curve
            curve_data = bpy.data.curves.new('connection', 'CURVE')
            curve_data.dimensions = '3D'
            
            # Create spline
            spline = curve_data.splines.new('POLY')
            spline.points.add(len(points) - 1)  # One point already exists
            
            # Set points
            for i, (x, y) in enumerate(points):
                spline.points[i].co = (x/100.0, -y/100.0, 0, 1)  # Scale and invert Y
                
            curve_obj = bpy.data.objects.new('connection', curve_data)
            curve_obj.data.bevel_depth = 0.02
            
            # Add to scene
            bpy.context.scene.collection.objects.link(curve_obj)
            self.connections.append(curve_obj)
            
            print(f"Created connection curve with {len(points)} points")
            return curve_obj
            
        except Exception as e:
            print(f"Error creating connection: {str(e)}")
            return None

    def convert(self, svg_content: str) -> Dict[str, List[bpy.types.Object]]:
        """Convert SVG content to Blender objects."""
        print("\nStarting SVG conversion...")
        
        try:
            # Clear existing results
            self.components = []
            self.connections = []
            
            # Parse SVG
            root = ET.fromstring(svg_content)
            print("\nParsed SVG structure:")
            self.debug_print_element(root)
            
            # Find and process components
            components = root.findall(".//g[@class='component aws-component']")
            print(f"\nFound {len(components)} component elements")
            for comp in components:
                self.create_component(comp)
                
            # Find and process connections
            paths = root.findall(".//path[@class='connection']")
            print(f"\nFound {len(paths)} connection paths")
            for path in paths:
                self.create_connection(path)
                
            return {
                'components': self.components,
                'connections': self.connections
            }
            
        except Exception as e:
            print(f"Error during SVG conversion: {str(e)}")
            return {
                'components': [],
                'connections': []
            }