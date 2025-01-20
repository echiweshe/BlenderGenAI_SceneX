# # SceneX/src/geometry/base.py
# import bpy
# import mathutils
# from typing import Optional, List, Tuple, Union
# from ..utils.logger import SceneXLogger

# class Geometry:
#     """Base class for all geometric objects"""
#     def __init__(self, color: Tuple[float, float, float, float] = (1, 1, 1, 1),
#                  stroke_width: float = 0.05,
#                  fill_opacity: float = 1.0):
#         self.logger = SceneXLogger("Geometry")
#         self.color = color
#         self.stroke_width = stroke_width
#         self.fill_opacity = fill_opacity
#         self.object = None  # Blender object reference
        
#     def create(self) -> bpy.types.Object:
#         """Create the geometric object - to be implemented by subclasses"""
#         raise NotImplementedError

#     def set_color(self, color: Tuple[float, float, float, float]):
#         """Set object color"""
#         if not self.object or not self.object.active_material:
#             return
            
#         material = self.object.active_material
#         if material.use_nodes:
#             principled = material.node_tree.nodes.get('Principled BSDF')
#             if principled:
#                 principled.inputs['Base Color'].default_value = color
#                 principled.inputs['Alpha'].default_value = color[3]

#     def set_stroke_width(self, width: float):
#         """Set stroke width for curves"""
#         if self.object and self.object.type == 'CURVE':
#             self.object.data.bevel_depth = width

#     def align_to_grid(self, position: mathutils.Vector):
#         """Align object to grid"""
#         if self.object:
#             self.object.location = position




import bpy
import mathutils
from typing import Optional, List, Tuple, Union
from ..utils.logger import SceneXLogger

class Geometry:
    """Base class for all geometric objects"""
    def __init__(self, color: Tuple[float, float, float, float] = (1, 1, 1, 1),
                 stroke_width: float = 0.05,
                 fill_opacity: float = 1.0):
        self.logger = SceneXLogger("Geometry")
        self.color = color
        self.stroke_width = stroke_width
        self.fill_opacity = fill_opacity
        self.object = None  # Blender object reference
        
    def create(self) -> bpy.types.Object:
        """Create the geometric object - to be implemented by subclasses"""
        raise NotImplementedError

    def _setup_material(self):
        """Create and setup material for the object"""
        if not self.object:
            return
            
        mat = bpy.data.materials.new(name=f"geometry_material_{id(self)}")
        mat.use_nodes = True
        
        # Setup nodes
        nodes = mat.node_tree.nodes
        principled = nodes.get("Principled BSDF")
        if not principled:
            principled = nodes.new('ShaderNodeBsdfPrincipled')
            
        principled.inputs['Base Color'].default_value = self.color
        principled.inputs['Alpha'].default_value = self.fill_opacity
        
        if self.fill_opacity < 1.0:
            mat.blend_method = 'BLEND'
            
        # Assign material
        if self.object.data.materials:
            self.object.data.materials[0] = mat
        else:
            self.object.data.materials.append(mat)

    def set_color(self, color: Tuple[float, float, float, float]):
        """Set object color"""
        if not self.object or not self.object.active_material:
            return
            
        material = self.object.active_material
        if material.use_nodes:
            principled = material.node_tree.nodes.get('Principled BSDF')
            if principled:
                principled.inputs['Base Color'].default_value = color
                principled.inputs['Alpha'].default_value = color[3]

    def set_stroke_width(self, width: float):
        """Set stroke width for curves"""
        if self.object and self.object.type == 'CURVE':
            self.object.data.bevel_depth = width

    def align_to_grid(self, position: mathutils.Vector):
        """Align object to grid"""
        if self.object:
            self.object.location = position