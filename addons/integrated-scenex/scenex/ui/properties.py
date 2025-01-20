# ui/properties.py
import bpy
from bpy.props import (StringProperty, BoolProperty, FloatProperty, 
                      EnumProperty, FloatVectorProperty, IntProperty)
from ..src.animation.rate_functions import RateFuncType

def get_rate_func_items():
    return [(rf.name, rf.name.title().replace('_', ' '), 
             f"Use {rf.name.lower().replace('_', ' ')} rate function")
            for rf in RateFuncType]

class SceneXProperties(bpy.types.PropertyGroup):
    """Property group for SceneX addon settings"""
    
    # Animation Properties
    animation_duration: IntProperty(
        name="Duration",
        description="Duration of animation in frames",
        default=30,
        min=1,
        soft_max=300
    )
    
    animation_type: EnumProperty(
        name="Animation Type",
        description="Type of animation to create",
        items=[
            ('GROW_FROM_CENTER', "Grow From Center", "Grow object from its center point"),
            ('WRITE', "Write", "Write text character by character"),
            ('FADE_IN', "Fade In", "Fade object into view"),
            ('ROTATE', "Rotate", "Rotate object around axis"),
            ('FLASH_AROUND', "Flash Around", "Create a flash effect around object")
        ],
        default='FADE_IN'
    )
    
    rate_function: EnumProperty(
        name="Rate Function",
        description="Animation rate function to use",
        items=get_rate_func_items(),
        default='LINEAR'
    )
    
    # Camera Properties
    camera_movement: EnumProperty(
        name="Camera Movement",
        description="Type of camera movement to perform",
        items=[
            ('DOLLY', "Dolly", "Move camera forward/backward"),
            ('ORBIT', "Orbit", "Orbit around target"),
            ('FLY_TO', "Fly To", "Smoothly move to new position"),
            ('FRAME_OBJECT', "Frame Object", "Frame selected object")
        ],
        default='DOLLY'
    )
    
    camera_target_distance: FloatProperty(
        name="Target Distance",
        description="Distance to maintain from camera target",
        default=10.0,
        min=0.1,
        soft_max=100.0
    )
    
    # Grid Properties
    grid_size: FloatProperty(
        name="Grid Size",
        description="Size of the coordinate grid",
        default=10.0,
        min=1.0,
        soft_max=50.0
    )
    
    grid_subdivisions: IntProperty(
        name="Grid Subdivisions",
        description="Number of grid subdivisions",
        default=10,
        min=1,
        soft_max=50
    )
    
    show_labels: BoolProperty(
        name="Show Labels",
        description="Show coordinate labels on grid",
        default=True
    )
    
    # Material Properties
    material_type: EnumProperty(
        name="Material Type",
        description="Type of material to create",
        items=[
            ('BASIC', "Basic", "Basic material with color"),
            ('GLASS', "Glass", "Transparent glass material"),
            ('EMISSION', "Emission", "Glowing emission material"),
            ('METALLIC', "Metallic", "Metallic material"),
            ('TOON', "Toon", "Toon/cel-shaded material")
        ],
        default='BASIC'
    )
    
    material_color: FloatVectorProperty(
        name="Color",
        description="Material color",
        subtype='COLOR',
        size=4,
        min=0.0,
        max=1.0,
        default=(1.0, 1.0, 1.0, 1.0)
    )

def register():
    bpy.utils.register_class(SceneXProperties)
    bpy.types.Scene.scenex = bpy.props.PointerProperty(type=SceneXProperties)
    print("SceneX Properties registered")

def unregister():
    del bpy.types.Scene.scenex
    bpy.utils.unregister_class(SceneXProperties)
    print("SceneX Properties unregistered")