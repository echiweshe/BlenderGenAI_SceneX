import bpy
import os
import tempfile
import subprocess
from pathlib import Path
from ..geometry.base import Geometry
from ..utils.logger import SceneXLogger

# Correct import for matplotlib
import matplotlib.pyplot as plt

class Text(Geometry):
    def __init__(self, text: str, size: float = 1.0, 
                 font_path: str = None, alignment: str = 'CENTER', **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.size = size
        self.font_path = font_path
        self.alignment = alignment
        self.logger = SceneXLogger("Text")

    def create(self) -> bpy.types.Object:
        bpy.ops.object.text_add(enter_editmode=False)
        self.object = bpy.context.active_object
        self.object.data.body = self.text
        
        # Apply font if specified
        if self.font_path and os.path.exists(self.font_path):
            font = bpy.data.fonts.load(self.font_path)
            self.object.data.font = font
            
        # Set text properties
        self.object.data.size = self.size
        self.object.data.align_x = self.alignment
        
        # Set up material
        self._setup_material()
        
        return self.object

class LaTeXText(Geometry):
    """Convert LaTeX expressions to geometry using pdflatex and svg conversion"""
    
    def __init__(self, tex: str, size: float = 1.0, **kwargs):
        super().__init__(**kwargs)
        self.tex = tex
        self.size = size
        self.logger = SceneXLogger("LaTeX")

    def create(self) -> bpy.types.Object:
        try:
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

                # Load image into Blender
                img = bpy.data.images.load(tmp.name)

                # Create plane for the texture
                bpy.ops.mesh.primitive_plane_add(size=self.size)
                self.object = bpy.context.active_object  # Set to newly created plane
                bpy.context.view_layer.objects.active = self.object  # Ensure correct active object

                # Create and assign material
                mat = bpy.data.materials.new(name="latex_material")
                mat.use_nodes = True
                mat.blend_method = 'BLEND'

                # Setup nodes for transparency
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

                self.object.data.materials.append(mat)  # Assign material to plane
                
                return self.object
        
        except Exception as e:
            self.logger.error(f"Error creating LaTeX: {str(e)}")
            return None

    def _create_tex_document(self) -> str:
        """Generate a LaTeX document string for rendering"""
        return f"""\\documentclass[preview]{{standalone}}
\\usepackage{{amsmath}}
\\begin{{document}}
${self.tex}$
\\end{{document}}"""
