# src/svg/svg.py
import bpy
import os
from pathlib import Path
import mathutils
from utils.logger import SceneXLogger

# Initialize logger
logger = SceneXLogger("SVG")

def import_svg(svg_filename, scale=5.0, location=(0, 0, 0)):
    """Import an SVG and return the parent container (Empty)."""
    logger.info(f"Starting SVG import process for {svg_filename}")
    
    svg_path = Path(os.path.join(os.path.dirname(__file__), svg_filename))
    logger.debug(f"Full SVG path: {svg_path}")
    
    if not svg_path.exists():
        logger.error(f"SVG file not found at: {svg_path}")
        raise FileNotFoundError(f"SVG file not found at: {svg_path}")

    # Store initial state
    initial_objects = set(bpy.data.objects)
    logger.debug(f"Number of objects before import: {len(initial_objects)}")

    try:
        logger.debug("Attempting to import SVG file...")
        bpy.ops.import_curve.svg(filepath=str(svg_path))
        logger.debug("SVG import operation completed")
    except Exception as e:
        logger.error(f"Error during SVG import: {str(e)}")
        return None
    
    # Get new objects
    new_objects = set(bpy.data.objects) - initial_objects
    logger.debug(f"New objects created: {len(new_objects)}")
    
    imported_objects = [obj for obj in new_objects if obj.type == 'CURVE']
    logger.debug(f"Number of curve objects found: {len(imported_objects)}")
    
    if not imported_objects:
        logger.error("No curve objects were imported from the SVG.")
        return None

    # Create Parent Empty
    logger.debug("Creating parent empty object...")
    bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, 0, 0))
    parent = bpy.context.active_object
    parent.name = "Logo_Container"

    # Parent imported objects
    logger.debug("Parenting imported objects...")
    for obj in imported_objects:
        logger.debug(f"Processing object: {obj.name}")
        obj.data.dimensions = '2D'
        obj.data.fill_mode = 'BOTH'
        obj.parent = parent
        obj.location = (0, 0, 0)
    
    # Scale and position
    logger.info("Scaling and positioning logo container...")
    scale_and_position_logo(parent, scale_factor=scale, location=location)
    
    logger.info(f"SVG import complete: {parent.name}")
    return parent

def scale_and_position_logo(logo_container, scale_factor=11.0, location=(0, 0, 0)):
    """Scale and place the logo at specified coordinates."""
    if not logo_container:
        logger.warning("No logo container provided")
        return
    
    logger.debug(f"Initial scale_factor: {scale_factor}")
    logo_container.scale = (scale_factor, scale_factor, scale_factor)
    logger.debug(f"Applied scale: {logo_container.scale}")
    
    logo_container.location = mathutils.Vector(location)
    logger.debug(f"Set position to: {location}")
    
    bpy.context.view_layer.update()
    logger.info(f"Logo positioned with scale factor: {scale_factor}")

def position_logo_bottom_right(logo_container, margin=1.0):
    """Position the logo at the bottom-right corner."""
    if not logo_container:
        logger.warning("No logo container provided for positioning")
        return
    
    logger.debug(f"Starting bottom-right positioning with margin: {margin}")
    position = (7, -4, 0)  # Fixed coordinate position
    
    logo_container.location = mathutils.Vector(position)
    logger.debug(f"Set position to: {position}")
    
    bpy.context.view_layer.update()
    logger.info(f"Logo positioned at: {position}")

def dynamic_scale(logo_container, target_width=1920):
    current_width = bpy.context.scene.render.resolution_x
    scale_factor = target_width / current_width
    logo_container.scale *= scale_factor
