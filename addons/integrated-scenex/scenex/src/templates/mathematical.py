# SceneX/src/templates/mathematical.py

class MathematicalScene(Scene):
    """Base class for mathematical animations"""
    def __init__(self):
        super().__init__()
        self.equations = []
        self.graphs = []

    def add_equation(self, tex: str, position: Vector):
        """Add LaTeX equation"""
        equation = LaTeXText(tex, size=0.8).create()
        self.coordinate_system.place_object(equation, position)
        self.equations.append(equation)
        return equation

    def add_graph(self, func, x_range=(-5, 5), position: Vector = Vector((0, 0, 0))):
        """Add mathematical graph"""
        pass  # Implement graphing functionality

    def animate_derivation(self):
        """Animate mathematical derivation"""
        config = AnimationConfig(duration=30)
        
        for equation in self.equations:
            self.play(Write(equation, config=config))