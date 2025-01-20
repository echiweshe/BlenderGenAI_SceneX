# ui/panels.py
import bpy

class SCENEX_PT_BasePanel:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "SceneX"

class SCENEX_PT_MainPanel(SCENEX_PT_BasePanel, bpy.types.Panel):
    """Main panel for SceneX"""
    bl_label = "SceneX"
    bl_idname = "SCENEX_PT_main"
    
    def draw(self, context):
        layout = self.layout
        
        # Preset menu
        row = layout.row(align=True)
        row.menu("SCENEX_MT_preset_menu", text="Presets")

class SCENEX_PT_AnimationPanel(SCENEX_PT_BasePanel, bpy.types.Panel):
    """Animation controls for SceneX"""
    bl_label = "Animation"
    bl_idname = "SCENEX_PT_animation"
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.scenex
        
        col = layout.column(align=True)
        col.prop(props, "animation_type")
        col.prop(props, "animation_duration")
        col.prop(props, "rate_function")
        
        row = layout.row()
        row.operator("scenex.add_animation")

class SCENEX_PT_CameraPanel(SCENEX_PT_BasePanel, bpy.types.Panel):
    """Camera controls for SceneX"""
    bl_label = "Camera"
    bl_idname = "SCENEX_PT_camera"
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.scenex
        
        col = layout.column(align=True)
        col.prop(props, "camera_movement")
        col.prop(props, "camera_target_distance")
        
        row = layout.row()
        row.operator("scenex.camera_move")

class SCENEX_PT_GridPanel(SCENEX_PT_BasePanel, bpy.types.Panel):
    """Grid controls for SceneX"""
    bl_label = "Grid"
    bl_idname = "SCENEX_PT_grid"
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.scenex
        
        col = layout.column(align=True)
        col.prop(props, "grid_size")
        col.prop(props, "grid_subdivisions")
        col.prop(props, "show_labels")
        
        row = layout.row()
        row.operator("scenex.create_grid")

class SCENEX_PT_MaterialPanel(SCENEX_PT_BasePanel, bpy.types.Panel):
    """Material controls for SceneX"""
    bl_label = "Material"
    bl_idname = "SCENEX_PT_material"
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.scenex
        
        col = layout.column(align=True)
        col.prop(props, "material_type")
        col.prop(props, "material_color")
        
        row = layout.row()
        row.operator("scenex.assign_material")

# Register/unregister all panels
classes = (
    SCENEX_PT_AnimationPanel,
    SCENEX_PT_CameraPanel,
    SCENEX_PT_GridPanel,
    SCENEX_PT_MaterialPanel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    print("SceneX Panels registered")

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    print("SceneX Panels unregistered")
