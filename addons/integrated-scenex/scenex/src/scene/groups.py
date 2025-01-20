# SceneX/src/scene/groups.py

import bpy
from typing import List, Optional
from mathutils import Vector, Matrix
from ..utils.logger import SceneXLogger

class Group:
    def __init__(self, name: str):
        self.name = name
        self.objects: List[bpy.types.Object] = []
        self.subgroups: List['Group'] = []
        self.parent: Optional['Group'] = None
        self.empty_center: Optional[bpy.types.Object] = None
        self.logger = SceneXLogger("Group")

    def add(self, *objects_or_groups) -> 'Group':
        for item in objects_or_groups:
            if isinstance(item, bpy.types.Object):
                self.objects.append(item)
            elif isinstance(item, Group):
                self.subgroups.append(item)
                item.parent = self
        self._update_center()
        return self

    def remove(self, *objects_or_groups) -> 'Group':
        for item in objects_or_groups:
            if isinstance(item, bpy.types.Object) and item in self.objects:
                self.objects.remove(item)
            elif isinstance(item, Group) and item in self.subgroups:
                self.subgroups.remove(item)
                item.parent = None
        self._update_center()
        return self

    def _update_center(self):
        if not self.empty_center:
            self.empty_center = bpy.data.objects.new("empty", None)
            bpy.context.scene.collection.objects.link(self.empty_center)
        
        all_objects = self.get_all_objects()
        if all_objects:
            center = Vector((0, 0, 0))
            for obj in all_objects:
                center += obj.location
            center /= len(all_objects)
            self.empty_center.location = center

    def get_all_objects(self) -> List[bpy.types.Object]:
        all_objects = self.objects.copy()
        for subgroup in self.subgroups:
            all_objects.extend(subgroup.get_all_objects())
        return all_objects

    def apply_transform(self, matrix: Matrix):
        if self.empty_center:
            current_matrix = self.empty_center.matrix_world.copy()
            for obj in self.get_all_objects():
                obj.matrix_world = matrix @ current_matrix.inverted() @ obj.matrix_world

    def get_bounds(self) -> tuple:
        all_objects = self.get_all_objects()
        if not all_objects:
            return None
            
        min_x = min_y = min_z = float('inf')
        max_x = max_y = max_z = float('-inf')
        
        for obj in all_objects:
            bounds = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
            min_x = min(min_x, *(b.x for b in bounds))
            min_y = min(min_y, *(b.y for b in bounds))
            min_z = min(min_z, *(b.z for b in bounds))
            max_x = max(max_x, *(b.x for b in bounds))
            max_y = max(max_y, *(b.y for b in bounds))
            max_z = max(max_z, *(b.z for b in bounds))
            
        return ((min_x, min_y, min_z), (max_x, max_y, max_z))

    def get_center(self) -> Vector:
        bounds = self.get_bounds()
        if bounds:
            min_point, max_point = bounds
            return Vector((
                (min_point[0] + max_point[0]) / 2,
                (min_point[1] + max_point[1]) / 2,
                (min_point[2] + max_point[2]) / 2
            ))
        return Vector((0, 0, 0))