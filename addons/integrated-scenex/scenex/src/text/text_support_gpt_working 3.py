import bpy
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for headless rendering
import matplotlib.pyplot as plt
import numpy as np
import tempfile
from PIL import Image
from pathlib import Path
from src.geometry.base import Geometry
from src.utils.logger import SceneXLogger


class LaTeXText(Geometry):
    def __init__(self, tex: str, size: float = 1.0, color=(1, 1, 1, 1), **kwargs):
        super().__init__(**kwargs)
        self.tex = tex
        self.size = size
        self.color = color
        self.logger = SceneXLogger("LaTeX")

    def create(self) -> bpy.types.Object:
        try:
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                # Create LaTeX-rendered image with matplotlib
                fig, ax = plt.subplots(figsize=(5, 1), dpi=300)
                ax.axis('off')
                fig.patch.set_alpha(0.0)  # Transparent background

                ax.text(0.5, 0.5, f"${self.tex}$",
                        horizontalalignment='center',
                        verticalalignment='center',
                        fontsize=30,
                        color=self.color[:3],  # RGB for matplotlib
                        transform=ax.transAxes)

                plt.tight_layout(pad=0)
                plt.savefig(tmp.name, transparent=True, bbox_inches='tight', pad_inches=0.1)
                plt.close(fig)

                # Load image into Blender
                img = bpy.data.images.load(tmp.name)

                # Create plane for texture
                bpy.ops.mesh.primitive_plane_add(size=self.size)
                self.object = bpy.context.active_object

                # Create and assign material
                mat = bpy.data.materials.new(name="latex_material")
                mat.use_nodes = True
                mat.blend_method = 'BLEND'

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

        except Exception as e:
            self.logger.error(f"Error creating LaTeX: {str(e)}")
            return None
