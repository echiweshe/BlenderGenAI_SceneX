# ui/handlers.py
import bpy
from ..src.utils.logger import SceneXLogger

logger = SceneXLogger("Handlers")

def update_animation_type(self, context):
    """Handle animation type changes"""
    try:
        if self.animation_type == 'WRITE' and context.active_object:
            if context.active_object.type != 'FONT':
                self.animation_type = 'FADE_IN'
                logger.warning("Write animation can only be applied to text objects")
                
    except Exception as e:
        logger.error(f"Error in animation type update: {str(e)}")

def update_camera_movement(self, context):
    """Handle camera movement type changes"""
    try:
        if not context.scene.camera:
            logger.warning("No camera in scene")
            return
            
        movement_type = self.camera_movement
        if movement_type == 'FRAME_OBJECT' and not context.selected_objects:
            logger.warning("No object selected to frame")
            return
            
        logger.info(f"Camera movement updated to: {movement_type}")
            
    except Exception as e:
        logger.error(f"Error in camera movement update: {str(e)}")

def update_material_type(self, context):
    """Handle material type changes"""
    try:
        if not context.active_object:
            logger.warning("No active object for material assignment")
            return
            
        # Update material preview if it exists
        if hasattr(context.active_object, 'active_material'):
            material_type = self.material_type
            # Future: Update material preview
            logger.info(f"Material type updated to: {material_type}")
            
    except Exception as e:
        logger.error(f"Error in material type update: {str(e)}")

def update_grid_settings(self, context):
    """Handle grid setting changes"""
    try:
        # Future: Update grid visualization
        logger.info("Grid settings updated")
        
    except Exception as e:
        logger.error(f"Error in grid settings update: {str(e)}")

# Register update handlers with properties
def register_handlers():
    """Register all property update handlers"""
    try:
        # Update SceneXProperties class to include update callbacks
        bpy.types.Scene.scenex.animation_type.update = update_animation_type
        bpy.types.Scene.scenex.camera_movement.update = update_camera_movement
        bpy.types.Scene.scenex.material_type.update = update_material_type
        bpy.types.Scene.scenex.grid_size.update = update_grid_settings
        bpy.types.Scene.scenex.grid_subdivisions.update = update_grid_settings
        
        logger.info("Property update handlers registered")
        
    except Exception as e:
        logger.error(f"Error registering update handlers: {str(e)}")

def unregister_handlers():
    """Unregister all property update handlers"""
    try:
        # Remove update callbacks
        bpy.types.Scene.scenex.animation_type.update = None
        bpy.types.Scene.scenex.camera_movement.update = None
        bpy.types.Scene.scenex.material_type.update = None
        bpy.types.Scene.scenex.grid_size.update = None
        bpy.types.Scene.scenex.grid_subdivisions.update = None
        
        logger.info("Property update handlers unregistered")
        
    except Exception as e:
        logger.error(f"Error unregistering update handlers: {str(e)}")

        