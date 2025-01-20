# SceneX Integration Architecture

## Background

The project integrates three independent systems:

1. **SceneX**: Manim-based animation system with precise coordinate system and animation API
2. **BlenderGenAI**: Natural language to Blender script generation using Claude AI
3. **AISceneGen**: Distributed scene generation system with React frontend and Redis queue

## Core Strengths to Preserve

### SceneX
- Precise coordinate system for object placement
- Animation API inspired by Manim
- Camera control system
- Scene templates for technical visualization

### BlenderGenAI
- Direct Blender script generation from natural language
- Integrated addon UI in Blender
- Flexible scene generation capability
- Claude AI integration

### AISceneGen 
- Distributed architecture using Redis
- Web-based interface
- Queue-based task processing
- Progress tracking and status updates

## Integration Architecture

### 1. Core Scene Generation Layer

```python
class SceneGenerator:
    """Core scene generation combining all systems"""
    def __init__(self):
        self.ai_processor = BlenderGenAIProcessor()
        self.manim_coords = SceneXCoordinateSystem()
        
    def generate_from_prompt(self, prompt: str, mode: str = "direct"):
        # Mode selection (direct script or SVG)
        scene_data = self._generate_scene_data(prompt, mode)
        
        # Apply SceneX coordinate system
        scene = self.manim_coords.apply_to_scene(scene_data)
        return scene
```

Handles:
- Script/SVG generation via BlenderGenAI
- Coordinate system application
- Scene data transformation

### 2. Processing Modes

#### Direct Mode (BlenderGenAI)
- Uses BlenderGenAI's existing script generation
- Preserves full Blender scripting capability
- Better for complex scenes and custom logic

#### SVG Mode (Claude)
- Generates scene layout as SVG
- Better for architectural diagrams
- Simpler but more constrained output

### 3. Deployment Options

#### Blender Addon
- Direct integration in Blender UI
- Immediate feedback
- Local processing

#### Distributed System
- Web interface from AISceneGen
- Redis queue for task management
- Progress tracking
- Better for batch processing

## Implementation Plan

### Phase 1: Core Integration
1. Create unified SceneGenerator class
2. Integrate SceneX coordinate system
3. Add SVG pipeline to BlenderGenAI

### Phase 2: Worker Updates
1. Update AISceneGen worker for unified generation
2. Add mode selection to task queue
3. Implement progress tracking

### Phase 3: UI Updates
1. Add SVG mode to BlenderGenAI panel
2. Update AISceneGen frontend for mode selection
3. Add preview capabilities

## API Examples

### Blender Addon
```python
# Direct mode
scene = api.process_addon_request(
    "Create a serverless API with Lambda and S3",
    mode="direct"
)

# SVG mode
scene = api.process_addon_request(
    "Create a network diagram",
    mode="svg"
)
```

### REST API
```python
# Queue task with mode selection
task_id = await api.process_api_request({
    "prompt": "Create cloud architecture",
    "mode": "svg",
    "options": {
        "coordinate_system": "manim",
        "template": "aws_architecture"
    }
})
```

## Folder Structure

```
integrated-scenex/
├── addons/
│   └── blendergenai/           # BlenderGenAI addon
│       ├── generators/
│       └── svg_pipeline/       # New SVG support
├── backend/                    # AISceneGen backend
│   ├── api/
│   └── worker/
├── frontend/                   # AISceneGen frontend
└── scenex/                     # Core SceneX library
    └── coordinate_system/
```

## Development Guidelines

1. **Preserving Capabilities**
   - Never break BlenderGenAI's script generation
   - Maintain SceneX's coordinate precision
   - Keep AISceneGen's distributed features

2. **Integration Points**
   - Use SceneX coordinates in all scene generation
   - Route all AI through BlenderGenAI's processor
   - Keep worker architecture from AISceneGen

3. **Testing**
   - Test both processing modes
   - Verify coordinate system accuracy
   - Check distributed processing
   
## Future Enhancements

1. **Enhanced SVG Pipeline**
   - Better layout algorithms
   - More architectural templates
   - Custom SVG components

2. **Extended Templates**
   - ML architecture diagrams
   - Network topology
   - Software architecture

3. **UI Improvements**
   - Live preview in web interface
   - Progress visualization
   - Template selection