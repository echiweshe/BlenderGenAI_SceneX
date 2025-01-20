import bpy
import anthropic
import re
import os
import sys

# def get_api_key(context, addon_name):
#     preferences = context.preferences
#     addon_prefs = preferences.addons[addon_name].preferences
#     return addon_prefs.api_key

# def init_props():
#     bpy.types.Scene.claude_chat_history = bpy.props.CollectionProperty(type=bpy.types.PropertyGroup)
#     bpy.types.Scene.claude_model = bpy.props.EnumProperty(
#         name="Claude Model",
#         description="Select the Claude model to use",
#         items=[
#             ("claude-3-opus-20240229", "Claude 3 Opus (most capable)", "Use Claude 3 Opus"),
#             ("claude-3-sonnet-20240229", "Claude 3 Sonnet (balanced)", "Use Claude 3 Sonnet"),
#             ("claude-3-haiku-20240307", "Claude 3 Haiku (fastest)", "Use Claude 3 Haiku"),
#         ],
#         default="claude-3-opus-20240229",
#     )
#     bpy.types.Scene.claude_chat_input = bpy.props.StringProperty(
#         name="Message",
#         description="Enter your message",
#         default="",
#     )
#     bpy.types.Scene.claude_button_pressed = bpy.props.BoolProperty(default=False)
#     bpy.types.PropertyGroup.type = bpy.props.StringProperty()
#     bpy.types.PropertyGroup.content = bpy.props.StringProperty()

# /BlenderGPT-main/utilities.py
import bpy
from pathlib import Path


def get_api_key(context, addon_name):
    """Get the API key from the addon preferences."""
    preferences = context.preferences
    addon_prefs = preferences.addons[addon_name].preferences
    return addon_prefs.api_key

def split_area_to_text_editor(context):
    """Split the current area and change one of them to a text editor."""
    area = context.area
    for region in area.regions:
        if region.type == 'WINDOW':
            override = {'area': area, 'region': region}
            bpy.ops.screen.area_split(override, direction='VERTICAL', factor=0.5)
            break

    new_area = context.screen.areas[-1]
    new_area.type = 'TEXT_EDITOR'
    return new_area

def init_props():
    """Initialize the property group for chat messages."""
    bpy.types.PropertyGroup.type = bpy.props.StringProperty()
    bpy.types.PropertyGroup.content = bpy.props.StringProperty()

def clear_props():
    del bpy.types.Scene.claude_chat_history
    del bpy.types.Scene.claude_chat_input
    del bpy.types.Scene.claude_button_pressed

def generate_blender_code(prompt, chat_history, context, system_prompt):
    client = anthropic.Client(api_key=get_api_key(context, "your_addon_name"))
    
    messages = [{"role": "system", "content": system_prompt}]
    for message in chat_history[-10:]:
        if message.type == "assistant":
            messages.append({"role": "assistant", "content": "```\n" + message.content + "\n```"})
        else:
            messages.append({"role": message.type.lower(), "content": message.content})

    # Convert messages to Anthropic's format
    formatted_messages = []
    for msg in messages:
        if msg["role"] == "system":
            formatted_messages.append({"role": "assistant", "content": f"System: {msg['content']}"})
        else:
            formatted_messages.append(msg)

    # Add the current user message
    formatted_messages.append({
        "role": "user", 
        "content": "Can you please write Blender code for me that accomplishes the following task: " + prompt + "? \n. Do not respond with anything that is not Python code. Do not provide explanations"
    })

    try:
        # Create a streaming response
        with client.messages.stream(
            model=context.scene.claude_model,
            max_tokens=1500,
            messages=formatted_messages,
        ) as stream:
            completion_text = ''
            for text in stream.text_stream:
                completion_text += text
                print(completion_text, flush=True, end='\r')

        # Extract code from between triple backticks
        completion_text = re.findall(r'```(.*?)```', completion_text, re.DOTALL)[0]
        completion_text = re.sub(r'^python', '', completion_text, flags=re.MULTILINE)
        
        return completion_text
    except Exception as e:
        print(f"Error generating code: {e}")
        return None

def split_area_to_text_editor(context):
    area = context.area
    for region in area.regions:
        if region.type == 'WINDOW':
            override = {'area': area, 'region': region}
            bpy.ops.screen.area_split(override, direction='VERTICAL', factor=0.5)
            break

    new_area = context.screen.areas[-1]
    new_area.type = 'TEXT_EDITOR'
    return new_area