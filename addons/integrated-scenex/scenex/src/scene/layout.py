# SceneX/src/scene/layout.py

import bpy
from enum import Enum
from typing import List, Tuple, Optional
from mathutils import Vector
from ..scene.groups import Group
from ..utils.logger import SceneXLogger

class LayoutType(Enum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"
    GRID = "grid"
    CIRCULAR = "circular"
    SPIRAL = "spiral"

class Layout:
    def __init__(self):
        self.logger = SceneXLogger("Layout")

    def arrange(self, objects: List[bpy.types.Object], 
                layout_type: LayoutType,
                spacing: float = 1.0,
                center: Vector = Vector((0, 0, 0)),
                padding: float = 0.5,
                columns: int = 3) -> None:
        
        if not objects:
            return

        if layout_type == LayoutType.HORIZONTAL:
            self._arrange_horizontal(objects, spacing, center, padding)
        elif layout_type == LayoutType.VERTICAL:
            self._arrange_vertical(objects, spacing, center, padding)
        elif layout_type == LayoutType.GRID:
            self._arrange_grid(objects, spacing, center, padding, columns)
        elif layout_type == LayoutType.CIRCULAR:
            self._arrange_circular(objects, spacing, center, padding)
        elif layout_type == LayoutType.SPIRAL:
            self._arrange_spiral(objects, spacing, center, padding)

    def _arrange_horizontal(self, objects, spacing, center, padding):
        total_width = sum(obj.dimensions.x for obj in objects) + spacing * (len(objects) - 1)
        start_x = center.x - total_width/2 + objects[0].dimensions.x/2
        
        current_x = start_x
        for obj in objects:
            obj.location = Vector((current_x, center.y, center.z))
            current_x += obj.dimensions.x + spacing

    def _arrange_vertical(self, objects, spacing, center, padding):
        total_height = sum(obj.dimensions.y for obj in objects) + spacing * (len(objects) - 1)
        start_y = center.y + total_height/2 - objects[0].dimensions.y/2
        
        current_y = start_y
        for obj in objects:
            obj.location = Vector((center.x, current_y, center.z))
            current_y -= obj.dimensions.y + spacing

    def _arrange_grid(self, objects, spacing, center, padding, columns):
        rows = (len(objects) + columns - 1) // columns
        row_heights = []
        col_widths = []
        
        for i in range(rows):
            row_objects = objects[i*columns:min((i+1)*columns, len(objects))]
            row_heights.append(max(obj.dimensions.y for obj in row_objects))
        
        for i in range(columns):
            col_objects = [obj for j, obj in enumerate(objects) if j % columns == i]
            if col_objects:
                col_widths.append(max(obj.dimensions.x for obj in col_objects))
        
        total_width = sum(col_widths) + spacing * (columns - 1)
        total_height = sum(row_heights) + spacing * (rows - 1)
        
        start_x = center.x - total_width/2
        start_y = center.y + total_height/2
        
        for i, obj in enumerate(objects):
            row = i // columns
            col = i % columns
            
            x = start_x + sum(col_widths[:col]) + spacing * col + col_widths[col]/2
            y = start_y - (sum(row_heights[:row]) + spacing * row + row_heights[row]/2)
            
            obj.location = Vector((x, y, center.z))

    def _arrange_circular(self, objects, spacing, center, padding):
        count = len(objects)
        radius = max(obj.dimensions.length/2 for obj in objects) + spacing
        angle_step = 2 * 3.14159 / count
        
        for i, obj in enumerate(objects):
            angle = i * angle_step
            x = center.x + radius * math.cos(angle)
            y = center.y + radius * math.sin(angle)
            obj.location = Vector((x, y, center.z))
            obj.rotation_euler.z = angle + 3.14159/2

    def _arrange_spiral(self, objects, spacing, center, padding):
        count = len(objects)
        base_radius = max(obj.dimensions.length/2 for obj in objects) + spacing
        angle_step = 2 * 3.14159 / 8  # More gradual spiral
        
        for i, obj in enumerate(objects):
            angle = i * angle_step
            radius = base_radius * (1 + i/count)
            x = center.x + radius * math.cos(angle)
            y = center.y + radius * math.sin(angle)
            obj.location = Vector((x, y, center.z))
            obj.rotation_euler.z = angle + 3.14159/2