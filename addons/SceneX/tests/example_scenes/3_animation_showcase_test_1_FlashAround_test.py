# SceneX/tests/example_scenes/animation_showcase_test.py

# SceneX/tests/example_scenes/animation_showcase_test.py
import bpy
import mathutils
import math
from src.core.scene import Scene
from src.animation.base import AnimationConfig
from src.animation.commonly_used_animations import (
    GrowFromCenter, GrowFromPoint, Write, 
    FadeInFrom, Rotate, FlashAround
)

class AnimationShowcaseScene(Scene):
    def construct(self):
        self.logger.info("Starting animation showcase scene")
        
        # Setup scene and render engine
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
        
        bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'
        if hasattr(bpy.context.scene.eevee, "use_ssr"):
            bpy.context.scene.eevee.use_ssr = True
            bpy.context.scene.eevee.use_ssr_refraction = True
        
        # Configure viewport for rendered preview
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        space.shading.type = 'RENDERED'
                        space.shading.use_scene_lights = True
                        space.shading.use_scene_world = True

        # Setup timeline (30fps)
        bpy.context.scene.render.fps = 30
        bpy.context.scene.frame_start = 1
        bpy.context.scene.frame_end = 300
        current_frame = 1

        # Row 1 - Top objects
        # GrowFromCenter Demo
        self.logger.info("Testing GrowFromCenter")
        cube = self.create_cube(size=1.0, location=(-2, 2, 0))
        grow = GrowFromCenter(cube, AnimationConfig(duration=30))
        current_frame = grow.create_animation(current_frame)
        
        # GrowFromPoint Demo
        self.logger.info("Testing GrowFromPoint")
        sphere = self.create_sphere(radius=0.5, location=(0, 2, 0))
        point = mathutils.Vector((-1, 2, 0))
        grow_point = GrowFromPoint(sphere, point, AnimationConfig(duration=30))
        current_frame = grow_point.create_animation(current_frame + 10)
        
        # FadeInFrom Demo
        self.logger.info("Testing FadeInFrom")
        cube2 = self.create_cube(size=0.8, location=(2, 2, 0))
        fade_in = FadeInFrom(cube2, mathutils.Vector((-1, 1, 0)), 
                           distance=3.0, config=AnimationConfig(duration=45))
        current_frame = fade_in.create_animation(current_frame + 10)

        # Row 2 - Center row with text
        # Write Demo
        self.logger.info("Testing Write")
        text = self.create_text("Welcome to SceneX", location=(0, 0, 0))
        write = Write(text, AnimationConfig(duration=60))
        current_frame = write.create_animation(current_frame + 10)

        # Row 3 - Bottom objects
        # Rotate Demo
        self.logger.info("Testing Rotate")
        cylinder = self.create_cylinder(radius=0.3, depth=1.5, location=(-2, -2, 0))
        rotate = Rotate(cylinder, math.radians(360), 'Z', 
                       config=AnimationConfig(duration=60))
        current_frame = rotate.create_animation(current_frame + 10)

        # FlashAround Demo
        self.logger.info("Testing FlashAround")
        target_sphere = self.create_sphere(radius=0.7, location=(2, -2, 0))
        flash = FlashAround(target_sphere, color=(1, 1, 0), 
                          config=AnimationConfig(duration=45))
        current_frame = flash.create_animation(current_frame + 10)

        # Set up camera
        bpy.ops.object.camera_add(location=(7, -7, 5))
        camera = bpy.context.active_object
        camera.rotation_euler = (math.radians(45), 0, math.radians(45))
        bpy.context.scene.camera = camera

        # Add lighting
        bpy.ops.object.light_add(type='SUN', location=(5, 5, 8))
        sun = bpy.context.active_object
        sun.data.energy = 3.0

        # Switch to camera view
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                area.spaces[0].region_3d.view_perspective = 'CAMERA'
                area.spaces[0].show_gizmo = True

        # Return to start
        bpy.context.scene.frame_set(1)
        
        self.logger.info("Animation showcase completed")

def main():
    try:
        scene = AnimationShowcaseScene()
        scene.construct()
        print("Animation showcase completed successfully")
        bpy.ops.screen.animation_play()
    except Exception as e:
        print(f"Error running animation showcase: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()