# SceneX/src/core/coordinate_system.py
import bpy
import mathutils
from src.utils.logger import SceneXLogger
from dataclasses import dataclass
from typing import Optional, Tuple, List, Dict

@dataclass
class GridConfig:
    """Configuration for coordinate grid"""
    x_range: Tuple[float, float] = (-8, 8)
    y_range: Tuple[float, float] = (-4, 4)
    x_step: float = 1.0
    y_step: float = 1.0
    color: Tuple[float, float, float, float] = (0.2, 0.2, 0.2, 1.0)
    line_thickness: float = 0.02
    show_axes: bool = True
    axes_color: Tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0)
    show_numbers: bool = True
    number_scale: float = 0.3

class CoordinateSystem:
    """Manim-style coordinate system"""
    
    def __init__(self, origin=(0, 0, 0), scale=1.0):
        self.origin = mathutils.Vector(origin)
        self.scale = scale
        self.axes: Dict[str, bpy.types.Object] = {}
        self.grid_lines: List[bpy.types.Object] = []
        self.numbers: List[bpy.types.Object] = []
        self.logger = SceneXLogger("CoordinateSystem")

    def create_grid(self, config: Optional[GridConfig] = None):
        """Create Manim-style grid with axes"""
        if config is None:
            config = GridConfig()
            
        self.logger.info("Creating coordinate grid")
        try:
            self._create_axes(config)
            self._create_grid_lines(config)
            if config.show_numbers:
                self._create_numbers(config)
        except Exception as e:
            self.logger.error(f"Error creating grid: {str(e)}")

    def _create_axes(self, config: GridConfig):
        """Create x and y axes"""
        self.logger.info("Creating axes")
        
        # Create X axis
        x_start = mathutils.Vector((config.x_range[0], 0, 0)) * self.scale
        x_end = mathutils.Vector((config.x_range[1], 0, 0)) * self.scale
        self.axes['x'] = self._create_line(x_start, x_end, config.axes_color, config.line_thickness * 2)
        
        # Create Y axis
        y_start = mathutils.Vector((0, config.y_range[0], 0)) * self.scale
        y_end = mathutils.Vector((0, config.y_range[1], 0)) * self.scale
        self.axes['y'] = self._create_line(y_start, y_end, config.axes_color, config.line_thickness * 2)

    def _create_grid_lines(self, config: GridConfig):
        """Create grid lines"""
        self.logger.info("Creating grid lines")
        
        # Create vertical lines
        for x in range(int(config.x_range[0]), int(config.x_range[1]) + 1):
            if x == 0:  # Skip zero as it's the axis
                continue
            start = mathutils.Vector((x, config.y_range[0], 0)) * self.scale
            end = mathutils.Vector((x, config.y_range[1], 0)) * self.scale
            line = self._create_line(start, end, config.color, config.line_thickness)
            self.grid_lines.append(line)

        # Create horizontal lines
        for y in range(int(config.y_range[0]), int(config.y_range[1]) + 1):
            if y == 0:  # Skip zero as it's the axis
                continue
            start = mathutils.Vector((config.x_range[0], y, 0)) * self.scale
            end = mathutils.Vector((config.x_range[1], y, 0)) * self.scale
            line = self._create_line(start, end, config.color, config.line_thickness)
            self.grid_lines.append(line)

    def _create_line(self, start: mathutils.Vector, end: mathutils.Vector, 
                    color: Tuple[float, float, float, float], thickness: float) -> bpy.types.Object:
        """Create a single line"""
        # Create curve data
        curve_data = bpy.data.curves.new(name="line", type='CURVE')
        curve_data.dimensions = '3D'
        curve_data.resolution_u = 2
        
        # Create spline
        spline = curve_data.splines.new('POLY')
        spline.points.add(1)  # Add second point
        
        # Set coordinates
        spline.points[0].co = (*start, 1)
        spline.points[1].co = (*end, 1)
        
        # Create object
        line = bpy.data.objects.new("line", curve_data)
        line.data.bevel_depth = thickness
        
        # Create material
        mat = bpy.data.materials.new(name="line_material")
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        nodes["Principled BSDF"].inputs["Base Color"].default_value = color
        line.data.materials.append(mat)
        
        # Link to scene
        bpy.context.scene.collection.objects.link(line)
        
        return line

    def _create_numbers(self, config: GridConfig):
        """Create number labels for axes"""
        self.logger.info("Creating number labels")
        
        # Create x axis numbers
        for x in range(int(config.x_range[0]), int(config.x_range[1]) + 1):
            if x == 0:
                continue
            pos = mathutils.Vector((x, -0.3, 0)) * self.scale
            self._create_number_text(str(x), pos, config.number_scale)

        # Create y axis numbers
        for y in range(int(config.y_range[0]), int(config.y_range[1]) + 1):
            if y == 0:
                continue
            pos = mathutils.Vector((-0.3, y, 0)) * self.scale
            self._create_number_text(str(y), pos, config.number_scale)

    def _create_number_text(self, text: str, location: mathutils.Vector, scale: float):
        """Create a number text object"""
        bpy.ops.object.text_add(location=location)
        text_obj = bpy.context.active_object
        text_obj.data.body = text
        text_obj.scale = (scale, scale, scale)
        self.numbers.append(text_obj)

    def place_object(self, obj: bpy.types.Object, position: mathutils.Vector):
        """Place object using Manim-style coordinates"""
        world_pos = self.origin + position * self.scale
        obj.location = world_pos
        self.logger.debug(f"Placed object at world position: {world_pos}")