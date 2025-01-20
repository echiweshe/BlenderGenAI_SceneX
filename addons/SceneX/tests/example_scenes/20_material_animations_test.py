# tests/example_scenes/20_material_animations_test.py

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
from src.geometry.shapes import Circle, Rectangle, Square
from src.animation.material_animations import (
    MaterialPropertyAnimation,
    MaterialPresetAnimation,
    MaterialBlendAnimation,
    MATERIAL_PRESETS
)
from src.animation.base import AnimationConfig

class MaterialAnimationTestScene(Scene):

    def setup_world_background(self):
        """Setup world background with a subtle gradient"""
        world = bpy.context.scene.world
        if not world:
            world = bpy.data.worlds.new("World")
            bpy.context.scene.world = world
            
        world.use_nodes = True
        nodes = world.node_tree.nodes
        links = world.node_tree.links
        
        # Clear existing nodes
        nodes.clear()
        
        # Create nodes for gradient background
        sky = nodes.new('ShaderNodeSkyTexture')
        sky.sky_type = 'NISHITA'
        sky.altitude = 0.5
        sky.air_density = 1.0
        sky.dust_density = 1.0
        
        mapping = nodes.new('ShaderNodeMapping')
        mapping.inputs['Rotation'].default_value = (0.5, 0.7, 0)
        
        tex_coord = nodes.new('ShaderNodeTexCoord')
        background = nodes.new('ShaderNodeBackground')
        output = nodes.new('ShaderNodeOutputWorld')
        
        # Connect nodes
        links.new(tex_coord.outputs['Generated'], mapping.inputs['Vector'])
        links.new(mapping.outputs['Vector'], sky.inputs['Vector'])
        links.new(sky.outputs['Color'], background.inputs['Color'])
        links.new(background.outputs['Background'], output.inputs['Surface'])
        
        # Adjust background strength
        background.inputs['Strength'].default_value = 0.5

    def create_environment(self):
        """Create ground plane and backdrop"""
        # Create ground plane
        bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, -0.01))
        ground = bpy.context.active_object
        
        # Create ground material
        ground_mat = bpy.data.materials.new(name="ground_material")
        ground_mat.use_nodes = True
        nodes = ground_mat.node_tree.nodes
        links = ground_mat.node_tree.links
        nodes.clear()
        
        # Create nodes for gradient ground material
        noise = nodes.new('ShaderNodeTexNoise')
        noise.inputs['Scale'].default_value = 5.0
        noise.inputs['Detail'].default_value = 2.0
        
        color_ramp = nodes.new('ShaderNodeValToRGB')
        color_ramp.color_ramp.elements[0].position = 0.4
        color_ramp.color_ramp.elements[0].color = (0.1, 0.1, 0.1, 1)
        color_ramp.color_ramp.elements[1].position = 0.6
        color_ramp.color_ramp.elements[1].color = (0.2, 0.2, 0.2, 1)
        
        principled = nodes.new('ShaderNodeBsdfPrincipled')
        output = nodes.new('ShaderNodeOutputMaterial')
        
        # Connect nodes
        links.new(noise.outputs['Color'], color_ramp.inputs['Fac'])
        links.new(color_ramp.outputs['Color'], principled.inputs['Base Color'])
        links.new(principled.outputs['BSDF'], output.inputs['Surface'])
        
        # Set material properties
        principled.inputs['Roughness'].default_value = 0.7
        principled.inputs['Specular'].default_value = 0.1
        
        # Assign material to ground plane
        ground.data.materials.append(ground_mat)
        
        # Create backdrop (curved plane)
        bpy.ops.mesh.primitive_plane_add(size=20)
        backdrop = bpy.context.active_object
        backdrop.location = (0, 10, 10)
        backdrop.rotation_euler = (math.radians(45), 0, 0)
        
        # Add subdivision and curve modifiers
        subdiv = backdrop.modifiers.new(name="Subdivision", type='SUBSURF')
        subdiv.levels = 3
        
        curve = backdrop.modifiers.new(name="Curve", type='SIMPLE_DEFORM')
        curve.deform_method = 'BEND'
        curve.angle = math.radians(45)
        
        # Create backdrop material
        backdrop_mat = bpy.data.materials.new(name="backdrop_material")
        backdrop_mat.use_nodes = True
        nodes = backdrop_mat.node_tree.nodes
        nodes.clear()
        
        # Create simple gradient material
        gradient = nodes.new('ShaderNodeTexGradient')
        color_ramp = nodes.new('ShaderNodeValToRGB')
        principled = nodes.new('ShaderNodeBsdfPrincipled')
        output = nodes.new('ShaderNodeOutputMaterial')
        
        # Setup gradient colors
        color_ramp.color_ramp.elements[0].position = 0.3
        color_ramp.color_ramp.elements[0].color = (0.15, 0.15, 0.15, 1)
        color_ramp.color_ramp.elements[1].position = 0.7
        color_ramp.color_ramp.elements[1].color = (0.3, 0.3, 0.3, 1)
        
        # Connect nodes
        links = backdrop_mat.node_tree.links
        links.new(gradient.outputs['Color'], color_ramp.inputs['Fac'])
        links.new(color_ramp.outputs['Color'], principled.inputs['Base Color'])
        links.new(principled.outputs['BSDF'], output.inputs['Surface'])
        
        # Assign material to backdrop
        backdrop.data.materials.append(backdrop_mat)
        
        return ground, backdrop

    def setup_scene(self):
        """Setup complete scene with background and lighting"""
        # Clear existing scene
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
        
        # Setup world background
        self.setup_world_background()
        
        # Create environment
        ground, backdrop = self.create_environment()
        
        # Set render engine and settings
        bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'
        if hasattr(bpy.context.scene.eevee, "use_ssr"):
            bpy.context.scene.eevee.use_ssr = True
            bpy.context.scene.eevee.use_ssr_refraction = True
        bpy.context.scene.eevee.use_bloom = True
        bpy.context.scene.eevee.bloom_intensity = 1.0
        
        # Setup lighting
        # Key light
        bpy.ops.object.light_add(type='AREA', location=(5, -5, 8))
        key_light = bpy.context.active_object
        key_light.data.energy = 500.0
        key_light.rotation_euler = (math.radians(45), 0, math.radians(45))
        key_light.data.size = 5.0
        
        # Fill light
        bpy.ops.object.light_add(type='AREA', location=(-5, -2, 4))
        fill_light = bpy.context.active_object
        fill_light.data.energy = 200.0
        fill_light.rotation_euler = (math.radians(30), 0, math.radians(-60))
        fill_light.data.size = 3.0
        
        # Rim light
        bpy.ops.object.light_add(type='AREA', location=(0, 5, 6))
        rim_light = bpy.context.active_object
        rim_light.data.energy = 300.0
        rim_light.rotation_euler = (math.radians(-45), 0, 0)
        rim_light.data.size = 4.0
        
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
   
    def construct(self):
        self.logger.info("Starting material animations test scene")
        
        # Setup scene with background
        self.setup_scene()
        
        # Create test objects
        sphere1 = self.create_sphere(radius=0.5, location=(-2, 0, 0))
        sphere2 = self.create_sphere(radius=0.5, location=(0, 0, 0))
        sphere3 = self.create_sphere(radius=0.5, location=(2, 0, 0))
        
        # Create materials
        metal_mat = self.create_material_from_preset('metal')
        plastic_mat = self.create_material_from_preset('plastic')
        glass_mat = self.create_material_from_preset('glass')
        
        # Assign initial materials
        sphere1.active_material = metal_mat
        sphere2.active_material = plastic_mat
        sphere3.active_material = glass_mat
        
        # Create animations
        current_frame = 1
        base_duration = 60
        
        # 1. Property Animation - Roughness transition
        roughness_anim = MaterialPropertyAnimation(
            sphere1,
            "Roughness",
            0.0,
            1.0,
            config=AnimationConfig(duration=base_duration)
        )
        current_frame = roughness_anim.create_animation(current_frame)
        
        # 2. Preset Sequence Animation
        preset_sequence = [
            MATERIAL_PRESETS['plastic'],
            MATERIAL_PRESETS['metal'],
            MATERIAL_PRESETS['glass']
        ]
        preset_anim = MaterialPresetAnimation(
            sphere2,
            preset_sequence,
            config=AnimationConfig(duration=base_duration * 2)
        )
        current_frame = preset_anim.create_animation(current_frame)
        
        # 3. Material Blend Animation
        blend_anim = MaterialBlendAnimation(
            sphere3,
            metal_mat,
            glass_mat,
            config=AnimationConfig(duration=base_duration)
        )
        current_frame = blend_anim.create_animation(current_frame)
        
        # Set frame range
        bpy.context.scene.frame_start = 1
        bpy.context.scene.frame_end = current_frame + 20
        
    def create_material_from_preset(self, preset_name):
        """Create a material from a preset"""
        mat = bpy.data.materials.new(name=preset_name)
        mat.use_nodes = True
        
        principled = mat.node_tree.nodes["Principled BSDF"]
        for prop, value in MATERIAL_PRESETS[preset_name].items():
            if prop in principled.inputs:
                principled.inputs[prop].default_value = value
                
        return mat

if __name__ == "__main__":
    scene = MaterialAnimationTestScene()
    scene.construct()