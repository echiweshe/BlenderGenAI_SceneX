# SceneX/src/templates/educational.py

class PresentationScene(Scene):
    """Base class for educational presentations"""
    def __init__(self, title: str = "Presentation"):
        super().__init__()
        self.slides = []
        self.current_slide = 0

    def add_slide(self, title: str, content: list):
        """Add slide with title and content"""
        slide_group = Group(f"slide_{len(self.slides)}")
        
        # Create title
        title_text = Text(title, size=1.0).create()
        self.coordinate_system.place_object(title_text, Vector((0, 3, 0)))
        slide_group.add(title_text)
        
        # Add content
        layout = Layout()
        y_pos = 2
        for item in content:
            if isinstance(item, str):
                text = Text(item, size=0.6).create()
                self.coordinate_system.place_object(text, Vector((0, y_pos, 0)))
                slide_group.add(text)
            else:
                slide_group.add(item)
            y_pos -= 1
            
        self.slides.append(slide_group)
        return slide_group

    def next_slide(self):
        """Animate transition to next slide"""
        if self.current_slide < len(self.slides) - 1:
            # Fade out current slide
            current = self.slides[self.current_slide]
            config = AnimationConfig(duration=20)
            self.play(FadeOut(current.get_all_objects(), config=config))
            
            # Fade in next slide
            self.current_slide += 1
            next_slide = self.slides[self.current_slide]
            self.play(FadeInFrom(next_slide.get_all_objects(), Vector((1, 0, 0)), config=config))