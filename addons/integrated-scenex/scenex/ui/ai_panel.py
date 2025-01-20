# ui/ai_panel.py

import bpy
from bpy.props import StringProperty
from ..src.ai.scene_generator import AISceneGenerator

class SCENEX_OT_GenerateScene(bpy.types.Operator):
    """Generate scene from natural language description"""
    bl_idname = "scenex.generate_scene"
    bl_label = "Generate Scene"
    bl_description = "Generate a scene from natural language description"
    bl_options = {'REGISTER', 'UNDO'}
    
    prompt: StringProperty(
        name="Description",
        description="Describe the architecture you want to create",
        default=""
    )
    
    def execute(self, context):
        if not self.prompt.strip():
            self.report({'ERROR'}, "Please provide a description")
            return {'CANCELLED'}
            
        generator = AISceneGenerator()
        try:
            # Process prompt and generate scene
            scene_data = generator.process_prompt(self.prompt)
            if scene_data:
                generator.generate_scene(scene_data)
                self.report({'INFO'}, "Scene generated successfully")
                return {'FINISHED'}
            else:
                self.report({'ERROR'}, "Could not generate scene from description")
                return {'CANCELLED'}
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "prompt", text="")
        layout.label(text="Example: Create a serverless ML pipeline with API Gateway and Lambda")

class SCENEX_PT_AIPanel(bpy.types.Panel):
    """Panel for AI scene generation"""
    bl_label = "AI Scene Generator"
    bl_idname = "SCENEX_PT_ai"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "SceneX"
    
    def draw(self, context):
        layout = self.layout
        
        col = layout.column(align=True)
        col.operator("scenex.generate_scene", text="Generate Scene", icon='SHADERFX')
        
        # Add quick presets
        box = layout.box()
        box.label(text="Quick Presets:")
        col = box.column(align=True)
        col.operator("scenex.generate_scene", text="Serverless API").prompt = "Create serverless API with API Gateway and Lambda"
        col.operator("scenex.generate_scene", text="ML Pipeline").prompt = "Create ML pipeline with SageMaker and S3"
        col.operator("scenex.generate_scene", text="VPC Network").prompt = "Create VPC with public and private subnets"

# Register classes
classes = (
    SCENEX_OT_GenerateScene,
    SCENEX_PT_AIPanel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)