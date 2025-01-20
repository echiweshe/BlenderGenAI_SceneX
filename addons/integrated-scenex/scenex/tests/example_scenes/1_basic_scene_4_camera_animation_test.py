# SceneX/tests/example_scenes/basic_scene_3_add_camera.py
import bpy
import mathutils
import math
from src.core.scene import Scene
from src.core.coordinate_system import GridConfig
from src.camera.camera import CameraConfig, CameraSystem

class BasicTestScene(Scene):
    def construct(self):
        self.logger.info("Starting basic test scene construction")
        
        # Setup scene
        self.setup()
        
        # Configure camera
        self.camera = CameraSystem(CameraConfig(
            distance=15.0,
            angle=45.0
        ))
        
        # Set initial camera position and keyframe
        initial_pos = mathutils.Vector((0, -15, 15))
        self.camera.camera.location = initial_pos
        self.camera.camera.keyframe_insert(data_path="location", frame=1)
        self.camera.camera.keyframe_insert(data_path="rotation_euler", frame=1)
        
        # Create coordinate system with grid
        self.coordinate_system.create_grid(GridConfig(
            x_range=(-5, 5),
            y_range=(-3, 3),
            line_thickness=0.02
        ))
        
        # Create shapes
        cube = self.create_cube(size=0.5, location=(-2, 0, 0))
        sphere = self.create_sphere(radius=0.25, location=(2, 0, 0))
        
        # Place objects
        self.coordinate_system.place_object(cube, mathutils.Vector((-2, 1, 0)))
        self.coordinate_system.place_object(sphere, mathutils.Vector((2, -1, 0)))
        
        # Setup timeline
        bpy.context.scene.frame_start = 1
        bpy.context.scene.frame_end = 250
        current_frame = 1

        # Animation sequence

        # Move 1: Initial position to front view (frames 1-50)
        current_frame = 1
        self.camera.camera.location = initial_pos
        self.camera.camera.keyframe_insert(data_path="location", frame=current_frame)
        self.camera.camera.rotation_euler = (math.radians(45), 0, 0)
        self.camera.camera.keyframe_insert(data_path="rotation_euler", frame=current_frame)

        current_frame = 50
        front_pos = mathutils.Vector((0, -8, 8))
        self.camera.camera.location = front_pos
        self.camera.camera.keyframe_insert(data_path="location", frame=current_frame)
        self.camera.camera.rotation_euler = (math.radians(45), 0, 0)
        self.camera.camera.keyframe_insert(data_path="rotation_euler", frame=current_frame)

        # Move 2: Circle around scene (frames 50-150)
        for frame in range(50, 151, 10):
            angle = (frame - 50) * (2 * math.pi) / 100  # Full rotation over 100 frames
            radius = 10
            x = radius * math.sin(angle)
            y = -radius * math.cos(angle)
            z = 8
            
            self.camera.camera.location = mathutils.Vector((x, y, z))
            self.camera.camera.keyframe_insert(data_path="location", frame=frame)
            
            # Point camera at center
            direction = -self.camera.camera.location.normalized()
            rot_quat = direction.to_track_quat('-Z', 'Y')
            self.camera.camera.rotation_euler = rot_quat.to_euler()
            self.camera.camera.keyframe_insert(data_path="rotation_euler", frame=frame)

        # Move 3: Pull back (frames 150-200)
        current_frame = 200
        back_pos = mathutils.Vector((0, -15, 15))
        self.camera.camera.location = back_pos
        self.camera.camera.keyframe_insert(data_path="location", frame=current_frame)
        self.camera.camera.rotation_euler = (math.radians(45), 0, 0)
        self.camera.camera.keyframe_insert(data_path="rotation_euler", frame=current_frame)

        # Move 4: Side view (frames 200-250)
        current_frame = 250
        side_pos = mathutils.Vector((15, 0, 5))
        self.camera.camera.location = side_pos
        self.camera.camera.keyframe_insert(data_path="location", frame=current_frame)
        self.camera.camera.rotation_euler = (math.radians(15), math.radians(90), 0)
        self.camera.camera.keyframe_insert(data_path="rotation_euler", frame=current_frame)

        # Set smooth interpolation for all keyframes
        if self.camera.camera.animation_data and self.camera.camera.animation_data.action:
            for fc in self.camera.camera.animation_data.action.fcurves:
                for kf in fc.keyframe_points:
                    kf.interpolation = 'BEZIER'
                    kf.easing = 'EASE_IN_OUT'

        # Switch to camera view
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        space.region_3d.view_perspective = 'CAMERA'
                        space.lock_camera = True  # Lock camera to view

        # Set current frame to start
        bpy.context.scene.frame_set(1)
        
        self.logger.info("Scene construction completed")

def main():
    try:
        # Create and run the test scene
        scene = BasicTestScene()
        scene.construct()
        print("Test scene completed successfully")
        
        # Start animation playback
        bpy.ops.screen.animation_play()
        
    except Exception as e:
        print(f"Error running test scene: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()