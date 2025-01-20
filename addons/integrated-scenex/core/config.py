# File: BlenderClaude/core/config.py

"""Configuration management for BlenderClaude addon.

Handles loading of environment variables and addon configuration.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

class Config:
    """Configuration manager for BlenderClaude."""
    
    def __init__(self):
        self._load_env()
        
    def _load_env(self):
        """Load environment variables from .env file."""
        # Get addon directory
        addon_dir = Path(__file__).parent.parent
        env_path = addon_dir / '.env'
        
        # Create .env if it doesn't exist
        if not env_path.exists():
            self._create_default_env(env_path)
        
        # Load environment variables
        load_dotenv(env_path)
    
    def _create_default_env(self, env_path):
        """Create default .env file."""
        default_env = """# BlenderClaude Environment Configuration
CLAUDE_API_KEY=your_api_key_here
SCENEX_PATH=/path/to/scenex

# Scene Generation Settings
DEFAULT_SCENE_CONFIG={"grid_size": 10, "spacing": 2.0}
"""
        with open(env_path, 'w') as f:
            f.write(default_env)
    
    @property
    def api_key(self) -> str:
        """Get Claude API key."""
        return os.getenv('CLAUDE_API_KEY', '')
    
    @property
    def scenex_path(self) -> str:
        """Get SceneX installation path."""
        return os.getenv('SCENEX_PATH', '')
    
    @property
    def scene_config(self) -> dict:
        """Get default scene configuration."""
        import json
        config_str = os.getenv('DEFAULT_SCENE_CONFIG', '{}')
        return json.loads(config_str)

# Global configuration instance
config = Config()