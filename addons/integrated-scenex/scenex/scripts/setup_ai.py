import os
import json
import shutil
from pathlib import Path
from typing import Dict, Any

class SceneXAISetup:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.ai_path = self.base_path / "src" / "ai"

    def setup_directory(self):
        """Create the complete AI directory structure"""
        try:
            # Create main directories
            directories = [
                "frontend/src/components",
                "frontend/src/hooks",
                "frontend/src/styles",
                "backend/api",
                "backend/services",
                "backend/utils",
                "core/generators",
                "core/processors",
                "core/models",
                "core/llm",
                "data/components",
                "data/presets",
                "data/relationships",
                "config",
                "tests"
            ]

            # Create all directories
            for dir_path in directories:
                full_path = self.ai_path / dir_path
                full_path.mkdir(parents=True, exist_ok=True)
                # Create __init__.py for Python packages
                if not dir_path.startswith("frontend"):
                    init_file = full_path / "__init__.py"
                    init_file.touch()

            # Create and populate files
            self._create_frontend_files()
            self._create_backend_files()
            self._create_core_files()
            self._create_data_files()
            self._create_config_files()
            self._create_test_files()

            print("SceneX AI directory structure created successfully!")

        except Exception as e:
            print(f"Error creating directory structure: {str(e)}")
            raise

    def _write_file(self, path: Path, content: str):
        """Write content to file, creating directories if needed"""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')

    def _create_frontend_files(self):
        """Create frontend configuration and component files"""
        # package.json
        package_json = {
            "name": "scenex-ai-frontend",
            "private": True,
            "version": "0.1.0",
            "type": "module",
            "scripts": {
                "dev": "vite",
                "build": "tsc && vite build",
                "preview": "vite preview"
            },
            "dependencies": {
                "@radix-ui/react-alert-dialog": "^1.0.5",
                "@radix-ui/react-slot": "^1.0.2",
                "class-variance-authority": "^0.7.0",
                "clsx": "^2.0.0",
                "lucide-react": "^0.263.1",
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "tailwind-merge": "^2.0.0",
                "tailwindcss-animate": "^1.0.7"
            },
            "devDependencies": {
                "@types/node": "^20.8.2",
                "@types/react": "^18.2.25",
                "@types/react-dom": "^18.2.10",
                "@vitejs/plugin-react": "^4.1.0",
                "autoprefixer": "^10.4.16",
                "postcss": "^8.4.31",
                "tailwindcss": "^3.3.3",
                "typescript": "^5.2.2",
                "vite": "^4.4.11"
            }
        }
        
        package_json_path = self.ai_path / "frontend" / "package.json"
        self._write_file(package_json_path, json.dumps(package_json, indent=2))

        # Create other frontend files
        frontend_files = {
            "vite.config.js": '''
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})''',
            "tsconfig.json": '''
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}''',
            "src/styles/globals.css": '''
@tailwind base;
@tailwind components;
@tailwind utilities;
 
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
  }
}
 
@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground;
  }
}''',
            "src/components/AISceneGenerator.tsx": '''
import React, { useState } from 'react';
import { Send, Loader2 } from 'lucide-react';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';

const AISceneGenerator = () => {
  const [loading, setLoading] = useState(false);
  const [prompt, setPrompt] = useState('');

  const handleSubmit = async () => {
    setLoading(true);
    try {
      // Call backend API
      const response = await fetch('/api/generate-scene', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt })
      });
      
      const data = await response.json();
      // Handle response
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="w-full max-w-4xl mx-auto">
      <CardHeader>
        <CardTitle>AI Scene Generator</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          className="w-full h-32 p-2 border rounded-lg"
          placeholder="Describe your scene..."
        />
        <button
          onClick={handleSubmit}
          disabled={loading}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg"
        >
          {loading ? <Loader2 className="animate-spin" /> : <Send />}
          Generate Scene
        </button>
      </CardContent>
    </Card>
  );
};

export default AISceneGenerator;'''
        }

        for file_path, content in frontend_files.items():
            full_path = self.ai_path / "frontend" / file_path
            self._write_file(full_path, content.strip())

    def _create_backend_files(self):
        """Create backend API and service files"""
        backend_files = {
            "api/routes.py": '''
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
from ..core.processors.prompt_processor import PromptProcessor
from ..core.generators.scene_generator import SceneGenerator
from ...utils.logger import SceneXLogger

app = FastAPI()
logger = SceneXLogger("SceneXAPI")

class SceneRequest(BaseModel):
    prompt: str
    options: Optional[Dict] = None

@app.post("/api/generate-scene")
async def generate_scene(request: SceneRequest):
    try:
        processor = PromptProcessor()
        scene_data = processor.process_prompt(request.prompt)
        
        generator = SceneGenerator()
        scene = generator.generate_scene(scene_data)
        
        return {"status": "success", "data": scene}
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
'''
        }

        for file_path, content in backend_files.items():
            full_path = self.ai_path / "backend" / file_path
            self._write_file(full_path, content.strip())

    def _create_core_files(self):
        """Create core functionality files"""
        core_files = {
            "llm/claude_client.py": '''
import anthropic
from typing import Dict
from ...utils.logger import SceneXLogger

class ClaudeClient:
    def __init__(self):
        self.client = anthropic.Client()
        self.logger = SceneXLogger("ClaudeClient")
    
    async def process_architecture(self, prompt: str) -> Dict:
        try:
            response = await self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            return self._parse_response(response.content)
        except Exception as e:
            self.logger.error(f"Claude error: {str(e)}")
            raise
''',
            "generators/scene_generator.py": '''
import bpy
from typing import Dict
from ...utils.logger import SceneXLogger

class SceneGenerator:
    def __init__(self):
        self.logger = SceneXLogger("SceneGenerator")
    
    def generate_scene(self, scene_data: Dict):
        try:
            # Create scene elements
            for component in scene_data["components"]:
                self._create_component(component)
                
            return {"status": "success"}
        except Exception as e:
            self.logger.error(f"Error: {str(e)}")
            raise
'''
        }

        for file_path, content in core_files.items():
            full_path = self.ai_path / "core" / file_path
            self._write_file(full_path, content.strip())

    def _create_data_files(self):
        """Create data definition files"""
        data_files = {
            "components/aws_components.py": '''
AWS_COMPONENTS = {
    "lambda": {
        "shape": "Rectangle",
        "color": (0.9, 0.5, 0.1, 1.0),
        "label": "Lambda",
        "category": "compute"
    },
    "s3": {
        "shape": "Square",
        "color": (0.5, 0.2, 0.9, 1.0),
        "label": "S3",
        "category": "storage"
    }
}'''
        }

        for file_path, content in data_files.items():
            full_path = self.ai_path / "data" / file_path
            self._write_file(full_path, content.strip())

    def _create_config_files(self):
        """Create configuration files"""
        config_files = {
            "settings.py": '''
# API Configuration
CLAUDE_API_KEY = "your_api_key_here"
API_ENDPOINT = "http://localhost:8000"

# Scene Generation Settings
DEFAULT_SCENE_CONFIG = {
    "grid_size": 10,
    "spacing": 2.0,
    "animation_duration": 30
}'''
        }

        for file_path, content in config_files.items():
            full_path = self.ai_path / "config" / file_path
            self._write_file(full_path, content.strip())

    def _create_test_files(self):
        """Create test files"""
        test_files = {
            "test_integration.py": '''
import asyncio
import unittest
from ..core.llm.claude_client import ClaudeClient
from ..core.generators.scene_generator import SceneGenerator

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.claude = ClaudeClient()
        self.generator = SceneGenerator()
    
    async def test_basic_scene(self):
        prompt = "Create a serverless API with Lambda and API Gateway"
        architecture = await self.claude.process_architecture(prompt)
        self.assertIn("components", architecture)
        
        scene = self.generator.generate_scene(architecture)
        self.assertIsNotNone(scene)

if __name__ == '__main__':
    unittest.main()'''
        }

        for file_path, content in test_files.items():
            full_path = self.ai_path / "tests" / file_path
            self._write_file(full_path, content.strip())


# Usage
if __name__ == "__main__":
    # Get the path to the Blender addons directory
    blender_addons_path = os.path.expanduser("~\\AppData\\Roaming\\Blender Foundation\\Blender\\4.2\\scripts\\addons\\SceneX")
    
    try:
        setup = SceneXAISetup(blender_addons_path)
        setup.setup_directory()
    except Exception as e:
        print(f"Setup failed: {str(e)}")
