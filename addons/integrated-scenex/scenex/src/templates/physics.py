# SceneX/src/templates/physics.py

import bpy
import math
from mathutils import Vector
from ..core.scene import Scene
from ..geometry.shapes import Circle, Square, Rectangle
from ..text.text_support import Text
from ..animation.base import AnimationConfig
from typing import List, Dict, Optional, Tuple

class PhysicsSimulationScene(Scene):
    """Base class for physics simulations"""
    def __init__(self):
        super().__init__()
        self.simulation_objects = []
        self.gravity = (0, 0, -9.81)
        self.frame_rate = 60
        self.simulation_duration = 250  # frames

    def setup_physics(self):
        """Configure physics settings"""
        scene = bpy.context.scene
        scene.use_gravity = True
        scene.gravity = self.gravity
        scene.frame_start = 1
        scene.frame_end = self.simulation_duration
        scene.render.fps = self.frame_rate

    def add_rigid_body(self, obj: bpy.types.Object, 
                      mass: float = 1.0,
                      friction: float = 0.5,
                      bounce: float = 0.5,
                      linear_damping: float = 0.05,
                      angular_damping: float = 0.05) -> bpy.types.Object:
        """Add rigid body physics to object"""
        bpy.context.view_layer.objects.active = obj
        bpy.ops.rigidbody.object_add()
        rb = obj.rigid_body
        
        rb.mass = mass
        rb.friction = friction
        rb.restitution = bounce
        rb.linear_damping = linear_damping
        rb.angular_damping = angular_damping
        
        self.simulation_objects.append(obj)
        return obj

    def add_collision_plane(self, location: Vector = Vector((0, 0, 0)), 
                          size: float = 10.0) -> bpy.types.Object:
        """Add collision plane"""
        bpy.ops.mesh.primitive_plane_add(size=size, location=location)
        plane = bpy.context.active_object
        
        bpy.ops.rigidbody.object_add()
        plane.rigid_body.type = 'PASSIVE'
        plane.rigid_body.friction = 0.5
        plane.rigid_body.restitution = 0.5
        
        return plane

    def add_constraint(self, obj1: bpy.types.Object, 
                      obj2: bpy.types.Object,
                      constraint_type: str = 'FIXED',
                      pivot: Optional[Vector] = None) -> None:
        """Add constraint between objects"""
        bpy.ops.rigidbody.constraint_add()
        constraint = bpy.context.object
        constraint.empty_display_size = 0.1
        
        con = constraint.rigid_body_constraint
        con.type = constraint_type
        con.object1 = obj1
        con.object2 = obj2
        
        if pivot:
            constraint.location = pivot

class PendulumScene(PhysicsSimulationScene):
    """Template for pendulum simulation"""
    def __init__(self, length: float = 5.0):
        super().__init__()
        self.length = length

    def setup_pendulum(self):
        # Create anchor point
        anchor = self.add_rigid_body(
            Square(size=0.5).create(),
            mass=0.0  # Make it static
        )
        anchor.location = Vector((0, 0, self.length))
        
        # Create pendulum bob
        bob = self.add_rigid_body(
            Circle(radius=0.3).create(),
            mass=1.0,
            angular_damping=0.3
        )
        bob.location = Vector((self.length, 0, 0))
        
        # Add constraint
        self.add_constraint(anchor, bob, 'POINT', anchor.location)

class CollisionScene(PhysicsSimulationScene):
    """Template for collision simulations"""
    def setup_collision(self, num_objects: int = 5):
        # Add ground plane
        self.add_collision_plane()
        
        # Add objects with different properties
        for i in range(num_objects):
            obj = self.add_rigid_body(
                Circle(radius=0.3).create(),
                mass=1.0,
                bounce=0.8
            )
            obj.location = Vector((i - num_objects/2, 0, 5))

class SpringScene(PhysicsSimulationScene):
    """Template for spring simulations"""
    def setup_spring(self, spring_constant: float = 10.0):
        # Create fixed point
        anchor = self.add_rigid_body(
            Square(size=0.3).create(),
            mass=0.0
        )
        
        # Create mass
        mass = self.add_rigid_body(
            Circle(radius=0.2).create(),
            mass=1.0,
            linear_damping=0.1
        )
        mass.location = Vector((0, 0, -2))
        
        # Add spring constraint
        constraint = self.add_constraint(
            anchor, mass, 'GENERIC_SPRING'
        )
        if constraint.rigid_body_constraint:
            constraint.rigid_body_constraint.spring_stiffness_y = spring_constant