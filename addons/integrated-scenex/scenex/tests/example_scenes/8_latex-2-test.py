# import bpy
# import math
# from mathutils import Vector
# from src.core.scene import Scene
# from src.text.text_support import LaTeXText
# from src.animation.commonly_used_animations import FadeInFrom
# from src.animation.base import AnimationConfig

# class LaTeXTestScene(Scene):
#     def construct(self):
#         self.logger.info("Starting LaTeX test scene")

#         # Clear the scene
#         bpy.ops.object.select_all(action='SELECT')
#         bpy.ops.object.delete()

#         # Setup the render engine
#         bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'
#         if hasattr(bpy.context.scene.eevee, "use_ssr"):
#             bpy.context.scene.eevee.use_ssr = True
#             bpy.context.scene.eevee.use_ssr_refraction = True

#         # Configure viewport
#         for area in bpy.context.screen.areas:
#             if area.type == 'VIEW_3D':
#                 for space in area.spaces:
#                     if space.type == 'VIEW_3D':
#                         space.shading.type = 'RENDERED'
#                         space.shading.use_scene_lights = True
#                         space.shading.use_scene_world = True

#         # Set up camera
#         bpy.ops.object.camera_add(location=(7, -7, 5))
#         camera = bpy.context.active_object
#         camera.rotation_euler = (math.radians(45), 0, math.radians(45))

#         bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
#         target = bpy.context.active_object
#         target.name = "CameraTarget"

#         track = camera.constraints.new(type='TRACK_TO')
#         track.target = target
#         track.track_axis = 'TRACK_NEGATIVE_Z'
#         track.up_axis = 'UP_Y'

#         bpy.context.scene.camera = camera

#         # # Add lighting
#         # bpy.ops.object.light_add(type='SUN', location=(5, 5, 8))
#         # sun = bpy.context.active_object
#         # sun.data.energy = 3.0

#         # Create LaTeX objects
#         equations = [
#             ("Einstein", "E = mc^2"),
#             ("Integral", "\\int_{-\\infty}^{\\infty} e^{-x^2} dx = \\sqrt{\\pi}"),
#             ("Matrix", "\\begin{pmatrix} a & b \\\\ c & d \\end{pmatrix}"),
#         ]

#         tex_objects = []
#         for name, tex in equations:
#             obj = LaTeXText(tex, size=1.5, color=(1, 1, 1, 1)).create()
#             if obj:
#                 tex_objects.append(obj)
#             else:
#                 self.logger.error(f"Failed to create LaTeX object for {name}")

#         # Position LaTeX objects
#         spacing = 1.5
#         for i, obj in enumerate(tex_objects):
#             obj.location = Vector((0, 2 - i * spacing, 0))

#         # Animate LaTeX appearing
#         config = AnimationConfig(duration=30)
#         for obj in tex_objects:
#             self.play(FadeInFrom(obj, direction=Vector((0, -1, 0)), config=config))

#         # Render the frame to confirm visualization
#         bpy.context.scene.render.filepath = "C:/Users/ernes/Desktop/latex_render.png"
#         bpy.ops.render.render(write_still=True)

# if __name__ == "__main__":
#     scene = LaTeXTestScene()
#     scene.construct()


# SceneX/src/text/text_support.py

# import sys
# print("Python path during runtime:", sys.executable)
# print("Python path to site-packages:", sys.path)

# import sys
# import site

# # Append user site-packages to sys.path
# sys.path.append(site.getusersitepackages())

# print("Updated Python path to site-packages:", sys.path)


import bpy
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import io
import tempfile
from PIL import Image

from src.core.scene import Scene
from src.text.text_support import LaTeXText, Text
from src.animation.commonly_used_animations import Write, FadeInFrom
from src.animation.base import AnimationConfig
from src.geometry.base import Geometry

class LaTeXText(Geometry):
    def __init__(self, tex: str, size: float = 1.0, **kwargs):
        super().__init__(**kwargs)
        self.tex = tex
        self.size = size


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

    def create(self) -> bpy.types.Object:
        # Create figure with transparent background
        fig = plt.figure(figsize=(5, 1), dpi=300)
        fig.patch.set_alpha(0.0)
        
        # Add text using matplotlib's LaTeX renderer
        plt.text(0.5, 0.5, f"${self.tex}$", 
                horizontalalignment='center',
                verticalalignment='center',
                transform=fig.transFigure,
                color=self.color[:3])
        
        plt.axis('off')
        
        # Save to temporary PNG with transparency
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            plt.savefig(tmp.name, 
                       transparent=True,
                       bbox_inches='tight',
                       pad_inches=0.1,
                       dpi=300)
            plt.close()
            
            # Create image texture
            img = bpy.data.images.load(tmp.name)
            
            # Create plane for the texture
            bpy.ops.mesh.primitive_plane_add(size=self.size)
            self.object = bpy.context.active_object
            
            # Create material
            mat = bpy.data.materials.new(name="latex_material")
            mat.use_nodes = True
            mat.blend_method = 'BLEND'
            
            # Setup nodes for transparent texture
            nodes = mat.node_tree.nodes
            links = mat.node_tree.links
            nodes.clear()
            
            tex_image = nodes.new('ShaderNodeTexImage')
            tex_image.image = img
            
            principled = nodes.new('ShaderNodeBsdfPrincipled')
            output = nodes.new('ShaderNodeOutputMaterial')
            
            links.new(tex_image.outputs['Color'], principled.inputs['Base Color'])
            links.new(tex_image.outputs['Alpha'], principled.inputs['Alpha'])
            links.new(principled.outputs['BSDF'], output.inputs['Surface'])
            
            self.object.data.materials.append(mat)
            
            return self.object

if __name__ == "__main__":
    scene = LaTeXText(tex="E = mc^2", size=1.5)
    scene.create()  # Correct method to create the LaTeX object
