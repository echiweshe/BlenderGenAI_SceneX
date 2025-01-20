# SceneX/tests/example_scenes/8_latex_test.py

import bpy
import math
from mathutils import Vector
from src.core.scene import Scene
from src.text.text_support import Text, LaTeXText
from src.animation.commonly_used_animations import FadeInFrom
from src.animation.base import AnimationConfig

class LaTeXTestScene(Scene):
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

        # Create LaTeX equations
        equations = [
            ("Simple", "E = mc^2"),
            ("Integral", "\\int_{-\\infty}^{\\infty} e^{-x^2} dx = \\sqrt{\\pi}"),
            ("Matrix", "\\begin{pmatrix} a & b \\\\ c & d \\end{pmatrix}"),
            ("Sum", "\\sum_{n=1}^{\\infty} \\frac{1}{n^2} = \\frac{\\pi^2}{6}")
        ]

        tex_objects = []
        for name, tex in equations:
            obj = LaTeXText(tex, size=0.6, color=(1, 1, 1, 1)).create()
            if obj:  # Only add if LaTeX creation successful
                tex_objects.append(obj)

        # Position vertically
        spacing = 1.5
        for i, obj in enumerate(tex_objects):
            self.coordinate_system.place_object(obj, Vector((0, 2-i*spacing, 0)))

        # Animate equations appearing one by one
        config = AnimationConfig(duration=30)
        
        for obj in tex_objects:
            self.play(FadeInFrom(obj, direction=Vector((-1, 0, 0)), config=config))

if __name__ == "__main__":
    scene = LaTeXTestScene()
    scene.construct()
