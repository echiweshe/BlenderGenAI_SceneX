# SceneX/src/templates/technical.py

import bpy
import math
from mathutils import Vector
from ..core.scene import Scene
from ..geometry.shapes import Circle, Square, Arrow
from ..text.text_support import Text
from ..animation.commonly_used_animations import FadeInFrom, Write
from ..animation.base import AnimationConfig
from ..scene.layout import Layout, LayoutType

class TechnicalDiagramScene(Scene):
    """Base class for technical diagram animations"""
    def __init__(self, title: str = "Technical Diagram"):
        super().__init__()
        self.title = title
        self.components = []
        self.connections = []
        self.labels = []

    def add_component(self, shape_type: str, position: Vector, label: str = ""):
        """Add a component to the diagram"""
        if shape_type == "circle":
            shape = Circle(radius=0.5).create()
        elif shape_type == "square":
            shape = Square(size=1.0).create()
        
        self.coordinate_system.place_object(shape, position)
        
        if label:
            text = Text(label, size=0.3).create()
            self.coordinate_system.place_object(text, position + Vector((0, -0.7, 0)))
            self.labels.append(text)
            
        self.components.append(shape)
        return shape

    def connect_components(self, start_obj, end_obj, arrow: bool = True):
        """Create connection between components"""
        start_pos = start_obj.location
        end_pos = end_obj.location
        
        if arrow:
            connection = Arrow(start=start_pos, end=end_pos).create()
        else:
            # Create line
            pass
            
        self.connections.append(connection)
        return connection

    def animate_diagram(self):
        """Animate the diagram components"""
        config = AnimationConfig(duration=30)
        
        # Fade in components
        for component in self.components:
            self.play(FadeInFrom(component, Vector((0, -1, 0)), config=config))
            
        # Write labels
        for label in self.labels:
            self.play(Write(label, config=config))
            
        # Show connections
        for connection in self.connections:
            self.play(FadeInFrom(connection, Vector((0, 0, -1)), config=config))
