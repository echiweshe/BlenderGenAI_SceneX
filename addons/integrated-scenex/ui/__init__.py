# integrated-scenex/ui/__init__.py

from . import operators
from . import panels
from . import properties

def register():
    operators.register()
    panels.register()
    properties.register()

def unregister():
    properties.unregister()
    panels.unregister()
    operators.unregister()