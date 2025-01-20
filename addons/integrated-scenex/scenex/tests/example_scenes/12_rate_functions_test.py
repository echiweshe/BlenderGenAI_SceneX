# SceneX/tests/example_scenes/12_rate_functions_test.py

import bpy
import math
from mathutils import Vector

# Add parent directory to path to find SceneX package
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(script_dir))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)


from src.core.scene import Scene
from src.geometry.shapes import Circle
from src.animation.commonly_used_animations import FadeInFrom, Rotate
from src.animation.base import AnimationConfig
from src.animation.rate_functions import RateFuncType

class RateFunctionsTest(Scene):
    def construct(self):
        self.logger.info("Starting rate functions test scene")

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
        circles = []
        for i in range(6):
            circle = Circle(radius=0.3).create()
            circles.append(circle)
            self.coordinate_system.place_object(circle, Vector((-3 + i, 2, 0)))

        # Test different rate functions
        rate_functions = [
            (RateFuncType.ELASTIC, "Elastic"),
            (RateFuncType.BOUNCE, "Bounce"),
            (RateFuncType.EASE_IN_OUT, "Ease In Out"),
            (RateFuncType.EXPONENTIAL, "Exponential"),
            (RateFuncType.BACK, "Back"),
            (RateFuncType.SMOOTH, "Smooth")
        ]

        for circle, (rate_func, name) in zip(circles, rate_functions):
            config = AnimationConfig(duration=60, rate_func=rate_func)
            self.play(
                FadeInFrom(circle, Vector((0, -2, 0)), config=config),
                Rotate(circle, config=config)
            )

if __name__ == "__main__":
    scene = RateFunctionsTest()
    scene.construct()