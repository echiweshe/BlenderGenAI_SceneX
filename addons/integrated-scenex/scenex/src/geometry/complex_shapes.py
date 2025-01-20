# SceneX/src/geometry/complex_shapes.py
import bpy
import mathutils
import math
from .base import Geometry
from typing import Optional, List, Tuple

class Arrow(Geometry):
    def __init__(self, 
                 start: Tuple[float, float, float],
                 end: Tuple[float, float, float],
                 head_length: float = 0.2,
                 head_width: float = 0.1,
                 **kwargs):
        super().__init__(**kwargs)
        self.start = mathutils.Vector(start)
        self.end = mathutils.Vector(end)
        self.head_length = head_length
        self.head_width = head_width

    def create(self) -> bpy.types.Object:
        direction = (self.end - self.start).normalized()
        length = (self.end - self.start).length
        right = direction.cross(mathutils.Vector((0, 0, 1)))
        
        # Create vertices for arrow head
        tip = self.end
        base = self.end - direction * self.head_length
        left_vert = base + right * self.head_width
        right_vert = base - right * self.head_width
        
        # Create shaft vertices
        shaft_width = self.head_width * 0.3
        shaft_left = self.start + right * shaft_width
        shaft_right = self.start - right * shaft_width
        
        verts = [self.start, shaft_left, shaft_right, left_vert, right_vert, tip]
        faces = [(0, 1, 2), (1, 3, 4, 2), (3, 5, 4)]

        mesh = bpy.data.meshes.new("arrow")
        mesh.from_pydata(verts, [], faces)
        mesh.update()

        self.object = bpy.data.objects.new("arrow", mesh)
        self._setup_material()
        bpy.context.scene.collection.objects.link(self.object)
        return self.object

class Arc(Geometry):
    def __init__(self, 
                 radius: float = 1.0,
                 start_angle: float = 0,
                 end_angle: float = math.pi/2,
                 segments: int = 32,
                 **kwargs):
        super().__init__(**kwargs)
        self.radius = radius
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.segments = segments

    def create(self) -> bpy.types.Object:
        curve = bpy.data.curves.new('arc', 'CURVE')
        curve.dimensions = '3D'
        
        spline = curve.splines.new('BEZIER')
        angle_range = self.end_angle - self.start_angle
        points_count = int(self.segments * (angle_range / (2 * math.pi)))
        spline.bezier_points.add(points_count - 1)
        
        for i in range(points_count):
            angle = self.start_angle + (angle_range * i / (points_count - 1))
            x = math.cos(angle) * self.radius
            y = math.sin(angle) * self.radius
            point = spline.bezier_points[i]
            point.co = (x, y, 0)
            point.handle_left_type = 'AUTO'
            point.handle_right_type = 'AUTO'
        
        self.object = bpy.data.objects.new('arc', curve)
        self.object.data.bevel_depth = self.stroke_width
        self._setup_material()
        bpy.context.scene.collection.objects.link(self.object)
        return self.object

class Star(Geometry):
    def __init__(self,
                 points: int = 5,
                 outer_radius: float = 1.0,
                 inner_radius: float = 0.5,
                 **kwargs):
        super().__init__(**kwargs)
        self.points = points
        self.outer_radius = outer_radius
        self.inner_radius = inner_radius

    def create(self) -> bpy.types.Object:
        verts = []
        point_angle = math.pi / self.points
        
        for i in range(self.points * 2):
            radius = self.outer_radius if i % 2 == 0 else self.inner_radius
            angle = i * point_angle
            x = math.cos(angle) * radius
            y = math.sin(angle) * radius
            verts.append((x, y, 0))

        faces = [list(range(len(verts)))]
        mesh = bpy.data.meshes.new("star")
        mesh.from_pydata(verts, [], faces)
        mesh.update()

        self.object = bpy.data.objects.new("star", mesh)
        self._setup_material()
        bpy.context.scene.collection.objects.link(self.object)
        return self.object
