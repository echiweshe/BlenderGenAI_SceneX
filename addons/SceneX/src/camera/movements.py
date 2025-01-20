# SceneX/src/camera/movements.py

import bpy
import math
from mathutils import Vector, Matrix, Euler
from typing import List, Optional, Union
from ..utils.logger import SceneXLogger
from ..scene.groups import Group

class CameraMovement:
    def __init__(self, camera_system):
        self.camera = camera_system.camera
        self.target = camera_system.target
        self.logger = SceneXLogger("CameraMovement")

    def dolly(self, distance: float, duration: int = 30):
        """Move camera forward/backward"""
        start_loc = self.camera.location.copy()
        direction = (self.target.location - start_loc).normalized()
        end_loc = start_loc + direction * distance

        self._animate_movement(start_loc, end_loc, duration)

    def orbit(self, angle: float, axis: str = 'Z', duration: int = 30):
        """Orbit around target"""
        center = self.target.location
        radius = (self.camera.location - center).length
        start_angle = math.atan2(self.camera.location.y - center.y, 
                               self.camera.location.x - center.x)

        for frame in range(duration + 1):
            current_angle = start_angle + (angle * frame / duration)
            if axis == 'Z':
                x = center.x + radius * math.cos(current_angle)
                y = center.y + radius * math.sin(current_angle)
                z = self.camera.location.z
            else:  # 'Y' axis
                x = center.x + radius * math.cos(current_angle)
                z = center.z + radius * math.sin(current_angle)
                y = self.camera.location.y

            self.camera.location = Vector((x, y, z))
            self.camera.keyframe_insert(data_path="location", frame=frame)

    def frame_object(self, obj: Union[bpy.types.Object, Group], padding: float = 1.2):
        """Frame camera to focus on object/group"""
        if isinstance(obj, Group):
            bounds = obj.get_bounds()
        else:
            bounds = [(min(v[i] for v in obj.bound_box), 
                      max(v[i] for v in obj.bound_box)) for i in range(3)]

        center = Vector(((bounds[0][0] + bounds[0][1])/2,
                        (bounds[1][0] + bounds[1][1])/2,
                        (bounds[2][0] + bounds[2][1])/2))

        size = max(bounds[0][1] - bounds[0][0],
                  bounds[1][1] - bounds[1][0],
                  bounds[2][1] - bounds[2][0])

        distance = size * padding
        self.target.location = center
        self.camera.location = center + Vector((0, -distance, distance/2))

    def fly_to(self, location: Vector, target: Optional[Vector] = None, 
               duration: int = 30):
        """Smoothly move camera to new position/target"""
        start_loc = self.camera.location.copy()
        start_target = self.target.location.copy()

        if target is None:
            target = self.target.location

        for frame in range(duration + 1):
            factor = frame / duration
            self.camera.location = start_loc.lerp(location, factor)
            self.target.location = start_target.lerp(target, factor)
            
            self.camera.keyframe_insert(data_path="location", frame=frame)
            self.target.keyframe_insert(data_path="location", frame=frame)

    def _animate_movement(self, start: Vector, end: Vector, duration: int):
        """Helper to animate camera movement"""
        for frame in range(duration + 1):
            factor = frame / duration
            self.camera.location = start.lerp(end, factor)
            self.camera.keyframe_insert(data_path="location", frame=frame)

    def set_orthographic(self, orthographic: bool = True):
        """Switch between orthographic and perspective"""
        self.camera.data.type = 'ORTHO' if orthographic else 'PERSP'
        if orthographic:
            self.camera.data.ortho_scale = 10.0