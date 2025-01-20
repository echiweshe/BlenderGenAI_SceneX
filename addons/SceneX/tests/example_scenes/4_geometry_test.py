# SceneX/tests/example_scenes/geometry_test.py
import bpy
import mathutils
import math
from src.core.scene import Scene

from src.geometry.shapes import (
    Line, Circle, Rectangle
)

class GeometryTestScene(Scene):
    def construct(self):
        self.logger.info("Starting geometry test scene")

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

        # # Setup timeline (30fps)
        # bpy.context.scene.render.fps = 30
        # bpy.context.scene.frame_start = 1
        # bpy.context.scene.frame_end = 300
        # current_frame = 1

        
        # Create various geometric objects
        # Line
        line = Line((-2, 0, 0), (2, 0, 0), 
                   color=(1, 0, 0, 1),
                   stroke_width=0.05)
        line.create()
        
        # Circle
        circle = Circle(radius=1.0,
                       color=(0, 1, 0, 1),
                       fill_opacity=0.5)
        circle.create()
        circle.align_to_grid(mathutils.Vector((0, 2, 0)))
        
        # Rectangle
        rect = Rectangle(width=2.0, height=1.0,
                        corner_radius=0.2,
                        color=(0, 0, 1, 1))
        rect.create()
        rect.align_to_grid(mathutils.Vector((0, -2, 0)))

        # Set up camera to target origin
        bpy.ops.object.camera_add(location=(7, -7, 5))
        camera = bpy.context.active_object
        camera.rotation_euler = (math.radians(45), 0, math.radians(45))
        
        # Add Empty at origin as camera target
        bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
        target = bpy.context.active_object
        target.name = "CameraTarget"
        
        # Add Track To constraint to camera
        track = camera.constraints.new(type='TRACK_TO')
        track.target = target
        track.track_axis = 'TRACK_NEGATIVE_Z'
        track.up_axis = 'UP_Y'  # Changed from 'Y' to 'UP_Y'
        
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
        scene = GeometryTestScene()
        scene.construct()
        print("Geometry test completed successfully")
    except Exception as e:
        print(f"Error running geometry test: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()