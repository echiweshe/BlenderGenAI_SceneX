# File: /home/ernestc/.config/blender/4.3/scripts/addons/BelnderGenAI/core/svg_converter.py

import bpy
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Tuple
import re

class SVGToSceneConverter:
    def __init__(self):
        self.components = []
        self.connections = []

    def get_tag(self, name: str) -> str:
        """Construct full tag name with namespace."""
        return f"{{{http://www.w3.org/2000/svg}}}{name}"

    def find_element(self, parent: ET.Element, tag: str, **attrs) -> List[ET.Element]:
        """Find elements with specified tag and attributes."""
        full_tag = self.get_tag(tag)
        elements = []
        for elem in parent.iter(full_tag):
            if all(elem.get(k) == v for k, v in attrs.items()):
                elements.append(elem)
        return elements

    def create_component(self, element: ET.Element) -> Optional[bpy.types.Object]:
        try:
            rect = next(element.iter(self.get_tag('rect')), None)
            if not rect:
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
            
            obj.scale = (width/2, height/2, 0.1)
            
            mat = bpy.data.materials.new(name=f"{obj.name}_material")
            mat.use_nodes = True
            color = (0.9, 0.5, 0.1, 1.0) if service_type == "lambda" else (0.5, 0.2, 0.9, 1.0)
            mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = color
            obj.data.materials.append(mat)
            
            print(f"Created {service_type} at ({x}, {y})")
            self.components.append(obj)
            return obj
            
        except Exception as e:
            print(f"Component creation error: {str(e)}")
            return None

    def create_connection(self, path_element: ET.Element) -> Optional[bpy.types.Object]:
        try:
            d = path_element.get('d', '')
            if not d:
                return None

            # Parse path data
            parts = re.findall(r'[ML]\s+(-?\d*\.?\d+)\s+(-?\d*\.?\d+)', d)
            if len(parts) != 2:
                return None

            # Create curve
            curve = bpy.data.curves.new('connection', 'CURVE')
            curve.dimensions = '3D'
            spline = curve.splines.new('POLY')
            spline.points.add(1)

            # Set points
            for i, (x, y) in enumerate(parts):
                spline.points[i].co = (float(x)/100.0, -float(y)/100.0, 0, 1)
            
            # Create object
            obj = bpy.data.objects.new('connection', curve)
            obj.data.bevel_depth = 0.02
            
            # Add material
            mat = bpy.data.materials.new(name="connection_material")
            mat.use_nodes = True
            mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.2, 0.2, 0.2, 1.0)
            obj.data.materials.append(mat)

            bpy.context.scene.collection.objects.link(obj)
            self.connections.append(obj)
            return obj

        except Exception as e:
            print(f"Connection creation error: {str(e)}")
            return None

    def convert(self, svg_content: str) -> Dict[str, List[bpy.types.Object]]:
        try:
            self.components = []
            self.connections = []
            
            root = ET.fromstring(svg_content)
            print("Parsing SVG...")

            # Find components and connections
            components = self.find_element(root, 'g', **{'class': 'component aws-component'})
            print(f"Found {len(components)} component elements")
            
            paths = self.find_element(root, 'path', **{'class': 'connection'})
            print(f"Found {len(paths)} connection paths")

            # Create objects
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