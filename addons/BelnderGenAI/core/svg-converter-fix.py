# File: /home/ernestc/.config/blender/4.3/scripts/addons/BelnderGenAI/core/svg_converter.py

import bpy
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Tuple
import re

class SVGToSceneConverter:
    def __init__(self):
        self.components = []
        self.connections = []
        self.ns = {'svg': 'http://www.w3.org/2000/svg'}
        print("Initialized SVG converter with namespace:", self.ns)

    def parse_svg_path(self, d: str) -> List[Tuple[float, float]]:
        try:
            d = re.sub(r'\s+', ' ', d.strip())
            parts = d.split()
            points = []
            
            if len(parts) >= 5 and parts[0] == 'M' and parts[3] == 'L':
                start_x = float(parts[1])
                start_y = float(parts[2])
                end_x = float(parts[4])
                end_y = float(parts[5])
                points = [(start_x, start_y), (end_x, end_y)]
                
            print(f"Parsed path points: {points}")
            return points
        except Exception as e:
            print(f"Path parsing error: {str(e)}")
            return []

    def create_component(self, element: ET.Element) -> Optional[bpy.types.Object]:
        try:
            rect = element.find('svg:rect', self.ns)
            if rect is None:
                print("No rect found in component")
                return None

            service_type = element.get('data-service', 'unknown')
            component_id = element.get('id', 'unknown')
            
            x = float(rect.get('x', 0)) / 100.0
            y = -float(rect.get('y', 0)) / 100.0
            width = float(rect.get('width', 1)) / 100.0
            height = float(rect.get('height', 1)) / 100.0
            
            bpy.ops.mesh.primitive_cube_add(location=(x, y, 0))
            obj = bpy.context.active_object
            obj.name = f"{service_type}_{component_id}"
            
            obj.scale.x = width / 2
            obj.scale.y = height / 2
            obj.scale.z = 0.1
            
            mat = bpy.data.materials.new(name=f"{obj.name}_material")
            mat.use_nodes = True
            color = (0.9, 0.5, 0.1, 1.0) if service_type == "lambda" else (0.5, 0.2, 0.9, 1.0)
            mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = color
            obj.data.materials.append(mat)
            
            print(f"Created {service_type} component at ({x}, {y})")
            self.components.append(obj)
            return obj
            
        except Exception as e:
            print(f"Component creation error: {str(e)}")
            return None

    def create_connection(self, element: ET.Element) -> Optional[bpy.types.Object]:
        try:
            path_data = element.get('d', '')
            points = self.parse_svg_path(path_data)
            if not points:
                return None
                
            curve_data = bpy.data.curves.new('connection', 'CURVE')
            curve_data.dimensions = '3D'
            
            spline = curve_data.splines.new('POLY')
            spline.points.add(1)
            
            for i, (x, y) in enumerate(points):
                spline.points[i].co = (x/100.0, -y/100.0, 0, 1)
                
            curve_obj = bpy.data.objects.new('connection', curve_data)
            curve_obj.data.bevel_depth = 0.02
            
            mat = bpy.data.materials.new(name="connection_material")
            mat.use_nodes = True
            mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.2, 0.2, 0.2, 1.0)
            curve_obj.data.materials.append(mat)
            
            bpy.context.scene.collection.objects.link(curve_obj)
            self.connections.append(curve_obj)
            print(f"Created connection with {len(points)} points")
            return curve_obj
            
        except Exception as e:
            print(f"Connection creation error: {str(e)}")
            return None

    def convert(self, svg_content: str) -> Dict[str, List[bpy.types.Object]]:
        try:
            self.components = []
            self.connections = []
            
            root = ET.fromstring(svg_content)
            components = root.findall(".//svg:g[@class='component aws-component']", self.ns)
            paths = root.findall(".//svg:path[@class='connection']", self.ns)
            
            print(f"\nFound {len(components)} components and {len(paths)} paths")
            
            for comp in components:
                self.create_component(comp)
                
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