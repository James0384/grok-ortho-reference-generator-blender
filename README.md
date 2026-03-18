# Grok Ortho Reference Generator

Blender add-on that generates perfect front & side orthographic reference images using the xAI Grok Imagine API. Supports image-to-image (upload existing model) and text-to-image generation. Ideal for hard-surface, character, or prop modeling workflows.

GitHub: https://github.com/James0384/grok-ortho-reference-generator-blender

## Features
- One-click front or side ortho generation (or both)
- Image-to-image mode preserves exact proportions/details
- Text-to-image mode for quick concept references
- Debug mode with instant colored placeholders (no API cost)
- Auto-imports as correctly rotated Image Empties
- Clean sidebar panel in 3D View

## Requirements
- Blender 4.0+
- xAI API key (Grok Imagine access)

## Installation
1. Download the ZIP or clone the repo
2. Blender → Edit → Preferences → Add-ons → Install… → select the zip or `grok-ortho-reference-generator-blender.py`
3. Enable "Grok Ortho Generator"

## Usage
1. N-key sidebar → Grok Optimizer tab
2. (Optional) paste xAI API key
3. Add object description or reference image path
4. Click Generate Front / Side / Both

References appear instantly in the scene.

## Portfolio Context
Professional 3D Production Artist (Star Spangled Adventures — 39 episodes shipped). This tool demonstrates real-time API integration, bpy scripting, and UI development for production pipelines. Built as a direct extension of my procedural and synthetic-data work.

Made by James Miller  
ArtStation: https://james03843.artstation.com  
Previous add-on: https://github.com/James0384/historical-scene-generator
