# Grok Ortho Reference Generator

Blender add-on that uses the **xAI Grok Imagine API** to create perfect orthographic front & side view references for modeling.

https://github.com/James0384/grok-ortho-reference-generator-blender

## Features
- Generate front or side ortho views (or both with one click)
- Two modes:
  - **Image-to-image**: Upload existing model → perfect ortho conversion
  - **Text-to-image**: Describe object from scratch
- Debug mode (instant colored placeholders — no API calls)
- Clean sidebar panel in 3D View
- Auto-imports images as Image Empties in scene (correct rotation & scale)

## Requirements
- Blender 4.0+
- xAI API key (Grok Imagine access)

## Installation
1. Download ZIP from **Releases** (or clone repo)
2. Blender → Edit → Preferences → Add-ons → Install… → select `grok-ortho-reference-generator-blender.py` or the zip
3. Search "Grok Ortho" and enable

## Usage
1. Open 3D View sidebar (N key) → **Grok Optimizer** tab
2. (Optional) Paste xAI API key
3. Either:
   - Provide reference image path, or
   - Write object description
4. Click **Generate Front** / **Generate Side** / **Generate Both**

Images appear as reference planes in the scene.

## License
MIT License – feel free to use & modify.

## Future ideas
- Batch generation
- Control over style/edge detection
- Automatic alignment helper

Made by James Miller  
Portfolio: https://james03843.artstation.com  
Previous add-on: https://github.com/James0384/historical-scene-generator# grok-ortho-reference-generator-blender
Blender add-on that generates perfect front & side orthographic reference images using the xAI Grok Imagine API. Supports image-to-image (from existing model) and text-to-image generation. Ideal for hard-surface, character, or prop modeling workflows.
