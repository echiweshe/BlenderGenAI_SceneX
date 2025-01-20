# SceneX/src/materials/material.py

import bpy
from dataclasses import dataclass
from typing import Tuple, Optional, Dict, Any
from enum import Enum
from ..utils.logger import SceneXLogger

class MaterialType(Enum):
    BASIC = "basic"
    GLASS = "glass" 
    EMISSION = "emission"
    METALLIC = "metallic"
    TOON = "toon"

@dataclass
class MaterialConfig:
    """Configuration for materials"""
    type: MaterialType = MaterialType.BASIC
    color: Tuple[float, float, float, float] = (1, 1, 1, 1)
    metallic: float = 0.0
    roughness: float = 0.5
    emission_strength: float = 0.0
    emission_color: Optional[Tuple[float, float, float, float]] = None
    alpha: float = 1.0
    ior: float = 1.45  # For glass
    use_subsurface: bool = False
    subsurface_color: Optional[Tuple[float, float, float, float]] = None

class Material:
    """Base material class"""
    def __init__(self, name: str, config: MaterialConfig):
        self.name = name
        self.config = config
        self.material = None
        self.logger = SceneXLogger("Material")
        
    def create(self) -> bpy.types.Material:
        """Create Blender material"""
        self.material = bpy.data.materials.new(name=self.name)
        self.material.use_nodes = True
        self.setup_nodes()
        return self.material
        
    def setup_nodes(self):
        """Set up node tree based on material type"""
        if not self.material:
            return
            
        nodes = self.material.node_tree.nodes
        links = self.material.node_tree.links
        nodes.clear()
        
        if self.config.type == MaterialType.BASIC:
            self._setup_basic_material(nodes, links)
        elif self.config.type == MaterialType.GLASS:
            self._setup_glass_material(nodes, links)
        elif self.config.type == MaterialType.EMISSION:
            self._setup_emission_material(nodes, links)
        elif self.config.type == MaterialType.METALLIC:
            self._setup_metallic_material(nodes, links)
        elif self.config.type == MaterialType.TOON:
            self._setup_toon_material(nodes, links)

    def _setup_basic_material(self, nodes, links):
        principled = nodes.new('ShaderNodeBsdfPrincipled')
        output = nodes.new('ShaderNodeOutputMaterial')
        
        principled.inputs['Base Color'].default_value = self.config.color
        principled.inputs['Alpha'].default_value = self.config.alpha
        principled.inputs['Roughness'].default_value = self.config.roughness
        
        links.new(principled.outputs['BSDF'], output.inputs['Surface'])
        
        if self.config.alpha < 1.0:
            self.material.blend_method = 'BLEND'

    def _setup_glass_material(self, nodes, links):
        glass = nodes.new('ShaderNodeBsdfGlass')
        output = nodes.new('ShaderNodeOutputMaterial')
        
        glass.inputs['Color'].default_value = self.config.color
        glass.inputs['Roughness'].default_value = self.config.roughness
        glass.inputs['IOR'].default_value = self.config.ior
        
        links.new(glass.outputs['BSDF'], output.inputs['Surface'])
        self.material.blend_method = 'BLEND'

    def _setup_emission_material(self, nodes, links):
        emission = nodes.new('ShaderNodeEmission')
        output = nodes.new('ShaderNodeOutputMaterial')
        
        emission.inputs['Color'].default_value = self.config.emission_color or self.config.color
        emission.inputs['Strength'].default_value = self.config.emission_strength
        
        links.new(emission.outputs['Emission'], output.inputs['Surface'])

    def _setup_metallic_material(self, nodes, links):
        principled = nodes.new('ShaderNodeBsdfPrincipled')
        output = nodes.new('ShaderNodeOutputMaterial')
        
        principled.inputs['Base Color'].default_value = self.config.color
        principled.inputs['Metallic'].default_value = 1.0
        principled.inputs['Roughness'].default_value = self.config.roughness
        
        links.new(principled.outputs['BSDF'], output.inputs['Surface'])

    def _setup_toon_material(self, nodes, links):
        diffuse = nodes.new('ShaderNodeBsdfDiffuse')
        toon = nodes.new('ShaderNodeBsdfToon')
        mix = nodes.new('ShaderNodeMixShader')
        output = nodes.new('ShaderNodeOutputMaterial')
        
        diffuse.inputs['Color'].default_value = self.config.color
        toon.inputs['Color'].default_value = self.config.color
        mix.inputs[0].default_value = 0.5
        
        links.new(diffuse.outputs['BSDF'], mix.inputs[1])
        links.new(toon.outputs['BSDF'], mix.inputs[2])
        links.new(mix.outputs['Shader'], output.inputs['Surface'])