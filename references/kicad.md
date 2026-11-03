# KiCad 10 Comprehensive Tool Reference

*Verified against installed KiCad version: `10.0.6` at `C:\Program Files\KiCad\10.0\bin\kicad-cli.exe`*

---

## 1. Schematic Capture & Hierarchy (`eeschema`)

### Hierarchical Sheets
- **What it does**: Splits complex schematics into logical multi-page blocks (e.g. Power, MCU, Analog Front End, Communication) with defined interface pins.
- **When to use**: Any design with $>30$ components or distinct functional modules.
- **Workflow**:
  - Place Sheet Symbol (`S` key) -> specify file name (e.g. `power.kicad_sch`).
  - Add Hierarchical Sheet Pins on sheet box matching signal names.
  - In sub-sheet, place Hierarchical Labels matching parent sheet pin names.
  - Global Labels (like power nets `+3V3`, `GND`) span all sheets automatically; local net labels remain scoped to their sheet.

### Symbol & Footprint Library Management
- **What it does**: Maps schematic logical pins to physical PCB land patterns and 3D models.
- **When to use**: Selecting parts, adding manufacturer symbols, verifying pin numbering.
- **CLI Commands**:
  - Upgrade legacy symbol library format:
    ```bash
    kicad-cli sym upgrade <library.kicad_sym>
    ```
  - Export SVG vector graphic of a symbol:
    ```bash
    kicad-cli sym export svg -o output.svg --symbol <symbol_name> <library.kicad_sym>
    ```
  - Upgrade footprint library:
    ```bash
    kicad-cli fp upgrade <footprint_dir.pretty>
    ```
  - Export SVG of a footprint:
    ```bash
    kicad-cli fp export svg -o footprint.svg --footprint <fp_name> <footprint_dir.pretty>
    ```

### Electrical Rules Check (ERC)
- **What it does**: Detects floating pins, pin direction conflicts (e.g. two outputs connected), missing power flags (`PWR_FLAG`), unannotated items.
- **When to use**: Mandatory before opening PCB layout.
- **CLI Command**:
  ```bash
  kicad-cli sch erc --severity-all --exit-code-violations --format report -o erc_report.txt <project>.kicad_sch
  ```
  - `--severity-all`: Reports errors, warnings, and exclusions.
  - `--exit-code-violations`: Exits non-zero on any violation (essential for CI pipelines).
  - `--format json`: Outputs machine-readable JSON for automated parsing.

### Built-in ngspice Schematic Simulation
- **What it does**: Runs SPICE simulations directly from schematic components with spice models assigned.
- **When to use**: Analog front ends, active filters, transient power-up spikes.
- **Configuration**:
  - In Symbol Properties -> `Edit Spice Model`: specify subcircuit `.lib` or `.model`.
  - Place `.tran 1u 10m` or `.ac dec 100 10 10Meg` text directives directly on schematic.
  - Launch simulator: `Inspect -> Simulator` or export netlist:
    ```bash
    kicad-cli sch export netlist --format spice -o circuit.cir <project>.kicad_sch
    ```

---

## 2. Board Setup, Layout & Routing (`pcbnew`)

### Board Setup & Design Rules
- **Physical Stackup**: Define layer count (2, 4, 6 layer), copper weight (1 oz / 0.5 oz), dielectric constants ($\varepsilon_r$), prepreg thickness.
- **Constraints**: Configure minimum trace width, clearance, via diameter, hole size, and annular ring matching the target fab (e.g. JLCPCB / PCBWay).
- **Custom Rules (`.kicad_dru`)**:
  - Syntax for conditional clearances:
    ```
    (rule "High_Voltage_Clearance"
      (condition "A.NetClass == 'HV' && B.NetClass == 'LV'")
      (constraint clearance (min 2.5mm)))
    ```

### Net Classes & High-Speed Routing
- **Net Classes**: Assign nets to classes (e.g. `Power`, `Default`, `RF_50`, `USB_90`) with dedicated widths, clearances, and via profiles.
- **Differential Pairs**:
  - Net names must end in `_P` and `_N` (or `+` and `-`).
  - Route with `Route -> Differential Pair` (`6` key).
  - Maintains target coupled trace gap and impedance ($90\,\Omega \pm 10\%$ for USB 2.0).
- **Length Tuning & Meanders**:
  - Tools: `Route -> Tune Length` (`7` key) for single traces; `Route -> Tune Differential Pair Length` (`8` key); `Route -> Tune Differential Pair Skew` (`9` key).
  - Adds accordion meanders to match propagation delay within $\le 1\,\text{mm}$ skew budget.

### Copper Zones & Teardrops
- **Copper Zones (`Ctrl+Shift+Z`)**:
  - Pour ground and power planes. Set thermal relief spoke width ($0.3 - 0.4\,\text{mm}$) and gap.
  - Force zone refill via CLI:
    ```bash
    kicad-cli pcb drc --refill-zones --save-board <project>.kicad_pcb
    ```
- **Teardrops**:
  - `Edit -> Edit Teardrops...`: Adds filleted copper tapers connecting traces to via rings and SMD pads, preventing pad breakout and drill stress fractures.

### Design Rules Check (DRC)
- **What it does**: Comprehensive physical geometry check: clearance, minimum annular ring, drill-to-track, silkscreen over exposed pads, unrouted nets, courtyard overlaps, parity with schematic.
- **CLI Command**:
  ```bash
  kicad-cli pcb drc --severity-all --schematic-parity --all-track-errors --refill-zones --exit-code-violations --format report -o drc_report.txt <project>.kicad_pcb
  ```

---

## 3. 3D Inspection & Solid Modeling Export

### Headless 3D Raytracing / Rendering
- **CLI Command**:
  ```bash
  kicad-cli pcb render --quality high --width 1920 --height 1080 --side top --floor --perspective --rotate -45,0,45 -o board_isometric.png <project>.kicad_pcb
  ```
  - `--side`: `top`, `bottom`, `left`, `right`, `front`, `back`.
  - `--preset`: `follow_plot_settings` or custom appearance presets.
  - `--background`: `transparent` or `opaque`.

### STEP & VRML Solid Export
- **STEP Export (Authoritative 3D CAD format for mechanical enclosures)**:
  ```bash
  kicad-cli pcb export step --subst-models --include-tracks --include-pads --include-zones --no-dnp -o mech/pcb.step <project>.kicad_pcb
  ```
  - `--subst-models`: Replaces VRML visual models with precision mechanical STEP models.
  - `--no-dnp`: Excludes components marked "Do Not Populate".
  - `--include-tracks` & `--include-zones`: Exports physical copper geometry for thermal FEA.
- **VRML Export (Photorealistic rendering for Blender)**:
  ```bash
  kicad-cli pcb export vrml --units mm -o board.wrl <project>.kicad_pcb
  ```

---

## 4. Fabrication Release & Documentation Exports

### Gerber & Drill Files
- **Plot Gerbers**:
  ```bash
  kicad-cli pcb export gerbers --board-plot-params --no-x2 --subtract-soldermask -o fab/gerbers/ <project>.kicad_pcb
  ```
- **Generate Excellon Drill Files**:
  ```bash
  kicad-cli pcb export drill --format excellon --excellon-units mm --excellon-separate-th --generate-map --generate-report -o fab/gerbers/ <project>.kicad_pcb
  ```
  - `--excellon-separate-th`: Generates independent files for Plated Through Hole (`PTH`) and Non-Plated Through Hole (`NPTH`), required by most fab houses.

### Component Placement List (CPL / Centroid)
- **Generate Pick-and-Place File**:
  ```bash
  kicad-cli pcb export pos --format csv --units mm --side both --smd-only --exclude-dnp -o fab/cpl.csv <project>.kicad_pcb
  ```

### Bill of Materials (BOM)
- **Generate Assembly BOM**:
  ```bash
  kicad-cli sch export bom --format-preset CSV --exclude-dnp --group-by "Value,Footprint" --fields "Reference,Value,Footprint,QUANTITY,DNP,LCSC" --labels "Refs,Val,Package,Qty,DNP,LCSC_Part" -o fab/bom.csv <project>.kicad_sch
  ```

### Vector & PDF Documentation
- **Schematic Multi-page PDF**:
  ```bash
  kicad-cli sch export pdf -o docs/schematic.pdf <project>.kicad_sch
  ```
- **PCB Assembly Drawings (PDF)**:
  ```bash
  kicad-cli pcb export pdf --layers "F.Fab,Edge.Cuts" -o docs/assembly_top.pdf <project>.kicad_pcb
  ```
- **SVG Layer Plots**:
  ```bash
  kicad-cli pcb export svg --layers "F.Cu,Edge.Cuts" -o docs/top_copper.svg <project>.kicad_pcb
  ```
- **IPC-2581 & ODB++ Modern Intelligent Fabrication Data**:
  ```bash
  kicad-cli pcb export ipc2581 -o fab/board.cvg <project>.kicad_pcb
  kicad-cli pcb export odb -o fab/odb_output/ <project>.kicad_pcb
  ```

---

## 5. Jobsets & Board Variants

### Automated Jobsets (`kicad-cli jobset`)
- **What it does**: Executes a saved batch export configuration recipe (`.kicad_jobset`) containing multiple targets (Gerbers, PDF, BOM, STEP, renders) in one execution.
- **CLI Command**:
  ```bash
  kicad-cli jobset run --stop-on-error -f release.kicad_jobset <project>.kicad_pcb
  ```

### Assembly Variants
- **What it does**: Manages alternative component populations (e.g. `Standard`, `No-Wireless`, `Extended-Battery`) within a single schematic.
- **Exporting with Variants**:
  - Supply `--variant <VariantName>` to `sch export bom`, `pcb export gerbers`, `pcb export pos`, `pcb export step`, or `pcb render`.
  - Uses `${VARIANT}` token in output filename paths for multi-variant release generation.

---

## 6. The `pcbnew` Python API

*Executable: `C:\Program Files\KiCad\10.0\bin\python.exe`*

### Scripted Board Manipulation & Automation
```python
import pcbnew

# 1. Load Board
board = pcbnew.LoadBoard("hardware/project.kicad_pcb")

# 2. Inspect Tracks and Vias
for track in board.GetTracks():
    start = track.GetStart()  # in internal units (nanometers: 1 mm = 1,000,000 nm)
    end = track.GetEnd()
    width_mm = track.GetWidth() / 1e6
    net_name = track.GetNetname()

# 3. Query Footprints and Pads
for fp in board.GetFootprints():
    ref = fp.GetReference()
    pos = fp.GetPosition()
    print(f"Component {ref} at ({pos.x/1e6:.2f}, {pos.y/1e6:.2f}) mm")

# 4. Measure Bounding Box
bbox = board.ComputeBoundingBox()
print(f"Board size: {bbox.GetWidth()/1e6:.2f} x {bbox.GetHeight()/1e6:.2f} mm")

# 5. Save Board
pcbnew.SaveBoard("hardware/project_modified.kicad_pcb", board)
```
