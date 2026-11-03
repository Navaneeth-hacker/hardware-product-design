# Blender 5.2 Photorealistic Hardware Rendering Reference

*Verified against installed version: `Blender 5.2.2 LTS` at `C:\Program Files\Blender Foundation\Blender 5.2\blender.exe`*

---

## 1. Headless Execution Syntax

Execute photorealistic PCB and enclosure renders without launching the graphical UI:

```bash
"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b --python scripts/render_pcb.py
```

### Verified CLI Flags
| Flag | Description |
| :--- | :--- |
| `-b`, `--background` | Runs Blender in headless background mode (no graphical display required). |
| `-P`, `--python <script.py>`| Runs the given Python script file after startup. |
| `--python-expr "<code_string>"` | Runs single Python expression string. |
| `-o <path>` | Set output image rendering path. |
| `-F <FORMAT>` | Set output render format (e.g. `PNG`, `JPEG`, `EXR`). |
| `-f <frame_num>` | Renders specified frame number and exits. |

---

## 2. Headless Python Script for Photorealistic Renders

```python
import bpy
import math
import os

# 1. Clear Default Scene
bpy.ops.wm.read_factory_settings(use_empty=True)

# 2. Configure Render Engine to Cycles (Raytracing)
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.device = 'GPU'  # Fallback to 'CPU' if no CUDA/OptiX
scene.cycles.samples = 128
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.film_transparent = True  # Transparent alpha background

# 3. Import KiCad VRML (.wrl) or glTF (.glb)
# Use KiCad's exported board model
model_path = os.path.abspath("hardware/board.glb")
if os.path.exists(model_path):
    bpy.ops.import_scene.gltf(filepath=model_path)
elif os.path.exists("hardware/board.wrl"):
    bpy.ops.import_scene.x3d(filepath="hardware/board.wrl")

# 4. Setup Studio Lighting
# Add Key Light
light_data = bpy.data.lights.new(name="KeyLight", type='AREA')
light_data.energy = 300.0  # Watts
light_data.size = 2.0
light_obj = bpy.data.objects.new(name="KeyLight", object_data=light_data)
scene.collection.objects.link(light_obj)
light_obj.location = (1.5, -2.0, 3.0)
light_obj.rotation_euler = (math.radians(45), 0, math.radians(30))

# 5. Camera Setup (Isometric / 45° Angle)
cam_data = bpy.data.cameras.new("StudioCamera")
cam_data.lens = 85.0  # 85mm portrait / product lens
cam_obj = bpy.data.objects.new("StudioCamera", cam_data)
scene.collection.objects.link(cam_obj)
scene.camera = cam_obj
cam_obj.location = (2.5, -3.0, 2.5)
cam_obj.rotation_euler = (math.radians(55), 0, math.radians(40))

# 6. Render and Save Image
scene.render.filepath = os.path.abspath("docs/product_render.png")
bpy.ops.render.render(write_still=True)
print("Photorealistic product render saved to docs/product_render.png")
```
