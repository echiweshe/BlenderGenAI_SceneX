# tests/example_scenes/test_transform_and_snap.py

import bpy
import sys
import os
import math
from mathutils import Vector

# Add parent directory to path to find SceneX package
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(script_dir))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)



# # Add SceneX to path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.core.scene import Scene
from src.animation.transform_between import TransformBetween, MorphBetween
from src.animation.base import AnimationConfig
from src.geometry.snapping import SnapSystem, SmartConnector
from src.animation.commonly_used_animations import FadeInFrom

class TransformTestScene(Scene):
    def __init__(self):
        super().__init__()
        self.snap_system = SnapSystem(grid_size=1.0)
        self.connector = SmartConnector()
        
    def construct(self):
        # Setup scene
        self.setup()
        
        # Create initial shapes
        cube = self.create_cube(size=1.0, location=(-3, 0, 0))
        sphere = self.create_sphere(radius=0.5, location=(3, 0, 0))
        cylinder = self.create_cylinder(radius=0.3, depth=2.0, location=(0, 2, 0))
        
        # Snap objects to grid
        for obj in [cube, sphere, cylinder]:
            self.snap_system.snap_to_grid(obj)
        
        # Create connections
        self.connector.connect_with_type(cube, sphere, 'DIRECT')
        self.connector.connect_with_type(sphere, cylinder, 'ARC')
        
        # Setup transform animation
        config = AnimationConfig(duration=60)
        transform = TransformBetween(cube, sphere, config)
        
        # Create animation sequence
        start_frame = 1
        
        # Fade in objects
        fade_config = AnimationConfig(duration=30)
        self.play(FadeInFrom(cube, Vector((0, 0, 1)), fade_config))
        self.play(FadeInFrom(sphere, Vector((0, 0, 1)), fade_config))
        self.play(FadeInFrom(cylinder, Vector((0, 0, 1)), fade_config))
        
        # Transform animation
        start_frame = 90  # Start after fade-ins
        transform.create_animation(start_frame)
        
        # Update timeline
        bpy.context.scene.frame_end = start_frame + config.duration

def run_test():
    # Clear existing scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    # Create and run test scene
    scene = TransformTestScene()
    scene.construct()

    
    # # Setup scene and render engine
    # bpy.ops.object.select_all(action='SELECT')
    # bpy.ops.object.delete()
    
    # bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'
    # if hasattr(bpy.context.scene.eevee, "use_ssr"):
    #     bpy.context.scene.eevee.use_ssr = True
    #     bpy.context.scene.eevee.use_ssr_refraction = True
    
    # # Configure viewport for rendered preview
    # for area in bpy.context.screen.areas:
    #     if area.type == 'VIEW_3D':
    #         for space in area.spaces:
    #             if space.type == 'VIEW_3D':
    #                 space.shading.type = 'RENDERED'
    #                 space.shading.use_scene_lights = True
    #                 space.shading.use_scene_world = True

    # # Set up camera to target origin
    # # bpy.ops.object.camera_add(location=(7, -7, 5))
    # # camera = bpy.context.active_object
    # # camera.rotation_euler = (math.radians(45), 0, math.radians(45))
    
    # bpy.ops.object.camera_add(location=(0, -10, 5))  # Move back for better view
    # camera = bpy.context.active_object
    # camera.rotation_euler = (math.radians(30), 0, 0)  # Less steep angle
    
    
    # # Add Empty at origin as camera target
    # bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
    # target = bpy.context.active_object
    # target.name = "CameraTarget"
    
    # # Add Track To constraint to camera
    # track = camera.constraints.new(type='TRACK_TO')
    # track.target = target
    # track.track_axis = 'TRACK_NEGATIVE_Z'
    # track.up_axis = 'UP_Y'
    
    # bpy.context.scene.camera = camera

    # # Add lighting
    # bpy.ops.object.light_add(type='SUN', location=(5, 5, 8))
    # sun = bpy.context.active_object
    # sun.data.energy = 3.0
    
    print("Test scene created successfully")

if __name__ == "__main__":
    run_test()