# tests/example_scenes/6_materials_test.py

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
from src.geometry.shapes import Circle, Rectangle
from src.geometry.complex_shapes import Star
from src.materials.material import Material, MaterialConfig, MaterialType
from src.animation.commonly_used_animations import FadeInFrom, Rotate
from src.animation.material_animations import MaterialAnimation, EmissionAnimation
from src.animation.base import AnimationConfig



class MaterialTestScene(Scene):
    def setup_scene(self):
        """Setup scene, camera, and lighting"""
        # Clear existing scene
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
        
        # Set render engine
        bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'
        
        # Setup render settings
        if hasattr(bpy.context.scene.eevee, "use_ssr"):
            bpy.context.scene.eevee.use_ssr = True
            bpy.context.scene.eevee.use_ssr_refraction = True
        bpy.context.scene.eevee.use_bloom = True
        bpy.context.scene.eevee.bloom_intensity = 1.0

        # Set up lighting
        bpy.ops.object.light_add(type='SUN', location=(5, 5, 8))
        sun = bpy.context.active_object
        sun.data.energy = 5.0
        sun.rotation_euler = (math.radians(45), math.radians(45), 0)
        
        # Add fill light
        bpy.ops.object.light_add(type='AREA', location=(-5, -5, 5))
        fill = bpy.context.active_object
        fill.data.energy = 200.0
        fill.rotation_euler = (math.radians(-45), 0, math.radians(-135))

        # Setup camera
        bpy.ops.object.camera_add(location=(7, -7, 5))
        camera = bpy.context.active_object
        camera.rotation_euler = (math.radians(45), 0, math.radians(45))
        
        # Add Empty as camera target
        bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
        target = bpy.context.active_object
        target.name = "CameraTarget"
        
        # Setup camera constraints
        track = camera.constraints.new(type='TRACK_TO')
        track.target = target
        track.track_axis = 'TRACK_NEGATIVE_Z'
        track.up_axis = 'UP_Y'
        
        bpy.context.scene.camera = camera

        # Set viewport shading
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                area.spaces[0].shading.type = 'RENDERED'
                area.spaces[0].region_3d.view_perspective = 'CAMERA'
                area.spaces[0].show_gizmo = True

    def setup_basic_material(self, name, color):
        """Create a basic material with Principled BSDF"""
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        
        # Clear existing nodes
        nodes = mat.node_tree.nodes
        nodes.clear()
        
        # Create new nodes
        principled = nodes.new('ShaderNodeBsdfPrincipled')
        principled.inputs['Base Color'].default_value = color
        principled.name = "Principled BSDF"  # Explicitly set name
        
        output = nodes.new('ShaderNodeOutputMaterial')
        
        # Link nodes
        mat.node_tree.links.new(principled.outputs[0], output.inputs[0])
        
        return mat

    def setup_materials(self):
        """Setup all materials with proper nodes"""
        materials = {}
        
        # Basic material
        materials['basic'] = self.setup_basic_material("basic", (1, 0, 0, 1))
        
        # Glass material
        glass_mat = bpy.data.materials.new(name="glass")
        glass_mat.use_nodes = True
        glass_mat.blend_method = 'BLEND'
        glass_mat.use_screen_refraction = True
        glass_mat.use_backface_culling = False
        
        nodes = glass_mat.node_tree.nodes
        nodes.clear()
        glass_bsdf = nodes.new('ShaderNodeBsdfGlass')
        output = nodes.new('ShaderNodeOutputMaterial')
        glass_mat.node_tree.links.new(glass_bsdf.outputs[0], output.inputs[0])
        glass_bsdf.inputs["Color"].default_value = (0.8, 0.9, 1, 1)
        glass_bsdf.inputs["IOR"].default_value = 1.45
        materials['glass'] = glass_mat
        
        # Emission material
        emission_mat = bpy.data.materials.new(name="emission")
        emission_mat.use_nodes = True
        nodes = emission_mat.node_tree.nodes
        nodes.clear()
        
        emission = nodes.new('ShaderNodeEmission')
        emission.name = "Emission"  # Important for animation
        output = nodes.new('ShaderNodeOutputMaterial')
        emission_mat.node_tree.links.new(emission.outputs[0], output.inputs[0])
        emission.inputs["Color"].default_value = (0, 1, 0, 1)
        emission.inputs["Strength"].default_value = 1.0
        materials['emission'] = emission_mat
        
        # Metallic material
        metallic_mat = self.setup_basic_material("metal", (0.8, 0.8, 0.8, 1))
        principled = metallic_mat.node_tree.nodes["Principled BSDF"]
        principled.inputs['Metallic'].default_value = 1.0
        principled.inputs['Roughness'].default_value = 0.1
        materials['metallic'] = metallic_mat
        
        # Toon material
        toon_mat = self.setup_basic_material("toon", (1, 0, 1, 1))
        materials['toon'] = toon_mat
        
        return materials

    def construct(self):
        self.logger.info("Starting materials test scene")
        
        # Setup scene
        self.setup_scene()
        
        # Create materials
        materials = self.setup_materials()
        
        # Create shapes with materials
        circle1 = Circle(radius=0.7).create()
        circle1.active_material = materials['basic']
        
        circle2 = Circle(radius=0.7).create()
        circle2.active_material = materials['glass']
        
        star = Star(points=5, outer_radius=0.7).create()
        star.active_material = materials['emission']
        
        rect = Rectangle(width=1.4, height=1.4).create()
        rect.active_material = materials['metallic']
        
        circle3 = Circle(radius=0.7).create()
        circle3.active_material = materials['toon']

        # Position objects
        self.coordinate_system.place_object(circle1, Vector((-2, 1, 0)))
        self.coordinate_system.place_object(circle2, Vector((0, 1, 0)))
        self.coordinate_system.place_object(star, Vector((2, 1, 0)))
        self.coordinate_system.place_object(rect, Vector((-1, -1, 0)))
        self.coordinate_system.place_object(circle3, Vector((1, -1, 0)))

        # Setup animation timeline
        bpy.context.scene.frame_start = 1
        current_frame = 1
        
        # Create animations with proper timing
        animations = [
            MaterialAnimation(circle1, (1,0,0,1), (0,1,0,1),
                            config=AnimationConfig(duration=30)),
            FadeInFrom(circle2, direction=Vector((0, -1, 0)),
                      config=AnimationConfig(duration=30, delay_frames=30)),
            EmissionAnimation(star, 1.0, 10.0,
                            config=AnimationConfig(duration=30, delay_frames=60)),
            FadeInFrom(rect, direction=Vector((0, -1, 0)),
                      config=AnimationConfig(duration=30, delay_frames=90)),
            Rotate(circle3, angle=math.pi*2,
                  config=AnimationConfig(duration=30, delay_frames=120))
        ]

        # Create keyframes for each animation
        for anim in animations:
            start_frame = current_frame + (anim.config.delay_frames or 0)
            end_frame = start_frame + anim.config.duration
            anim.create_animation(start_frame)
            current_frame = end_frame

        # Set scene frame range
        bpy.context.scene.frame_end = current_frame + 20
        bpy.context.scene.frame_set(1)

if __name__ == "__main__":
    scene = MaterialTestScene()
    scene.construct()