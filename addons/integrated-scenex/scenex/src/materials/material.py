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
    type: MaterialType = MaterialType.BASIC
    color: Tuple[float, float, float, float] = (1, 1, 1, 1)
    roughness: float = 0.5
    emission_strength: float = 0.0
    emission_color: Optional[Tuple[float, float, float, float]] = None
    alpha: float = 1.0
    ior: float = 1.45


class Material:
    def __init__(self, name: str, config: MaterialConfig):
        self.name = name
        self.config = config
        self.material = None
        self.logger = SceneXLogger("Material")

    def create(self) -> bpy.types.Material:
        self.material = bpy.data.materials.new(name=self.name)
        self.material.use_nodes = True
        self.setup_nodes()
        return self.material

    def setup_nodes(self):
        if not self.material:
            return

        nodes = self.material.node_tree.nodes
        links = self.material.node_tree.links
        nodes.clear()

        principled = nodes.new('ShaderNodeBsdfPrincipled')
        output = nodes.new('ShaderNodeOutputMaterial')

        principled.inputs['Base Color'].default_value = self.config.color
        principled.inputs['Roughness'].default_value = self.config.roughness

        links.new(principled.outputs['BSDF'], output.inputs['Surface'])

        if self.config.alpha < 1.0:
            self.material.blend_method = 'BLEND'
