# SceneX/src/geometry/svg_handler.py

import bpy
import xml.etree.ElementTree as ET
import math
from pathlib import Path
from mathutils import Vector, Matrix
from ..utils.logger import SceneXLogger

class SVGHandler:
    def __init__(self):
        self.logger = SceneXLogger("SVGHandler")
        self.scale = 1.0
        self.commands = {
            'M': self._move_to,
            'L': self._line_to,
            'H': self._horizontal_line_to,
            'V': self._vertical_line_to,
            'C': self._cubic_bezier,
            'S': self._smooth_cubic_bezier,
            'Q': self._quadratic_bezier,
            'T': self._smooth_quadratic_bezier,
            'A': self._arc,
            'Z': self._close_path
        }

    def import_svg(self, filepath: str) -> bpy.types.Object:
        """Import SVG file and convert to Blender curves"""
        try:
            tree = ET.parse(filepath)
            root = tree.getroot()
            
            # Create empty collection for SVG parts
            collection = bpy.data.collections.new("SVG_Parts")
            bpy.context.scene.collection.children.link(collection)
            
            # Process SVG elements
            self._process_element(root, collection)
            
            return collection
            
        except Exception as e:
            self.logger.error(f"Error importing SVG: {str(e)}")
            return None

    def _process_element(self, element: ET.Element, collection: bpy.types.Collection):
        """Process SVG element and its children"""
        if element.tag.endswith('path'):
            path_data = element.get('d')
            if path_data:
                curve = self._create_curve_from_path(path_data)
                if curve:
                    collection.objects.link(curve)
                    
        for child in element:
            self._process_element(child, collection)

    def _create_curve_from_path(self, path_data: str) -> bpy.types.Object:
        """Convert SVG path data to Blender curve"""
        try:
            curve_data = bpy.data.curves.new('path', 'CURVE')
            curve_data.dimensions = '3D'
            
            spline = curve_data.splines.new('BEZIER')
            commands = self._parse_path_data(path_data)
            
            current_point = Vector((0, 0, 0))
            for cmd, params in commands:
                if cmd in self.commands:
                    current_point = self.commands[cmd](spline, current_point, params)
            
            curve_obj = bpy.data.objects.new('path', curve_data)
            return curve_obj
            
        except Exception as e:
            self.logger.error(f"Error creating curve: {str(e)}")
            return None

    def _parse_path_data(self, path_data: str) -> list:
        """Parse SVG path data into command list"""
        commands = []
        current_cmd = None
        current_params = []
        
        # Split path data into tokens
        tokens = path_data.replace(',', ' ').split()
        
        for token in tokens:
            if token[0].isalpha():
                if current_cmd:
                    commands.append((current_cmd, current_params))
                current_cmd = token
                current_params = []
            else:
                current_params.append(float(token))
                
        if current_cmd:
            commands.append((current_cmd, current_params))
            
        return commands

    # Path command implementations
    def _move_to(self, spline, current, params):
        point = Vector((params[0], params[1], 0)) * self.scale
        return point

    def _line_to(self, spline, current, params):
        point = Vector((params[0], params[1], 0)) * self.scale
        self._add_line_point(spline, current, point)
        return point

    def _horizontal_line_to(self, spline, current, params):
        point = Vector((params[0], current.y, 0)) * self.scale
        self._add_line_point(spline, current, point)
        return point

    def _vertical_line_to(self, spline, current, params):
        point = Vector((current.x, params[0], 0)) * self.scale
        self._add_line_point(spline, current, point)
        return point

    def _cubic_bezier(self, spline, current, params):
        c1 = Vector((params[0], params[1], 0)) * self.scale
        c2 = Vector((params[2], params[3], 0)) * self.scale
        end = Vector((params[4], params[5], 0)) * self.scale
        self._add_bezier_point(spline, current, c1, c2, end)
        return end

    def _add_line_point(self, spline, start, end):
        """Add line segment to spline"""
        spline.bezier_points.add(1)
        point = spline.bezier_points[-1]
        point.co = end
        point.handle_left = start
        point.handle_right = end

    def _add_bezier_point(self, spline, start, c1, c2, end):
        """Add bezier curve segment to spline"""
        spline.bezier_points.add(1)
        point = spline.bezier_points[-1]
        point.co = end
        point.handle_left = c1
        point.handle_right = c2

    def _close_path(self, spline, current, params):
        """Close the current path"""
        if len(spline.bezier_points) > 0:
            spline.use_cyclic_u = True
        return current