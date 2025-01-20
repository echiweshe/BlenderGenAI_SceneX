# SceneX/src/animation/manim_animations.py
import bpy
import mathutils
from typing import Optional, List, Tuple, Union
from .base import Animation, AnimationConfig
from ..utils.logger import SceneXLogger  # Add this import

class GrowFromCenter(Animation):
    """Grow an object from its center point"""
    def __init__(self, target: bpy.types.Object, config: Optional[AnimationConfig] = None):
        super().__init__(target, config)
        self.original_scale = target.scale.copy()
        
    def create_keyframes(self, start_frame: int, end_frame: int):
        # Start from zero scale
        self.target.scale = (0, 0, 0)
        self.target.keyframe_insert(data_path="scale", frame=start_frame)
        
        # End at original scale
        self.target.scale = self.original_scale
        self.target.keyframe_insert(data_path="scale", frame=end_frame)

class GrowFromPoint(Animation):
    """Grow an object from a specific point"""
    def __init__(self, target: bpy.types.Object, point: mathutils.Vector, 
                 config: Optional[AnimationConfig] = None):
        super().__init__(target, config)
        self.point = point
        self.original_scale = target.scale.copy()
        self.original_location = target.location.copy()
        
    def create_keyframes(self, start_frame: int, end_frame: int):
        # Calculate offset between center and grow point
        offset = self.original_location - self.point
        
        # Start from point with zero scale
        self.target.scale = (0, 0, 0)
        self.target.location = self.point
        self.target.keyframe_insert(data_path="scale", frame=start_frame)
        self.target.keyframe_insert(data_path="location", frame=start_frame)
        
        # End at original position and scale
        self.target.scale = self.original_scale
        self.target.location = self.original_location
        self.target.keyframe_insert(data_path="scale", frame=end_frame)
        self.target.keyframe_insert(data_path="location", frame=end_frame)

class Write(Animation):
    """Write text character by character"""
    
    def __init__(self, target: bpy.types.Object, config: Optional[AnimationConfig] = None):
        super().__init__(target, config)
        if not target.type == 'FONT':
            raise ValueError("Write animation can only be applied to text objects")
        self.full_text = target.data.body
        self.handler = None
        
    def create_keyframes(self, start_frame: int, end_frame: int):
        try:
            # Calculate frames per character
            text_length = len(self.full_text)
            frames_per_char = max(1, (end_frame - start_frame) // max(1, text_length))
            
            # Create a custom property to store the text progress
            self.target["text_progress"] = 0.0
            
            # Keyframe the custom property
            self.target.keyframe_insert(data_path='["text_progress"]', frame=start_frame)
            self.target["text_progress"] = float(text_length)
            self.target.keyframe_insert(data_path='["text_progress"]', frame=end_frame)
            
            # Set up the frame change handler
            def text_update(scene):
                obj = self.target
                if obj is None or scene.frame_current < start_frame:
                    return
                    
                if scene.frame_current > end_frame:
                    obj.data.body = self.full_text
                    return
                    
                progress = min(text_length, int(obj.get("text_progress", 0)))
                obj.data.body = self.full_text[:progress]
            
            # Remove any existing handlers for this object
            for handler in bpy.app.handlers.frame_change_post:
                if hasattr(handler, "__name__") and handler.__name__ == f"text_update_{self.target.name}":
                    bpy.app.handlers.frame_change_post.remove(handler)
            
            # Add the new handler
            text_update.__name__ = f"text_update_{self.target.name}"
            bpy.app.handlers.frame_change_post.append(text_update)
            self.handler = text_update
            
            # Set smooth interpolation
            if self.target.animation_data and self.target.animation_data.action:
                for fc in self.target.animation_data.action.fcurves:
                    if fc.data_path == '["text_progress"]':
                        for kf in fc.keyframe_points:
                            kf.interpolation = 'LINEAR'
            
            self.logger.info(f"Write animation setup for text: {self.full_text[:10]}...")
            return end_frame
            
        except Exception as e:
            self.logger.error(f"Error creating write animation: {str(e)}")
            return start_frame
    
    def cleanup(self):
        """Remove the frame handler when animation is done"""
        if self.handler and self.handler in bpy.app.handlers.frame_change_post:
            bpy.app.handlers.frame_change_post.remove(self.handler)


class FadeInFrom(Animation):
    """Fade in while moving from a direction"""
    def __init__(self, target: bpy.types.Object, direction: mathutils.Vector, 
                 distance: float = 5.0, config: Optional[AnimationConfig] = None):
        super().__init__(target, config)
        self.direction = direction.normalized()
        self.distance = distance
        self.original_location = target.location.copy()
        
    def create_keyframes(self, start_frame: int, end_frame: int):
        # Setup material for fade
        if not self.target.active_material:
            mat = bpy.data.materials.new(name=f"{self.target.name}_material")
            mat.use_nodes = True
            self.target.active_material = mat
        
        mat = self.target.active_material
        mat.blend_method = 'BLEND'
        principled = mat.node_tree.nodes["Principled BSDF"]
        
        # Start position and fully transparent
        start_pos = self.original_location + self.direction * self.distance
        self.target.location = start_pos
        principled.inputs['Alpha'].default_value = 0
        
        self.target.keyframe_insert(data_path="location", frame=start_frame)
        principled.inputs['Alpha'].keyframe_insert(data_path="default_value", 
                                                 frame=start_frame)
        
        # End position and fully opaque
        self.target.location = self.original_location
        principled.inputs['Alpha'].default_value = 1
        
        self.target.keyframe_insert(data_path="location", frame=end_frame)
        principled.inputs['Alpha'].keyframe_insert(data_path="default_value", 
                                                 frame=end_frame)

class Rotate(Animation):
    """Rotate object around an axis"""
    def __init__(self, target: bpy.types.Object, angle: float, 
                 axis: str = 'Z', config: Optional[AnimationConfig] = None):
        super().__init__(target, config)
        self.angle = angle
        self.axis = axis.upper()
        self.original_rotation = target.rotation_euler.copy()
        
    def create_keyframes(self, start_frame: int, end_frame: int):
        try:
            # Start rotation
            self.target.keyframe_insert(data_path="rotation_euler", frame=start_frame)
            
            # End rotation
            axis_idx = {'X': 0, 'Y': 1, 'Z': 2}[self.axis]
            final_rotation = self.original_rotation.copy()
            final_rotation[axis_idx] += self.angle
            
            self.target.rotation_euler = final_rotation
            self.target.keyframe_insert(data_path="rotation_euler", frame=end_frame)
            
        except Exception as e:
            self.logger.error(f"Error creating rotation animation: {str(e)}")
            return start_frame
        
class FlashAround(Animation):
    """Create a flash/highlight effect around an object"""
    def __init__(self, target: bpy.types.Object, color: Tuple[float, float, float] = (1, 1, 0),
                 thickness: float = 0.1, config: Optional[AnimationConfig] = None):
        super().__init__(target, config)
        self.color = color
        self.thickness = thickness
        self.highlight_obj = None
    
    def create_keyframes(self, start_frame: int, end_frame: int):
        try:
            # Create emission material
            mat = bpy.data.materials.new(name="highlight_material")
            mat.use_nodes = True
            mat.blend_method = 'BLEND'
            
            nodes = mat.node_tree.nodes
            links = mat.node_tree.links
            
            # Clear existing nodes
            nodes.clear()
            
            # Add new nodes
            emission = nodes.new('ShaderNodeEmission')
            output = nodes.new('ShaderNodeOutputMaterial')
            
            # Set up nodes
            emission.inputs['Color'].default_value = (*self.color, 1)
            links.new(emission.outputs['Emission'], output.inputs['Surface'])
            
            # Create highlight object
            bpy.ops.mesh.primitive_circle_add(
                vertices=32,
                radius=self.target.dimensions.length/2 + self.thickness,
                location=self.target.location
            )
            self.highlight_obj = bpy.context.active_object
            self.highlight_obj.data.materials.append(mat)
            
            # Animate emission strength using material node tree
            strength_path = 'nodes["Emission"].inputs[1].default_value'
            
            # Start (no emission)
            emission.inputs['Strength'].default_value = 0
            mat.node_tree.keyframe_insert(data_path=strength_path, frame=start_frame)
            
            # Peak (full emission)
            mid_frame = (start_frame + end_frame) // 2
            emission.inputs['Strength'].default_value = 5
            mat.node_tree.keyframe_insert(data_path=strength_path, frame=mid_frame)
            
            # End (no emission)
            emission.inputs['Strength'].default_value = 0
            mat.node_tree.keyframe_insert(data_path=strength_path, frame=end_frame)
            
            return end_frame
            
        except Exception as e:
            self.logger.error(f"Error creating FlashAround animation: {str(e)}")
            return start_frame

    def cleanup(self):
        """Remove highlight object when done"""
        if self.highlight_obj:
            bpy.data.objects.remove(self.highlight_obj, do_unlink=True)