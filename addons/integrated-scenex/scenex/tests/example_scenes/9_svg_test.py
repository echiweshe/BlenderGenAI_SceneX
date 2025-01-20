# tests/example_scenes/9_svg_test.py

import bpy
import sys
import os
from pathlib import Path

# Add parent directory to path to find SceneX package
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(script_dir))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from src.core.scene import Scene
from src.svg.svg_handler import SVGHandler
from src.camera.camera import CameraConfig, CameraSystem
from src.animation.commonly_used_animations import FadeInFrom
from src.animation.base import AnimationConfig

class SVGTestScene(Scene):
    def __init__(self):
        super().__init__()
        self.svg_handler = SVGHandler()
        
    def construct(self):
        # Setup scene
        self.setup()
        
        # Set camera for better view
        camera_config = CameraConfig(
            frame_width=14.0,
            frame_height=8.0,
            position=(0, -10, 5)
        )
        self.camera = CameraSystem(camera_config)
        
        # Import SVG with moderate scale
        svg_container = self.svg_handler.import_svg(
            "SceneX_logo.svg",
            scale=2.0,  # More reasonable scale
            location=(0, 0, 0)  # Center at origin
        )
        
        if not svg_container:
            self.logger.error("Failed to import SVG")
            return
            
        # Get SVG dimensions for reference
        dimensions = self.svg_handler.get_svg_dimensions(svg_container)
        self.logger.info(f"SVG dimensions: {dimensions}")
        
        # Add fade-in animation - now using Vector for direction
        config = AnimationConfig(duration=30)
        direction = Vector((0, 0, 1))  # Convert tuple to Vector
        self.play(FadeInFrom(svg_container, direction=direction, config=config))

def test_svg():
    # Clear existing scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    # Create and run test scene
    scene = SVGTestScene()
    scene.construct()
    
    print("SVG test scene completed")

if __name__ == "__main__":
    test_svg()