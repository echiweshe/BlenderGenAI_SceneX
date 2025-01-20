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
        
        # Clear existing objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

        # Add lighting
        bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
        sun = bpy.context.active_object
        sun.data.energy = 5.0

        # Configure viewport for better visibility
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        space.shading.type = 'MATERIAL'
                        space.shading.use_scene_lights = True
                        space.shading.use_scene_world = True

        # Create objects with initial materials
        cube = self.create_cube(size=1.0, location=(-2, 0, 0))
        sphere = self.create_sphere(radius=0.5, location=(2, 0, 0))
        
        # Set up materials with color for better visibility
        for obj in [cube, sphere]:
            mat = bpy.data.materials.new(name=f"{obj.name}_material")
            mat.use_nodes = True
            principled = mat.node_tree.nodes.get('Principled BSDF')
            if principled:
                # Set a base color (blue for cube, red for sphere)
                if obj == cube:
                    principled.inputs['Base Color'].default_value = (0.2, 0.4, 0.8, 1.0)
                else:
                    principled.inputs['Base Color'].default_value = (0.8, 0.2, 0.2, 1.0)
            
            if obj.data.materials:
                obj.data.materials[0] = mat
            else:
                obj.data.materials.append(mat)

        # Setup timeline
        bpy.context.scene.frame_start = 1
        bpy.context.scene.frame_end = 300
        current_frame = 1
        
        # Animation sequence
        fade_in_config = AnimationConfig(duration=30, ease_type='EASE_IN')
        fade_in1 = FadeIn(cube, fade_in_config)
        fade_in2 = FadeIn(sphere, fade_in_config)
        current_frame = fade_in1.create_animation(current_frame)
        current_frame = fade_in2.create_animation(current_frame)
        
        # Transform cube
        transform_config = AnimationConfig(duration=60)
        end_state = {
            "location": mathutils.Vector((2, 2, 2)),
            "rotation": mathutils.Euler((math.radians(45), 0, 0)),
            "scale": mathutils.Vector((2, 2, 2))
        }
        transform = Transform(cube, end_state, transform_config)
        current_frame = transform.create_animation(current_frame + 10)
        
        # Scale sphere
        scale_config = AnimationConfig(duration=30, ease_type='EASE_OUT')
        scale = Scale(sphere, 2.0, scale_config)
        current_frame = scale.create_animation(current_frame + 10)
        
        # Fade out both objects
        fade_out_config = AnimationConfig(duration=30, ease_type='EASE_IN_OUT')
        fade_out1 = FadeOut(cube, fade_out_config)
        fade_out2 = FadeOut(sphere, fade_out_config)
        current_frame = fade_out1.create_animation(current_frame + 30)
        current_frame = fade_out2.create_animation(current_frame)

        # Set up camera for better view
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