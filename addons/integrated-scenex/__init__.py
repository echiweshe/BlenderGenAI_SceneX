bl_info = {
    "name": "Integrated SceneX",
    "blender": (2, 82, 0),
    "category": "Animation",
    "author": "Original: Aarya (@gd3kr), SceneX Integration",
    "version": (2, 0, 0),
    "location": "View3D > UI > SceneX",
    "description": "AI-powered animation system with Manim-style precision.",
}

import sys
import os
import bpy
from bpy.types import (AddonPreferences, Operator, Panel, PropertyGroup)
from bpy.props import (StringProperty, BoolProperty, IntProperty, EnumProperty, CollectionProperty)
import re

libs_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "lib")
if libs_path not in sys.path:
    sys.path.append(libs_path)

import anthropic
from .utilities import *

system_prompt = """You are an assistant made for the purposes of helping the user with Blender, the 3D software. 
- Respond with your answers in markdown (```).
- Preferably import entire modules instead of bits. 
- Do not perform destructive operations on the meshes. 
- Do not use cap_ends. Do not do more than what is asked (setting up render settings, adding cameras, etc).
- Do not respond with anything that is not Python code."""

class MessagePropertyGroup(PropertyGroup):
    type: StringProperty()
    content: StringProperty()

class IntegratedSceneXPreferences(AddonPreferences):
    bl_idname = __name__

    api_key: StringProperty(
        name="API Key",
        description="Enter your Anthropic Claude API Key",
        default="",
        subtype="PASSWORD",
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "api_key")
        layout.label(text="Enter your Anthropic API key from console.anthropic.com")

class SceneX_OT_DeleteMessage(Operator):
    bl_idname = "scenex.delete_message"
    bl_label = "Delete Message"
    bl_options = {'REGISTER', 'UNDO'}

    message_index: IntProperty()

    def execute(self, context):
        context.scene.claude_chat_history.remove(self.message_index)
        return {'FINISHED'}

class SceneX_OT_ShowCode(Operator):
    bl_idname = "scenex.show_code"
    bl_label = "Show Code"
    bl_options = {'REGISTER', 'UNDO'}

    code: StringProperty(
        name="Code",
        description="The generated code",
        default="",
    )

    def execute(self, context):
        text_name = "SceneX_Generated_Code.py"
        text = bpy.data.texts.get(text_name)
        if text is None:
            text = bpy.data.texts.new(text_name)

        text.clear()
        text.write(self.code)

        text_editor_area = None
        for area in context.screen.areas:
            if area.type == 'TEXT_EDITOR':
                text_editor_area = area
                break

        if text_editor_area is None:
            text_editor_area = split_area_to_text_editor(context)
        
        text_editor_area.spaces.active.text = text
        return {'FINISHED'}

class SceneX_PT_Panel(Panel):
    bl_label = "SceneX Assistant"
    bl_idname = "SCENEX_PT_main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SceneX'

    def draw(self, context):
        layout = self.layout
        column = layout.column(align=True)

        column.label(text="Chat history:")
        box = column.box()
        for index, message in enumerate(context.scene.claude_chat_history):
            if message.type == 'assistant':
                row = box.row()
                row.label(text="Assistant: ")
                show_code_op = row.operator("scenex.show_code", text="Show Code")
                show_code_op.code = message.content
                delete_message_op = row.operator("scenex.delete_message", text="", icon="TRASH", emboss=False)
                delete_message_op.message_index = index
            else:
                row = box.row()
                row.label(text=f"User: {message.content}")
                delete_message_op = row.operator("scenex.delete_message", text="", icon="TRASH", emboss=False)
                delete_message_op.message_index = index

        column.separator()
        column.label(text="Claude Model:")
        column.prop(context.scene, "claude_model", text="")
        column.label(text="Enter your message:")
        column.prop(context.scene, "chat_input", text="")
        button_label = "Please wait..." if context.scene.processing else "Generate"
        row = column.row(align=True)
        row.operator("scenex.execute", text=button_label)
        row.operator("scenex.clear_chat", text="Clear Chat")
        column.separator()

class SceneX_OT_ClearChat(Operator):
    bl_idname = "scenex.clear_chat"
    bl_label = "Clear Chat"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.scene.claude_chat_history.clear()
        return {'FINISHED'}

class SceneX_OT_Execute(Operator):
    bl_idname = "scenex.execute"
    bl_label = "Generate Scene"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        api_key = get_api_key(context, __name__)
        if not api_key:
            api_key = os.getenv("ANTHROPIC_API_KEY")

        if not api_key:
            self.report({'ERROR'}, "No API key detected. Please set the API key in the addon preferences.")
            return {'CANCELLED'}

        context.scene.processing = True
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        
        try:
            client = anthropic.Client(api_key=api_key)
            messages = []
            for msg in context.scene.claude_chat_history[-10:]:
                role = "assistant" if msg.type == "assistant" else "user"
                messages.append({"role": role, "content": msg.content})
                
            messages.append({
                "role": "user",
                "content": f"{system_prompt}\n\nUser: {context.scene.chat_input}"
            })
            
            response = client.messages.create(
                model=context.scene.claude_model,
                max_tokens=1500,
                messages=messages
            )
            
            blender_code = response.content[0].text
            code_match = re.findall(r'```(?:python)?(.*?)```', blender_code, re.DOTALL)
            if code_match:
                blender_code = code_match[0].strip()
            
            message = context.scene.claude_chat_history.add()
            message.type = 'user'
            message.content = context.scene.chat_input
            context.scene.chat_input = ""

            if blender_code:
                message = context.scene.claude_chat_history.add()
                message.type = 'assistant'
                message.content = blender_code

                global_namespace = globals().copy()
                try:
                    exec(blender_code, global_namespace)
                except Exception as e:
                    self.report({'ERROR'}, f"Error executing generated code: {e}")
                    context.scene.processing = False
                    return {'CANCELLED'}

        except Exception as e:
            self.report({'ERROR'}, f"Error with Claude API: {e}")
            context.scene.processing = False
            return {'CANCELLED'}

        context.scene.processing = False
        return {'FINISHED'}

def register():
    bpy.utils.register_class(MessagePropertyGroup)
    bpy.utils.register_class(IntegratedSceneXPreferences)
    bpy.utils.register_class(SceneX_OT_Execute)
    bpy.utils.register_class(SceneX_PT_Panel)
    bpy.utils.register_class(SceneX_OT_ClearChat)
    bpy.utils.register_class(SceneX_OT_ShowCode)
    bpy.utils.register_class(SceneX_OT_DeleteMessage)

    bpy.types.Scene.claude_model = EnumProperty(
        name="Claude Model",
        items=[
            ("claude-3-opus-20240229", "Claude 3 Opus", "Most capable"),
            ("claude-3-sonnet-20240229", "Claude 3 Sonnet", "Balanced"),
            ("claude-3-haiku-20240307", "Claude 3 Haiku", "Fastest"),
        ],
        default="claude-3-opus-20240229"
    )
    
    bpy.types.Scene.chat_input = StringProperty(
        name="Message",
        default=""
    )
    
    bpy.types.Scene.claude_chat_history = CollectionProperty(type=MessagePropertyGroup)
    bpy.types.Scene.processing = BoolProperty(default=False)

def unregister():
    bpy.utils.unregister_class(MessagePropertyGroup)
    bpy.utils.unregister_class(IntegratedSceneXPreferences)
    bpy.utils.unregister_class(SceneX_OT_Execute)
    bpy.utils.unregister_class(SceneX_PT_Panel)
    bpy.utils.unregister_class(SceneX_OT_ClearChat)
    bpy.utils.unregister_class(SceneX_OT_ShowCode)
    bpy.utils.unregister_class(SceneX_OT_DeleteMessage)

    del bpy.types.Scene.claude_model
    del bpy.types.Scene.chat_input
    del bpy.types.Scene.claude_chat_history
    del bpy.types.Scene.processing

if __name__ == "__main__":
    register()