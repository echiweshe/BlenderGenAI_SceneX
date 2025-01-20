# File: /home/ernestc/.config/blender/4.3/scripts/addons/BelnderGenAI/core/svg_converter.py

import bpy
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Tuple
import re

class SVGToSceneConverter:
    SCALE_FACTOR = 0.05  # Reduced scale for better Blender viewport fit
    COMPONENT_DEPTH = 0.2  # Increased depth for better visibility
    CONNECTION_THICKNESS = 0.05  # Thicker connections
    
    def __init__(self):
        self.components = []
        self.connections = []
        self.ns = {'svg': 'http://www.w3.org/2000/svg'}

    def create_component(self, element: ET.Element) -> Optional[bpy.types.Object]:
        try:
            rect = element.find('svg:rect', self.ns)
            if not rect:
                return None

            service_type = element.get('data-service', 'unknown')
            component_id = element.get('id', 'unknown')
            
            # Scale coordinates
            x = float(rect.get('x', 0)) * self.SCALE_FACTOR
            y = -float(rect.get('y', 0)) * self.SCALE_FACTOR
            width = float(rect.get('width', 1)) * self.SCALE_FACTOR
            height = float(rect.get('height', 1)) * self.SCALE_FACTOR
            
            # Create component
            bpy.ops.mesh.primitive_cube_add(location=(x, y, 0))
            obj = bpy.context.active_object
            obj.name = f"{service_type}_{component_id}"
            
            # Scale with better proportions
            obj.scale = (width, height, self.COMPONENT_DEPTH)
            
            # Add material with improved colors
            mat = bpy.data.materials.new(name=f"{obj.name}_material")
            mat.use_nodes = True
            nodes = mat.node_tree.nodes
            principled = nodes["Principled BSDF"]
            
            if service_type == "lambda":
                color = (0.95, 0.45, 0.1, 1.0)  # Brighter orange
                principled.inputs["Metallic"].default_value = 0.3
            else:  # s3
                color = (0.45, 0.2, 0.95, 1.0)  # Brighter purple
                principled.inputs["Metallic"].default_value = 0.5
                
            principled.inputs["Base Color"].default_value = color
            principled.inputs["Roughness"].default_value = 0.3
            obj.data.materials.append(mat)
            
            print(f"Created {service_type} at ({x}, {y})")
            self.components.append(obj)
            return obj
            
        except Exception as e:
            print(f"Component creation error: {str(e)}")
            return None

    def create_connection(self, element: ET.Element) -> Optional[bpy.types.Object]:
        try:
            path_data = element.get('d', '')
            if not path_data:
                return None
                
            # Parse path points
            points = []
            for cmd_match in re.finditer(r'([ML])\s*([\d.-]+)\s*([\d.-]+)', path_data):
                cmd, x, y = cmd_match.groups()
                points.append((
                    float(x) * self.SCALE_FACTOR,
                    -float(y) * self.SCALE_FACTOR,
                    0
                ))
                
            if len(points) < 2:
                return None
                
            # Create curve
            curve_data = bpy.data.curves.new('connection', 'CURVE')
            curve_data.dimensions = '3D'
            
            spline = curve_data.splines.new('POLY')
            spline.points.add(len(points) - 1)
            
            # Set points
            for i, point in enumerate(points):
                spline.points[i].co = (*point, 1)
                
            # Create object with thicker line
            curve_obj = bpy.data.objects.new('connection', curve_data)
            curve_obj.data.bevel_depth = self.CONNECTION_THICKNESS
            
            # Add material with improved appearance
            mat = bpy.data.materials.new(name="connection_material")
            mat.use_nodes = True
            nodes = mat.node_tree.nodes
            principled = nodes["Principled BSDF"]
            principled.inputs["Base Color"].default_value = (0.1, 0.1, 0.1, 1.0)
            principled.inputs["Metallic"].default_value = 0.8
            principled.inputs["Roughness"].default_value = 0.2
            curve_obj.data.materials.append(mat)
            
            bpy.context.scene.collection.objects.link(curve_obj)
            self.connections.append(curve_obj)
            return curve_obj
            
        except Exception as e:
            print(f"Connection creation error: {str(e)}")
            return None

    def convert(self, svg_content: str) -> Dict[str, List[bpy.types.Object]]:
        try:
            self.components = []
            self.connections = []
            
            root = ET.fromstring(svg_content)
            print(f"Input SVG content:\n{svg_content}")
            
            components = root.findall(".//svg:g[@class='component aws-component']", self.ns)
            paths = root.findall(".//svg:path[@class='connection']", self.ns)
            
            print(f"\nFound {len(components)} component elements")
            for comp in components:
                self.create_component(comp)
                
            print(f"\nFound {len(paths)} connection paths")
            for path in paths:
                self.create_connection(path)
                
            return {
                'components': self.components,
                'connections': self.connections
            }
            
        except Exception as e:
            print(f"Conversion error: {str(e)}")
            return {
                'components': [],
                'connections': []
            }