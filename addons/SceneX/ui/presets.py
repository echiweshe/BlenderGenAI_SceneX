# ui/presets.py
import bpy
import os
import json
from bpy.props import StringProperty
from bpy.types import Operator, Menu
from ..src.utils.logger import SceneXLogger

logger = SceneXLogger("Presets")

class SCENEX_MT_PresetMenu(Menu):
    bl_label = "SceneX Presets"
    bl_idname = "SCENEX_MT_preset_menu"
    preset_subdir = "scenex/presets"
    preset_operator = "script.execute_preset"
    
    def draw(self, context):
        self.draw_preset(context)
    
    def draw_preset(self, context):
        layout = self.layout
        layout.operator("scenex.save_preset", text="Save Current Settings")
        layout.separator()
        
        # Add preset operators
        layout.operator_context = 'EXEC_DEFAULT'
        
        # Animation presets
        layout.label(text="Animation Presets:")
        layout.operator("scenex.load_preset", text="Basic Fade In").preset_name = "basic_fade"
        layout.operator("scenex.load_preset", text="Dramatic Entrance").preset_name = "dramatic_entrance"
        
        # Camera presets
        layout.label(text="Camera Presets:")
        layout.operator("scenex.load_preset", text="Overview Shot").preset_name = "camera_overview"
        layout.operator("scenex.load_preset", text="Close Up").preset_name = "camera_closeup"
        
        # Material presets
        layout.label(text="Material Presets:")
        layout.operator("scenex.load_preset", text="Glass Material").preset_name = "glass_material"
        layout.operator("scenex.load_preset", text="Metallic Material").preset_name = "metallic_material"

class SCENEX_OT_SavePreset(Operator):
    """Save current settings as a preset"""
    bl_idname = "scenex.save_preset"
    bl_label = "Save Preset"
    bl_description = "Save current SceneX settings as a preset"
    bl_options = {'REGISTER', 'UNDO'}
    
    preset_name: StringProperty(
        name="Preset Name",
        description="Name of the preset to save",
        default="New Preset"
    )
    
    def execute(self, context):
        try:
            props = context.scene.scenex
            preset_data = {
                "animation_type": props.animation_type,
                "animation_duration": props.animation_duration,
                "rate_function": props.rate_function,
                "camera_movement": props.camera_movement,
                "camera_target_distance": props.camera_target_distance,
                "material_type": props.material_type,
                "material_color": list(props.material_color),
                "grid_size": props.grid_size,
                "grid_subdivisions": props.grid_subdivisions,
                "show_labels": props.show_labels
            }
            
            # Create presets directory if it doesn't exist
            presets_path = os.path.join(bpy.utils.user_resource('SCRIPTS'), 
                                      "presets", "scenex")
            os.makedirs(presets_path, exist_ok=True)
            
            # Save preset file
            preset_file = os.path.join(presets_path, f"{self.preset_name}.json")
            with open(preset_file, 'w') as f:
                json.dump(preset_data, f, indent=4)
            
            self.report({'INFO'}, f"Saved preset: {self.preset_name}")
            return {'FINISHED'}
            
        except Exception as e:
            logger.error(f"Error saving preset: {str(e)}")
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class SCENEX_OT_LoadPreset(Operator):
    """Load a saved preset"""
    bl_idname = "scenex.load_preset"
    bl_label = "Load Preset"
    bl_description = "Load a saved SceneX preset"
    bl_options = {'REGISTER', 'UNDO'}
    
    preset_name: StringProperty(
        name="Preset Name",
        description="Name of the preset to load"
    )
    
    def execute(self, context):
        try:
            # Load preset file
            presets_path = os.path.join(bpy.utils.user_resource('SCRIPTS'), 
                                      "presets", "scenex")
            preset_file = os.path.join(presets_path, f"{self.preset_name}.json")
            
            if not os.path.exists(preset_file):
                # Load from default presets
                default_presets = self.get_default_presets()
                if self.preset_name in default_presets:
                    preset_data = default_presets[self.preset_name]
                else:
                    self.report({'ERROR'}, f"Preset not found: {self.preset_name}")
                    return {'CANCELLED'}
            else:
                with open(preset_file, 'r') as f:
                    preset_data = json.load(f)
            
            # Apply preset data
            props = context.scene.scenex
            for key, value in preset_data.items():
                if hasattr(props, key):
                    if key == "material_color":
                        setattr(props, key, tuple(value))
                    else:
                        setattr(props, key, value)
            
            self.report({'INFO'}, f"Loaded preset: {self.preset_name}")
            return {'FINISHED'}
            
        except Exception as e:
            logger.error(f"Error loading preset: {str(e)}")
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}
    
    def get_default_presets(self):
        """Get built-in default presets"""
        return {
            "basic_fade": {
                "animation_type": "FADE_IN",
                "animation_duration": 30,
                "rate_function": "SMOOTH"
            },
            "dramatic_entrance": {
                "animation_type": "GROW_FROM_CENTER",
                "animation_duration": 45,
                "rate_function": "EXPONENTIAL"
            },
            "camera_overview": {
                "camera_movement": "ORBIT",
                "camera_target_distance": 15.0
            },
            "camera_closeup": {
                "camera_movement": "DOLLY",
                "camera_target_distance": 5.0
            },
            "glass_material": {
                "material_type": "GLASS",
                "material_color": [0.9, 0.9, 1.0, 0.2]
            },
            "metallic_material": {
                "material_type": "METALLIC",
                "material_color": [0.8, 0.8, 0.8, 1.0]
            }
        }

# Register/unregister preset system
classes = (
    SCENEX_MT_PresetMenu,
    SCENEX_OT_SavePreset,
    SCENEX_OT_LoadPreset,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    print("SceneX Preset System registered")

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    print("SceneX Preset System unregistered")
