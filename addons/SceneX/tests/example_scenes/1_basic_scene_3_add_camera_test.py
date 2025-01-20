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
        
        # Setup the scene first
        self.setup()
        
        # Configure camera
        self.camera = CameraSystem(CameraConfig(
            distance=15.0,
            angle=45.0
        ))
        self.camera.setup()
        
        # Create coordinate system with grid
        self.coordinate_system.create_grid(GridConfig(
            x_range=(-5, 5),
            y_range=(-3, 3),
            line_thickness=0.02
        ))
        
        # Create basic shapes
        cube = self.create_cube(size=0.5, location=(-2, 0, 0))
        sphere = self.create_sphere(radius=0.25, location=(2, 0, 0))
        
        # Place objects using coordinate system
        self.coordinate_system.place_object(cube, mathutils.Vector((-2, 1, 0)))
        self.coordinate_system.place_object(sphere, mathutils.Vector((2, -1, 0)))
        
        # Frame the scene
        self.camera.frame_point(mathutils.Vector((0, 0, 0)))
        
        # Add some camera movement
        self.camera.zoom(0.8)  # Zoom in slightly
        self.camera.rotate(math.radians(30), math.radians(45))  # Rotate for better view
        
        # Switch to camera view in all 3D viewports
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        space.region_3d.view_perspective = 'CAMERA'
        
        self.logger.info("Scene construction completed")

def main():
    try:
        # Create and run the test scene
        scene = BasicTestScene()
        scene.construct()
        print("Test scene completed successfully")
        
        # Keep Blender open
        bpy.ops.wm.window_fullscreen_toggle()  # Optional: toggle fullscreen
        
    except Exception as e:
        print(f"Error running test scene: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()


    ## blender --window-geometry 0 0 1920 1080 --python .\tests\example_scenes\basic_scene_3_add_camera.py