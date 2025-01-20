# SceneX/tests/example_scenes/18_physics_test.py

from src.templates.physics import (
    PendulumScene,
    CollisionScene,
    SpringScene
)
from mathutils import Vector

class DoublePendulumTest(PendulumScene):
    def construct(self):
        self.logger.info("Starting double pendulum simulation")

        # Setup scene and render engine
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
        
        bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'
        if hasattr(bpy.context.scene.eevee, "use_ssr"):
            bpy.context.scene.eevee.use_ssr = True
            bpy.context.scene.eevee.use_ssr_refraction = True
        
        # Configure viewport for rendered preview
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        space.shading.type = 'RENDERED'
                        space.shading.use_scene_lights = True
                        space.shading.use_scene_world = True

        # Set up camera to target origin
        # bpy.ops.object.camera_add(location=(7, -7, 5))
        # camera = bpy.context.active_object
        # camera.rotation_euler = (math.radians(45), 0, math.radians(45))
        
        bpy.ops.object.camera_add(location=(0, -10, 5))  # Move back for better view
        camera = bpy.context.active_object
        camera.rotation_euler = (math.radians(30), 0, 0)  # Less steep angle
        
        
        # Add Empty at origin as camera target
        bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
        target = bpy.context.active_object
        target.name = "CameraTarget"
        
        # Add Track To constraint to camera
        track = camera.constraints.new(type='TRACK_TO')
        track.target = target
        track.track_axis = 'TRACK_NEGATIVE_Z'
        track.up_axis = 'UP_Y'
        
        bpy.context.scene.camera = camera

        # Add lighting
        bpy.ops.object.light_add(type='SUN', location=(5, 5, 8))
        sun = bpy.context.active_object
        sun.data.energy = 3.0
        
        # Setup scene and physics
        self.setup_physics()
        self.gravity = (0, 0, -9.81)
        
        # Create first pendulum
        anchor1 = Vector((0, 0, 5))
        bob1_pos = Vector((2, 0, 3))
        self.setup_pendulum()
        
        # Create second pendulum
        anchor2 = bob1_pos
        bob2_pos = Vector((4, 0, 1))
        self.length = 2.0
        self.setup_pendulum()

class CollisionTest(CollisionScene):
    def construct(self):
        self.logger.info("Starting collision simulation")

        # Setup scene and physics
        self.setup_physics()
        
        # Create objects for collision
        self.setup_collision(num_objects=7)

class SpringTest(SpringScene):
    def construct(self):
        self.logger.info("Starting spring simulation")

        # Setup scene and physics
        self.setup_physics()
        
        # Create spring system
        self.setup_spring(spring_constant=15.0)

def run_physics_tests():
    # Test double pendulum
    pendulum_scene = DoublePendulumTest()
    pendulum_scene.construct()
    
    # Test collisions
    collision_scene = CollisionTest()
    collision_scene.construct()
    
    # Test spring
    spring_scene = SpringTest()
    spring_scene.construct()

if __name__ == "__main__":
    run_physics_tests()