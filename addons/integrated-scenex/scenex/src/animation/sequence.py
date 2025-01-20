# SceneX/src/animation/sequence.py

from typing import List
from .base import Animation, AnimationConfig

class AnimationSequence:
    def __init__(self, *animations: Animation, config: AnimationConfig = None):
        self.animations = animations
        self.config = config or AnimationConfig()
        
    def create_keyframes(self, start_frame: int) -> int:
        current_frame = start_frame
        for anim in self.animations:
            anim.config = anim.config or self.config
            current_frame = anim.create_animation(current_frame)
        return current_frame

class AnimationGroup:
    def __init__(self, *animations: Animation, config: AnimationConfig = None):
        self.animations = animations
        self.config = config or AnimationConfig()
        
    def create_keyframes(self, start_frame: int) -> int:
        for anim in self.animations:
            anim.config = anim.config or self.config
            anim.create_animation(start_frame)
        return start_frame + self.config.duration

class Succession(AnimationSequence):
    """Animations that smoothly flow into each other"""
    def create_keyframes(self, start_frame: int) -> int:
        overlap_frames = 10  # Frames where animations overlap
        current_frame = start_frame
        
        for i, anim in enumerate(self.animations):
            if i > 0:  # Start this animation before previous one ends
                current_frame -= overlap_frames
            current_frame = anim.create_animation(current_frame)
            
        return current_frame