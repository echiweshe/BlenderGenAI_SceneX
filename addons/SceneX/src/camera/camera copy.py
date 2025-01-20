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
    frame_width: float = 14.0  # Manim-style default
    frame_height: float = 8.0
    focal_length: float = 50
    distance: float = 10.0
    angle: float = 55.0  # Degrees
    position: Tuple[float, float, float] = (0, 0, 0)

class CameraSystem:
    def __init__(self, config: Optional[CameraConfig] = None):
        self.config = config or CameraConfig()
        self.camera = None
        self.target = None
        self.logger = SceneXLogger("CameraSystem")

    def setup(self):
        """Initialize camera with Manim-style defaults"""
        self.logger.info("Setting up camera")
        
        try:
            # Create camera if it doesn't exist
            if not self.camera:
                bpy.ops.object.camera_add()
                self.camera = bpy.context.active_object
                
            # Set as active camera
            bpy.context.scene.camera = self.camera
            
            # Set initial position
            self.camera.location = (0, -self.config.distance, self.config.distance)
            self.camera.rotation_euler = (math.radians(self.config.angle), 0, 0)
            
            # Configure camera settings
            cam_data = self.camera.data
            cam_data.lens = self.config.focal_length
            
            # Create target empty for tracking
            if not self.target:
                bpy.ops.object.empty_add(type='PLAIN_AXES')
                self.target = bpy.context.active_object
                self.target.name = "CameraTarget"
                
            # Setup camera constraints
            self._setup_constraints()
            
            self.logger.info("Camera setup complete")
            
        except Exception as e:
            self.logger.error(f"Error setting up camera: {str(e)}")

    def _setup_constraints(self):
        """Setup camera constraints for tracking"""
        # Clear existing constraints
        self.camera.constraints.clear()
        
        # Add track to constraint
        track = self.camera.constraints.new(type='TRACK_TO')
        track.target = self.target
        track.track_axis = 'TRACK_NEGATIVE_Z'
        track.up_axis = 'UP_Y'

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

    def rotate(self, phi: float, theta: float):
        """Rotate camera around target (phi: up/down, theta: left/right)"""
        try:
            # Calculate new position
            distance = self.config.distance
            x = distance * math.sin(theta) * math.cos(phi)
            y = distance * math.cos(theta) * math.cos(phi)
            z = distance * math.sin(phi)
            
            # Update camera position
            self.camera.location = (x, y, z)
            
            # Update scene
            bpy.context.view_layer.update()
            
        except Exception as e:
            self.logger.error(f"Error rotating camera: {str(e)}")



    # ANIMATIOM - SceneX/src/camera/camera.py
    # Add to existing CameraSystem class:

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
            # Calculate start position
            phi_start, theta_start = start_angles
            x_start = self.config.distance * math.sin(theta_start) * math.cos(phi_start)
            y_start = self.config.distance * math.cos(theta_start) * math.cos(phi_start)
            z_start = self.config.distance * math.sin(phi_start)
            
            # Calculate end position
            phi_end, theta_end = end_angles
            x_end = self.config.distance * math.sin(theta_end) * math.cos(phi_end)
            y_end = self.config.distance * math.cos(theta_end) * math.cos(phi_end)
            z_end = self.config.distance * math.sin(phi_end)
            
            # Set keyframes
            self.camera.location = (x_start, y_start, z_start)
            self.camera.keyframe_insert(data_path="location", frame=start_frame)
            
            self.camera.location = (x_end, y_end, z_end)
            self.camera.keyframe_insert(data_path="location", frame=end_frame)
            
            # Set interpolation
            if self.camera.animation_data and self.camera.animation_data.action:
                for fc in self.camera.animation_data.action.fcurves:
                    for kf in fc.keyframe_points:
                        kf.interpolation = 'BEZIER'
                        kf.easing = 'EASE_IN_OUT'
                        
        except Exception as e:
            self.logger.error(f"Error animating camera rotation: {str(e)}")