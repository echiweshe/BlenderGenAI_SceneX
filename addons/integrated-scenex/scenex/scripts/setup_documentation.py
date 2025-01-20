# SceneX/scripts/setup_documentation.py

import os
from pathlib import Path

def create_structure():
    """Create documentation directory structure"""
    base_dir = Path("docs")
    
    # Create main directories
    directories = [
        base_dir,
        base_dir / "tutorials",
        base_dir / "reference",
        base_dir / "examples"
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

def write_file(path: Path, content: str):
    """Write content to file"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def setup_documentation():
    """Setup all documentation files"""
    create_structure()
    
    # Main README
    readme_content = '''# SceneX Documentation

SceneX is a Blender animation framework inspired by Manim, designed for creating educational and technical animations. 

## Table of Contents

1. [Quick Start](quickstart.md)
2. Tutorials
   - [Creating Your First Scene](tutorials/basic_scene.md)
   - [Working with Animations](tutorials/animations.md)
   - [Geometric Shapes](tutorials/shapes.md)
   - [Camera Control](tutorials/camera.md)
3. API Reference
   - [Geometry System](reference/geometry.md)
   - [Animation System](reference/animations.md)
   - [Camera System](reference/camera.md)
   - [Scene Management](reference/scene.md)
4. Examples
   - [Technical Diagrams](examples/technical.md)
   - [Mathematical Animations](examples/mathematical.md)
   - [Educational Presentations](examples/educational.md)
5. [Contributing](contributing.md)

[Rest of README content...]'''

    # Quick Start
    quickstart_content = '''# Quick Start Guide

## Installation

[Installation instructions...]

## Your First Scene

```python
[Basic scene example...]
```

## Core Concepts

[Core concepts explanation...]'''

    # Tutorial content
    tutorial_files = {
        'basic_scene.md': '''# Creating Your First Scene

## Scene Setup

[Scene setup instructions...]

## Basic Objects

[Working with objects...]

## Simple Animations

[Basic animation examples...]''',
        
        'animations.md': '''# Working with Animations

## Animation Types

[Animation types explanation...]

## Creating Custom Animations

[Custom animation guide...]''',
        
        'shapes.md': '''# Geometric Shapes

## Basic Shapes

[Basic shapes documentation...]

## Complex Shapes

[Complex shapes guide...]''',
        
        'camera.md': '''# Camera Control

## Camera Setup

[Camera setup guide...]

## Camera Movements

[Camera movement examples...]'''
    }

    # Reference content
    reference_files = {
        'geometry.md': '''# Geometry System Reference

## Classes

[Class documentation...]

## Methods

[Method documentation...]''',
        
        'animations.md': '''# Animation System Reference

## Animation Base Class

[Base class documentation...]

## Animation Types

[Animation types reference...]''',
        
        'camera.md': '''# Camera System Reference

## Camera Configuration

[Configuration documentation...]

## Camera Methods

[Method documentation...]''',
        
        'scene.md': '''# Scene Management Reference

## Scene Class

[Scene class documentation...]

## Scene Methods

[Method documentation...]'''
    }

    # Example content
    example_files = {
        'technical.md': '''# Technical Diagram Examples

## Basic Diagrams

[Basic diagram examples...]

## Complex Systems

[Complex system examples...]''',
        
        'mathematical.md': '''# Mathematical Animation Examples

## Equation Animations

[Equation animation examples...]

## Graph Animations

[Graph animation examples...]''',
        
        'educational.md': '''# Educational Presentation Examples

## Lecture Slides

[Lecture slide examples...]

## Interactive Demonstrations

[Interactive demo examples...]'''
    }

    # Write main files
    write_file(Path("docs/README.md"), readme_content)
    write_file(Path("docs/quickstart.md"), quickstart_content)
    write_file(Path("docs/contributing.md"), '''# Contributing Guide

[Contributing guidelines...]''')

    # Write tutorial files
    for filename, content in tutorial_files.items():
        write_file(Path("docs/tutorials") / filename, content)

    # Write reference files
    for filename, content in reference_files.items():
        write_file(Path("docs/reference") / filename, content)

    # Write example files
    for filename, content in example_files.items():
        write_file(Path("docs/examples") / filename, content)

if __name__ == "__main__":
    setup_documentation()
    print("Documentation structure created successfully!")