# SceneX/tests/example_scenes/animation_test_scene.py
import bpy
import mathutils
import math
from src.core.scene import Scene
from src.animation.transform import Transform, FadeIn, FadeOut, Scale
from src.animation.base import AnimationConfig

class AnimationTestScene(Scene):
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
        
        # Animation sequence
        # Fade In (2 seconds)
        fade_in_config = AnimationConfig(duration=60)
        fade_in1 = FadeIn(cube, fade_in_config)
        fade_in2 = FadeIn(sphere, fade_in_config)
        current_frame = fade_in1.create_animation(current_frame)
        current_frame = fade_in2.create_animation(current_frame)
        
        # Transform and scale during full visibility (4 seconds)
        current_frame += 30  # Small pause after fade in
        
        transform_config = AnimationConfig(duration=120)
        end_state = {
            "location": mathutils.Vector((2, 2, 2)),
            "rotation": mathutils.Euler((math.radians(45), 0, 0)),
            "scale": mathutils.Vector((2, 2, 2))
        }
        transform = Transform(cube, end_state, transform_config)
        current_frame = transform.create_animation(current_frame)
        
        scale = Scale(sphere, 2.0, transform_config)
        current_frame = scale.create_animation(current_frame)
        
        # Fade Out (2 seconds)
        current_frame += 30  # Small pause before fade out
        fade_out_config = AnimationConfig(duration=60)
        fade_out1 = FadeOut(cube, fade_out_config)
        fade_out2 = FadeOut(sphere, fade_out_config)
        current_frame = fade_out1.create_animation(current_frame)
        current_frame = fade_out2.create_animation(current_frame)
        
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