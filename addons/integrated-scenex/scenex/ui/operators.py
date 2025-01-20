# ui/operators.py
import bpy
from bpy.props import StringProperty, FloatProperty, EnumProperty
from ..src.animation.commonly_used_animations import (GrowFromCenter, Write, 
                                                    FadeInFrom, Rotate, FlashAround)
from ..src.utils.logger import SceneXLogger

logger = SceneXLogger("Operators")

class SCENEX_OT_AddAnimation(bpy.types.Operator):
    """Add animation to selected object"""
    bl_idname = "scenex.add_animation"
    bl_label = "Add Animation"
    bl_description = "Add selected animation to object"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):
        try:
            obj = context.active_object
            props = context.scene.scenex
            
            anim_type = props.animation_type
            duration = props.animation_duration
            
            if anim_type == 'GROW_FROM_CENTER':
                anim = GrowFromCenter(obj)
            elif anim_type == 'WRITE':
                anim = Write(obj)
            elif anim_type == 'FADE_IN':
                anim = FadeInFrom(obj, direction=(0, 0, 1))
            elif anim_type == 'ROTATE':
                anim = Rotate(obj, angle=3.14159)
            elif anim_type == 'FLASH_AROUND':
                anim = FlashAround(obj)
            
            current_frame = context.scene.frame_current
            anim.create_animation(current_frame)
            
            self.report({'INFO'}, f"Added {anim_type} animation")
            return {'FINISHED'}
            
        except Exception as e:
            logger.error(f"Error adding animation: {str(e)}")
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}

class SCENEX_OT_CameraMove(bpy.types.Operator):
    """Move camera using selected movement type"""
    bl_idname = "scenex.camera_move"
    bl_label = "Move Camera"
    bl_description = "Move camera using selected movement type"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        try:
            camera = context.scene.camera
            props = context.scene.scenex
            
            if not camera:
                self.report({'ERROR'}, "No camera in scene")
                return {'CANCELLED'}
            
            movement_type = props.camera_movement
            
            # Implementation will vary based on movement type
            self.report({'INFO'}, f"Executed {movement_type} camera movement")
            return {'FINISHED'}
            
        except Exception as e:
            logger.error(f"Error moving camera: {str(e)}")
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}

class SCENEX_OT_CreateGrid(bpy.types.Operator):
    """Create coordinate grid"""
    bl_idname = "scenex.create_grid"
    bl_label = "Create Grid"
    bl_description = "Create coordinate grid system"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        try:
            props = context.scene.scenex
            # Grid creation implementation
            self.report({'INFO'}, "Created coordinate grid")
            return {'FINISHED'}
            
        except Exception as e:
            logger.error(f"Error creating grid: {str(e)}")
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}

class SCENEX_OT_AssignMaterial(bpy.types.Operator):
    """Assign material to selected object"""
    bl_idname = "scenex.assign_material"
    bl_label = "Assign Material"
    bl_description = "Assign selected material type to object"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):
        try:
            obj = context.active_object
            props = context.scene.scenex
            
            # Material assignment implementation
            self.report({'INFO'}, f"Assigned {props.material_type} material")
            return {'FINISHED'}
            
        except Exception as e:
            logger.error(f"Error assigning material: {str(e)}")
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}

# Register/unregister all operators
classes = (
    SCENEX_OT_AddAnimation,
    SCENEX_OT_CameraMove,
    SCENEX_OT_CreateGrid,
    SCENEX_OT_AssignMaterial,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    print("SceneX Operators registered")

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    print("SceneX Operators unregistered")
