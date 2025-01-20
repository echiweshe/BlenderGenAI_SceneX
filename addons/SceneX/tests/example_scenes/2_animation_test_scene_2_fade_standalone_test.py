# SceneX/tests/example_scenes/fade_test_simple.py
import bpy
import math

def create_test_scene():
    # Clear existing scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    # Set up scene timing (assuming 30fps)
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = 180  # 6 seconds total
    bpy.context.scene.render.fps = 30
    
    # Create a cube
    bpy.ops.mesh.primitive_cube_add(size=2.0, location=(0, 0, 0))
    cube = bpy.context.active_object
    
    # Create and setup material for transparency
    mat = bpy.data.materials.new(name="FadeMaterial")
    mat.use_nodes = True
    mat.blend_method = 'BLEND'
    
    # Get the principled BSDF node
    principled = mat.node_tree.nodes["Principled BSDF"]
    principled.inputs["Base Color"].default_value = (0.8, 0.1, 0.1, 1.0)  # Red color
    
    # Assign material to cube
    cube.data.materials.append(mat)
    
    # Set up animation keyframes for fading
    # Fade in: 0-2 seconds (frames 1-60)
    principled.inputs['Alpha'].default_value = 0
    principled.inputs['Alpha'].keyframe_insert(data_path="default_value", frame=1)
    principled.inputs['Alpha'].default_value = 1
    principled.inputs['Alpha'].keyframe_insert(data_path="default_value", frame=60)
    
    # Full visibility: 2-4 seconds (frames 60-120)
    principled.inputs['Alpha'].default_value = 1
    principled.inputs['Alpha'].keyframe_insert(data_path="default_value", frame=120)
    
    # Fade out: 4-6 seconds (frames 120-180)
    principled.inputs['Alpha'].default_value = 0
    principled.inputs['Alpha'].keyframe_insert(data_path="default_value", frame=180)
    
    # Set up camera
    bpy.ops.object.camera_add(location=(5, -5, 5))
    camera = bpy.context.active_object
    camera.rotation_euler = (math.radians(60), 0, math.radians(45))
    bpy.context.scene.camera = camera
    
    # Add lighting
    bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
    sun = bpy.context.active_object
    sun.data.energy = 5.0
    
    # Set up viewport
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    # Set to rendered view
                    space.shading.type = 'RENDERED'
                    # Switch to camera view
                    space.region_3d.view_perspective = 'CAMERA'
    
    # Set up render engine
    bpy.context.scene.render.engine = 'BLENDER_EEVEE'
    bpy.context.scene.eevee.use_ssr = True
    bpy.context.scene.eevee.use_ssr_refraction = True
    
    # Return to frame 1
    bpy.context.scene.frame_set(1)

def main():
    try:
        create_test_scene()
        print("Test scene created successfully")
        # Start animation playback
        bpy.ops.screen.animation_play()
    except Exception as e:
        print(f"Error creating test scene: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()