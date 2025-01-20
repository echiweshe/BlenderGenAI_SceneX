import bpy
import os
import sys
from pathlib import Path
import math

def setup_paths():
    """Setup the Python path to include SceneX modules"""
    current_dir = Path(__file__).parent.parent  # SceneX root
    if str(current_dir) not in sys.path:
        sys.path.append(str(current_dir))
        print(f"Added {current_dir} to Python path")

class SceneSetup:
    """Handle scene configuration and setup"""
    
    @staticmethod
    def setup_render_engine():
        """Configure render engine settings"""
        try:
            scene = bpy.context.scene
            # Set render engine
            if hasattr(scene.render, "engine"):
                scene.render.engine = 'CYCLES'  # Use Cycles as fallback
                
            # Try to set EEVEE Next if available
            engines = [e.identifier for e in bpy.types.RenderEngine.bl_rna.properties['type'].enum_items]
            if 'BLENDER_EEVEE_NEXT' in engines:
                scene.render.engine = 'BLENDER_EEVEE_NEXT'
                
            # Configure EEVEE settings if available
            if hasattr(scene, "eevee"):
                scene.eevee.use_ssr = True
                scene.eevee.use_ssr_refraction = True
                scene.eevee.use_gtao = True
                scene.eevee.gtao_distance = 0.2
                scene.eevee.use_bloom = True
        except Exception as e:
            print(f"Warning: Could not set render engine: {str(e)}")

class CameraSetup:
    """Handle camera setup and positioning"""
    
    @staticmethod
    def create_camera(location=(7, -7, 5)):
        """Create and configure camera"""
        try:
            # Remove existing cameras
            for obj in bpy.data.objects:
                if obj.type == 'CAMERA':
                    bpy.data.objects.remove(obj, do_unlink=True)
            
            # Create new camera
            bpy.ops.object.camera_add(location=location)
            camera = bpy.context.active_object
            camera.name = "SceneCamera"
            
            # Set camera properties
            camera.data.lens = 50
            camera.data.clip_start = 0.1
            camera.data.clip_end = 1000
            
            # Create target empty
            bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
            target = bpy.context.active_object
            target.name = "CameraTarget"
            
            # Setup tracking constraint
            track = camera.constraints.new(type='TRACK_TO')
            track.target = target
            track.track_axis = 'TRACK_NEGATIVE_Z'
            track.up_axis = 'UP_Y'
            
            # Make active camera
            bpy.context.scene.camera = camera

            # Switch all 3D viewports to camera view
            for area in bpy.context.screen.areas:
                if area.type == 'VIEW_3D':
                    # Switch to camera perspective
                    area.spaces[0].region_3d.view_perspective = 'CAMERA'
                    # Set this as the lock camera to view
                    area.spaces[0].use_camera_lock = True
                    # Set viewport shading
                    space = area.spaces[0]
                    space.shading.type = 'MATERIAL'
                    space.shading.use_scene_lights = True
                    space.shading.use_scene_world = True
            
            return camera, target
            
        except Exception as e:
            print(f"Error setting up camera: {str(e)}")
            return None, None

    @staticmethod
    def align_view_to_camera():
        """Align the 3D view to the active camera"""
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                override = bpy.context.copy()
                override['area'] = area
                bpy.ops.view3d.view_camera(override)
                area.spaces[0].use_camera_lock = True
                area.spaces[0].region_3d.view_perspective = 'CAMERA'
                area.tag_redraw()

class AWSComponentBuilder:
    """Helper class to build AWS components in Blender"""
    
    @staticmethod
    def create_lambda(location=(0, 0, 0), scale=(1.5, 1, 0.5)):
        bpy.ops.mesh.primitive_cube_add(size=1, location=location)
        obj = bpy.context.active_object
        obj.name = "lambda_function"
        obj.scale = scale
        
        # Add material
        mat = bpy.data.materials.new(name="lambda_material")
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.9, 0.5, 0.1, 1)  # Orange
        obj.data.materials.append(mat)
        
        return obj
    
    @staticmethod
    def create_s3(location=(2, 0, 0)):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=1, location=location)
        obj = bpy.context.active_object
        obj.name = "s3_bucket"
        
        # Add material
        mat = bpy.data.materials.new(name="s3_material")
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.5, 0.2, 0.9, 1)  # Purple
        obj.data.materials.append(mat)
        
        return obj
    
    @staticmethod
    def create_apigateway(location=(0, 2, 0)):
        bpy.ops.mesh.primitive_cube_add(size=1, location=location)
        obj = bpy.context.active_object
        obj.name = "api_gateway"
        obj.scale = (1, 0.2, 1)
        
        # Add material
        mat = bpy.data.materials.new(name="apigateway_material")
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.2, 0.6, 0.8, 1)  # Blue
        obj.data.materials.append(mat)
        
        return obj

    @staticmethod
    def create_connection(start_obj, end_obj, name="connection"):
        """Create a connection line between two objects"""
        curve_data = bpy.data.curves.new(name, type='CURVE')
        curve_data.dimensions = '3D'
        
        polyline = curve_data.splines.new('POLY')
        polyline.points.add(1)
        
        # Get object centers
        start_pos = start_obj.location
        end_pos = end_obj.location
        
        polyline.points[0].co = (*start_pos, 1)
        polyline.points[1].co = (*end_pos, 1)
        
        curve_obj = bpy.data.objects.new(name, curve_data)
        curve_obj.data.bevel_depth = 0.02
        
        # Add material
        mat = bpy.data.materials.new(name=f"{name}_material")
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.2, 0.2, 0.2, 1)  # Dark gray
        curve_obj.data.materials.append(mat)
        
        bpy.context.scene.collection.objects.link(curve_obj)
        return curve_obj

class BlenderAISceneTest:
    """Test AI Scene Generation in Blender"""
    
    def __init__(self):
        self.builder = AWSComponentBuilder()
        self.setup_scene()
        
    def setup_scene(self):
        """Setup complete scene environment"""
        try:
            # Clear existing scene
            bpy.ops.object.select_all(action='SELECT')
            bpy.ops.object.delete()
            
            # Setup render engine
            SceneSetup.setup_render_engine()
            
            # Setup camera and lighting
            self.camera, self.target = CameraSetup.create_camera()
            self.setup_lighting()
            
            # Ensure camera view
            CameraSetup.align_view_to_camera()
            
            print("Scene setup completed successfully")
            
        except Exception as e:
            print(f"Error in scene setup: {str(e)}")

    def setup_lighting(self):
        """Set up scene lighting"""
        # Add main light
        bpy.ops.object.light_add(type='SUN', location=(5, 5, 8))
        sun = bpy.context.active_object
        sun.data.energy = 3.0
        sun.data.angle = 0.1  # Sharper shadows
        
        # Add fill light
        bpy.ops.object.light_add(type='SUN', location=(-3, -3, 4))
        fill = bpy.context.active_object
        fill.data.energy = 1.0
        fill.data.angle = 0.3  # Softer shadows

    def create_mock_scene(self, scene_type="lambda_s3"):
        """Create a test scene based on type"""
        if scene_type == "lambda_s3":
            # Create Lambda and S3
            lambda_obj = self.builder.create_lambda()
            s3_obj = self.builder.create_s3()
            self.builder.create_connection(lambda_obj, s3_obj, "lambda_to_s3")
            
            # Position camera for this scene
            self.camera.location = (5, -5, 3)
            
        elif scene_type == "api_lambda_s3":
            # Create vertically arranged components
            api_obj = self.builder.create_apigateway((0, 2, 0))
            lambda_obj = self.builder.create_lambda((0, 0, 0))
            s3_obj = self.builder.create_s3((0, -2, 0))
            
            # Create connections
            self.builder.create_connection(api_obj, lambda_obj, "api_to_lambda")
            self.builder.create_connection(lambda_obj, s3_obj, "lambda_to_s3")
            
            # Position camera for this scene
            self.camera.location = (7, 0, 4)
        
        # Ensure camera view
        CameraSetup.align_view_to_camera()

    def test_scene_creation(self, scene_type="lambda_s3"):
        """Test the scene creation functionality"""
        try:
            print(f"Starting AI Scene Generation test for {scene_type}...")
            
            # Create test scene
            self.create_mock_scene(scene_type)
            
            # Verify objects were created
            expected_objects = {
                "lambda_s3": ["lambda_function", "s3_bucket", "lambda_to_s3"],
                "api_lambda_s3": ["api_gateway", "lambda_function", "s3_bucket", 
                                "api_to_lambda", "lambda_to_s3"]
            }
            
            for obj_name in expected_objects[scene_type]:
                obj = bpy.data.objects.get(obj_name)
                assert obj is not None, f"Object {obj_name} not found in scene"
                print(f"Verified object: {obj_name}")
            
            print("Scene generation test completed successfully")
            return True
            
        except Exception as e:
            print(f"Test failed: {str(e)}")
            return False

def main():
    """Main test function"""
    setup_paths()
    
    # Run tests for different scene types
    test = BlenderAISceneTest()
    
    # Test basic Lambda to S3 scene
    test.test_scene_creation("lambda_s3")
    
    # Clear and test API Gateway to Lambda to S3 scene
    test.setup_scene()
    test.test_scene_creation("api_lambda_s3")

if __name__ == "__main__":
    main()