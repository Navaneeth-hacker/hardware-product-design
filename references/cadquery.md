# CadQuery Parametric 3D CAD Reference

*Python parametric modeling framework based on OpenCascade.*

---

## 1. Fluent Workplane API & Selectors

CadQuery constructs geometry by chaining operations on active `Workplane` contexts using selector strings:

```python
import cadquery as cq

# 1. Base Box with Filleted Edges
box = (
    cq.Workplane("XY")
    .box(100.0, 65.0, 25.0)
    .edges("|Z")            # Select edges parallel to Z axis
    .fillet(3.0)
)

# 2. Hollow out Interior (Shelling)
enclosure = box.faces(">Z").shell(-2.0)  # Remove top face, 2.0mm wall

# 3. Add Mounting Bosses inside bottom face
bosses = (
    enclosure.faces("<Z")
    .workplane(centerOption="CenterOfBoundBox")
    .rect(85.0, 50.0, forConstruction=True)
    .vertices()
    .circle(4.0 / 2.0)       # 4.0mm OD boss
    .extrude(8.0)            # 8.0mm standoff height
)

# 4. Drill Pilot Holes for M2 Screws
enclosure_final = (
    bosses.faces(">Z")
    .workplane()
    .rect(85.0, 50.0, forConstruction=True)
    .vertices()
    .hole(1.6, depth=6.0)    # 1.6mm pilot hole, 6mm deep
)

# 5. Export Manufacturing Files
cq.exporters.export(enclosure_final, "mech/enclosure.step")
cq.exporters.export(enclosure_final, "mech/enclosure.stl", tolerance=0.03, angularTolerance=0.1)
```

---

## 2. Advanced Selector Strings

| Selector String | Description | Example Usage |
| :--- | :--- | :--- |
| `>Z`, `<Z` | Face with maximum/minimum Z coordinate | `.faces(">Z")` (select top face) |
| `>X`, `<X` | Face with maximum/minimum X coordinate | `.faces(">X")` (select right face) |
| `|Z` | Edges/faces parallel to Z axis | `.edges("|Z").fillet(2.0)` |
| `#Z` | Edges/faces perpendicular to Z axis | `.faces("#Z")` (all horizontal faces) |
| `%PLANE` | Geometry lying in or parallel to plane | `.faces("%XY")` |
| `>>[0]` | Nearest element in a sorted list | `.faces(">Z").vertices(">>[0]")` |

---

## 3. Assemblies & Collision Detection

Using `cq.Assembly` to mate components and verify clearances:

```python
import cadquery as cq

# 1. Load Parts
enclosure = cq.importers.importStep("mech/enclosure.step")
pcb = cq.importers.importStep("mech/pcb.step")

# 2. Build Assembly Hierarchy
assy = cq.Assembly()
assy.add(enclosure, name="Enclosure", color=cq.Color(0.2, 0.2, 0.2, 0.8))
assy.add(pcb, name="PCB", loc=cq.Location(cq.Vector(0, 0, 8.0)), color=cq.Color(0.1, 0.6, 0.2, 1.0))

# 3. Collision / Interference Test
# Extract underlying OpenCascade shapes
enclosure_shape = assy.objects["Enclosure"].obj
pcb_shape = assy.objects["PCB"].obj.moved(assy.objects["PCB"].loc)

intersection = enclosure_shape.intersect(pcb_shape)

if intersection.val().Volume() > 0.001:
    print(f"INTERFERENCE DETECTED: {intersection.val().Volume():.3f} mm^3")
else:
    print("NO INTERFERENCE: PCB fits cleanly.")

# 4. Save Assembly
assy.save("mech/product_assembly.step")
```

---

## 4. Headless Execution & CQGI

CadQuery scripts can be executed headlessly via standard Python:
```bash
python scripts/build_case.py
```
Or parameterized via the CadQuery Gateway Interface (CQGI):
```python
import cadquery as cq
from cadquery import cqgi

model = cqgi.parse(open("mech/parametric_case.py").read())
build_result = model.build(build_parameters={"length": 110.0, "width": 70.0})
if build_result.success:
    cq.exporters.export(build_result.first_result.shape, "mech/case.step")
```
