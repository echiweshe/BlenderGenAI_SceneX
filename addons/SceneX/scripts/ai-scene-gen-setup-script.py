import os
import subprocess
from pathlib import Path

def create_directory_structure():
    """Create the project directory structure"""
    base_dir = Path.home() / "Documents" / "src" / "AISceneGen"
    
    # Create main directories
    directories = [
        base_dir / "frontend" / "src" / "components",
        base_dir / "frontend" / "src" / "hooks",
        base_dir / "backend" / "app" / "api",
        base_dir / "backend" / "app" / "core",
        base_dir / "worker"
    ]
    
    for dir_path in directories:
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {dir_path}")

def create_frontend():
    """Initialize frontend with Vite and React"""
    base_dir = Path.home() / "Documents" / "src" / "AISceneGen" / "frontend"
    
    # Create package.json
    subprocess.run(["npm", "create", "vite@latest", ".", "--", "--template", "react-ts"], 
                  cwd=str(base_dir))
    
    # Install dependencies
    subprocess.run(["npm", "install"], cwd=str(base_dir))
    
    # Install additional dependencies
    additional_deps = [
        "tailwindcss",
        "postcss",
        "autoprefixer",
        "lucide-react",
        "@radix-ui/react-alert-dialog",
        "@radix-ui/react-slot"
    ]
    subprocess.run(["npm", "install", "--save"] + additional_deps, cwd=str(base_dir))

def create_backend():
    """Initialize backend with FastAPI"""
    base_dir = Path.home() / "Documents" / "src" / "AISceneGen" / "backend"
    
    # Create requirements.txt
    requirements = """
fastapi==0.104.1
uvicorn==0.24.0
python-dotenv==1.0.0
redis==5.0.1
pydantic==2.4.2
python-multipart==0.0.6
httpx==0.25.1
anthropic==0.5.0
    """.strip()
    
    with open(base_dir / "requirements.txt", "w") as f:
        f.write(requirements)
    
    # Create .env file
    env_content = """
REDIS_URL=redis://localhost:6379
CLAUDE_API_KEY=your_api_key_here
SCENEX_ADDON_PATH=/path/to/scenex/addon
    """.strip()
    
    with open(base_dir / ".env", "w") as f:
        f.write(env_content)

def main():
    """Set up the complete project"""
    print("Setting up AISceneGen project...")
    
    create_directory_structure()
    create_frontend()
    create_backend()
    
    print("\nProject setup complete!")
    print("\nNext steps:")
    print("1. cd ~/Documents/src/AISceneGen/backend")
    print("2. python -m venv venv")
    print("3. source venv/bin/activate  # or .\\venv\\Scripts\\activate on Windows")
    print("4. pip install -r requirements.txt")
    print("\n5. cd ../frontend")
    print("6. npm install")
    print("7. Update .env with your settings")
    print("\n8. Start Redis server")
    print("9. Start backend: uvicorn app.main:app --reload")
    print("10. Start frontend: npm run dev")

if __name__ == "__main__":
    main()