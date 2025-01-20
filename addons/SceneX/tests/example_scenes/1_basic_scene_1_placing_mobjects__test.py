# SceneX/tests/example_scenes/basic_scene.py
import bpy
import mathutils
from src.core.scene import Scene
from src.core.mobject import Mobject

class BasicTestScene(Scene):
    def construct(self):
        self.logger.info("Starting basic test scene construction")
        
        # Setup the scene first
        self.setup()
        
        # Create basic shapes
        self.logger.info("Creating shapes")
        cube = self.create_cube(size=1.0, location=(-2, 0, 0))
        if cube:
            self.logger.info("Cube created successfully")
        else:
            self.logger.error("Failed to create cube")
            return

        sphere = self.create_sphere(radius=0.5, location=(2, 0, 0))
        if sphere:
            self.logger.info("Sphere created successfully")
        else:
            self.logger.error("Failed to create sphere")
            return

        # Test coordinate system
        self.logger.info("Testing coordinate system placement")
        self.coordinate_system.place_object(cube, mathutils.Vector((-2, 0, 0)))
        self.coordinate_system.place_object(sphere, mathutils.Vector((2, 0, 0)))
        
        # Test camera
        self.logger.info("Testing camera framing")
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