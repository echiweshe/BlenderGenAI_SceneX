# integrated-scenex/ui/operators.py

import bpy
from ..core.scene_generator import SceneGenerator

class GenerateScene(bpy.types.Operator):
    bl_idname = "scenex.generate_scene"
    bl_label = "Generate Scene"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        generator = SceneGenerator()
        result = generator.generate_from_prompt(context.scene.chat_input)
        if result["success"]:
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, str(result["error"]))
            return {'CANCELLED'}

def register():
    bpy.utils.register_class(GenerateScene)

def unregister():
    bpy.utils.unregister_class(GenerateScene)