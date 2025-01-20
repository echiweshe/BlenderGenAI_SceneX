import bpy
import xml.etree.ElementTree as ET
import math
from typing import Dict, List, Optional, Tuple
from mathutils import Vector

class SVGToSceneConverter:
    def __init__(self):
        self.components = []
        self.connections = []
        self.ns = {'svg': 'http://www.w3.org/2000/svg'}
        self.scale_factor = 0.01  # Reduced scale for better sizing
        self.component_depth = 0.2
        self.connection_thickness = 0.02
        
    def create_component(self, element: ET.Element) -> Optional[bpy.types.Object]:
        try:
            rect = element.find('svg:rect', self.ns)
            if not rect:
                return None

            # Get component info
            service_type = element.get('data-service', 'unknown')
            component_id = element.get('id', 'unknown')
            
            # Parse position, ensuring center alignment
            x = float(rect.get('x', 0)) 
            y = -float(rect.get('y', 0))  # Invert Y coordinate
            width = float(rect.get('width', 64))
            height = float(rect.get('height', 64))
            
            # Calculate center position
            center_x = (x + width/2) * self.scale_factor
            center_y = (y - height/2) * self.scale_factor
            
            # Create cube
            bpy.ops.mesh.primitive_cube_add(location=(center_x, center_y, 0))
            obj = bpy.context.active_object
            obj.name = f"{service_type}_{component_id}"
            
            # Scale to match SVG dimensions
            obj.scale = (width * self.scale_factor / 2, 
                        height * self.scale_factor / 2,
                        self.component_depth)
            
            # Set up material
            mat = bpy.data.materials.new(name=f"{obj.name}_material")
            mat.use_nodes = True
            nodes = mat.node_tree.nodes
            principled = nodes["Principled BSDF"]
            
            # Set color based on service type
            if service_type == "lambda":
                color = (0.95, 0.45, 0.1, 1.0)  # Orange
            else:
                color = (0.45, 0.2, 0.95, 1.0)  # Purple
                
            principled.inputs["Base Color"].default_value = color
            obj.data.materials.append(mat)
            
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
                
            # Parse path data
            points = []
            for cmd_match in path_data.split():
                if cmd_match.startswith('M') or cmd_match.startswith('L'):
                    coords = cmd_match[1:].split(',')
                    if len(coords) >= 2:
                        x = float(coords[0])
                        y = float(coords[1])
                        points.append((
                            x * self.scale_factor,
                            -y * self.scale_factor,
                            0
                        ))
                        
            if len(points) < 2:
                return None
                
            # Create curve object
            curve = bpy.data.curves.new('connection', 'CURVE')
            curve.dimensions = '3D'
            
            # Create spline
            spline = curve.splines.new('POLY')
            spline.points.add(len(points) - 1)
            
            # Set points
            for i, point in enumerate(points):
                spline.points[i].co = (*point, 1)
                
            # Create curve object
            curve_obj = bpy.data.objects.new('connection', curve)
            curve_obj.data.bevel_depth = self.connection_thickness
            
            # Create material
            mat = bpy.data.materials.new(name="connection_material")
            mat.use_nodes = True
            nodes = mat.node_tree.nodes
            principled = nodes["Principled BSDF"]
            principled.inputs["Base Color"].default_value = (0.1, 0.1, 0.1, 1.0)
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
            
            # Parse SVG
            root = ET.fromstring(svg_content)
            print("Parsed SVG structure:")
            self._print_element(root)
            
            # Process components
            components = root.findall(".//svg:g[@class='component aws-component']", self.ns)
            print(f"\nFound {len(components)} component elements")
            
            for comp in components:
                print("\nProcessing component element:")
                self._print_element(comp)
                self.create_component(comp)
                
            # Process connections
            paths = root.findall(".//svg:path[@class='connection']", self.ns)
            print(f"\nFound {len(paths)} connection paths")
            
            for path in paths:
                print("\nProcessing connection element:")
                self._print_element(path)
                self.create_connection(path)
                
            return {
                'components': self.components,
                'connections': self.connections
            }
            
        except Exception as e:
            print(f"Conversion error: {str(e)}")
            return {'components': [], 'connections': []}
            
    def _print_element(self, elem: ET.Element, level: int = 0):
        indent = "  " * level
        print(f"{indent}Tag: {elem.tag}")
        print(f"{indent}Attributes: {elem.attrib}")
        if elem.text and elem.text.strip():
            print(f"{indent}Text: {elem.text.strip()}")
        for child in elem:
            self._print_element(child, level + 1)