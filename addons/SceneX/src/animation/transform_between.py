# src/animation/transform_between.py

import bpy
import bmesh
import random
from mathutils import Vector, interpolate
from .base import Animation, AnimationConfig
from ..utils.logger import SceneXLogger

class TransformBetween(Animation):
    """Transform one mesh object into another"""
    def __init__(self, source_obj: bpy.types.Object, target_obj: bpy.types.Object, 
                 config: AnimationConfig = None):
        super().__init__(source_obj, config)
        self.target_obj = target_obj
        self.logger = SceneXLogger("TransformBetween")
        
        # Store vertex data
        self.source_verts = [v.co.copy() for v in source_obj.data.vertices]
        self.target_verts = self._get_corresponding_verts()
        
    def _get_corresponding_verts(self):
        """Map vertices between source and target meshes"""
        source_verts = len(self.source_verts)
        target_verts = len(self.target_obj.data.vertices)
        
        if source_verts != target_verts:
            self.logger.warning(f"Vertex count mismatch: {source_verts} vs {target_verts}")
            # Resample target mesh to match source vertex count
            return self._resample_mesh(self.target_obj, source_verts)
            
        return [v.co.copy() for v in self.target_obj.data.vertices]
    
    def _resample_mesh(self, obj, target_count):
        """Resample mesh to have target number of vertices"""
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        
        # Subdivide or simplify mesh to match vertex count
        while len(bm.verts) < target_count:
            bmesh.ops.subdivide_edges(bm, 
                edges=bm.edges[:], 
                cuts=1)
        
        while len(bm.verts) > target_count:
            bmesh.ops.dissolve_edges(bm,
                edges=[e for e in bm.edges if len(e.link_faces) == 2],
                use_verts=True)
        
        verts = [v.co.copy() for v in bm.verts]
        bm.free()
        return verts
    
    def create_keyframes(self, start_frame: int, end_frame: int):
        """Create vertex animation keyframes"""
        try:
            # Enable mesh shape keys
            if not self.target.data.shape_keys:
                self.target.shape_key_add(name="Basis")
            
            # Add target shape key
            shape_key = self.target.shape_key_add(name="Target")
            
            # Keyframe vertex positions
            for frame in range(start_frame, end_frame + 1):
                factor = (frame - start_frame) / (end_frame - start_frame)
                factor = self.config.rate_func(factor)
                
                # Interpolate vertex positions
                for i, (start, end) in enumerate(zip(self.source_verts, self.target_verts)):
                    shape_key.data[i].co = start.lerp(end, factor)
                
                shape_key.value = factor
                shape_key.keyframe_insert("value", frame=frame)
                
            self.logger.info("Created transform animation keyframes")
            
        except Exception as e:
            self.logger.error(f"Error creating transform animation: {str(e)}")

class MorphBetween(TransformBetween):
    """Morph between objects with different topologies using surface sampling"""
    def __init__(self, source_obj: bpy.types.Object, target_obj: bpy.types.Object, 
                 samples: int = 1000, config: AnimationConfig = None):
        self.samples = samples
        super().__init__(source_obj, target_obj, config)
    
    def _get_corresponding_verts(self):
        """Sample points on both meshes"""
        source_points = self._sample_surface(self.target, self.samples)
        target_points = self._sample_surface(self.target_obj, self.samples)
        return target_points
    
    def _sample_surface(self, obj, count):
        """Randomly sample points on mesh surface"""
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        bmesh.ops.triangulate(bm, faces=bm.faces[:])
        
        total_area = sum(f.calc_area() for f in bm.faces)
        points = []
        
        for face in bm.faces:
            # Sample proportional to face area
            n_points = int((face.calc_area() / total_area) * count)
            points.extend(self._sample_triangle(face, n_points))
        
        bm.free()
        return points
    
    def _sample_triangle(self, face, count):
        """Generate random points within a triangle"""
        points = []
        verts = [v.co for v in face.verts]
        
        for _ in range(count):
            # Random barycentric coordinates
            u = random.random()
            v = random.random() * (1 - u)
            w = 1 - u - v
            
            # Interpolate position
            point = verts[0] * u + verts[1] * v + verts[2] * w
            points.append(point)
        
        return points