# SceneX/src/animation/base.py
import bpy
import mathutils
from dataclasses import dataclass
from typing import Optional, Tuple, List, Callable
from ..utils.logger import SceneXLogger

@dataclass
class AnimationConfig:
    """Configuration for animations"""
    duration: int = 30  # Duration in frames
    start_frame: Optional[int] = None
    rate_func: Callable[[float], float] = lambda x: x  # Linear by default
    delay_frames: int = 0
    ease_type: str = 'EASE_IN_OUT'  # LINEAR, EASE_IN, EASE_OUT, EASE_IN_OUT

class Animation:
    """Base class for all animations"""
    
    def __init__(self, target: bpy.types.Object, config: Optional[AnimationConfig] = None):
        self.target = target
        self.config = config or AnimationConfig()
        self.logger = SceneXLogger("Animation")
        self.start_state = {}
        self.store_initial_state()

    def store_initial_state(self):
        """Store the initial state of the object"""
        if not self.target:
            return
            
        self.start_state = {
            "location": self.target.location.copy(),
            "rotation": self.target.rotation_euler.copy(),
            "scale": self.target.scale.copy()
        }
        
        # Store material properties if exists
        if self.target.active_material:
            mat = self.target.active_material
            if mat.use_nodes:
                principled = mat.node_tree.nodes.get('Principled BSDF')
                if principled:
                    self.start_state["color"] = principled.inputs['Base Color'].default_value[:]
                    self.start_state["alpha"] = principled.inputs['Alpha'].default_value

    def create_animation(self, start_frame: int):
        """Create the animation starting at the given frame"""
        if self.config.start_frame is None:
            self.config.start_frame = start_frame
            
        end_frame = self.config.start_frame + self.config.duration
        
        try:
            self.create_keyframes(self.config.start_frame, end_frame)
            self.setup_fcurves()
            return end_frame
        except Exception as e:
            self.logger.error(f"Error creating animation: {str(e)}")
            return start_frame

    def create_keyframes(self, start_frame: int, end_frame: int):
        """Override in subclasses to create specific keyframes"""
        raise NotImplementedError

    def setup_fcurves(self):
        """Setup F-curves with proper interpolation"""
        if not self.target.animation_data or not self.target.animation_data.action:
            return
            
        for fc in self.target.animation_data.action.fcurves:
            for kf in fc.keyframe_points:
                kf.interpolation = 'BEZIER'
                if self.config.ease_type == 'LINEAR':
                    kf.easing = 'LINEAR'
                else:
                    kf.easing = self.config.ease_type