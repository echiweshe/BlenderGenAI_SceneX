# integrated-scenex/core/coordinate_system.py

import bpy
import mathutils
from typing import Dict, Any, Tuple, List
import numpy as np

class ManimCoordinateSystem:
    def __init__(self):
        self.unit_scale = 1.0
        self.origin = mathutils.Vector((0, 0, 0))
        self.scale = mathutils.Vector((1, 1, 1))
        
    def apply_to_scene(self, scene_data: Dict[str, Any]) -> Dict[str, Any]:
        transformed_scene = scene_data.copy()
        
        if "objects" in transformed_scene:
            transformed_scene["objects"] = [
                self._transform_object(obj) 
                for obj in transformed_scene["objects"]
            ]
            
        return transformed_scene
        
    def _transform_point(self, point: Tuple[float, float, float]) -> Tuple[float, float, float]:
        if isinstance(point, (tuple, list)):
            point = mathutils.Vector(point)
        transformed = (point - self.origin) * self.scale
        return tuple(transformed)