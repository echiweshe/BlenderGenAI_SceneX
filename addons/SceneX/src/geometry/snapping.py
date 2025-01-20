# src/geometry/snapping.py

import bpy
import mathutils
from ..utils.logger import SceneXLogger

class SnapSystem:
    """Handle object snapping and connections"""
    def __init__(self, grid_size: float = 1.0):
        self.grid_size = grid_size
        self.logger = SceneXLogger("SnapSystem")
        self.connection_lines = []
    
    def snap_to_grid(self, obj: bpy.types.Object):
        """Snap object to nearest grid point"""
        try:
            location = obj.location.copy()
            
            # Snap to grid
            location.x = round(location.x / self.grid_size) * self.grid_size
            location.y = round(location.y / self.grid_size) * self.grid_size
            location.z = round(location.z / self.grid_size) * self.grid_size
            
            obj.location = location
            self.logger.info(f"Snapped {obj.name} to grid")
            
        except Exception as e:
            self.logger.error(f"Error snapping to grid: {str(e)}")
    
    def connect_objects(self, obj1: bpy.types.Object, obj2: bpy.types.Object, 
                       type: str = 'LINE', thickness: float = 0.05):
        """Create a visual connection between two objects"""
        try:
            # Get connection points (object centers for now)
            start = obj1.location
            end = obj2.location
            
            # Create curve
            curve_data = bpy.data.curves.new('connection', 'CURVE')
            curve_data.dimensions = '3D'
            
            # Create spline
            spline = curve_data.splines.new('BEZIER')
            spline.bezier_points.add(1)
            
            # Set points
            spline.bezier_points[0].co = start
            spline.bezier_points[1].co = end
            
            # Set handles
            direction = (end - start).normalized()
            handle_length = (end - start).length / 3
            
            spline.bezier_points[0].handle_right = start + direction * handle_length
            spline.bezier_points[0].handle_left = start
            spline.bezier_points[1].handle_left = end - direction * handle_length
            spline.bezier_points[1].handle_right = end
            
            # Create curve object
            curve_obj = bpy.data.objects.new('connection', curve_data)
            curve_obj.data.bevel_depth = thickness
            
            # Link to scene
            bpy.context.scene.collection.objects.link(curve_obj)
            self.connection_lines.append(curve_obj)
            
            self.logger.info(f"Created connection between {obj1.name} and {obj2.name}")
            return curve_obj
            
        except Exception as e:
            self.logger.error(f"Error creating connection: {str(e)}")
            return None
    
    def update_connections(self):
        """Update all connection line positions"""
        for line in self.connection_lines:
            if len(line.data.splines[0].bezier_points) >= 2:
                points = line.data.splines[0].bezier_points
                start_obj = line.get('start_object')
                end_obj = line.get('end_object')
                
                if start_obj and end_obj:
                    points[0].co = start_obj.location
                    points[1].co = end_obj.location
    
    def remove_connections(self):
        """Remove all connection lines"""
        for line in self.connection_lines:
            bpy.data.objects.remove(line, do_unlink=True)
        self.connection_lines.clear()

class SmartConnector:
    """Automatically create and maintain object connections"""
    def __init__(self):
        self.snap_system = SnapSystem()
        self.logger = SceneXLogger("SmartConnector")
        self.connections = {}  # Store object relationships
    
    def connect_with_type(self, obj1: bpy.types.Object, obj2: bpy.types.Object, 
                         connection_type: str = 'DIRECT'):
        """Create a typed connection between objects"""
        try:
            if connection_type == 'DIRECT':
                curve = self.snap_system.connect_objects(obj1, obj2)
            elif connection_type == 'ORTHOGONAL':
                curve = self._create_orthogonal_connection(obj1, obj2)
            elif connection_type == 'ARC':
                curve = self._create_arc_connection(obj1, obj2)
            
            if curve:
                # Store relationship
                curve['start_object'] = obj1
                curve['end_object'] = obj2
                curve['connection_type'] = connection_type
                
                # Add to connections dict
                key = (obj1.name, obj2.name)
                self.connections[key] = curve
            
            return curve
            
        except Exception as e:
            self.logger.error(f"Error creating typed connection: {str(e)}")
            return None
    
    def _create_orthogonal_connection(self, obj1, obj2):
        """Create connection with orthogonal segments"""
        # Implementation for orthogonal path routing
        pass
    
    def _create_arc_connection(self, obj1, obj2):
        """Create curved arc connection"""
        # Implementation for arc connections
        pass
    
    def update_all_connections(self):
        """Update all connection positions"""
        for (start_name, end_name), curve in self.connections.items():
            start_obj = bpy.data.objects.get(start_name)
            end_obj = bpy.data.objects.get(end_name)
            
            if start_obj and end_obj:
                connection_type = curve.get('connection_type', 'DIRECT')
                if connection_type == 'DIRECT':
                    self.snap_system.update_connections()
                elif connection_type == 'ORTHOGONAL':
                    self._update_orthogonal_connection(curve, start_obj, end_obj)
                elif connection_type == 'ARC':
                    self._update_arc_connection(curve, start_obj, end_obj)
    
    def _update_orthogonal_connection(self, curve, start_obj, end_obj):
        """Update orthogonal connection path"""
        # Implementation for updating orthogonal paths
        pass
    
    def _update_arc_connection(self, curve, start_obj, end_obj):
        """Update arc connection curve"""
        # Implementation for updating arc connections
        pass