# File: BlenderClaude/operators/svg_generation.py

"""SVG generation operators for BlenderClaude addon.

This module handles the generation of SVG content using Claude's AI capabilities
and converts them into Blender scenes using SceneX framework.
"""

import bpy
import os
import re
from bpy.types import Operator
from bpy.props import StringProperty, EnumProperty
import anthropic
from ..utilities import get_api_key
from ..core.XV1_svg_converter import SVGToSceneConverter
from ..core.prompts import SVG_SYSTEM_PROMPTS

class CLAUDE_OT_GenerateSVG(Operator):
    """Generate SVG content from natural language description using Claude."""
    
    bl_idname = "claude.generate_svg"
    bl_label = "Generate SVG"
    bl_options = {'REGISTER', 'UNDO'}

    # Scene type selection
    scene_type: EnumProperty(
        name="Scene Type",
        description="Type of scene to generate",
        items=[
            ('AWS', "AWS Architecture", "Create AWS architecture diagrams"),
            ('NETWORK', "Network Topology", "Create network topology diagrams"),
            ('AI', "AI/ML Pipeline", "Create AI/ML workflow diagrams"),
            ('CUSTOM', "Custom", "Create custom technical diagrams")
        ],
        default='AWS'
    )

    # Description input
    description: StringProperty(
        name="Description",
        description="Describe the scene you want to create",
        default="",
    )

    def invoke(self, context, event):
        """Show the scene generation dialog."""
        return context.window_manager.invoke_props_dialog(self, width=400)

    def draw(self, context):
        """Draw the operator's UI."""
        layout = self.layout
        layout.prop(self, "scene_type")
        layout.prop(self, "description", text="")
        layout.label(text="Example: Create a serverless API with Lambda and API Gateway")

    def execute(self, context):
        """Execute the SVG generation operation."""
        try:
            # Get API key
            api_key = get_api_key(context, __name__)
            if not api_key:
                api_key = os.getenv("ANTHROPIC_API_KEY")

            if not api_key:
                self.report({'ERROR'}, "No API key found. Please set in preferences.")
                return {'CANCELLED'}

            # Initialize Claude client
            client = anthropic.Client(api_key=api_key)

            # Get appropriate system prompt based on scene type
            system_prompt = SVG_SYSTEM_PROMPTS.get(
                self.scene_type,
                SVG_SYSTEM_PROMPTS['CUSTOM']
            )

            # Generate SVG using Claude
            response = client.messages.create(
                model=context.scene.claude_model,
                max_tokens=4000,
                messages=[{
                    "role": "user",
                    "content": (
                        f"{system_prompt}\n\n"
                        f"Create an SVG diagram for: {self.description}"
                    )
                }]
            )

            # Extract SVG code
            svg_code = response.content[0].text
            svg_match = re.findall(r'<svg.*?</svg>', svg_code, re.DOTALL)
            
            if not svg_match:
                self.report({'ERROR'}, "No SVG found in response")
                return {'CANCELLED'}

            svg_code = svg_match[0]

            # Convert SVG to scene
            converter = SVGToSceneConverter()
            scene_data = converter.convert(svg_code)

            # Create scene elements
            self._create_scene_elements(context, scene_data)

            # Store in text editor for reference
            self._store_svg_code(context, svg_code)

            # Update UI
            self._update_ui(context, svg_code)

            self.report({'INFO'}, "Scene generated successfully!")
            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"Error generating scene: {str(e)}")
            return {'CANCELLED'}

    def _create_scene_elements(self, context, scene_data):
        """Create Blender objects from scene data."""
        # Create empty parent for scene
        bpy.ops.object.empty_add(type='PLAIN_AXES')
        parent = context.active_object
        parent.name = "Generated_Scene"

        # Create objects based on scene data
        for element in scene_data['elements']:
            if element['type'] == 'component':
                self._create_component(element, parent)
            elif element['type'] == 'connection':
                self._create_connection(element, parent)

    def _create_component(self, element_data, parent):
        """Create a scene component."""
        # Component creation logic here
        pass

    def _create_connection(self, element_data, parent):
        """Create a connection between components."""
        # Connection creation logic here
        pass

    def _store_svg_code(self, context, svg_code):
        """Store SVG code in text editor."""
        text_name = "Generated_SVG.svg"
        text = bpy.data.texts.get(text_name)
        if text is None:
            text = bpy.data.texts.new(text_name)
        text.clear()
        text.write(svg_code)

    def _update_ui(self, context, svg_code):
        """Update UI with generated content."""
        # Add to chat history
        message = context.scene.claude_chat_history.add()
        message.type = 'user'
        message.content = self.description

        message = context.scene.claude_chat_history.add()
        message.type = 'assistant'
        message.content = svg_code

        # Clear input field
        context.scene.claude_chat_input = ""