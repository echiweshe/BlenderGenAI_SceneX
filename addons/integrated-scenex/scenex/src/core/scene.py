# SceneX/src/core/scene.py
import bpy
import mathutils
from src.core.coordinate_system import CoordinateSystem
from src.camera.camera import CameraSystem
from src.utils.logger import SceneXLogger

class Scene:
    def __init__(self):
        self.logger = SceneXLogger("Scene")
        self.coordinate_system = CoordinateSystem()
        self.camera = CameraSystem()
        self.mobjects = []
        self.logger.info("Scene initialized")

    def create_text(self, content: str, location: tuple[float, float, float] = (0, 0, 0), 
                    size: float = 1.0) -> bpy.types.Object:
        """Create a text object in the scene"""
        self.logger.info(f"Creating text object: {content}")
        try:
            bpy.ops.object.text_add(location=location)
            text_obj = bpy.context.active_object
            text_obj.data.body = content
            text_obj.data.size = size  # Control text size
            
            # Create default material for text
            mat = bpy.data.materials.new(name=f"text_material_{text_obj.name}")
            mat.use_nodes = True
            principled = mat.node_tree.nodes["Principled BSDF"]
            principled.inputs["Base Color"].default_value = (1, 1, 1, 1)  # White text
            
            if text_obj.data.materials:
                text_obj.data.materials[0] = mat
            else:
                text_obj.data.materials.append(mat)
                
            return text_obj
        except Exception as e:
            self.logger.error(f"Error creating text: {str(e)}")
            return None

    def create_cube(self, size: float = 1.0, location: tuple[float, float, float] = (0, 0, 0)) -> bpy.types.Object:
        """Create a cube in the scene"""
        self.logger.info(f"Creating cube at location {location}")
        try:
            bpy.ops.mesh.primitive_cube_add(size=size, location=location)
            cube = bpy.context.active_object
            self.mobjects.append(cube)  # Add to mobjects list
            return cube
        except Exception as e:
            self.logger.error(f"Error creating cube: {str(e)}")
            return None

    def create_sphere(self, radius: float = 1.0, location: tuple[float, float, float] = (0, 0, 0)) -> bpy.types.Object:
        """Create a UV sphere in the scene"""
        self.logger.info(f"Creating sphere at location {location}")
        try:
            bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=location)
            sphere = bpy.context.active_object
            self.mobjects.append(sphere)  # Add to mobjects list
            return sphere
        except Exception as e:
            self.logger.error(f"Error creating sphere: {str(e)}")
            return None

    def create_cylinder(self, radius: float = 1.0, depth: float = 2.0, 
                       location: tuple[float, float, float] = (0, 0, 0)) -> bpy.types.Object:
        """Create a cylinder in the scene"""
        self.logger.info(f"Creating cylinder at location {location}")
        try:
            bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, location=location)
            cylinder = bpy.context.active_object
            self.mobjects.append(cylinder)  # Add to mobjects list
            return cylinder
        except Exception as e:
            self.logger.error(f"Error creating cylinder: {str(e)}")
            return None

    def create_circle(self, radius=1.0, location=(0, 0, 0)):
        """Create a circle primitive"""
        self.logger.info(f"Creating circle at location {location}")
        try:
            bpy.ops.mesh.primitive_circle_add(radius=radius, location=location)
            circle = bpy.context.active_object
            self.mobjects.append(circle)
            return circle
        except Exception as e:
            self.logger.error(f"Error creating circle: {str(e)}")
            return None

    def create_empty(self, location=(0, 0, 0)):
        """Create an empty object"""
        self.logger.info(f"Creating empty at location {location}")
        try:
            bpy.ops.object.empty_add(location=location)
            empty = bpy.context.active_object
            self.mobjects.append(empty)
            return empty
        except Exception as e:
            self.logger.error(f"Error creating empty: {str(e)}")
            return None

    def setup(self):
        """Setup the scene"""
        self.logger.info("Setting up scene")
        try:
            # Clear existing objects
            bpy.ops.object.select_all(action='SELECT')
            bpy.ops.object.delete()

            # Initialize coordinate system
            self.coordinate_system = CoordinateSystem()
            
            # Setup camera
            self.camera.setup()
            
        except Exception as e:
            self.logger.error(f"Error setting up scene: {str(e)}")

    def play(self, *animations):
        """Play animations"""
        self.logger.info("Playing animations")
        # Animation implementation will go here
        pass

    def construct(self):
        """Override this method in subclasses"""
        raise NotImplementedError("Must implement construct() method")