# SceneX/tests/example_scenes/basic_scene_2.py
import bpy
import mathutils
from src.core.scene import Scene
from src.core.mobject import Mobject
from src.core.coordinate_system import GridConfig  # Add this import

class BasicTestScene(Scene):
    def construct(self):
        self.logger.info("Starting basic test scene construction")
        
        # Setup the scene first
        self.setup()
        
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
        
        self.logger.info("Scene construction completed")

def main():
    try:
        # Create and run the test scene
        scene = BasicTestScene()
        scene.construct()
        print("Test scene completed successfully")
        
    except Exception as e:
        print(f"Error running test scene: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()