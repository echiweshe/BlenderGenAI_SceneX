# File: /home/ernestc/.config/blender/4.3/scripts/addons/BelnderGenAI/core/svg_converter.py

import bpy
import xml.etree.ElementTree as ET
import math
from typing import Dict, List, Union, Optional

class SVGToSceneConverter:
    """Converts SVG content to Blender scene objects."""

    def __init__(self):
        """Initialize the SVG converter."""
        self.components = []
        self.connections = []

    def parse_position(self, element: ET.Element) -> tuple[float, float]:
        """
        Parse x,y position from SVG element.
        
        Args:
            element: SVG element with x,y attributes
            
        Returns:
            Tuple of (x, y) coordinates
        """
        x = float(element.get('x', 0))
        y = float(element.get('y', 0))
        # Convert SVG coordinates to Blender coordinates
        return (x/100.0, -y/100.0, 0)  # Scale down and invert Y

    def create_component(self, element: ET.Element) -> Optional[bpy.types.Object]:
        """
        Create a Blender object for an SVG component.
        
        Args:
            element: SVG element representing a component
            
        Returns:
            Created Blender object or None if creation fails
        """
        try:
            # Get component attributes
            service_type = element.get('data-service', 'unknown')
            component_id = element.get('id', f'component_{len(self.components)}')
            
            # Find rect element for dimensions
            rect = element.find('.//rect')
            if not rect:
                print(f"Warning: No rect found for component {service_type}")
                return None
                
            # Get position and size
            position = self.parse_position(rect)
            width = float(rect.get('width', 64)) / 100.0
            height = float(rect.get('height', 64)) / 100.0
            
            # Create cube for component
            bpy.ops.mesh.primitive_cube_add(
                size=1.0,
                location=position
            )
            obj = bpy.context.active_object
            obj.name = f"{service_type}_{component_id}"
            
            # Scale to match SVG dimensions
            obj.scale.x = width
            obj.scale.y = height
            obj.scale.z = 0.2  # Thin depth
            
            # Add to components list
            self.components.append(obj)
            return obj
            
        except Exception as e:
            print(f"Error creating component: {str(e)}")
            return None

    def create_connection(self, element: ET.Element) -> Optional[bpy.types.Object]:
        """
        Create a connection curve between components.
        
        Args:
            element: SVG path element representing connection
            
        Returns:
            Created Blender curve object or None if creation fails
        """
        try:
            # Parse path data
            d = element.get('d', '')
            if not d:
                return None
                
            # Extract coordinates
            parts = d.split()
            if len(parts) < 4:
                return None
                
            # Get start and end points
            start_x = float(parts[1]) / 100.0
            start_y = -float(parts[2]) / 100.0
            end_x = float(parts[3]) / 100.0
            end_y = -float(parts[4]) / 100.0
            
            # Create curve
            curve_data = bpy.data.curves.new(name='connection', type='CURVE')
            curve_data.dimensions = '3D'
            
            # Create spline
            spline = curve_data.splines.new('POLY')
            spline.points.add(1)
            
            # Set points
            spline.points[0].co = (start_x, start_y, 0, 1)
            spline.points[1].co = (end_x, end_y, 0, 1)
            
            # Create curve object
            curve_obj = bpy.data.objects.new('connection', curve_data)
            curve_obj.data.bevel_depth = 0.02
            
            # Add to scene
            bpy.context.scene.collection.objects.link(curve_obj)
            self.connections.append(curve_obj)
            
            return curve_obj
            
        except Exception as e:
            print(f"Error processing connection: {str(e)}")
            return None

    def convert(self, svg_content: str) -> Dict[str, List[bpy.types.Object]]:
        """
        Convert SVG content to Blender scene objects.
        
        Args:
            svg_content: String containing SVG XML
            
        Returns:
            Dictionary with 'components' and 'connections' lists
        """
        print("Starting SVG conversion...")
        
        try:
            # Clear existing lists
            self.components.clear()
            self.connections.clear()
            
            # Parse SVG
            root = ET.fromstring(svg_content)
            print("Successfully parsed SVG")
            
            # Process components
            for component in root.findall(".//g[@class='component']"):
                self.create_component(component)
                
            # Process connections
            for connection in root.findall(".//path[@class='connection']"):
                self.create_connection(connection)
                
            return {
                'components': self.components,
                'connections': self.connections
            }
            
        except Exception as e:
            print(f"Error converting SVG: {str(e)}")
            return {
                'components': [],
                'connections': []
            }