# SceneX/tests/example_scenes/15_layout_test.py

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
from src.scene.layout import Layout, LayoutType
from src.animation.commonly_used_animations import FadeInFrom
from src.animation.base import AnimationConfig

class LayoutTest(Scene):
    def construct(self):
        self.logger.info("Starting layout test scene")

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
        shapes = []
        for i in range(9):
            if i % 2 == 0:
                obj = Circle(radius=0.3).create()
            else:
                obj = Square(size=0.6).create()
            shapes.append(obj)

        # Test different layouts
        layout = Layout()
        
        # Test horizontal layout
        layout.arrange(shapes[:3], LayoutType.HORIZONTAL, 
                      spacing=1.0, center=Vector((0, 2, 0)))

        # Test vertical layout
        layout.arrange(shapes[3:6], LayoutType.VERTICAL, 
                      spacing=1.0, center=Vector((-2, 0, 0)))

        # Test grid layout
        layout.arrange(shapes[6:], LayoutType.GRID, 
                      spacing=1.0, center=Vector((2, 0, 0)), columns=2)

        # Animate
        config = AnimationConfig(duration=30)
        for obj in shapes:
            self.play(FadeInFrom(obj, Vector((0, -1, 0)), config=config))

if __name__ == "__main__":
    scene = LayoutTest()
    scene.construct()