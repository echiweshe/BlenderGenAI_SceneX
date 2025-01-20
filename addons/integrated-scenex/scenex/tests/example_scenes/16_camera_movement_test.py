# SceneX/tests/example_scenes/16_camera_movement_test.py

import bpy
import math
from mathutils import Vector

# Add parent directory to path to find SceneX package
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(script_dir))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)


from src.core.scene import Scene
from src.geometry.shapes import Circle, Square
from src.camera.movements import CameraMovement
from src.scene.groups import Group
from src.animation.base import AnimationConfig

class CameraMovementTest(Scene):
    def construct(self):
        self.logger.info("Starting camera movement test")

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
        track.up_axis = 'UP_Y'
        
        bpy.context.scene.camera = camera

        # Add lighting
        bpy.ops.object.light_add(type='SUN', location=(5, 5, 8))
        sun = bpy.context.active_object
        sun.data.energy = 3.0

        # Create test objects
        circle = Circle(radius=1.0).create()
        square = Square(size=2.0).create()
        group = Group("test_group").add(circle, square)

        # Position objects
        circle.location = Vector((-2, 0, 0))
        square.location = Vector((2, 0, 0))

        # Initialize camera movement
        cam_move = CameraMovement(self.camera)

        # Test camera movements
        cam_move.dolly(-5, duration=30)  # Move back
        cam_move.orbit(math.pi, duration=60)  # Orbit 180 degrees
        cam_move.frame_object(group)  # Frame both objects
        cam_move.fly_to(Vector((5, -5, 5)), Vector((0, 0, 0)), duration=30)

if __name__ == "__main__":
    scene = CameraMovementTest()
    scene.construct()