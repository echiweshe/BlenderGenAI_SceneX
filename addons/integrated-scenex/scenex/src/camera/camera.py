# SceneX/src/camera/camera.py
import bpy
import math
import mathutils
from src.utils.logger import SceneXLogger
from dataclasses import dataclass
from typing import Optional, Tuple

@dataclass
class CameraConfig:
    """Configuration for camera setup"""
    frame_width: float = 14.0
    frame_height: float = 8.0
    focal_length: float = 50
    distance: float = 10.0
    angle: float = 55.0
    position: Tuple[float, float, float] = (7, -7, 5)
    target_origin: bool = True

class CameraSystem:
    def __init__(self, config: Optional[CameraConfig] = None):
        self.config = config or CameraConfig()
        self.camera = None
        self.target = None
        self.logger = SceneXLogger("CameraSystem")
        self.setup()

    def setup(self):
        """Initialize camera with Manim-style defaults"""
        self.logger.info("Setting up camera")
        try:
            # Create camera
            if not self.camera:
                bpy.ops.object.camera_add(location=self.config.position)
                self.camera = bpy.context.active_object
            
            # Set as active camera
            bpy.context.scene.camera = self.camera
            self.camera.rotation_euler = (math.radians(45), 0, math.radians(45))
            
            # Create target for tracking
            if self.config.target_origin:
                bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
                self.target = bpy.context.active_object
                self.target.name = "CameraTarget"
                self._setup_constraints()

            # Setup keyframes
            self.camera.keyframe_insert(data_path="location", frame=1)
            self.camera.keyframe_insert(data_path="rotation_euler", frame=1)
            
            if self.target:
                self.target.keyframe_insert(data_path="location", frame=1)

            # Create animation data
            if not self.camera.animation_data:
                self.camera.animation_data_create()
                
            self.logger.info("Camera setup complete")
            
        except Exception as e:
            self.logger.error(f"Error setting up camera: {str(e)}")

    def _setup_constraints(self):
        """Setup camera constraints for tracking"""
        self.camera.constraints.clear()
        track = self.camera.constraints.new(type='TRACK_TO')
        track.target = self.target
        track.track_axis = 'TRACK_NEGATIVE_Z'
        track.up_axis = 'UP_Y'

    # [Rest of the existing methods remain unchanged: frame_point, 
    #  animate_movement, animate_rotation_around_target, zoom]

    def frame_point(self, point: mathutils.Vector):
        """Frame camera to look at specific point"""
        self.logger.info(f"Framing point: {point}")
        
        try:
            # Move target to point
            self.target.location = point
            
            # Update scene
            bpy.context.view_layer.update()
            
        except Exception as e:
            self.logger.error(f"Error framing point: {str(e)}")

    def animate_movement(self, start_frame: int, end_frame: int, 
                        target_location: mathutils.Vector, 
                        target_rotation: Optional[Tuple[float, float, float]] = None):
        """Animate camera movement between frames"""
        self.logger.info(f"Animating camera from frame {start_frame} to {end_frame}")
        
        try:
            # Set initial keyframe
            self.camera.location.keyframe_insert(data_path="location", frame=start_frame)
            if target_rotation:
                self.camera.rotation_euler.keyframe_insert(data_path="rotation_euler", frame=start_frame)
            
            # Set target keyframe
            self.camera.location = target_location
            self.camera.keyframe_insert(data_path="location", frame=end_frame)
            
            if target_rotation:
                self.camera.rotation_euler = mathutils.Euler(target_rotation)
                self.camera.keyframe_insert(data_path="rotation_euler", frame=end_frame)
                
            # Set interpolation
            if self.camera.animation_data and self.camera.animation_data.action:
                for fc in self.camera.animation_data.action.fcurves:
                    for kf in fc.keyframe_points:
                        kf.interpolation = 'BEZIER'
                        kf.easing = 'EASE_IN_OUT'
                    
        except Exception as e:
            self.logger.error(f"Error animating camera: {str(e)}")

    def animate_rotation_around_target(self, start_frame: int, end_frame: int, 
                                     start_angles: Tuple[float, float], 
                                     end_angles: Tuple[float, float]):
        """Animate camera rotating around target point"""
        self.logger.info(f"Animating camera rotation from frame {start_frame} to {end_frame}")
        
        try:
            # Temporarily clear constraints
            constraints = self.camera.constraints.copy()
            self.camera.constraints.clear()
            
            # Calculate and set start position
            phi_start, theta_start = start_angles
            x_start = self.config.distance * math.sin(theta_start) * math.cos(phi_start)
            y_start = self.config.distance * math.cos(theta_start) * math.cos(phi_start)
            z_start = self.config.distance * math.sin(phi_start)
            
            self.camera.location = (x_start, y_start, z_start)
            self.camera.keyframe_insert(data_path="location", frame=start_frame)
            
            # Calculate and set end position
            phi_end, theta_end = end_angles
            x_end = self.config.distance * math.sin(theta_end) * math.cos(phi_end)
            y_end = self.config.distance * math.cos(theta_end) * math.cos(phi_end)
            z_end = self.config.distance * math.sin(phi_end)
            
            self.camera.location = (x_end, y_end, z_end)
            self.camera.keyframe_insert(data_path="location", frame=end_frame)
            
            # Also animate rotation to keep facing center
            for frame in range(start_frame, end_frame + 1, 10):  # Add intermediate keyframes
                t = (frame - start_frame) / (end_frame - start_frame)
                theta_current = theta_start + t * (theta_end - theta_start)
                phi_current = phi_start + t * (phi_end - phi_start)
                
                # Update camera rotation to look at target
                direction = -mathutils.Vector((
                    math.sin(theta_current) * math.cos(phi_current),
                    math.cos(theta_current) * math.cos(phi_current),
                    math.sin(phi_current)
                ))
                rot_quat = direction.to_track_quat('-Z', 'Y')
                self.camera.rotation_euler = rot_quat.to_euler()
                self.camera.keyframe_insert(data_path="rotation_euler", frame=frame)
            
            # Restore constraints
            for constraint in constraints:
                self.camera.constraints.append(constraint)
            
            # Set smooth interpolation
            if self.camera.animation_data and self.camera.animation_data.action:
                for fc in self.camera.animation_data.action.fcurves:
                    for kf in fc.keyframe_points:
                        kf.interpolation = 'BEZIER'
                        kf.easing = 'EASE_IN_OUT'
                        
        except Exception as e:
            self.logger.error(f"Error animating camera rotation: {str(e)}")

    def zoom(self, factor: float):
        """Zoom camera by factor"""
        try:
            # Adjust camera distance
            current_loc = mathutils.Vector(self.camera.location)
            target_loc = mathutils.Vector(self.target.location)
            direction = (current_loc - target_loc).normalized()
            
            new_distance = self.config.distance * factor
            new_loc = target_loc + direction * new_distance
            
            self.camera.location = new_loc
            
        except Exception as e:
            self.logger.error(f"Error zooming camera: {str(e)}")
