# SceneX/tests/example_scenes/17_template_tests.py


# Add parent directory to path to find SceneX package
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(script_dir))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)


from src.templates.technical import TechnicalDiagramScene
from src.templates.mathematical import MathematicalScene
from src.templates.educational import PresentationScene
from mathutils import Vector

class NetworkDiagram(TechnicalDiagramScene):
    def construct(self):
        # Create network components
        server = self.add_component("square", Vector((0, 2, 0)), "Server")
        client1 = self.add_component("circle", Vector((-2, 0, 0)), "Client 1")
        client2 = self.add_component("circle", Vector((2, 0, 0)), "Client 2")
        
        # Add connections
        self.connect_components(client1, server)
        self.connect_components(client2, server)
        
        # Animate
        self.animate_diagram()

class EquationDerivation(MathematicalScene):
    def construct(self):
        # Create equations
        eq1 = self.add_equation("E = mc^2", Vector((0, 2, 0)))
        eq2 = self.add_equation("F = ma", Vector((0, 0, 0)))
        eq3 = self.add_equation("PV = nRT", Vector((0, -2, 0)))
        
        # Animate
        self.animate_derivation()

class PhysicsLesson(PresentationScene):
    def construct(self):
        # Create slides
        self.add_slide("Newton's Laws", [
            "1. An object will remain at rest or in uniform motion unless acted upon by a force",
            "2. F = ma",
            "3. Every action has an equal and opposite reaction"
        ])
        
        self.add_slide("Conservation Laws", [
            "- Conservation of Energy",
            "- Conservation of Momentum",
            "- Conservation of Angular Momentum"
        ])
        
        # Animate presentation
        self.next_slide()

if __name__ == "__main__":
    # Test each template
    network = NetworkDiagram()
    network.construct()
    
    math = EquationDerivation()
    math.construct()
    
    lesson = PhysicsLesson()
    lesson.construct()