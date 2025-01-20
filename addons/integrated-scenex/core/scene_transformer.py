# integrated-scenex/core/scene_transformer.py

from typing import Dict, Any
import mathutils
from .coordinate_system import ManimCoordinateSystem

class SceneTransformer:
    def __init__(self):
        self.coords = ManimCoordinateSystem()
        
    def transform_blender_script(self, script: str) -> str:
        """Transform Blender script to use Manim coordinates"""
        # Extract location values
        import re
        
        # Transform location coordinates
        def replace_location(match):
            coords = eval(match.group(1))
            transformed = self.coords._transform_point(coords)
            return f"location={transformed}"
            
        # Replace location tuples in script
        script = re.sub(
            r'location=\(([-\d., ]+)\)',
            replace_location,
            script
        )
        
        return script

    def transform_position(self, x: float, y: float, z: float) -> tuple:
        """Transform single position"""
        return self.coords._transform_point((x, y, z))