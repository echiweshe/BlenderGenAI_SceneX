# SceneX/src/scene/grid.py

import bpy
import math
from mathutils import Vector
from ..utils.logger import SceneXLogger

class GridSystem:
    def __init__(self):
        self.axes = {}
        self.grid_lines = []
        self.labels = []
        self.logger = SceneXLogger("GridSystem")

    def create_coordinate_system(self, 
                               x_range=(-10, 10),
                               y_range=(-10, 10),
                               grid_step=1.0,
                               show_axes=True,
                               show_grid=True,
                               show_labels=True,
                               axis_color=(1, 1, 1, 1),
                               grid_color=(0.2, 0.2, 0.2, 0.5),
                               line_width=0.01):

        if show_axes:
            self._create_axes(x_range, y_range, axis_color, line_width*2)

        if show_grid:
            self._create_grid(x_range, y_range, grid_step, grid_color, line_width)

        if show_labels:
            self._create_labels(x_range, y_range, grid_step, axis_color)

    def _create_axes(self, x_range, y_range, color, width):
        # X-axis
        curve_data = bpy.data.curves.new('x_axis', 'CURVE')
        curve_data.dimensions = '3D'
        spline = curve_data.splines.new('POLY')
        spline.points.add(1)
        spline.points[0].co = (x_range[0], 0, 0, 1)
        spline.points[1].co = (x_range[1], 0, 0, 1)
        x_axis = bpy.data.objects.new('x_axis', curve_data)
        x_axis.data.bevel_depth = width
        self.axes['x'] = x_axis

        # Y-axis
        curve_data = bpy.data.curves.new('y_axis', 'CURVE')
        curve_data.dimensions = '3D'
        spline = curve_data.splines.new('POLY')
        spline.points.add(1)
        spline.points[0].co = (0, y_range[0], 0, 1)
        spline.points[1].co = (0, y_range[1], 0, 1)
        y_axis = bpy.data.objects.new('y_axis', curve_data)
        y_axis.data.bevel_depth = width
        self.axes['y'] = y_axis

        for axis in self.axes.values():
            bpy.context.scene.collection.objects.link(axis)
            mat = bpy.data.materials.new(name=f"{axis.name}_material")
            mat.use_nodes = True
            mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = color
            axis.data.materials.append(mat)

    def _create_grid(self, x_range, y_range, step, color, width):
        # Create vertical lines
        for x in range(int(x_range[0]), int(x_range[1]) + 1, int(step)):
            if x == 0:
                continue
            curve_data = bpy.data.curves.new(f'grid_v_{x}', 'CURVE')
            curve_data.dimensions = '3D'
            spline = curve_data.splines.new('POLY')
            spline.points.add(1)
            spline.points[0].co = (x, y_range[0], 0, 1)
            spline.points[1].co = (x, y_range[1], 0, 1)
            line = bpy.data.objects.new(f'grid_v_{x}', curve_data)
            line.data.bevel_depth = width
            self.grid_lines.append(line)

        # Create horizontal lines
        for y in range(int(y_range[0]), int(y_range[1]) + 1, int(step)):
            if y == 0:
                continue
            curve_data = bpy.data.curves.new(f'grid_h_{y}', 'CURVE')
            curve_data.dimensions = '3D'
            spline = curve_data.splines.new('POLY')
            spline.points.add(1)
            spline.points[0].co = (x_range[0], y, 0, 1)
            spline.points[1].co = (x_range[1], y, 0, 1)
            line = bpy.data.objects.new(f'grid_h_{y}', curve_data)
            line.data.bevel_depth = width
            self.grid_lines.append(line)

        for line in self.grid_lines:
            bpy.context.scene.collection.objects.link(line)
            mat = bpy.data.materials.new(name=f"{line.name}_material")
            mat.use_nodes = True
            mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = color
            line.data.materials.append(mat)

    def _create_labels(self, x_range, y_range, step, color):
        for x in range(int(x_range[0]), int(x_range[1]) + 1, int(step)):
            if x == 0:
                continue
            bpy.ops.object.text_add(location=(x, -0.5, 0))
            text = bpy.context.active_object
            text.data.body = str(x)
            text.scale = (0.3, 0.3, 0.3)
            self.labels.append(text)

        for y in range(int(y_range[0]), int(y_range[1]) + 1, int(step)):
            if y == 0:
                continue
            bpy.ops.object.text_add(location=(-0.5, y, 0))
            text = bpy.context.active_object
            text.data.body = str(y)
            text.scale = (0.3, 0.3, 0.3)
            self.labels.append(text)

        for label in self.labels:
            mat = bpy.data.materials.new(name=f"{label.name}_material")
            mat.use_nodes = True
            mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = color
            label.data.materials.append(mat)