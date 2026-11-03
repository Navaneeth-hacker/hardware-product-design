# build123d Parametric Hardware CAD Reference

*Python 3D CAD framework built on the OpenCascade technology kernel (`cadquery-ocp`).*

---

## 1. Core Architecture & Context Managers

`build123d` uses Python context managers (`BuildPart`, `BuildSketch`, `BuildLine`) to author parametric solid geometry naturally:

```python
from build123d import *

# 1. Authoring a Parametric Enclosure Base
wall_thickness = 2.0
pcb_l, pcb_w = 85.0, 56.0
clearance = 0.4  # FDM 3D print clearance
box_l = pcb_l + 2 * (wall_thickness + clearance)
box_w = pcb_w + 2 * (wall_thickness + clearance)
box_h = 24.0

with BuildPart() as enclosure_bottom:
    # Outer Solid
    Box(box_l, box_w, box_h)
    # Fillet vertical corners
    fillet(enclosure_bottom.edges().filter_by(Axis.Z), radius=3.0)
    # Hollow interior from top face
    top_face = enclosure_bottom.faces().sort_by(Axis.Z)[-1]
    offset(openings=top_face, amount=-wall_thickness)

    # Add Screw Bosses in corners
    boss_offset_x = (box_l / 2.0) - wall_thickness - 4.0
    boss_offset_y = (box_w / 2.0) - wall_thickness - 4.0
    
    with Locations([
        (boss_offset_x, boss_offset_y),
        (-boss_offset_x, boss_offset_y),
        (boss_offset_x, -boss_offset_y),
        (-boss_offset_x, -boss_offset_y)
    ]):
        with BuildSketch(Plane.XY.offset(wall_thickness)):
            Circle(radius=4.0 / 2.0)          # Boss outer diameter 4.0mm
        extrude(amount=box_h - wall_thickness - 2.0)
        
        # Tap holes for M2 self-tapping screws (1.6mm pilot hole)
        with BuildSketch(Plane.XY.offset(wall_thickness)):
            Circle(radius=1.6 / 2.0)
        extrude(amount=box_h, mode=Mode.SUBTRACT)

# Export Solid
export_step(enclosure_bottom.part, "mech/enclosure_bottom.step")
export_stl(enclosure_bottom.part, "mech/enclosure_bottom.stl", tolerance=0.03)
```

---

## 2. Assemblies & PCB Mating Checks

Load the physical board STEP exported from KiCad and programmatically check clearances and interference:

```python
from build123d import *

# 1. Import KiCad Board STEP
pcb_solid = import_step("mech/pcb.step")

# 2. Build or Import Enclosure
enclosure_solid = import_step("mech/enclosure_bottom.step")

# 3. Position PCB inside Enclosure
# Place PCB resting on boss standoffs (Z = standoff_height)
positioned_pcb = pcb_solid.move(Location((0, 0, 6.0)))

# 4. Programmatic Interference / Collision Verification
collision = enclosure_solid.intersect(positioned_pcb)

if collision.volume > 0.0001:  # volume in mm^3
    print(f"CRITICAL WARNING: Mechanical Interference Detected!")
    print(f"Collision Volume: {collision.volume:.3f} mm^3")
    bbox = collision.bounding_box()
    print(f"Collision Bounds: X=[{bbox.min.X:.1f}, {bbox.max.X:.1f}], Y=[{bbox.min.Y:.1f}, {bbox.max.Y:.1f}], Z=[{bbox.min.Z:.1f}, {bbox.max.Z:.1f}]")
else:
    print("SUCCESS: Zero interference. PCB mates cleanly with enclosure.")

# 5. Build Compound Assembly
assembly = Compound(children=[enclosure_solid, positioned_pcb])
export_step(assembly, "mech/assembly_verified.step")
```

---

## 3. Fillets, Chamfers & Thin-Wall Shelling

- **Filleting Selective Edges**:
  - Vertical edges only: `fillet(part.edges().filter_by(Axis.Z), radius=2.5)`
  - Edges on a specific face: `fillet(face.edges(), radius=1.0)`
- **Chamfers**:
  - Lead-in chamfer for mating lids: `chamfer(lid.edges().sort_by(Axis.Z)[0], length=1.0)`
- **Shelling / Hollow Bodies**:
  - `offset(openings=part.faces().sort_by(Axis.Z)[-1], amount=-2.0)`

---

## 4. Export Formats & Options

- **STEP (`export_step`)**:
  ```python
  export_step(part, "mech/output.step")
  ```
- **STL (`export_stl`)**:
  ```python
  export_stl(part, "mech/output.stl", tolerance=0.02, angular_tolerance=0.1)
  ```
- **DXF (`export_dxf`)**:
  ```python
  # Export 2D sketch / face for laser cutting or CNC routing
  export_dxf(sketch, "mech/panel_cutout.dxf")
  ```
- **SVG (`export_svg`)**:
  ```python
  export_svg(part, "mech/drawing.svg")
  ```
