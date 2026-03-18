bl_info = {
    "name": "Grok-Integrated Scene Optimizer",
    "author": "James Miller",
    "version": (0, 16),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Grok Optimizer",
    "description": "Generate front/side ortho references using official Grok Imagine API",
    "category": "3D View",
}

import bpy
import os
import requests
import base64
from bpy.types import Operator, Panel, PropertyGroup
from bpy.props import StringProperty, BoolProperty

# ====================== DEBUG PLACEHOLDER ======================
def create_placeholder_image(view_type):
    temp_dir = bpy.app.tempdir
    path = os.path.join(temp_dir, f"{view_type}_ortho.png")
    color = (1.0, 0.0, 0.0, 1.0) if view_type == "front" else (0.0, 0.0, 1.0, 1.0)
    img = bpy.data.images.new(f"{view_type}_placeholder", 1024, 1024)
    img.pixels[:] = [color[i % 4] for i in range(1024 * 1024 * 4)]
    img.filepath_raw = path
    img.save()
    return path

# ====================== IMAGE GENERATION ======================
def generate_ortho_image(prompt, api_key, image_path=None, view_type="front", debug_mode=True):
    print(f"[GROK-OPT] Generating {view_type} view | debug={debug_mode}")

    if debug_mode:
        print("[DEBUG MODE] Creating colored placeholder")
        return create_placeholder_image(view_type)

    if not api_key:
        raise ValueError("xAI API key required")

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    has_reference = image_path and os.path.exists(image_path)

    # Simplified prompt logic
    if has_reference:
        base_prompt = (
            "Use the provided image exactly as the subject. "
            "Preserve all details, proportions, shapes, colors and features without any changes. "
            f"Convert it to a perfect {view_type} orthographic view. "
            "Technical illustration, perfectly flat, no perspective, clean white background, high resolution, centered."
        )
        # If user provided extra description, append it
        if prompt.strip():
            base_prompt += f" Additional description: {prompt}."
    else:
        if not prompt.strip():
            raise ValueError("Object description required when no reference image is provided")
        base_prompt = (
            f"{prompt}, perfect {view_type} orthographic view, "
            "technical illustration style, detailed, high resolution, clean background, centered subject"
        )

    full_prompt = base_prompt

    print("=== FULL PROMPT BEING SENT ===")
    print(full_prompt)
    print("==============================")

    if has_reference:
        # Image-to-Image: /edits endpoint
        endpoint = "https://api.x.ai/v1/images/edits"
        with open(image_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode('utf-8')
        payload = {
            "model": "grok-imagine-image",
            "prompt": full_prompt,
            "image": {
                "url": f"data:image/png;base64,{b64}"
            },
            "response_format": "url"
        }
    else:
        # Text-to-Image: /generations
        endpoint = "https://api.x.ai/v1/images/generations"
        payload = {
            "model": "grok-imagine-image",
            "prompt": full_prompt,
            "n": 1,
            "width": 1024,
            "height": 1024,
            "response_format": "url"
        }

    response = requests.post(endpoint, json=payload, headers=headers, timeout=60)
    response.raise_for_status()

    image_url = response.json()["data"][0]["url"]
    local_path = os.path.join(bpy.app.tempdir, f"{view_type}_ortho_{os.urandom(4).hex()}.png")
    with open(local_path, 'wb') as f:
        f.write(requests.get(image_url).content)

    print(f"[SUCCESS] Saved to {local_path}")
    return local_path

# ====================== OPERATORS ======================
class SCENE_OT_generate_view(Operator):
    bl_idname = "scene.generate_view"
    bl_label = "Generate View"
    view_type: StringProperty()

    def execute(self, context):
        props = context.scene.grok_optimizer_props
        if not self.view_type:
            self.view_type = "front"

        print(f"[BUTTON] {self.bl_label} pressed → view_type = '{self.view_type}'")

        try:
            local_path = generate_ortho_image(
                prompt=props.prompt,
                api_key=props.api_key.strip(),
                image_path=props.image_path if props.image_path.strip() else None,
                view_type=self.view_type,
                debug_mode=props.debug_mode
            )
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}

        loc = (0, 5, 0) if self.view_type == "front" else (-5, 0, 0)
        rot = (1.5708, 0, 0) if self.view_type == "front" else (1.5708, 0, 1.5708)

        bpy.ops.object.empty_add(type='IMAGE', location=loc)
        empty = bpy.context.object
        empty.empty_display_size = 5.0
        empty.data = bpy.data.images.load(local_path)
        empty.rotation_euler = rot
        empty.name = f"Ref_{self.view_type.capitalize()}"

        self.report({'INFO'}, f"{self.view_type.capitalize()} ortho imported!")
        return {'FINISHED'}

class SCENE_OT_generate_front(SCENE_OT_generate_view):
    bl_idname = "scene.generate_front"
    bl_label = "Generate Front"
    view_type: StringProperty(default="front")

class SCENE_OT_generate_side(SCENE_OT_generate_view):
    bl_idname = "scene.generate_side"
    bl_label = "Generate Side"
    view_type: StringProperty(default="side")

class SCENE_OT_generate_both(Operator):
    bl_idname = "scene.generate_both"
    bl_label = "Generate Both"
    def execute(self, context):
        bpy.ops.scene.generate_front()
        bpy.ops.scene.generate_side()
        return {'FINISHED'}

# ====================== PANEL ======================
class SCENE_PT_grok_optimizer(Panel):
    bl_label = "Grok Ortho Generator"
    bl_idname = "SCENE_PT_grok_optimizer"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Grok Optimizer"

    def draw(self, context):
        layout = self.layout
        props = context.scene.grok_optimizer_props

        layout.prop(props, "debug_mode")
        col = layout.column()
        col.enabled = not props.debug_mode
        col.prop(props, "api_key")

        if props.image_path.strip():
            prompt_label = "Object Description (optional)"
        else:
            prompt_label = "Object Description (required)"
        layout.prop(props, "prompt", text=prompt_label)

        layout.prop(props, "image_path")

        row = layout.row(align=True)
        row.scale_y = 1.4
        row.operator("scene.generate_front")
        row.operator("scene.generate_side")
        layout.operator("scene.generate_both")

# ====================== PROPERTIES ======================
class GrokOptimizerProps(PropertyGroup):
    debug_mode: BoolProperty(default=True)
    api_key: StringProperty(subtype='PASSWORD', default="")
    prompt: StringProperty(default="")
    image_path: StringProperty(subtype='FILE_PATH', default="")

# ====================== REGISTRATION ======================
def register():
    bpy.utils.register_class(GrokOptimizerProps)
    bpy.types.Scene.grok_optimizer_props = bpy.props.PointerProperty(type=GrokOptimizerProps)
    
    bpy.utils.register_class(SCENE_OT_generate_view)
    bpy.utils.register_class(SCENE_OT_generate_front)
    bpy.utils.register_class(SCENE_OT_generate_side)
    bpy.utils.register_class(SCENE_OT_generate_both)
    bpy.utils.register_class(SCENE_PT_grok_optimizer)

def unregister():
    bpy.utils.unregister_class(SCENE_PT_grok_optimizer)
    bpy.utils.unregister_class(SCENE_OT_generate_both)
    bpy.utils.unregister_class(SCENE_OT_generate_side)
    bpy.utils.unregister_class(SCENE_OT_generate_front)
    bpy.utils.unregister_class(SCENE_OT_generate_view)
    
    del bpy.types.Scene.grok_optimizer_props
    bpy.utils.unregister_class(GrokOptimizerProps)

if __name__ == "__main__":
    register()