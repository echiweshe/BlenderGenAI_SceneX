# # /BlenderGPT-main/__init__.py
# import sys
# import os
# import bpy
# import bpy.props
# import re
# from bpy.types import AddonPreferences  # Add this import

# # Add the 'libs' folder to the Python path
# libs_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "lib")
# if libs_path not in sys.path:
#     sys.path.append(libs_path)

# import anthropic

# from .utilities import *

# bl_info = {
#     "name": "Claude Blender Assistant",
#     "blender": (2, 82, 0),
#     "category": "Object",
#     "author": "Aarya (@gd3kr), Modified for Claude",
#     "version": (2, 0, 0),
#     "location": "3D View > UI > Claude Blender Assistant",
#     "description": "Generate Blender Python code using Anthropic's Claude to perform various tasks.",
#     "warning": "",
#     "wiki_url": "",
#     "tracker_url": "",
# }

# # Change the class definition
# class ClaudeAddonPreferences(AddonPreferences):  # Now inherits from the imported AddonPreferences
#     bl_idname = __name__

#     api_key: bpy.props.StringProperty(
#         name="API Key",
#         description="Enter your Anthropic Claude API Key",
#         default="",
#         subtype="PASSWORD",
#     )

#     def draw(self, context):
#         layout = self.layout
#         layout.prop(self, "api_key")
#         layout.label(text="Enter your Anthropic API key from console.anthropic.com")

# # [Rest of the code remains the same...]
# # Addon Preferences for API key
# class BlenderGPTPreferences(AddonPreferences):
#     bl_idname = "BlenderGPT"  # This should match your addon's name/folder

#     api_key: StringProperty(
#         name="Claude API Key",
#         description="Enter your Anthropic Claude API key",
#         default="",
#         subtype='PASSWORD'  # This hides the API key
#     )

#     def draw(self, context):
#         layout = self.layout
#         layout.prop(self, "api_key")
#         layout.label(text="Enter your Anthropic API key. Get one at: https://console.anthropic.com/")

# class GPT_PT_Panel(bpy.types.Panel):
#     bl_label = "BlenderGPT"
#     bl_idname = "GPT_PT_Panel"
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'
#     bl_category = 'BlenderGPT'

#     def draw(self, context):
#         layout = self.layout
#         scene = context.scene

#         # Add model selection
#         layout.prop(scene, "claude_model")
        
#         # Add text input box
#         layout.prop(scene, "claude_chat_input")
        
#         # Add execute button
#         row = layout.row()
#         row.scale_y = 2.0  # Make button bigger
#         row.operator("gpt.execute")

#         # Add chat history
#         box = layout.box()
#         box.label(text="Chat History:")
        
#         for message in scene.claude_chat_history:
#             msg_box = box.box()
#             msg_box.label(text=f"{message.type}:")
#             msg_box.label(text=message.content)

# # def register():
# #     bpy.utils.register_class(BlenderGPTPreferences)
# #     bpy.utils.register_class(GPT_PT_Panel)
    
# #     # Register properties
# #     bpy.types.Scene.claude_model = bpy.props.EnumProperty(
# #         name="Claude Model",
# #         description="Select the Claude model to use",
# #         items=[
# #             ("claude-3-opus-20240229", "Claude 3 Opus (most capable)", "Use Claude 3 Opus"),
# #             ("claude-3-sonnet-20240229", "Claude 3 Sonnet (balanced)", "Use Claude 3 Sonnet"),
# #             ("claude-3-haiku-20240307", "Claude 3 Haiku (fastest)", "Use Claude 3 Haiku"),
# #         ],
# #         default="claude-3-opus-20240229"
# #     )
    
# #     bpy.types.Scene.claude_chat_input = bpy.props.StringProperty(
# #         name="Message",
# #         description="Enter your prompt",
# #         default=""
# #     )
    
# #     bpy.types.Scene.claude_chat_history = bpy.props.CollectionProperty(type=bpy.types.PropertyGroup)


# def register():
#     # Register property types first
#     bpy.types.PropertyGroup.type = bpy.props.StringProperty()
#     bpy.types.PropertyGroup.content = bpy.props.StringProperty()
    
#     # Register classes
#     bpy.utils.register_class(ClaudeAddonPreferences)
#     bpy.utils.register_class(Claude_OT_Execute)
#     bpy.utils.register_class(Claude_PT_Panel)
#     bpy.utils.register_class(Claude_OT_ClearChat)
#     bpy.utils.register_class(Claude_OT_ShowCode)
#     bpy.utils.register_class(Claude_OT_DeleteMessage)

#     # Register properties
#     bpy.types.Scene.claude_model = bpy.props.EnumProperty(
#         name="Claude Model",
#         description="Select the Claude model to use",
#         items=[
#             ("claude-3-opus-20240229", "Claude 3 Opus (most capable)", "Use Claude 3 Opus"),
#             ("claude-3-sonnet-20240229", "Claude 3 Sonnet (balanced)", "Use Claude 3 Sonnet"),
#             ("claude-3-haiku-20240307", "Claude 3 Haiku (fastest)", "Use Claude 3 Haiku"),
#         ],
#         default="claude-3-opus-20240229"
#     )
    
#     bpy.types.Scene.claude_chat_input = bpy.props.StringProperty(
#         name="Message",
#         description="Enter your prompt",
#         default=""
#     )
    
#     bpy.types.Scene.claude_chat_history = bpy.props.CollectionProperty(type=bpy.types.PropertyGroup)
#     bpy.types.Scene.claude_button_pressed = bpy.props.BoolProperty(default=False)
    
#     bpy.types.VIEW3D_MT_mesh_add.append(menu_func)


# def unregister():
#     bpy.utils.unregister_class(BlenderGPTPreferences)
#     bpy.utils.unregister_class(GPT_PT_Panel)
    
#     del bpy.types.Scene.claude_model
#     del bpy.types.Scene.claude_chat_input
#     del bpy.types.Scene.claude_chat_history

# # Function to get API key
# def get_api_key(context):
#     preferences = context.preferences
#     addon_prefs = preferences.addons["BlenderGPT"].preferences
#     return addon_prefs.api_key

# # Modified generate_blender_code function
# def generate_blender_code(prompt, chat_history, context):
#     api_key = get_api_key(context)
#     if not api_key:
#         raise ValueError("API key not found. Please enter your API key in the addon preferences.")

#     client = anthropic.Client(api_key=api_key)
    
#     messages = []
#     for message in chat_history[-10:]:
#         if message.type == "assistant":
#             messages.append({"role": "assistant", "content": message.content})
#         else:
#             messages.append({"role": "user", "content": message.content})

#     try:
#         response = client.messages.create(
#             model=context.scene.claude_model,
#             max_tokens=1500,
#             messages=[{
#                 "role": "user", 
#                 "content": f"Write Blender Python code for: {prompt}. Provide only the code, no explanations."
#             }]
#         )
        
#         # Extract code from response
#         completion_text = response.content[0].text
#         code_match = re.findall(r'```(?:python)?(.*?)```', completion_text, re.DOTALL)
#         if code_match:
#             return code_match[0].strip()
#         return completion_text.strip()
        
#     except Exception as e:
#         print(f"Error generating code: {e}")
#         return None

# class GPT_OT_Execute(bpy.types.Operator):
#     bl_idname = "gpt.execute"
#     bl_label = "Generate and Execute Code"
    
#     def execute(self, context):
#         prompt = context.scene.claude_chat_input
#         if not prompt:
#             self.report({'ERROR'}, "Please enter a prompt")
#             return {'CANCELLED'}
            
#         try:
#             code = generate_blender_code(prompt, context.scene.claude_chat_history, context)
#             if code:
#                 # Add to chat history
#                 item = context.scene.claude_chat_history.add()
#                 item.type = "user"
#                 item.content = prompt
                
#                 item = context.scene.claude_chat_history.add()
#                 item.type = "assistant"
#                 item.content = code
                
#                 # Execute the code
#                 exec(code)
                
#                 # Clear input field
#                 context.scene.claude_chat_input = ""
                
#             return {'FINISHED'}
#         except Exception as e:
#             self.report({'ERROR'}, f"Error: {str(e)}")
#             return {'CANCELLED'}

# if __name__ == "__main__":
#     register()





# # /BlenderGPT-main/__init__.py
# import sys
# import os
# import bpy
# from bpy.types import (
#     AddonPreferences,
#     Operator,
#     Panel,
#     PropertyGroup
# )
# from bpy.props import (
#     StringProperty,
#     BoolProperty,
#     IntProperty,
#     EnumProperty,
#     CollectionProperty
# )
# import re

# # Add the 'libs' folder to the Python path
# libs_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "lib")
# if libs_path not in sys.path:
#     sys.path.append(libs_path)

# import anthropic

# from .utilities import *

# bl_info = {
#     "name": "Claude Blender Assistant",
#     "blender": (2, 82, 0),
#     "category": "Object",
#     "author": "Aarya (@gd3kr), Modified for Claude",
#     "version": (2, 0, 0),
#     "location": "3D View > UI > Claude Blender Assistant",
#     "description": "Generate Blender Python code using Anthropic's Claude to perform various tasks.",
#     "warning": "",
#     "wiki_url": "",
#     "tracker_url": "",
# }

# class MessagePropertyGroup(PropertyGroup):
#     type: StringProperty()
#     content: StringProperty()

# class ClaudeAddonPreferences(AddonPreferences):
#     bl_idname = __name__

#     api_key: StringProperty(
#         name="API Key",
#         description="Enter your Anthropic Claude API Key",
#         default="",
#         subtype="PASSWORD",
#     )

#     def draw(self, context):
#         layout = self.layout
#         layout.prop(self, "api_key")
#         layout.label(text="Enter your Anthropic API key from console.anthropic.com")

# class Claude_OT_DeleteMessage(Operator):
#     bl_idname = "claude.delete_message"
#     bl_label = "Delete Message"
#     bl_options = {'REGISTER', 'UNDO'}

#     message_index: IntProperty()

#     def execute(self, context):
#         context.scene.claude_chat_history.remove(self.message_index)
#         return {'FINISHED'}

# class Claude_OT_ShowCode(Operator):
#     bl_idname = "claude.show_code"
#     bl_label = "Show Code"
#     bl_options = {'REGISTER', 'UNDO'}

#     code: StringProperty(
#         name="Code",
#         description="The generated code",
#         default="",
#     )

#     def execute(self, context):
#         text_name = "Claude_Generated_Code.py"
#         text = bpy.data.texts.get(text_name)
#         if text is None:
#             text = bpy.data.texts.new(text_name)

#         text.clear()
#         text.write(self.code)

#         text_editor_area = None
#         for area in context.screen.areas:
#             if area.type == 'TEXT_EDITOR':
#                 text_editor_area = area
#                 break

#         if text_editor_area is None:
#             text_editor_area = split_area_to_text_editor(context)
        
#         text_editor_area.spaces.active.text = text

#         return {'FINISHED'}

# class Claude_PT_Panel(Panel):
#     bl_label = "Claude Blender Assistant"
#     bl_idname = "CLAUDE_PT_Panel"
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'
#     bl_category = 'Claude Assistant'

#     def draw(self, context):
#         layout = self.layout
#         column = layout.column(align=True)

#         column.label(text="Chat history:")
#         box = column.box()
#         for index, message in enumerate(context.scene.claude_chat_history):
#             if message.type == 'assistant':
#                 row = box.row()
#                 row.label(text="Assistant: ")
#                 show_code_op = row.operator("claude.show_code", text="Show Code")
#                 show_code_op.code = message.content
#                 delete_message_op = row.operator("claude.delete_message", text="", icon="TRASH", emboss=False)
#                 delete_message_op.message_index = index
#             else:
#                 row = box.row()
#                 row.label(text=f"User: {message.content}")
#                 delete_message_op = row.operator("claude.delete_message", text="", icon="TRASH", emboss=False)
#                 delete_message_op.message_index = index

#         column.separator()
        
#         column.label(text="Claude Model:")
#         column.prop(context.scene, "claude_model", text="")

#         column.label(text="Enter your message:")
#         column.prop(context.scene, "claude_chat_input", text="")
#         button_label = "Please wait...(this might take some time)" if context.scene.claude_button_pressed else "Execute"
#         row = column.row(align=True)
#         row.operator("claude.send_message", text=button_label)
#         row.operator("claude.clear_chat", text="Clear Chat")

#         column.separator()

# [...remaining classes stay the same...]

# def register():
#     # Register classes
#     bpy.utils.register_class(MessagePropertyGroup)
#     bpy.utils.register_class(ClaudeAddonPreferences)
#     bpy.utils.register_class(Claude_OT_Execute)
#     bpy.utils.register_class(Claude_PT_Panel)
#     bpy.utils.register_class(Claude_OT_ClearChat)
#     bpy.utils.register_class(Claude_OT_ShowCode)
#     bpy.utils.register_class(Claude_OT_DeleteMessage)

#     # Register properties
#     bpy.types.Scene.claude_model = EnumProperty(
#         name="Claude Model",
#         description="Select the Claude model to use",
#         items=[
#             ("claude-3-opus-20240229", "Claude 3 Opus (most capable)", "Use Claude 3 Opus"),
#             ("claude-3-sonnet-20240229", "Claude 3 Sonnet (balanced)", "Use Claude 3 Sonnet"),
#             ("claude-3-haiku-20240307", "Claude 3 Haiku (fastest)", "Use Claude 3 Haiku"),
#         ],
#         default="claude-3-opus-20240229"
#     )
    
#     bpy.types.Scene.claude_chat_input = StringProperty(
#         name="Message",
#         description="Enter your prompt",
#         default=""
#     )
    
#     bpy.types.Scene.claude_chat_history = CollectionProperty(type=MessagePropertyGroup)
#     bpy.types.Scene.claude_button_pressed = BoolProperty(default=False)
    
#     bpy.types.VIEW3D_MT_mesh_add.append(menu_func)

# def unregister():
#     # Unregister classes
#     bpy.utils.unregister_class(MessagePropertyGroup)
#     bpy.utils.unregister_class(ClaudeAddonPreferences)
#     bpy.utils.unregister_class(Claude_OT_Execute)
#     bpy.utils.unregister_class(Claude_PT_Panel)
#     bpy.utils.unregister_class(Claude_OT_ClearChat)
#     bpy.utils.unregister_class(Claude_OT_ShowCode)
#     bpy.utils.unregister_class(Claude_OT_DeleteMessage)

#     # Remove properties
#     del bpy.types.Scene.claude_model
#     del bpy.types.Scene.claude_chat_input
#     del bpy.types.Scene.claude_chat_history
#     del bpy.types.Scene.claude_button_pressed
    
#     bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)

# if __name__ == "__main__":
#     register()



# /BlenderGPT-main/__init__.py
import sys
import os
import bpy
from bpy.types import (
    AddonPreferences,
    Operator,
    Panel,
    PropertyGroup
)
from bpy.props import (
    StringProperty,
    BoolProperty,
    IntProperty,
    EnumProperty,
    CollectionProperty
)
import re

# Add the 'libs' folder to the Python path
libs_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "lib")
if libs_path not in sys.path:
    sys.path.append(libs_path)

import anthropic

from .utilities import *

bl_info = {
    "name": "Claude Blender Assistant",
    "blender": (2, 82, 0),
    "category": "Object",
    "author": "Aarya (@gd3kr), Modified for Claude",
    "version": (2, 0, 0),
    "location": "3D View > UI > Claude Blender Assistant",
    "description": "Generate Blender Python code using Anthropic's Claude to perform various tasks.",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
}

system_prompt = """You are an assistant made for the purposes of helping the user with Blender, the 3D software. 
- Respond with your answers in markdown (```).
- Preferably import entire modules instead of bits. 
- Do not perform destructive operations on the meshes. 
- Do not use cap_ends. Do not do more than what is asked (setting up render settings, adding cameras, etc).
- Do not respond with anything that is not Python code.

Example:

user: create 10 cubes in random locations from -10 to 10
assistant:
import bpy
import random
# how many cubes you want to add
count = 10
for _ in range(count):
    x = random.randint(-10, 10)
    y = random.randint(-10, 10)
    z = random.randint(-10, 10)
    bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
"""



class MessagePropertyGroup(PropertyGroup):
    type: StringProperty()
    content: StringProperty()

class ClaudeAddonPreferences(AddonPreferences):
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

class Claude_OT_DeleteMessage(Operator):
    bl_idname = "claude.delete_message"
    bl_label = "Delete Message"
    bl_options = {'REGISTER', 'UNDO'}

    message_index: IntProperty()

    def execute(self, context):
        context.scene.claude_chat_history.remove(self.message_index)
        return {'FINISHED'}

class Claude_OT_ShowCode(Operator):
    bl_idname = "claude.show_code"
    bl_label = "Show Code"
    bl_options = {'REGISTER', 'UNDO'}

    code: StringProperty(
        name="Code",
        description="The generated code",
        default="",
    )

    def execute(self, context):
        text_name = "Claude_Generated_Code.py"
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

class Claude_PT_Panel(Panel):
    bl_label = "Claude Blender Assistant"
    bl_idname = "CLAUDE_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Claude Assistant'

    def draw(self, context):
        layout = self.layout
        column = layout.column(align=True)

        column.label(text="Chat history:")
        box = column.box()
        for index, message in enumerate(context.scene.claude_chat_history):
            if message.type == 'assistant':
                row = box.row()
                row.label(text="Assistant: ")
                show_code_op = row.operator("claude.show_code", text="Show Code")
                show_code_op.code = message.content
                delete_message_op = row.operator("claude.delete_message", text="", icon="TRASH", emboss=False)
                delete_message_op.message_index = index
            else:
                row = box.row()
                row.label(text=f"User: {message.content}")
                delete_message_op = row.operator("claude.delete_message", text="", icon="TRASH", emboss=False)
                delete_message_op.message_index = index

        column.separator()
        
        column.label(text="Claude Model:")
        column.prop(context.scene, "claude_model", text="")

        column.label(text="Enter your message:")
        column.prop(context.scene, "claude_chat_input", text="")
        button_label = "Please wait...(this might take some time)" if context.scene.claude_button_pressed else "Execute"
        row = column.row(align=True)
        row.operator("claude.send_message", text=button_label)
        row.operator("claude.clear_chat", text="Clear Chat")

        column.separator()

class Claude_OT_ClearChat(Operator):
    bl_idname = "claude.clear_chat"
    bl_label = "Clear Chat"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.scene.claude_chat_history.clear()
        return {'FINISHED'}

class Claude_OT_Execute(Operator):
    bl_idname = "claude.send_message"
    bl_label = "Send Message"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        api_key = get_api_key(context, __name__)
        if not api_key:
            api_key = os.getenv("ANTHROPIC_API_KEY")

        if not api_key:
            self.report({'ERROR'}, "No API key detected. Please set the API key in the addon preferences.")
            return {'CANCELLED'}

        context.scene.claude_button_pressed = True
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        
        try:
            client = anthropic.Client(api_key=api_key)
            
            # Prepare chat history for context
            messages = []
            for msg in context.scene.claude_chat_history[-10:]:
                role = "assistant" if msg.type == "assistant" else "user"
                messages.append({"role": role, "content": msg.content})
                
            # Add current message
            messages.append({
                "role": "user",
                "content": f"{system_prompt}\n\nUser: {context.scene.claude_chat_input}"
            })
            
            # Get response from Claude
            response = client.messages.create(
                model=context.scene.claude_model,
                max_tokens=1500,
                messages=messages
            )
            
            blender_code = response.content[0].text
            # Extract code from between triple backticks
            code_match = re.findall(r'```(?:python)?(.*?)```', blender_code, re.DOTALL)
            if code_match:
                blender_code = code_match[0].strip()
            
            # Add messages to chat history
            message = context.scene.claude_chat_history.add()
            message.type = 'user'
            message.content = context.scene.claude_chat_input

            # Clear the chat input field
            context.scene.claude_chat_input = ""

            if blender_code:
                message = context.scene.claude_chat_history.add()
                message.type = 'assistant'
                message.content = blender_code

                global_namespace = globals().copy()
                
                try:
                    exec(blender_code, global_namespace)
                except Exception as e:
                    self.report({'ERROR'}, f"Error executing generated code: {e}")
                    context.scene.claude_button_pressed = False
                    return {'CANCELLED'}

        except Exception as e:
            self.report({'ERROR'}, f"Error with Claude API: {e}")
            context.scene.claude_button_pressed = False
            return {'CANCELLED'}

        context.scene.claude_button_pressed = False
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(Claude_OT_Execute.bl_idname)

def register():
    # Register classes
    bpy.utils.register_class(MessagePropertyGroup)
    bpy.utils.register_class(ClaudeAddonPreferences)
    bpy.utils.register_class(Claude_OT_Execute)
    bpy.utils.register_class(Claude_PT_Panel)
    bpy.utils.register_class(Claude_OT_ClearChat)
    bpy.utils.register_class(Claude_OT_ShowCode)
    bpy.utils.register_class(Claude_OT_DeleteMessage)

    # Register properties
    bpy.types.Scene.claude_model = EnumProperty(
        name="Claude Model",
        description="Select the Claude model to use",
        items=[
            ("claude-3-opus-20240229", "Claude 3 Opus (most capable)", "Use Claude 3 Opus"),
            ("claude-3-sonnet-20240229", "Claude 3 Sonnet (balanced)", "Use Claude 3 Sonnet"),
            ("claude-3-haiku-20240307", "Claude 3 Haiku (fastest)", "Use Claude 3 Haiku"),
        ],
        default="claude-3-opus-20240229"
    )
    
    bpy.types.Scene.claude_chat_input = StringProperty(
        name="Message",
        description="Enter your prompt",
        default=""
    )
    
    bpy.types.Scene.claude_chat_history = CollectionProperty(type=MessagePropertyGroup)
    bpy.types.Scene.claude_button_pressed = BoolProperty(default=False)
    
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)

def unregister():
    # Unregister classes
    bpy.utils.unregister_class(MessagePropertyGroup)
    bpy.utils.unregister_class(ClaudeAddonPreferences)
    bpy.utils.unregister_class(Claude_OT_Execute)
    bpy.utils.unregister_class(Claude_PT_Panel)
    bpy.utils.unregister_class(Claude_OT_ClearChat)
    bpy.utils.unregister_class(Claude_OT_ShowCode)
    bpy.utils.unregister_class(Claude_OT_DeleteMessage)

    # Remove properties
    del bpy.types.Scene.claude_model
    del bpy.types.Scene.claude_chat_input
    del bpy.types.Scene.claude_chat_history
    del bpy.types.Scene.claude_button_pressed
    
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)

if __name__ == "__main__":
    register()