# File: /home/user/.config/blender/4.3/scripts/addons/BelnderGenAI/operators/claude_panel.py

"""SVG scene generation panel and operator.

Handles the UI panel and Claude integration for generating SVG-based scenes.
"""

import os
import bpy
import anthropic
from bpy.types import Operator, Panel
from bpy.props import StringProperty, EnumProperty
from ..core.svg_converter import SVGToSceneConverter


class CLAUDE_OT_GenerateSVG(Operator):
    """Generate SVG scene from natural language using Claude."""
    
    bl_idname = "claude.generate_svg"
    bl_label = "Generate Scene"
    bl_options = {'REGISTER', 'UNDO'}

    scene_type: EnumProperty(
        name="Scene Type",
        description="Type of scene to generate",
        items=[
            ('AWS', "AWS Architecture", "AWS architecture diagrams"),
            ('NETWORK', "Network Topology", "Network topology diagrams"),
            ('AI', "AI/ML Pipeline", "AI/ML workflow diagrams")
        ],
        default='AWS'
    )

    def execute(self, context):
        try:
            prompt = context.scene.claude_prompt
            api_key = os.getenv("ANTHROPIC_API_KEY")
            
            if not api_key:
                self.report({'ERROR'}, "Missing API key")
                return {'CANCELLED'}

            client = anthropic.Client(api_key=api_key)
            system_prompt = self._get_system_prompt()

            response = client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=4000,
                temperature=0,
                messages=[{
                    "role": "user", 
                    "content": f"Create an SVG diagram for: {prompt}"
                }],
                system=system_prompt
            )

            svg_content = response.content[0].text
            converter = SVGToSceneConverter()
            converter.convert(svg_content)

            self.report({'INFO'}, "Scene generated successfully")
            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}

    def _get_system_prompt(self):
        """Get system prompt for Claude."""
        return '''Generate SVG diagrams using AWS architectural components:
        - Use standard AWS symbols (64x64 rectangles) 
        - Position components logically with proper spacing
        - Create clear connections between components
        - Include text labels
        - Return only SVG XML without explanations'''


class CLAUDE_PT_Panel(Panel):
    """Panel for Claude scene generation."""
    
    bl_label = "Claude Scene Generator"
    bl_idname = "CLAUDE_PT_main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Claude"

    def draw(self, context):
        layout = self.layout
        
        # Scene type selector
        row = layout.row()
        row.prop(context.scene, "scene_type")
        
        # Multi-line text input
        box = layout.box()
        col = box.column()
        col.scale_y = 3.0
        col.prop(
            context.scene,
            "claude_prompt",
            text="",
            options={'TEXTEDIT_UPDATE'}
        )
        
        # Generate button
        layout.operator("claude.generate_svg")


def register():
    bpy.types.Scene.claude_prompt = StringProperty(
        name="Description",
        description="Describe the scene to generate",
        default="",
        maxlen=1024,
        options={'TEXTEDIT_UPDATE'}
    )
    
    bpy.types.Scene.scene_type = EnumProperty(
        name="Type",
        description="Type of scene to generate",
        items=[
            ('AWS', "AWS Architecture", "AWS architecture diagrams"),
            ('NETWORK', "Network Topology", "Network topology diagrams"),
            ('AI', "AI/ML Pipeline", "AI/ML workflow diagrams")
        ],
        default='AWS'
    )

    bpy.utils.register_class(CLAUDE_OT_GenerateSVG)
    bpy.utils.register_class(CLAUDE_PT_Panel)


def unregister():
    bpy.utils.unregister_class(CLAUDE_OT_GenerateSVG)
    bpy.utils.unregister_class(CLAUDE_PT_Panel)
    
    del bpy.types.Scene.claude_prompt
    del bpy.types.Scene.scene_type
