# integrated-scenex/core/scene_generator.py

import bpy
from typing import Dict, Any
import anthropic
from .coordinate_system import ManimCoordinateSystem

class SceneGenerator:
    def __init__(self):
        self.coords = ManimCoordinateSystem()
        self.client = anthropic.Client()
        
    async def generate_from_prompt(self, prompt: str, mode: str = "direct") -> Dict[str, Any]:
        try:
            scene_data = await self._generate_scene_data(prompt, mode)
            scene = self.coords.apply_to_scene(scene_data)
            return {
                "success": True,
                "scene": scene
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def _generate_scene_data(self, prompt: str, mode: str) -> Dict[str, Any]:
        response = await self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=2000,
            messages=[{
                "role": "user",
                "content": f"Create a scene for: {prompt}"
            }]
        )
        return response.content[0].text