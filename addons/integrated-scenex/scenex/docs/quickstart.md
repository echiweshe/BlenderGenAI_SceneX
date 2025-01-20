# SceneX Documentation

## Overview
SceneX is a Blender animation framework inspired by Manim, designed for creating educational and technical animations. It provides high-level abstractions for geometry, animations, and scene composition.

## Quick Start

```python
from src.core.scene import Scene
from src.geometry.shapes import Circle, Square
from src.animation.commonly_used_animations import FadeInFrom
from src.animation.base import AnimationConfig
from mathutils import Vector

class MyFirstScene(Scene):
    def construct(self):
        # Create shapes
        circle = Circle(radius=0.5).create()
        square = Square(size=1.0).create()

        # Position objects
        self.coordinate_system.place_object(circle, Vector((-1, 0, 0)))
        self.coordinate_system.place_object(square, Vector((1, 0, 0)))

        # Animate
        config = AnimationConfig(duration=30)
        self.play(FadeInFrom(circle, Vector((0, -1, 0)), config=config))

# Run the scene
scene = MyFirstScene()
scene.construct()
```

## Core Components

### 1. Geometry System
- Basic Shapes: Circle, Square, Rectangle, Line
- Complex Shapes: Arrow, Arc, Star
- Text and LaTeX Support
- SVG Import

Example:
```python
# Creating shapes
circle = Circle(radius=0.5, color=(1, 0, 0, 1)).create()
arrow = Arrow(start=(-1, 0, 0), end=(1, 0, 0)).create()

# Text creation
text = Text("Hello World", size=1.0).create()
```

### 2. Animation System
- Basic Animations: FadeIn, FadeOut, Rotate
- Transform Animations
- Animation Sequences and Groups
- Custom Rate Functions

Example:
```python
# Single animation
self.play(FadeInFrom(circle, Vector((0, -1, 0)), config))

# Animation sequence
sequence = AnimationSequence(
    FadeInFrom(circle, Vector((0, -1, 0)), config),
    Rotate(circle, config)
)
self.play(sequence)
```

### 3. Scene Composition
- Object Groups
- Layout Management
- Camera Control
- Grid System

Example:
```python
# Create and manage groups
group = Group("shapes").add(circle, square)
layout = Layout()
layout.arrange(group.get_all_objects(), LayoutType.HORIZONTAL)

# Camera movement
camera_movement = CameraMovement(self.camera)
camera_movement.frame_object(group)
```

## Advanced Features

### 1. Rate Functions
Available rate functions for animations:
- LINEAR
- SMOOTH
- RUSH_INTO
- RUSH_FROM
- EASE_IN
- EASE_OUT
- EXPONENTIAL
- ELASTIC
- BOUNCE
- BACK

### 2. Layout Types
Available layout arrangements:
- HORIZONTAL
- VERTICAL
- GRID
- CIRCULAR
- SPIRAL

### 3. Camera Movements
- Dolly (forward/backward)
- Orbit
- Frame objects
- Fly to position

## Best Practices

1. Scene Organization
```python
class WellOrganizedScene(Scene):
    def construct(self):
        # Setup
        self.setup_objects()
        
        # Animations
        self.animate_sequence()
        
        # Cleanup
        self.cleanup()
        
    def setup_objects(self):
        # Create and position objects
        pass
        
    def animate_sequence(self):
        # Define animation sequence
        pass
        
    def cleanup(self):
        # Cleanup code
        pass
```

2. Object Naming
```python
# Good practice
main_circle = Circle(radius=0.5).create()
main_circle.name = "main_circle"

# Group related objects
equation_group = Group("equation")
equation_group.add(symbol1, symbol2, equals_sign)
```

3. Animation Timing
```python
# Use consistent timing
standard_duration = 30
quick_duration = 15
slow_duration = 60

config = AnimationConfig(duration=standard_duration)
```

## Common Patterns

1. Creating Technical Diagrams
```python
def create_technical_diagram():
    # Create components
    components = [
        Square(size=1.0).create(),
        Circle(radius=0.5).create(),
        Arrow(start=(0,0), end=(1,1)).create()
    ]
    
    # Arrange components
    layout = Layout()
    layout.arrange(components, LayoutType.HORIZONTAL)
    
    # Add labels
    labels = [
        Text("Component A").create(),
        Text("Component B").create()
    ]
    
    return components, labels
```

2. Educational Animations
```python
def create_math_animation():
    # Create equation
    equation = LaTeXText("E = mc^2").create()
    
    # Highlight parts
    self.play(
        FadeInFrom(equation, Vector((0, -1, 0)), config),
        FlashAround(equation, color=(1, 1, 0))
    )
```

## Troubleshooting

Common issues and solutions:
1. Object not visible: Check material settings and camera position
2. Animation not playing: Verify frame ranges and animation configuration
3. Layout issues: Check object dimensions and spacing parameters

## Contributing

Guidelines for contributing:
1. Follow PEP 8 style guide
2. Add unit tests for new features
3. Update documentation
4. Use type hints
5. Follow existing patterns