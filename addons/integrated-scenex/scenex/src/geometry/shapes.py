# SceneX/src/geometry/shapes.py
import bpy
import mathutils
import math
from typing import Optional, List, Tuple, Union

from src.geometry.base import Geometry
from src.utils.logger import SceneXLogger

class Line(Geometry):
    def __init__(self, start: Tuple[float, float, float], 
                 end: Tuple[float, float, float], **kwargs):
        super().__init__(**kwargs)
        self.start = mathutils.Vector(start)
        self.end = mathutils.Vector(end)
        
    def create(self) -> bpy.types.Object:
        """Create a line between two points"""
        # Create curve
        curve_data = bpy.data.curves.new('line', 'CURVE')
        curve_data.dimensions = '3D'
        
        # Create spline
        spline = curve_data.splines.new('POLY')
        spline.points.add(1)
        
        # Set points
        spline.points[0].co = (*self.start, 1)
        spline.points[1].co = (*self.end, 1)
        
        # Create object
        self.object = bpy.data.objects.new('line', curve_data)
        self.object.data.bevel_depth = self.stroke_width
        
        # Add material
        mat = bpy.data.materials.new(name="line_material")
        mat.use_nodes = True
        principled = mat.node_tree.nodes["Principled BSDF"]
        principled.inputs["Base Color"].default_value = self.color
        self.object.data.materials.append(mat)
        
        # Link to scene
        bpy.context.scene.collection.objects.link(self.object)
        return self.object

class Circle(Geometry):
    def __init__(self, radius: float = 1.0, 
                 segments: int = 32,
                 fill: bool = True, **kwargs):
        super().__init__(**kwargs)
        self.radius = radius
        self.segments = segments
        self.fill = fill
        
    def create(self) -> bpy.types.Object:
        """Create a circle"""
        if self.fill:
            bpy.ops.mesh.primitive_circle_add(
                vertices=self.segments,
                radius=self.radius,
                fill_type='TRIFAN'
            )
        else:
            bpy.ops.curve.primitive_bezier_circle_add(radius=self.radius)
            
        self.object = bpy.context.active_object
        
        # Add material
        mat = bpy.data.materials.new(name="circle_material")
        mat.use_nodes = True
        principled = mat.node_tree.nodes["Principled BSDF"]
        principled.inputs["Base Color"].default_value = self.color
        
        if not self.fill:
            self.object.data.bevel_depth = self.stroke_width
            
        self.object.data.materials.append(mat)
        return self.object

class Rectangle(Geometry):
    def __init__(self, width: float = 2.0, 
                 height: float = 1.0,
                 corner_radius: float = 0.0, **kwargs):
        super().__init__(**kwargs)
        self.width = width
        self.height = height
        self.corner_radius = corner_radius
        
    def create(self) -> bpy.types.Object:
        """Create a rectangle"""
        # Create vertices
        verts = []
        if self.corner_radius > 0:
            # Add rounded corners
            steps = 8  # Steps per corner
            for i in range(4):  # 4 corners
                cx = (self.width/2) * (1 if i in (0,3) else -1)
                cy = (self.height/2) * (1 if i < 2 else -1)
                for j in range(steps):
                    angle = math.pi/2 * (i + j/steps)
                    x = cx + self.corner_radius * math.cos(angle)
                    y = cy + self.corner_radius * math.sin(angle)
                    verts.append((x, y, 0))
        else:
            # Simple rectangle
            verts = [
                (self.width/2, self.height/2, 0),
                (-self.width/2, self.height/2, 0),
                (-self.width/2, -self.height/2, 0),
                (self.width/2, -self.height/2, 0)
            ]

        # Create mesh
        mesh = bpy.data.meshes.new("rectangle")
        mesh.from_pydata(verts, [], [list(range(len(verts)))])
        mesh.update()
        
        self.object = bpy.data.objects.new("rectangle", mesh)
        
        # Add material
        mat = bpy.data.materials.new(name="rectangle_material")
        mat.use_nodes = True
        principled = mat.node_tree.nodes["Principled BSDF"]
        principled.inputs["Base Color"].default_value = self.color
        self.object.data.materials.append(mat)
        
        bpy.context.scene.collection.objects.link(self.object)
        return self.object
    
# Square inherits from Rectangle - should we proceed with rate functions for animations?
class Square(Rectangle):
    def __init__(self, size: float = 1.0, **kwargs):
        super().__init__(width=size, height=size, **kwargs)