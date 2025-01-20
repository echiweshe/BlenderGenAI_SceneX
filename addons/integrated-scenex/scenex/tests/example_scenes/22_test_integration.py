# src/ai/tests/test_integration.py
import asyncio
import bpy
from ..core.llm.claude_client import ClaudeClient
from ..core.generators.scene_generator import SceneGenerator
from ..backend.api.routes import generate_scene
from ...utils.logger import SceneXLogger

class IntegrationTest:
    def __init__(self):
        self.logger = SceneXLogger("IntegrationTest")
        self.claude = ClaudeClient()
        self.generator = SceneGenerator()

    async def test_basic_scene(self):
        """Test basic scene generation flow"""
        try:
            # Test prompt
            prompt = """Create a serverless ML inference API with:
            1. API Gateway for REST endpoint
            2. Lambda function for processing
            3. SageMaker endpoint for ML inference
            4. S3 bucket for storing results"""

            # 1. Test Claude processing
            self.logger.info("Testing Claude processing...")
            architecture = await self.claude.process_architecture(prompt)
            assert "components" in architecture, "Missing components in architecture"
            assert "connections" in architecture, "Missing connections in architecture"

            # 2. Test scene generation
            self.logger.info("Testing scene generation...")
            scene = self.generator.generate_scene(architecture)
            assert scene, "Failed to generate scene"

            # 3. Verify Blender objects
            self.logger.info("Verifying Blender objects...")
            for component in architecture["components"]:
                obj_name = f"{component['type']}_{component['name']}"
                obj = bpy.data.objects.get(obj_name)
                assert obj, f"Missing object: {obj_name}"

            # 4. Test connections
            self.logger.info("Verifying connections...")
            for connection in architecture["connections"]:
                from_obj = bpy.data.objects.get(f"{connection['from']}")
                to_obj = bpy.data.objects.get(f"{connection['to']}")
                assert from_obj and to_obj, "Missing connection objects"

            self.logger.info("All tests passed successfully!")
            return True

        except Exception as e:
            self.logger.error(f"Integration test failed: {str(e)}")
            return False

def run_tests():
    """Run all integration tests"""
    test = IntegrationTest()
    asyncio.run(test.test_basic_scene())

if __name__ == "__main__":
    run_tests()