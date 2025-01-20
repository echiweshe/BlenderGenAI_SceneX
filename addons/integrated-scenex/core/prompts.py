# File: BlenderClaude/core/prompts.py

"""System prompts for SVG generation using Claude.

Contains specialized prompts for different types of technical diagrams.
"""

SVG_SYSTEM_PROMPTS = {
    'AWS': """You are an expert at creating AWS architecture diagrams.
Create a precise SVG diagram following these guidelines:
- Use standard AWS architecture symbols
- Maintain consistent sizing (64x64 for service icons)
- Create logical data flow connections
- Include clear service labels
- Use AWS color scheme
- Organize in logical tiers (frontend, backend, storage)
- Include arrows showing data flow direction
""",

    'NETWORK': """You are an expert at creating network topology diagrams.
Create a precise SVG diagram following these guidelines:
- Use standard network symbols (routers, switches, firewalls)
- Show network segmentation
- Include proper IP addressing zones
- Show security boundaries
- Use consistent connection types
- Label network segments
- Include protocol indicators where relevant
""",

    'AI': """You are an expert at creating AI/ML pipeline diagrams.
Create a precise SVG diagram following these guidelines:
- Show data flow through ML pipeline
- Include data preprocessing steps
- Show model training components
- Include evaluation metrics
- Show deployment pipeline
- Use consistent ML symbols
- Label key components and transformations
""",

    'CUSTOM': """You are an expert at creating technical diagrams.
Create a precise SVG diagram following these guidelines:
- Use clear, consistent symbols
- Show logical flow and relationships
- Include appropriate labels
- Maintain proper spacing
- Use a clear visual hierarchy
- Include directional indicators where needed
"""
}

# Common SVG styling to be applied to all diagrams
SVG_STYLE_TEMPLATE = """
<defs>
    <style type="text/css">
        .component { fill: #f8f9fa; stroke: #495057; stroke-width: 2; }
        .label { font-family: Arial; font-size: 12px; fill: #212529; }
        .connection { stroke: #adb5bd; stroke-width: 2; fill: none; }
        .arrow { fill: #adb5bd; }
    </style>
</defs>
"""

# Example snippets for common components
SVG_COMPONENT_TEMPLATES = {
    'service': '''
    <g class="service-component">
        <rect x="0" y="0" width="64" height="64" class="component"/>
        <text x="32" y="80" class="label" text-anchor="middle">{label}</text>
    </g>
    ''',
    
    'connection': '''
    <g class="connection">
        <path d="M {start_x},{start_y} {end_x},{end_y}" class="connection"/>
        <polygon points="{arrow_points}" class="arrow"/>
    </g>
    '''
}