# SceneX/src/geometry/alignment.py

import bpy
from enum import Enum
from typing import List, Tuple
from mathutils import Vector
from ..utils.logger import SceneXLogger

class AlignmentType(Enum):
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    TOP = 'TOP'
    BOTTOM = 'BOTTOM'
    CENTER = 'CENTER'
    DISTRIBUTE_H = 'DISTRIBUTE_H'
    DISTRIBUTE_V = 'DISTRIBUTE_V'

class AlignmentHandler:
    def __init__(self):
        self.logger = SceneXLogger("AlignmentHandler")

    def align_objects(self, objects: List[bpy.types.Object], align_type: AlignmentType):
        if not objects:
            return

        bounds = self._get_group_bounds(objects)
        
        for obj in objects:
            if align_type == AlignmentType.LEFT:
                obj.location.x = bounds.min.x
            elif align_type == AlignmentType.RIGHT:
                obj.location.x = bounds.max.x
            elif align_type == AlignmentType.TOP:
                obj.location.y = bounds.max.y
            elif align_type == AlignmentType.BOTTOM:
                obj.location.y = bounds.min.y
            elif align_type == AlignmentType.CENTER:
                center = (bounds.min + bounds.max) / 2
                obj.location.x = center.x
                obj.location.y = center.y

    def distribute_objects(self, objects: List[bpy.types.Object], 
                         spacing: float = 1.0, 
                         direction: AlignmentType = AlignmentType.DISTRIBUTE_H):
        if not objects:
            return

        sorted_objects = sorted(objects, 
            key=lambda obj: obj.location.x if direction == AlignmentType.DISTRIBUTE_H 
            else obj.location.y)

        bounds = self._get_group_bounds(objects)
        total_distance = (bounds.max - bounds.min).length
        interval = total_distance / (len(objects) - 1) if len(objects) > 1 else 0

        for i, obj in enumerate(sorted_objects):
            if direction == AlignmentType.DISTRIBUTE_H:
                obj.location.x = bounds.min.x + (i * interval)
            else:
                obj.location.y = bounds.min.y + (i * interval)

    def grid_arrange(self, objects: List[bpy.types.Object], 
                    rows: int, cols: int, 
                    spacing: Tuple[float, float] = (1.0, 1.0)):
        if not objects:
            return

        x_spacing, y_spacing = spacing
        for i, obj in enumerate(objects):
            row = i // cols
            col = i % cols
            obj.location.x = col * x_spacing
            obj.location.y = -row * y_spacing

    def _get_group_bounds(self, objects: List[bpy.types.Object]):
        """Calculate bounding box for group of objects"""
        vertices = []
        for obj in objects:
            for v in obj.bound_box:
                world_v = obj.matrix_world @ Vector((v[0], v[1], v[2]))
                vertices.append(world_v)

        min_v = Vector((min(v.x for v in vertices),
                       min(v.y for v in vertices),
                       min(v.z for v in vertices)))
        max_v = Vector((max(v.x for v in vertices),
                       max(v.y for v in vertices),
                       max(v.z for v in vertices)))

        return type('Bounds', (), {'min': min_v, 'max': max_v})()

    def snap_to_grid(self, obj: bpy.types.Object, grid_size: float = 1.0):
        """Snap object to nearest grid point"""
        obj.location.x = round(obj.location.x / grid_size) * grid_size
        obj.location.y = round(obj.location.y / grid_size) * grid_size
        obj.location.z = round(obj.location.z / grid_size) * grid_size

    def align_to_axis(self, objects: List[bpy.types.Object], axis: str = 'X'):
        """Align objects along specified axis"""
        if not objects:
            return
            
        avg = sum((obj.location[axis.lower()] for obj in objects)) / len(objects)
        for obj in objects:
            setattr(obj.location, axis.lower(), avg)