# FreeCAD 1.1 Headless & Scripting Reference

*Verified against installed FreeCAD version: `1.1.4 (Revision 20260928)` at `C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe`*

---

## 1. Running Headless FreeCAD Scripts

Execute Python automation scripts using `freecadcmd.exe`:
```bash
"C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" scripts/build_enclosure.py
```
To run batch parametric regeneration with arguments:
```bash
"C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" --pass width=120 height=80 scripts/generate.py
```

---

## 2. Workbenches & Python API

### Part & PartDesign Workbenches
- **What it does**: Constructive Solid Geometry (CSG) primitives (`Part`) and feature-based parametric solids with Sketches (`PartDesign`).
- **Headless Python Script**:
  ```python
  import FreeCAD, Part

  doc = FreeCAD.newDocument("Enclosure")
  # 1. Create base box
  box = doc.addObject("Part::Box", "MainBox")
  box.Length = 100.0  # mm
  box.Width = 60.0
  box.Height = 30.0

  # 2. Hollow out box (Thickness/Shelling)
  # Fillet edges
  edges = box.Shape.Edges
  fillet = doc.addObject("Part::Fillet", "BoxFillet")
  fillet.Base = box
  fillet.Edges = [(1, 3.0, 3.0), (2, 3.0, 3.0)]  # (edge_index, r1, r2)

  doc.recompute()
  ```

### Sketcher Workbench
- **What it does**: 2D constrained profiles (points, lines, arcs, dimensions, horizontal/vertical/tangent constraints) driving 3D pads and pockets.
- **Python Scripting**:
  ```python
  import FreeCAD, Sketcher, PartDesign

  doc = FreeCAD.newDocument("ParametricPart")
  body = doc.addObject("PartDesign::Body", "Body")
  sketch = doc.addObject("Sketcher::SketchObject", "Sketch")
  body.addObject(sketch)

  # Add lines and geometric constraints
  sketch.addGeometry(Part.LineSegment(FreeCAD.Vector(0,0,0), FreeCAD.Vector(50,0,0)), False)
  sketch.addConstraint(Sketcher.Constraint("Horizontal", 0))
  sketch.addConstraint(Sketcher.Constraint("DistanceX", 0, 1, 0, 2, 50.0))
  doc.recompute()
  ```

### Assembly Workbench (FreeCAD 1.0/1.1 Native Assembly)
- **What it does**: Positions multiple bodies and hardware components (PCB STEP, Top Enclosure, Bottom Enclosure, M3 Screws) with joint constraints (Fixed, Revolute, Slider, Rigid).
- **Collision & Clearance Check**:
  ```python
  # Check interference between PCB and enclosure
  shape1 = doc.getObject("PCB").Shape
  shape2 = doc.getObject("EnclosureTop").Shape
  intersection = shape1.common(shape2)

  if intersection.Volume > 0.001:
      print(f"INTERFERENCE DETECTED! Volume: {intersection.Volume:.3f} mm^3")
      bbox = intersection.BoundBox
      print(f"Collision Center: X={bbox.Center.x:.2f}, Y={bbox.Center.y:.2f}, Z={bbox.Center.z:.2f}")
  else:
      print("CLEARANCE VERIFIED: Zero interference.")
  ```

### TechDraw Workbench
- **What it does**: Generates technical 2D drawings with dimension callouts, projection views, cross-sections, and title blocks.
- **Exporting to SVG/DXF**:
  ```python
  import TechDraw
  page = doc.addObject("TechDraw::DrawPage", "Page")
  template = doc.addObject("TechDraw::DrawSVGTemplate", "Template")
  template.Template = "C:/Program Files/FreeCAD 1.1/data/Mod/TechDraw/Templates/A4_Landscape_TD.svg"
  page.Template = template

  view = doc.addObject("TechDraw::DrawViewPart", "TopView")
  view.Source = doc.getObject("MainBox")
  view.Direction = FreeCAD.Vector(0, 0, 1)
  page.addView(view)
  doc.recompute()

  # Export DXF
  import TechDrawGui  # or export directly via TechDraw.writeDXFPage(page, "mech/drawing.dxf")
  ```

### FEM Workbench (Integrated CalculiX & Gmsh)
- **What it does**: Setup finite element structural stress and thermal conduction studies directly on 3D geometry.
- **Workflow**:
  1. Define Analysis container (`Fem::FemAnalysis`).
  2. Mesh with Gmsh (`Fem::FemMeshGmsh`).
  3. Assign Material: Mechanical elasticity ($E=2.3\,\text{GPa}, \nu=0.38$ for PLA/PETG) or Thermal conductivity ($k=0.2\,\text{W/m}\cdot\text{K}$).
  4. Apply Constraints: Fixed face boundary (`Fem::ConstraintFixed`), thermal heat flux or fixed temperature (`Fem::ConstraintTemperature`).
  5. Solve headlessly using bundled `ccx.exe`.

### Spreadsheet Workbench
- **What it does**: Master parametric driver table. Cell values (e.g. `A1=WallThickness=2.0`, `A2=PCB_Length=85.0`) bind directly to Sketcher constraints and Part dimensions.

### CAM / Path Workbench
- **What it does**: CNC toolpath generation for milled aluminum enclosures (2.5D pocketing, profiling, drilling, adaptive clearing). Generates standard G-code (`.nc`).

### Mesh Workbench
- **What it does**: Converts solid Brep shapes to triangulated meshes for 3D printing.
- **High-Quality STL Export**:
  ```python
  import Mesh
  mesh = doc.addObject("Mesh::Feature", "Mesh")
  mesh.Mesh = Mesh.Mesh(doc.getObject("MainBox").Shape.tessellate(0.02))  # 0.02mm chordal deflection
  Mesh.export([mesh], "mech/enclosure.stl")
  ```

---

## 3. Scripted STEP & STL Export Template

```python
import FreeCAD, Part, Mesh
import os

def export_manufacturing_models(doc, output_dir="mech"):
    os.makedirs(output_dir, exist_ok=True)
    objects_to_export = [obj for obj in doc.Objects if hasattr(obj, "Shape") and obj.Shape.Volume > 0]
    
    # 1. Export STEP (Standard for CNC / Tooling)
    step_path = os.path.join(output_dir, "enclosure.step")
    Part.export(objects_to_export, step_path)
    print(f"Exported STEP: {step_path}")

    # 2. Export High-Resolution STL (3D Printing)
    for obj in objects_to_export:
        stl_path = os.path.join(output_dir, f"{obj.Name}.stl")
        mesh_data = Mesh.Mesh(obj.Shape.tessellate(0.03))  # fine tolerance
        mesh_data.write(stl_path)
        print(f"Exported STL: {stl_path}")

if __name__ == "__main__":
    doc = FreeCAD.ActiveDocument
    if doc:
        export_manufacturing_models(doc)
```
