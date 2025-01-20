import bpy
import mathutils
from typing import List, Optional
from ..utils.logger import SceneXLogger

class Mobject:
    """Base class for mobile objects with Manim-style functionality"""
    def __init__(self):
        self.object = None
        self.points = []
        self.submobjects = []
        self.logger = SceneXLogger("Mobject")
        
    def add(self, *mobjects):
        """Add submobjects (Manim-style)"""
        
    def shift(self, vector):
        """Move by vector (Manim-style)"""