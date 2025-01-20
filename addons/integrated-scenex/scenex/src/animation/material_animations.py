# src/animation/material_animations.py


import bpy
from typing import Optional, Tuple, Dict, Any, List
from .base import Animation, AnimationConfig
from ..utils.logger import SceneXLogger

class MaterialAnimation(Animation):
    """Animate material color changes"""
    def __init__(self, target: bpy.types.Object, 
                 start_color: Tuple[float, float, float, float],
                 end_color: Tuple[float, float, float, float], 
                 config: Optional[AnimationConfig] = None):
        super().__init__(target, config)
        self.start_color = start_color
        self.end_color = end_color
        self.logger = SceneXLogger("MaterialAnimation")

    def create_keyframes(self, start_frame: int, end_frame: int):
        try:
            if not self.target.active_material:
                self.logger.warning("No active material found on target object")
                return start_frame
                
            mat = self.target.active_material
            principled = mat.node_tree.nodes.get('Principled BSDF')
            if not principled:
                self.logger.warning("No Principled BSDF node found in material")
                return start_frame
                
            # Start color
            principled.inputs['Base Color'].default_value = self.start_color
            principled.inputs['Base Color'].keyframe_insert(data_path="default_value", frame=start_frame)
            
            # End color
            principled.inputs['Base Color'].default_value = self.end_color
            principled.inputs['Base Color'].keyframe_insert(data_path="default_value", frame=end_frame)
            
            self.logger.info(f"Created color animation from {self.start_color} to {self.end_color}")
            return end_frame
            
        except Exception as e:
            self.logger.error(f"Error creating material animation: {str(e)}")
            return start_frame

class EmissionAnimation(Animation):
    """Animate emission strength changes"""
    def __init__(self, target: bpy.types.Object, 
                 start_strength: float, 
                 end_strength: float, 
                 config: Optional[AnimationConfig] = None):
        super().__init__(target, config)
        self.start_strength = start_strength
        self.end_strength = end_strength
        self.logger = SceneXLogger("EmissionAnimation")

    def create_keyframes(self, start_frame: int, end_frame: int):
        try:
            if not self.target.active_material:
                self.logger.warning("No active material found on target object")
                return start_frame
                
            mat = self.target.active_material
            nodes = mat.node_tree.nodes
            emission = nodes.get("Emission")
            if not emission:
                self.logger.warning("No Emission node found in material")
                return start_frame
                
            # Start strength
            emission.inputs["Strength"].default_value = self.start_strength
            emission.inputs["Strength"].keyframe_insert(data_path="default_value", frame=start_frame)
            
            # End strength
            emission.inputs["Strength"].default_value = self.end_strength
            emission.inputs["Strength"].keyframe_insert(data_path="default_value", frame=end_frame)
            
            self.logger.info(f"Created emission animation from {self.start_strength} to {self.end_strength}")
            return end_frame
            
        except Exception as e:
            self.logger.error(f"Error creating emission animation: {str(e)}")
            return start_frame
        
        
class MaterialPropertyAnimation(Animation):
    """Animate any material property"""
    def __init__(self, target: bpy.types.Object,
                 property_path: str,
                 start_value: float,
                 end_value: float,
                 node_name: str = 'Principled BSDF',
                 config: Optional[AnimationConfig] = None):
        super().__init__(target, config)
        self.property_path = property_path
        self.start_value = start_value
        self.end_value = end_value
        self.node_name = node_name
        self.logger = SceneXLogger("MaterialPropertyAnimation")

    def create_keyframes(self, start_frame: int, end_frame: int):
        try:
            if not self.target.active_material:
                self.logger.warning("No active material found")
                return start_frame

            mat = self.target.active_material
            node = mat.node_tree.nodes.get(self.node_name)
            if not node:
                self.logger.warning(f"Node {self.node_name} not found")
                return start_frame

            # Set start value
            node.inputs[self.property_path].default_value = self.start_value
            node.inputs[self.property_path].keyframe_insert(
                data_path="default_value", frame=start_frame)

            # Set end value
            node.inputs[self.property_path].default_value = self.end_value
            node.inputs[self.property_path].keyframe_insert(
                data_path="default_value", frame=end_frame)

            return end_frame

        except Exception as e:
            self.logger.error(f"Error animating material property: {str(e)}")
            return start_frame

class MaterialPresetAnimation(Animation):
    """Animate between material presets"""
    def __init__(self, target: bpy.types.Object,
                 preset_sequence: List[Dict[str, float]],
                 node_name: str = 'Principled BSDF',
                 config: Optional[AnimationConfig] = None):
        super().__init__(target, config)
        self.preset_sequence = preset_sequence
        self.node_name = node_name
        self.logger = SceneXLogger("MaterialPresetAnimation")

    def create_keyframes(self, start_frame: int, end_frame: int):
        try:
            if not self.target.active_material:
                self.logger.warning("No active material found")
                return start_frame

            mat = self.target.active_material
            node = mat.node_tree.nodes.get(self.node_name)
            if not node:
                self.logger.warning(f"Node {self.node_name} not found")
                return start_frame

            frame_interval = (end_frame - start_frame) / (len(self.preset_sequence) - 1)
            
            for i, preset in enumerate(self.preset_sequence):
                current_frame = start_frame + (i * frame_interval)
                
                for prop_name, value in preset.items():
                    if prop_name in node.inputs:
                        node.inputs[prop_name].default_value = value
                        node.inputs[prop_name].keyframe_insert(
                            data_path="default_value", frame=current_frame)

            return end_frame

        except Exception as e:
            self.logger.error(f"Error animating material preset: {str(e)}")
            return start_frame

class MaterialBlendAnimation(Animation):
    """Blend between two complete materials"""
    def __init__(self, target: bpy.types.Object,
                 material1: bpy.types.Material,
                 material2: bpy.types.Material,
                 config: Optional[AnimationConfig] = None):
        super().__init__(target, config)
        self.material1 = material1
        self.material2 = material2
        self.logger = SceneXLogger("MaterialBlendAnimation")

    def create_keyframes(self, start_frame: int, end_frame: int):
        try:
            # Create blend material
            blend_mat = bpy.data.materials.new(name="blend_material")
            blend_mat.use_nodes = True
            nodes = blend_mat.node_tree.nodes
            links = blend_mat.node_tree.links
            
            # Clear existing nodes
            nodes.clear()
            
            # Add nodes
            mat1 = nodes.new('ShaderNodeMaterial')
            mat2 = nodes.new('ShaderNodeMaterial')
            mix = nodes.new('ShaderNodeMixShader')
            output = nodes.new('ShaderNodeOutputMaterial')
            
            # Setup materials
            mat1.material = self.material1
            mat2.material = self.material2
            
            # Connect nodes
            links.new(mat1.outputs['Surface'], mix.inputs[1])
            links.new(mat2.outputs['Surface'], mix.inputs[2])
            links.new(mix.outputs['Shader'], output.inputs['Surface'])
            
            # Create keyframes
            mix.inputs[0].default_value = 0
            mix.inputs[0].keyframe_insert(data_path="default_value", frame=start_frame)
            
            mix.inputs[0].default_value = 1
            mix.inputs[0].keyframe_insert(data_path="default_value", frame=end_frame)
            
            # Assign blended material
            self.target.active_material = blend_mat
            
            return end_frame

        except Exception as e:
            self.logger.error(f"Error creating material blend: {str(e)}")
            return start_frame

# Example material presets
MATERIAL_PRESETS = {
    'metal': {
        'Metallic': 1.0,
        'Roughness': 0.2,
        'Base Color': (0.8, 0.8, 0.8, 1.0)
    },
    'plastic': {
        'Metallic': 0.0,
        'Roughness': 0.4,
        'Base Color': (0.2, 0.5, 1.0, 1.0)
    },
    'glass': {
        'Transmission': 1.0,
        'Roughness': 0.0,
        'Base Color': (0.8, 0.9, 1.0, 1.0),
        'IOR': 1.45
    }
}