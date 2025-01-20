# tests/example_scenes/5_geometry_complex_shapes_test.py

import bpy
import sys
import os
from pathlib import Path
import math
from mathutils import Vector

# Add parent directory to path to find SceneX package
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(script_dir))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from src.core.scene import Scene
from src.geometry.shapes import Line, Circle, Rectangle, Square
from src.geometry.complex_shapes import Arc, Arrow, Star
from src.svg.svg_handler import SVGHandler
from src.camera.camera import CameraConfig, CameraSystem
from src.animation.commonly_used_animations import (
    FadeInFrom,
    GrowFromCenter,
    Write,
    Rotate,
    FlashAround
)
from src.animation.base import AnimationConfig

class GeometryComplexTestScene(Scene):
    def construct(self):
        self.logger.info("Starting geometry complex shapes test scene")

        # Setup scene
        self.setup_scene()
        self.setup_lighting()
        
        # Create and animate shapes
        shapes = self.create_shapes()
        self.position_shapes(shapes)
        self.animate_shapes(shapes)

    def setup_scene(self):
        """Setup basic scene parameters"""
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

        # Setup camera
        camera_config = CameraConfig(
            frame_width=14.0,
            frame_height=8.0,
            position=(7, -7, 5)
        )
        self.camera = CameraSystem(camera_config)

        # Set render engine and shading
        bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                area.spaces[0].shading.type = 'RENDERED'

    def setup_lighting(self):
        """Setup scene lighting"""
        # Add main directional light
        bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
        sun = bpy.context.active_object
        sun.data.energy = 5.0
        sun.rotation_euler = (math.radians(45), math.radians(45), 0)

        # Add fill light
        bpy.ops.object.light_add(type='AREA', location=(-5, -5, 5))
        fill = bpy.context.active_object
        fill.data.energy = 200.0
        fill.rotation_euler = (math.radians(-45), 0, math.radians(-135))

        # Set world background to slightly darker grey
        world = bpy.context.scene.world
        if not world:
            world = bpy.data.worlds.new("World")
            bpy.context.scene.world = world
        world.use_nodes = True
        world.node_tree.nodes["Background"].inputs[0].default_value = (0.1, 0.1, 0.1, 1)

    def create_shapes(self):
        """Create all geometric shapes"""
        line = Line((-1, 0, 0), (1, 0, 0), 
                   color=(1, 0, 0, 1),
                   stroke_width=0.05).create()
                   
        circle = Circle(radius=0.7,
                       color=(0, 1, 0, 1),
                       fill_opacity=0.5).create()
        
        arc = Arc(radius=0.7,
                 start_angle=0,
                 end_angle=math.pi/2,
                 color=(0, 0, 1, 1),
                 stroke_width=0.05).create()
        
        arrow = Arrow(start=(-0.5, -0.5, 0),
                     end=(0.5, 0.5, 0),
                     head_length=0.2,
                     head_width=0.15,
                     color=(1, 1, 0, 1)).create()
        
        star = Star(points=5,
                   outer_radius=0.7,
                   inner_radius=0.3,
                   color=(1, 0, 1, 1)).create()
                   
        return {'line': line, 'circle': circle, 'arc': arc, 
                'arrow': arrow, 'star': star}

    def position_shapes(self, shapes):
        """Position all shapes in the scene"""
        positions = {
            'line': Vector((-2, 1, 0)),
            'circle': Vector((0, 1, 0)),
            'arc': Vector((2, 1, 0)),
            'arrow': Vector((-1.5, -1, 0)),
            'star': Vector((1.5, -1, 0))
        }
        
        for name, obj in shapes.items():
            self.coordinate_system.place_object(obj, positions[name])

    def animate_shapes(self, shapes):
        """Create and apply animations to shapes"""
        # Set initial timeline
        bpy.context.scene.frame_start = 1
        current_frame = 1

        # Create animation configs with different start times
        configs = {
            'line': AnimationConfig(duration=20),
            'circle': AnimationConfig(duration=20, delay_frames=20),
            'arc': AnimationConfig(duration=20, delay_frames=40),
            'arrow': AnimationConfig(duration=20, delay_frames=60),
            'star_rotate': AnimationConfig(duration=30, delay_frames=80),
            'star_flash': AnimationConfig(duration=10, delay_frames=110)
        }

        try:
            # Line animation
            anim = GrowFromCenter(shapes['line'], configs['line'])
            current_frame = anim.create_animation(current_frame)

            # Circle animation
            fade_direction = Vector((0, -1, 0))
            anim = FadeInFrom(shapes['circle'], fade_direction, config=configs['circle'])
            current_frame = anim.create_animation(current_frame + configs['circle'].delay_frames)

            # Arc animation
            anim = GrowFromCenter(shapes['arc'], configs['arc'])
            current_frame = anim.create_animation(current_frame + configs['arc'].delay_frames)

            # Arrow animation
            arrow_direction = Vector((-1, 0, 0))
            anim = FadeInFrom(shapes['arrow'], arrow_direction, config=configs['arrow'])
            current_frame = anim.create_animation(current_frame + configs['arrow'].delay_frames)

            # Star animations
            rotate = Rotate(shapes['star'], math.pi * 2, axis='Z', config=configs['star_rotate'])
            current_frame = rotate.create_animation(current_frame + configs['star_rotate'].delay_frames)

            flash = FlashAround(shapes['star'], 
                              color=(1, 1, 0),
                              thickness=0.1,
                              config=configs['star_flash'])
            current_frame = flash.create_animation(current_frame + configs['star_flash'].delay_frames)

            # Set timeline end
            bpy.context.scene.frame_end = current_frame + 20  # Add some padding
            bpy.context.scene.frame_current = 1  # Reset to start

            self.logger.info(f"Animation timeline set: 1 to {current_frame}")

        except Exception as e:
            self.logger.error(f"Error creating animations: {str(e)}")
            raise


if __name__ == "__main__":
    scene = GeometryComplexTestScene()
    scene.construct()