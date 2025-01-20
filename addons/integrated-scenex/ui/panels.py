# integrated-scenex/ui/panels.py

import bpy

class SceneXPanel(bpy.types.Panel):
    bl_label = "SceneX"
    bl_idname = "VIEW3D_PT_scenex"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SceneX'

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, "claude_model")
        layout.prop(context.scene, "chat_input")
        layout.operator("scenex.generate_scene")

def register():
    bpy.utils.register_class(SceneXPanel)

def unregister():
    bpy.utils.unregister_class(SceneXPanel)