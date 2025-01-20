import bpy
import os
import tempfile
import json
from datetime import datetime
from bpy.props import (StringProperty, FloatProperty, EnumProperty, 
                      CollectionProperty, BoolProperty, IntProperty)
from bpy.types import (PropertyGroup, Operator, AddonPreferences, 
                      Panel, UIList)

bl_info = {
    "name": "Advanced TTS",
    "description": "Advanced Text to Speech using Coqui TTS",
    "author": "Custom Script",
    "version": (1, 1, 0),
    "blender": (2, 80, 0),
    "location": "Sequence Editor > Side Panel > Advanced TTS",
    "warning": "",
    "doc_url": "",
    "category": "Sequencer",
    "support": "TESTING"
}

# Will be imported when TTS is actually used
TTS = None
MODELS = None

AVAILABLE_LANGUAGES = [
    ('en', 'English', ''),
    ('fr', 'French', ''),
    ('de', 'German', ''),
    ('es', 'Spanish', ''),
    ('it', 'Italian', ''),
    ('ja', 'Japanese', ''),
    ('ko', 'Korean', ''),
    ('zh', 'Chinese', ''),
]

EMOTIONS = [
    ('neutral', 'Neutral', ''),
    ('happy', 'Happy', ''),
    ('sad', 'Sad', ''),
    ('angry', 'Angry', ''),
    ('excited', 'Excited', ''),
]

def ensure_tts():
    """Ensure TTS is imported and available"""
    global TTS, MODELS
    if TTS is None:
        try:
            from TTS.api import TTS
            MODELS = TTS.list_models()
        except ImportError:
            raise ImportError("Please install TTS: pip install TTS")

def get_language_specific_models(self, context):
    """Get models specific to selected language"""
    ensure_tts()
    lang = context.scene.tts_settings.language
    return [(model, model.split("/")[-1], "") for model in MODELS if lang in model]

# Define base classes first
class TTSEntry(PropertyGroup):
    """Class for batch processing entries"""
    text: StringProperty(
        name="Text",
        description="Text to convert to speech",
        default=""
    )
    enabled: BoolProperty(
        name="Enable",
        description="Process this entry",
        default=True
    )
    emotion: EnumProperty(
        name="Emotion",
        items=EMOTIONS,
        default='neutral'
    )
    channel: IntProperty(
        name="Channel",
        default=1,
        min=1
    )

class TTSSettings(PropertyGroup):
    """Class for global TTS settings"""
    language: EnumProperty(
        name="Language",
        items=AVAILABLE_LANGUAGES,
        default='en'
    )
    entries: CollectionProperty(type=TTSEntry)
    active_entry_index: IntProperty()

class TTSPreferences(AddonPreferences):
    """Addon preferences"""
    bl_idname = __name__

    model_name: EnumProperty(
        name="TTS Model",
        description="Select TTS model to use",
        items=get_language_specific_models
    )
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "model_name")

# Then UI classes
class SEQUENCER_UL_tts_list(UIList):
    """Custom UI list for TTS entries"""
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.prop(item, "text", text="", emboss=False)
            layout.prop(item, "enabled", text="")
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.prop(item, "enabled", text="")

# Then operators
class SEQUENCER_OT_show_tts_help(Operator):
    """Show TTS Help"""
    bl_idname = "sequencer.show_tts_help"
    bl_label = "TTS Help"
    bl_description = "Show TTS addon documentation and examples"
    
    def draw(self, context):
        layout = self.layout
        layout.label(text="Advanced TTS Help", icon='QUESTION')
        
        box = layout.box()
        col = box.column()
        col.label(text="Basic Usage:", icon='PLAY')
        col.label(text="1. Add new entry with + button")
        col.label(text="2. Enter text and select emotion")
        col.label(text="3. Choose channel number")
        col.label(text="4. Click 'Create TTS Strip'")
        
        box = layout.box()
        col = box.column()
        col.label(text="Examples:", icon='FILE_TEXT')
        col.operator("sequencer.load_tts_example", text="Character Dialogue").example_type = 'dialogue'
        col.operator("sequencer.load_tts_example", text="Narration with Music").example_type = 'narration'
        col.operator("sequencer.load_tts_example", text="Multi-language Scene").example_type = 'multilang'
        col.operator("sequencer.load_tts_example", text="Batch Script Processing").example_type = 'batch'
        
    def execute(self, context):
        return context.window_manager.invoke_props_dialog(self, width=400)

class SEQUENCER_OT_tts_list_action(Operator):
    """Batch list actions"""
    bl_idname = "sequencer.tts_list_action"
    bl_label = "Batch List Actions"
    bl_description = "Add or remove items from the batch list"
    bl_options = {'REGISTER', 'UNDO'}
    
    action: EnumProperty(
        items=(
            ('ADD', "Add", "Add a new item"),
            ('REMOVE', "Remove", "Remove the selected item"),
            ('UP', "Up", "Move the selected item up"),
            ('DOWN', "Down", "Move the selected item down"),
        ),
        default='ADD'
    )

    def execute(self, context):
        settings = context.scene.tts_settings
        index = settings.active_entry_index

        if self.action == 'ADD':
            settings.entries.add()
        elif self.action == 'REMOVE':
            settings.entries.remove(index)
        elif self.action == 'UP' and index > 0:
            settings.entries.move(index, index - 1)
            settings.active_entry_index -= 1
        elif self.action == 'DOWN' and index < len(settings.entries) - 1:
            settings.entries.move(index, index + 1)
            settings.active_entry_index += 1

        return {'FINISHED'}

class SEQUENCER_OT_load_tts_example(Operator):
    """Load TTS Example"""
    bl_idname = "sequencer.load_tts_example"
    bl_label = "Load TTS Example"
    
    example_type: EnumProperty(
        items=[
            ('dialogue', "Character Dialogue", "Load character dialogue example"),
            ('narration', "Narration with Music", "Load narration with background music example"),
            ('multilang', "Multi-language Scene", "Load multi-language scene example"),
            ('batch', "Batch Processing", "Load batch script processing example")
        ]
    )
    
    def execute(self, context):
        settings = context.scene.tts_settings
        
        # Clear existing entries
        settings.entries.clear()
        
        if self.example_type == 'dialogue':
            dialogues = [
                ("Hello there! How are you today?", "happy", 1),
                ("I'm doing great, thanks for asking!", "excited", 2),
                ("Would you like to join me for coffee?", "neutral", 1),
                ("That sounds wonderful!", "happy", 2)
            ]
            for text, emotion, channel in dialogues:
                entry = settings.entries.add()
                entry.text = text
                entry.emotion = emotion
                entry.channel = channel
                
        elif self.example_type == 'narration':
            narration = [
                ("In a world far beyond our own...", "neutral", 1),
                ("Where magic and science intertwine...", "neutral", 1),
                ("A story begins to unfold...", "neutral", 1)
            ]
            for text, emotion, channel in narration:
                entry = settings.entries.add()
                entry.text = text
                entry.emotion = emotion
                entry.channel = channel
                
        elif self.example_type == 'multilang':
            multilang = [
                ("Hello, welcome to our presentation.", "neutral", 1),
                ("Bonjour, bienvenue à notre présentation.", "neutral", 2),
                ("Hola, bienvenidos a nuestra presentación.", "neutral", 3)
            ]
            for text, emotion, channel in multilang:
                entry = settings.entries.add()
                entry.text = text
                entry.emotion = emotion
                entry.channel = channel
                
        elif self.example_type == 'batch':
            script = """
            [Narrator]: Once upon a time...
            [Alice]: Hi, I'm Alice!
            [Bob]: Nice to meet you, Alice.
            [Narrator]: And so began their adventure...
            """.strip().split('\n')
            
            for line in script:
                if line.strip():
                    entry = settings.entries.add()
                    if '[Narrator]:' in line:
                        entry.text = line.split('[Narrator]:')[1].strip()
                        entry.emotion = 'neutral'
                        entry.channel = 1
                    elif '[Alice]:' in line:
                        entry.text = line.split('[Alice]:')[1].strip()
                        entry.emotion = 'happy'
                        entry.channel = 2
                    elif '[Bob]:' in line:
                        entry.text = line.split('[Bob]:')[1].strip()
                        entry.emotion = 'neutral'
                        entry.channel = 3
        
        self.report({'INFO'}, f"Loaded {self.example_type} example")
        return {'FINISHED'}

class SEQUENCER_OT_advanced_tts(Operator):
    """Create Advanced TTS Audio Strip"""
    bl_idname = "sequencer.advanced_tts_strip"
    bl_label = "Create TTS Strip"
    bl_description = "Create a new TTS audio strip"
    bl_options = {'REGISTER', 'UNDO'}

    speed: FloatProperty(
        name="Speed",
        description="Speech speed multiplier",
        default=1.0,
        min=0.5,
        max=2.0
    )

    pitch: FloatProperty(
        name="Pitch",
        description="Voice pitch adjustment",
        default=1.0,
        min=0.5,
        max=2.0
    )

    def execute(self, context):
        settings = context.scene.tts_settings
        frame_start = context.scene.frame_current
        
        for entry in settings.entries:
            if entry.enabled:
                try:
                    ensure_tts()
                    
                    prefs = context.preferences.addons[__name__].preferences
                    model_name = prefs.model_name
                    
                    tts = TTS(model_name)
                    
                    temp_dir = tempfile.gettempdir()
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    temp_file = os.path.join(temp_dir, f"tts_audio_{timestamp}.wav")
                    
                    emotion_settings = {
                        'happy': {'pitch': self.pitch * 1.1, 'speed': self.speed * 1.1},
                        'sad': {'pitch': self.pitch * 0.9, 'speed': self.speed * 0.9},
                        'angry': {'pitch': self.pitch * 1.2, 'speed': self.speed * 1.2},
                        'excited': {'pitch': self.pitch * 1.3, 'speed': self.speed * 1.15},
                        'neutral': {'pitch': self.pitch, 'speed': self.speed}
                    }
                    
                    settings = emotion_settings[entry.emotion]
                    
                    tts.tts_to_file(
                        text=entry.text,
                        file_path=temp_file,
                        speed=settings['speed']
                    )
                    
                    if not context.scene.sequence_editor:
                        context.scene.sequence_editor_create()
                    
                    sound_strip = context.scene.sequence_editor.sequences.new_sound(
                        name=f"TTS_{entry.emotion}_{timestamp}",
                        filepath=temp_file,
                        channel=entry.channel,
                        frame_start=frame_start
                    )
                    
                    frame_start += sound_strip.frame_final_duration + 24  # Add 1 second gap
                except Exception as e:
                    self.report({'ERROR'}, f"Error processing entry: {str(e)}")
                    return {'CANCELLED'}
        
        return {'FINISHED'}

class SEQUENCER_PT_advanced_tts(Panel):
    """Panel for Advanced TTS"""
    bl_label = "Advanced TTS"
    bl_idname = "SEQUENCER_PT_advanced_tts"
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Advanced TTS'

    def draw(self, context):
        layout = self.layout
        settings = context.scene.tts_settings

        # Help button at the top
        layout.operator("sequencer.show_tts_help", icon='QUESTION')
        
        layout.prop(settings, "language")

        row = layout.row()
        row.template_list("SEQUENCER_UL_tts_list", "tts_entries", settings,
                         "entries", settings, "active_entry_index")

        col = row.column(align=True)
        col.operator("sequencer.tts_list_action", icon='ADD', text="").action = 'ADD'
        col.operator("sequencer.tts_list_action", icon='REMOVE', text="").action = 'REMOVE'
        col.separator()
        col.operator("sequencer.tts_list_action", icon='TRIA_UP', text="").action = 'UP'
        col.operator("sequencer.tts_list_action", icon='TRIA_DOWN', text="").action = 'DOWN'

        if len(settings.entries) > 0 and settings.active_entry_index >= 0:
            entry = settings.entries[settings.active_entry_index]
            layout.prop(entry, "text")
            layout.prop(entry, "emotion")
            layout.prop(entry, "channel")
            layout.prop(entry, "enabled")

        layout.operator("sequencer.advanced_tts_strip")

# Final registration
classes = (
    TTSEntry,
    TTSSettings,
    TTSPreferences,
    SEQUENCER_UL_tts_list,
    SEQUENCER_OT_tts_list_action,
    SEQUENCER_OT_advanced_tts,
    SEQUENCER_OT_show_tts_help,
    SEQUENCER_OT_load_tts_example,
    SEQUENCER_PT_advanced_tts,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.tts_settings = bpy.props.PointerProperty(type=TTSSettings)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.tts_settings

if __name__ == "__main__":
    register()