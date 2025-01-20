# SceneX/tests/example_scenes/7_text_test.py

import bpy
import math
from mathutils import Vector
from src.core.scene import Scene
from src.text.text_support import Text
from src.animation.commonly_used_animations import Write, FadeInFrom
from src.animation.base import AnimationConfig

class TextTestScene(Scene):
    def construct(self):
        self.logger.info("Starting text test scene")

        # Setup scene and render engine
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
        
        bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'
        if hasattr(bpy.context.scene.eevee, "use_ssr"):
            bpy.context.scene.eevee.use_ssr = True
            bpy.context.scene.eevee.use_ssr_refraction = True
        
        # Configure viewport
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        space.shading.type = 'RENDERED'
                        space.shading.use_scene_lights = True
                        space.shading.use_scene_world = True

        # Set up camera
        bpy.ops.object.camera_add(location=(7, -7, 5))
        camera = bpy.context.active_object
        camera.rotation_euler = (math.radians(45), 0, math.radians(45))
        
        bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
        target = bpy.context.active_object
        target.name = "CameraTarget"
        
        track = camera.constraints.new(type='TRACK_TO')
        track.target = target
        track.track_axis = 'TRACK_NEGATIVE_Z'
        track.up_axis = 'UP_Y'
        
        bpy.context.scene.camera = camera

        # Add lighting
        bpy.ops.object.light_add(type='SUN', location=(5, 5, 8))
        sun = bpy.context.active_object
        sun.data.energy = 3.0

        # Create text objects
        title = Text("SceneX Demo", size=1.0, 
                    color=(1, 1, 1, 1)).create()
        
        subtitle = Text("Math & Physics", size=0.6,
                       color=(0.2, 0.8, 1, 1)).create()

        # Position objects
        self.coordinate_system.place_object(title, Vector((0, 2, 0)))
        self.coordinate_system.place_object(subtitle, Vector((0, 1, 0)))

        # Switch to camera view
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                area.spaces[0].region_3d.view_perspective = 'CAMERA'
                area.spaces[0].show_gizmo = True

        # Set frame range
        bpy.context.scene.frame_start = 1
        bpy.context.scene.frame_end = 100
        bpy.context.scene.frame_current = 1

        # Create animations
        config = AnimationConfig(duration=50)
        
        animations = [
            Write(title, config=config),
            Write(subtitle, config=config)
        ]

        # Create keyframes
        current_frame = 1
        for anim in animations:
            start_frame = current_frame
            end_frame = start_frame + anim.config.duration
            anim.create_animation(start_frame)
            current_frame = end_frame

if __name__ == "__main__":
    scene = TextTestScene()
    scene.construct()
