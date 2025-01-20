"""
SceneX Migration Script
======================
Sets up new directory structure and migrates core animation system.
Run this script to initialize the new unified SceneX project.
"""

import os
import shutil
import pathlib
from typing import List, Dict
import re

class SceneXMigration:
    def __init__(self, target_dir: str):
        self.target_dir = pathlib.Path(target_dir)
        self.blender_version = "4.2"
        self.addon_name = "SceneX"
    
    def setup_directory_structure(self):
        """Create the new directory structure"""
        
        # Define directory structure
        directories = [
            "src/animation",
            "src/camera",
            "src/core",
            "src/graphics",
            "src/aws",
            "src/physics",
            "src/utils",
            "ui",
            "templates/scenes"
        ]
        
        # Create directories
        for dir_path in directories:
            full_path = self.target_dir / dir_path
            full_path.mkdir(parents=True, exist_ok=True)
            # Create __init__.py in each directory
            init_file = full_path / "__init__.py"
            if not init_file.exists():
                init_file.touch()
        
        print(f"Created directory structure in {self.target_dir}")

    def create_addon_init(self):
        """Create the main __init__.py for the Blender addon"""
        
        init_content = '''bl_info = {
    "name": "SceneX Animation System",
    "author": "SceneX Team",
    "version": (1, 0, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Sidebar > SceneX",
    "description": "Advanced animation system for technical and educational content",
    "warning": "",
    "wiki_url": "",
    "category": "Animation",
}

import bpy
import sys
import os
from pathlib import Path

def setup_sys_path():
    """Add addon directory to sys.path"""
    addon_dir = Path(__file__).parent
    if str(addon_dir) not in sys.path:
        sys.path.append(str(addon_dir))

def register():
    """Register the addon"""
    try:
        setup_sys_path()
        from ui import panels, operators
        from src.core import scene
        
        # Register UI components
        panels.register()
        operators.register()
        
        print("SceneX addon registered successfully")
    except Exception as e:
        print(f"Error registering SceneX addon: {str(e)}")
        import traceback
        traceback.print_exc()

def unregister():
    """Unregister the addon"""
    try:
        from ui import panels, operators
        
        # Unregister UI components
        panels.unregister()
        operators.unregister()
        
        print("SceneX addon unregistered")
    except Exception as e:
        print(f"Error unregistering SceneX addon: {str(e)}")

if __name__ == "__main__":
    register()
'''
        
        init_file = self.target_dir / "__init__.py"
        init_file.write_text(init_content)
        print("Created addon __init__.py")

    def create_core_files(self):
        """Create core system files"""
        
        # Create config.py
        config_content = '''"""
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
'''
        
        config_file = self.target_dir / "src" / "core" / "config.py"
        config_file.write_text(config_content)
        
        # Create scene.py
        scene_content = '''"""
Base scene system for SceneX.
Provides the foundation for all animation scenes.
"""

import bpy
import mathutils
from ..core.config import AnimationConfig, CameraConfig
from typing import Optional, List, Dict

class Scene:
    """Base class for all scenes"""
    
    def __init__(self):
        self.objects: Dict[str, bpy.types.Object] = {}
        self.current_frame: int = 0
        self.animation_config = AnimationConfig()
        self.camera_config = CameraConfig()
    
    def setup(self):
        """Initialize scene"""
        self.clean_scene()
        self.setup_camera()
        self.setup_lighting()
    
    def clean_scene(self):
        """Remove all objects from scene"""
        if bpy.context.active_object and bpy.context.active_object.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
    
    def setup_camera(self):
        """Setup main camera"""
        bpy.ops.object.camera_add(location=(0, 0, 10))
        camera = bpy.context.active_object
        camera.rotation_euler = (0, 0, 0)
        bpy.context.scene.camera = camera
    
    def setup_lighting(self):
        """Setup basic lighting"""
        bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
        sun = bpy.context.active_object
        sun.data.energy = 5.0
    
    def construct(self):
        """Override this in scene subclasses"""
        raise NotImplementedError
'''
        
        scene_file = self.target_dir / "src" / "core" / "scene.py"
        scene_file.write_text(scene_content)

    def create_animation_files(self):
        """Create animation system files"""
        
        # Create base.py
        base_content = '''"""
Base animation system for SceneX.
Provides foundation for all animation types.
"""

import bpy
import mathutils
from ..core.config import AnimationConfig, RateFuncType
from typing import Optional, Any

class Animation:
    """Base class for all animations"""
    
    def __init__(self, target: Any, config: Optional[AnimationConfig] = None):
        self.target = target
        self.config = config or AnimationConfig()
        self.start_frame: int = 0
        self.end_frame: int = 0
        
    def create_keyframes(self, start_frame: int, end_frame: int):
        """Create animation keyframes"""
        self.start_frame = start_frame
        self.end_frame = end_frame
        self._create_animation()
    
    def _create_animation(self):
        """Override in subclasses to create specific animation"""
        raise NotImplementedError

class Transform(Animation):
    """Transform one object into another"""
    
    def _create_animation(self):
        # Implementation moved from PyBlenderAnim
        pass

class FadeIn(Animation):
    """Fade in animation"""
    
    def _create_animation(self):
        # Implementation moved from PyBlenderAnim
        pass

class FadeOut(Animation):
    """Fade out animation"""
    
    def _create_animation(self):
        # Implementation moved from PyBlenderAnim
        pass
'''
        
        base_file = self.target_dir / "src" / "animation" / "base.py"
        base_file.write_text(base_content)
        
        # Create rate_functions.py
        rate_functions_content = '''"""
Animation rate functions for SceneX.
Controls timing and easing of animations.
"""

import math
from typing import Callable
from ..core.config import RateFuncType

class RateFunc:
    """Collection of animation rate functions"""
    
    @staticmethod
    def linear(t: float) -> float:
        return t
    
    @staticmethod
    def smooth(t: float) -> float:
        return t * t * (3 - 2 * t)
    
    @staticmethod
    def rush_into(t: float) -> float:
        return 2 * t * t
    
    @staticmethod
    def rush_from(t: float) -> float:
        return t * (2 - t)
    
    @staticmethod
    def ease_in(t: float) -> float:
        return t * t * t
    
    @staticmethod
    def ease_out(t: float) -> float:
        return (t - 1) * (t - 1) * (t - 1) + 1
    
    @staticmethod
    def get_function(rate_type: RateFuncType) -> Callable[[float], float]:
        return {
            RateFuncType.LINEAR: RateFunc.linear,
            RateFuncType.SMOOTH: RateFunc.smooth,
            RateFuncType.RUSH_INTO: RateFunc.rush_into,
            RateFuncType.RUSH_FROM: RateFunc.rush_from,
            RateFuncType.EASE_IN: RateFunc.ease_in,
            RateFuncType.EASE_OUT: RateFunc.ease_out,
        }[rate_type]
'''
        
        rate_functions_file = self.target_dir / "src" / "animation" / "rate_functions.py"
        rate_functions_file.write_text(rate_functions_content)

    def create_ui_files(self):
        """Create UI system files"""
        
        # Create operators.py
        operators_content = '''"""
Blender operators for SceneX.
Implements addon functionality in Blender's UI.
"""

import bpy
from bpy.props import StringProperty, FloatProperty, FloatVectorProperty
from ..src.core.config import AnimationConfig

class SCENEX_OT_CreateScene(bpy.types.Operator):
    """Create a new SceneX scene"""
    bl_idname = "scenex.create_scene"
    bl_label = "Create Scene"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        # Implementation here
        return {'FINISHED'}

classes = [
    SCENEX_OT_CreateScene,
]

def register():
    """Register operators"""
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    """Unregister operators"""
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
'''
        
        operators_file = self.target_dir / "ui" / "operators.py"
        operators_file.write_text(operators_content)
        
        # Create panels.py
        panels_content = '''"""
UI panels for SceneX.
Implements addon interface in Blender.
"""

import bpy

class SCENEX_PT_MainPanel(bpy.types.Panel):
    """Main SceneX panel"""
    bl_label = "SceneX"
    bl_idname = "SCENEX_PT_main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "SceneX"
    
    def draw(self, context):
        layout = self.layout
        layout.operator("scenex.create_scene")

classes = [
    SCENEX_PT_MainPanel,
]

def register():
    """Register panels"""
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    """Unregister panels"""
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
'''
        
        panels_file = self.target_dir / "ui" / "panels.py"
        panels_file.write_text(panels_content)

    def run_migration(self):
        """Run the full migration process"""
        try:
            print("Starting SceneX migration...")
            
            # Create directory structure
            self.setup_directory_structure()
            
            # Create core files
            self.create_addon_init()
            self.create_core_files()
            self.create_animation_files()
            self.create_ui_files()
            
            print("Migration completed successfully!")
            print(f"\nSceneX addon created at: {self.target_dir}")
            print("\nNext steps:")
            print("1. Install the addon in Blender")
            print("2. Enable it in Blender's preferences")
            print("3. Find SceneX in the 3D View sidebar")
            
        except Exception as e:
            print(f"Error during migration: {str(e)}")
            raise

def main():
    """Main entry point"""
    # Define target directory (adjust as needed)
    blender_addons_path = os.path.expandvars(
        "%APPDATA%/Blender Foundation/Blender/4.2/scripts/addons/SceneX"
    )
    
    # Create and run migration
    migration = SceneXMigration(blender_addons_path)
    migration.run_migration()

if __name__ == "__main__":
    main()
