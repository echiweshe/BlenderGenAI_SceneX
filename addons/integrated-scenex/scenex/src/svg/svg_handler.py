# src/svg/svg_handler.py

import bpy
import os
from pathlib import Path
from ..utils.logger import SceneXLogger

class SVGHandler:
    """Handle SVG import and manipulation"""
    def __init__(self):
        self.logger = SceneXLogger("SVGHandler")
        
    def import_svg(self, svg_filename: str, scale: float = 1.0, location=(0, 0, 0)):
        """Import SVG and return parent container"""
        self.logger.info(f"Starting SVG import for {svg_filename}")
        
        # Get SVG path
        svg_path = Path(os.path.join(os.path.dirname(__file__), svg_filename))
        self.logger.debug(f"Full SVG path: {svg_path}")
        
        if not svg_path.exists():
            self.logger.error(f"SVG file not found at: {svg_path}")
            raise FileNotFoundError(f"SVG file not found at: {svg_path}")

        # Store initial state
        initial_objects = set(bpy.data.objects)

        try:
            # Import SVG
            self.logger.debug("Importing SVG file...")
            bpy.ops.import_curve.svg(filepath=str(svg_path))
            
            # Get new objects
            new_objects = [obj for obj in bpy.data.objects 
                         if obj not in initial_objects and obj.type in ['CURVE', 'GPENCIL']]
            
            if not new_objects:
                self.logger.error("No curve objects imported from SVG")
                return None

            # Create parent empty
            bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
            parent = bpy.context.active_object
            parent.name = "SVG_Container"

            # Process imported objects
            for obj in new_objects:
                self.logger.debug(f"Processing {obj.name}")
                if obj.type == 'CURVE':
                    obj.data.dimensions = '2D'
                    obj.data.fill_mode = 'BOTH'
                obj.parent = parent
                obj.location = (0, 0, 0)

            # Apply scale and position
            parent.scale = (scale, scale, scale)
            parent.location = location
            
            self.logger.info("SVG import completed successfully")
            return parent

        except Exception as e:
            self.logger.error(f"Error during SVG import: {str(e)}")
            return None

    def scale_svg(self, svg_container, scale_factor: float = 1.0):
        """Scale SVG container"""
        if not svg_container:
            self.logger.warning("No SVG container provided for scaling")
            return
            
        svg_container.scale = (scale_factor, scale_factor, scale_factor)
        self.logger.info(f"SVG scaled by factor: {scale_factor}")

    def position_svg(self, svg_container, location=(0, 0, 0)):
        """Position SVG container"""
        if not svg_container:
            self.logger.warning("No SVG container provided for positioning")
            return
            
        svg_container.location = location
        self.logger.info(f"SVG positioned at: {location}")

    def get_svg_dimensions(self, svg_container):
        """Get dimensions of SVG container"""
        if not svg_container:
            return (0, 0, 0)
            
        # Calculate bounds from all child objects
        min_x = min_y = min_z = float('inf')
        max_x = max_y = max_z = float('-inf')
        
        for obj in svg_container.children:
            if obj.type == 'CURVE':
                for point in obj.bound_box:
                    x, y, z = point
                    min_x = min(min_x, x)
                    max_x = max(max_x, x)
                    min_y = min(min_y, y)
                    max_y = max(max_y, y)
                    min_z = min(min_z, z)
                    max_z = max(max_z, z)
        
        return (
            max_x - min_x,
            max_y - min_y,
            max_z - min_z
        )