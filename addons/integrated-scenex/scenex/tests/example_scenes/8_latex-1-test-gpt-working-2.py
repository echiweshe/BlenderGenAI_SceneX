import bpy
import math
from mathutils import Vector
from src.core.scene import Scene
from src.text.text_support import LaTeXText
from src.animation.commonly_used_animations import FadeInFrom
from src.animation.base import AnimationConfig


class LaTeXTestScene(Scene):
    def construct(self):
        self.logger.info("Starting materials test scene")

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

        # LaTeX Equations (Corrected for Matplotlib)
        equations = [
            ("Einstein", "E = mc^2"),
            ("Gaussian Integral", "\\int_{-\\infty}^{\\infty} e^{-x^2} dx = \\sqrt{\\pi}"),
            ("Matrix Form", "\\\\left( \\begin{matrix} a & b \\\\ c & d \\end{matrix} \\\\right)"),
            ("Summation", "\\sum_{n=1}^{\\infty} \\frac{1}{n^2} = \\frac{\\pi^2}{6}")
        ]

        tex_objects = []
        for name, tex in equations:
            obj = LaTeXText(tex=tex, size=1.2, color=(1, 1, 1, 1)).create()
            if obj:
                self.logger.info(f"LaTeX object created for {name}")
                tex_objects.append(obj)
            else:
                self.logger.error(f"Failed to create LaTeX object for {name}")

        # Positioning and Animation
        spacing = 1.5
        for i, obj in enumerate(tex_objects):
            obj.location = Vector((0, 2 - i * spacing, 0))

        # Fade-In Animation
        config = AnimationConfig(duration=30)
        for obj in tex_objects:
            self.play(FadeInFrom(obj, direction=Vector((-1, 0, 0)), config=config))

        # Render to File
        bpy.context.scene.render.filepath = "C:/Users/ernes/Desktop/latex_render.png"
        bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    scene = LaTeXTestScene()
    scene.construct()
