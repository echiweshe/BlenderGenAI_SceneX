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
from src.text.text_support import Text
from src.animation.commonly_used_animations import Write, FadeInFrom
from src.animation.base import AnimationConfig
from src.geometry.base import Geometry

class LaTeXText(Geometry):
    def __init__(self, tex: str, size: float = 1.0, **kwargs):
        super().__init__(**kwargs)
        self.tex = tex
        self.size = size

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