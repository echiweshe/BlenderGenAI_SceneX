# SceneX/tests/example_scenes/commonly_used_animations.py
import bpy
import mathutils
import math
from src.core.scene import Scene
from src.animation.transform import Transform, FadeIn, FadeOut, Scale
from src.animation.base import AnimationConfig
from src.animation.commonly_used_animations import (  # Updated import path
    GrowFromCenter, GrowFromPoint, Write, 
    FadeInFrom, Rotate, FlashAround
)

class AnimationTestScene(Scene):
    def create_text(self, content: str, location: tuple[float, float, float] = (0, 0, 0)) -> bpy.types.Object:
        bpy.ops.object.text_add(location=location)
        text_obj = bpy.context.object
        text_obj.data.body = content
        return text_obj

    def construct(self):
        self.logger.info("Starting animation test scene")
        
        # Clear scene and setup render engine
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
        
        # Set render engine and settings for Blender 4.2
        bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'  # Updated from BLENDER_EEVEE
        if hasattr(bpy.context.scene.eevee, "use_ssr"):  # Handle EEVEE Next settings
            bpy.context.scene.eevee.use_ssr = True
            bpy.context.scene.eevee.use_ssr_refraction = True
               
        # Add lighting
        bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
        sun = bpy.context.active_object
        sun.data.energy = 5.0
        
        # Configure viewport for rendered preview
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        space.shading.type = 'RENDERED'
                        space.shading.use_scene_lights = True
                        space.shading.use_scene_world = True
        
        # Create objects with initial materials
        cube = self.create_cube(size=1.0, location=(-2, 0, 0))
        sphere = self.create_sphere(radius=0.5, location=(2, 0, 0))
        
        # Setup initial materials with colors
        for obj, color in [(cube, (0.2, 0.4, 0.8, 1.0)), (sphere, (0.8, 0.2, 0.2, 1.0))]:
            mat = bpy.data.materials.new(name=f"{obj.name}_material")
            mat.use_nodes = True
            mat.blend_method = 'BLEND'
            principled = mat.node_tree.nodes["Principled BSDF"]
            principled.inputs["Base Color"].default_value = color
            if obj.data.materials:
                obj.data.materials[0] = mat
            else:
                obj.data.materials.append(mat)
        
        # Setup timeline (30fps)
        bpy.context.scene.render.fps = 30
        bpy.context.scene.frame_start = 1
        bpy.context.scene.frame_end = 300
        current_frame = 1
                
        # Test GrowFromCenter
        cube = self.create_cube(size=1.0)
        grow = GrowFromCenter(cube, AnimationConfig(duration=30))
        current_frame = grow.create_animation(1)
        
        # Test FadeInFrom
        sphere = self.create_sphere(radius=0.5, location=(2, 0, 0))
        fade_in = FadeInFrom(sphere, mathutils.Vector((-1, 0, 0)), 
                           config=AnimationConfig(duration=30))
        current_frame = fade_in.create_animation(current_frame + 10)
        
        # # Test Write
        text_obj = self.create_text("Hello", location=(-1, 1, 1))
        write_anim = Write(text_obj, AnimationConfig(duration=60))
        current_frame = write_anim.create_animation(current_frame)
        
        # Test Rotate
        rotate = Rotate(cube, math.radians(360), 'Z', 
                      AnimationConfig(duration=60))
        current_frame = rotate.create_animation(current_frame + 10)
        
        # Test FlashAround
        flash = FlashAround(sphere, config=AnimationConfig(duration=30))
        current_frame = flash.create_animation(current_frame + 10)

        # Set up camera
        bpy.ops.object.camera_add(location=(5, -5, 5))
        camera = bpy.context.active_object
        camera.rotation_euler = (math.radians(60), 0, math.radians(45))
        bpy.context.scene.camera = camera
        
        # Switch to camera view
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                area.spaces[0].region_3d.view_perspective = 'CAMERA'
        
        # Set current frame to start
        bpy.context.scene.frame_set(1)
        
        self.logger.info("Animation test scene completed")

def main():
    try:
        scene = AnimationTestScene()
        scene.construct()
        print("Animation test scene completed successfully")
        bpy.ops.screen.animation_play()
    except Exception as e:
        print(f"Error running animation test: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()