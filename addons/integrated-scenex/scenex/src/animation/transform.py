# SceneX/src/animation/transform.py
import bpy
import mathutils
from typing import Optional
from .base import Animation, AnimationConfig

class Transform(Animation):
    """Transform from current state to target state"""
    
    def __init__(self, target: bpy.types.Object, end_state: dict, config: Optional[AnimationConfig] = None):
        super().__init__(target, config)
        self.end_state = end_state

    def create_keyframes(self, start_frame: int, end_frame: int):
        # Initial keyframe
        self.target.location = self.start_state["location"]
        self.target.rotation_euler = self.start_state["rotation"]
        self.target.scale = self.start_state["scale"]
        
        self.target.keyframe_insert(data_path="location", frame=start_frame)
        self.target.keyframe_insert(data_path="rotation_euler", frame=start_frame)
        self.target.keyframe_insert(data_path="scale", frame=start_frame)
        
        # End keyframe
        self.target.location = self.end_state.get("location", self.start_state["location"])
        self.target.rotation_euler = self.end_state.get("rotation", self.start_state["rotation"])
        self.target.scale = self.end_state.get("scale", self.start_state["scale"])
        
        self.target.keyframe_insert(data_path="location", frame=end_frame)
        self.target.keyframe_insert(data_path="rotation_euler", frame=end_frame)
        self.target.keyframe_insert(data_path="scale", frame=end_frame)

class FadeIn(Animation):
    """Fade in animation using material transparency"""
    
    def create_keyframes(self, start_frame: int, end_frame: int):
        # Create material if it doesn't exist
        if not self.target.active_material:
            mat = bpy.data.materials.new(name=f"{self.target.name}_material")
            mat.use_nodes = True
            self.target.active_material = mat
        
        mat = self.target.active_material
        mat.blend_method = 'BLEND'
        
        # Get the principled BSDF node
        principled = mat.node_tree.nodes.get("Principled BSDF")
        if not principled:
            principled = mat.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
        
        # Set up and keyframe the alpha value
        principled.inputs['Alpha'].default_value = 0
        principled.inputs['Alpha'].keyframe_insert(data_path="default_value", frame=start_frame)
        
        principled.inputs['Alpha'].default_value = 1
        principled.inputs['Alpha'].keyframe_insert(data_path="default_value", frame=end_frame)

class FadeOut(Animation):
    """Fade out animation using material transparency"""
    
    def create_keyframes(self, start_frame: int, end_frame: int):
        # Create material if it doesn't exist
        if not self.target.active_material:
            mat = bpy.data.materials.new(name=f"{self.target.name}_material")
            mat.use_nodes = True
            self.target.active_material = mat
        
        mat = self.target.active_material
        mat.blend_method = 'BLEND'
        
        # Get the principled BSDF node
        principled = mat.node_tree.nodes.get("Principled BSDF")
        if not principled:
            principled = mat.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
        
        # Set up and keyframe the alpha value
        principled.inputs['Alpha'].default_value = 1
        principled.inputs['Alpha'].keyframe_insert(data_path="default_value", frame=start_frame)
        
        principled.inputs['Alpha'].default_value = 0
        principled.inputs['Alpha'].keyframe_insert(data_path="default_value", frame=end_frame)

class Scale(Animation):
    """Scale animation"""
    
    def __init__(self, target: bpy.types.Object, scale_factor: float, config: Optional[AnimationConfig] = None):
        super().__init__(target, config)
        self.scale_factor = scale_factor

    def create_keyframes(self, start_frame: int, end_frame: int):
        # Start at current scale
        self.target.keyframe_insert(data_path="scale", frame=start_frame)
        
        # End at scaled value
        self.target.scale = self.target.scale * self.scale_factor
        self.target.keyframe_insert(data_path="scale", frame=end_frame)