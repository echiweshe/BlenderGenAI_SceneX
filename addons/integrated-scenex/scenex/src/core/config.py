"""
Configuration system for SceneX.
Defines all configuration classes used throughout the system.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Tuple, Dict, Any
from enum import Enum, auto

class RateFuncType(Enum):
    """Standard animation rate functions"""
    LINEAR = auto()
    SMOOTH = auto()
    RUSH_INTO = auto()
    RUSH_FROM = auto()
    EASE_IN = auto()
    EASE_OUT = auto()
    EASE_IN_OUT = auto()
    EXPONENTIAL_DECAY = auto()

@dataclass
class AnimationConfig:
    """Configuration for animations"""
    duration: float = 1.0
    rate_func: RateFuncType = RateFuncType.SMOOTH
    frame_rate: int = 60
    delay: float = 0.0
    remover: bool = False

@dataclass
class CameraConfig:
    """Configuration for scene camera"""
    pixel_width: int = 1920
    pixel_height: int = 1080
    frame_rate: int = 60
    focal_distance: float = 10.0
    phi: float = 0  # rotation around X axis
    theta: float = 0  # rotation around Z axis
    frame_width: float = 14.0
    frame_height: float = 8.0
    orthographic: bool = True
    background_color: Tuple[float, float, float, float] = (0.1, 0.1, 0.1, 1)

@dataclass
class MaterialConfig:
    """Configuration for materials"""
    name: str = "default"
    color: Tuple[float, float, float, float] = (1, 1, 1, 1)
    metallic: float = 0.0
    roughness: float = 0.5
    emission_strength: float = 0.0
    alpha: float = 1.0
