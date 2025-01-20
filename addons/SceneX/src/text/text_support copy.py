# SceneX/src/text/text_support.py

import bpy
import os
import tempfile
import subprocess
from pathlib import Path
from ..geometry.base import Geometry
from ..utils.logger import SceneXLogger

# import matplotlib

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
            # Create temporary directory
            with tempfile.TemporaryDirectory() as tmp_dir:
                # Generate LaTeX document
                tex_path = Path(tmp_dir) / "equation.tex"
                with open(tex_path, "w") as f:
                    f.write(self._create_tex_document())
                
                # Convert to PDF
                subprocess.run(["pdflatex", "-interaction=nonstopmode", 
                             str(tex_path)], cwd=tmp_dir, capture_output=True)
                
                # Convert PDF to SVG
                pdf_path = Path(tmp_dir) / "equation.pdf"
                svg_path = Path(tmp_dir) / "equation.svg"
                subprocess.run(["pdftocairo", "-svg", str(pdf_path), str(svg_path)], 
                             capture_output=True)
                
                # Import SVG
                bpy.ops.import_curve.svg(filepath=str(svg_path))
                self.object = bpy.context.selected_objects[-1]
                self.object.scale = (self.size, self.size, self.size)
                
                # Set up material
                self._setup_material()
                
                return self.object
                
        except Exception as e:
            self.logger.error(f"Error creating LaTeX: {str(e)}")
            return None
            
    def _create_tex_document(self) -> str:
        return f"""\\documentclass[preview]{{standalone}}
\\usepackage{{amsmath}}
\\begin{{document}}
${self.tex}$
\\end{{document}}"""