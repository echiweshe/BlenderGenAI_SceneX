bl_info = {
    "name": "SceneX Animation System",
    "author": "Your Name",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > SceneX",
    "description": "Animation system for creating mathematical and educational animations",
    "warning": "",
    "category": "Animation"
}

import bpy

# Import UI modules
from .ui import operators
from .ui import panels
from .ui import properties
from .ui import handlers
from .ui import presets

# These core imports should only be imported where needed, not in the main __init__.py
# from .src.animation import base, commonly_used_animations, rate_functions
# from .src.camera import camera
# from .src.core import scene, coordinate_system
# from .src.geometry import shapes, complex_shapes
# from .src.utils import logger

modules = (
    properties,
    operators,
    panels,
    presets,
)

def register():
    for mod in modules:
        mod.register()
    handlers.register_handlers()
    print("SceneX Animation System registered successfully")

def unregister():
    handlers.unregister_handlers()
    for mod in reversed(modules):
        mod.unregister()
    print("SceneX Animation System unregistered")

if __name__ == "__main__":
    register()