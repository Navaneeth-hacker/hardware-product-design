# 3D Slicer Headless CLI Reference (PrusaSlicer & OrcaSlicer)

*Automated slicing engines for rapid enclosure prototyping and additive manufacturing.*

---

## 1. PrusaSlicer Headless CLI Execution

On Windows, always invoke **`prusa-slicer-console.exe`** for CLI automation:

```bash
# Basic G-code generation from STL
prusa-slicer-console --export-gcode -o mech/enclosure.gcode mech/enclosure.stl

# Load configuration profile and slice with custom layer height
prusa-slicer-console --load config/prusa_mk4_petg.ini --layer-height 0.20 --fill-density 20% --export-gcode -o mech/enclosure_bottom.gcode mech/enclosure_bottom.stl
```

### Verified CLI Flags
| Flag | Aliases | Description |
| :--- | :--- | :--- |
| `--export-gcode` | `-g`, `--gcode` | Slices the input geometry and exports toolpaths to G-code. |
| `--slice` | `-s` | Triggers the slicing process explicitly. |
| `--load <file.ini>`| None | Loads print, filament, and printer presets from an `.ini` or `.3mf` file. |
| `-o <file.gcode>` | `--output` | Destination output path for generated G-code. |
| `--center <X,Y>` | None | Center model coordinates on build plate (e.g. `--center 125,105`). |
| `--scale <N>` | None | Scales model by numeric multiplier or percentage. |
| `--rotate <deg>` | None | Rotates model around Z axis. |
| `--repair` | None | Repairs non-manifold edges, inverted normals, and mesh holes. |
| `--help-fff` | None | Lists every FFF/FDM configurable parameter variable. |

---

## 2. Parameter Overrides for Functional Enclosures

When slicing mechanical housings, pass functional parameters to guarantee structural stiffness and screw retention:

- **Perimeter Shells**: Set $\ge 4$ perimeters (approx. $1.6 - 2.0\,\text{mm}$ solid wall) so screw threads bite into solid plastic rather than hollow infill.
- **Infill Density & Pattern**: Use **Gyroid** or **Rectilinear** infill at $25 - 40\%$ density for isotropic mechanical strength.
- **Top / Bottom Solid Layers**: Minimum 5 layers top and bottom.

Example CLI invocation with inline overrides:
```bash
prusa-slicer-console \
  --load config/base_printer.ini \
  --perimeters 4 \
  --fill-pattern gyroid \
  --fill-density 30% \
  --layer-height 0.20 \
  --temperature 240 \
  --bed-temperature 85 \
  --export-gcode \
  -o mech/enclosure_stiff.gcode \
  mech/enclosure.stl
```

---

## 3. OrcaSlicer CLI Syntax

OrcaSlicer (fork of BambuStudio / PrusaSlicer) uses identical slicing flag semantics:

```bash
orca-slicer --load config/bambu_x1c.json --export-gcode -o mech/enclosure.gcode mech/enclosure.stl
```
