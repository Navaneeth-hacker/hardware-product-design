# KiKit Panelization & Production Reference

*CLI automation tool for multi-board panelization, framing, and fabrication exports.*

---

## 1. Overview & Panelization Architecture

KiKit arranges individual KiCad boards into production panels suitable for automated surface-mount assembly rails and pick-and-place feeders.

CLI configuration is structured into logical categories:
- `--layout`: Grid geometry, board spacing, and rotation.
- `--tabs`: Structural tabs holding boards to the panel frame.
- `--cuts`: Breakaway mechanisms (mousebites with perforated drills or V-scoring).
- `--framing`: Waste rails surrounding the panel for conveyor clamping.
- `--tooling`: Alignment holes for SMT placement machines.
- `--fiducials`: Optical camera alignment marks on panel rails.
- `--text`: Etched or silkscreen batch identifiers and revision text.

---

## 2. Command Line Interface (`kikit panelize`)

```bash
kikit panelize [OPTIONS] input.kicad_pcb output_panel.kicad_pcb
```

### Complete Production Panel Recipe (V-Cuts & Mousebites)

```bash
kikit panelize \
  --layout "grid; rows: 2; cols: 3; space: 2.5mm" \
  --tabs "fixed; width: 3.5mm; vcount: 2; hcount: 1" \
  --cuts "mousebites; drill: 0.5mm; spacing: 0.8mm; offset: 0.2mm" \
  --framing "railstb; width: 5mm; space: 2.5mm" \
  --tooling "circle; size: 3.0mm; hoffset: 5mm; voffset: 2.5mm" \
  --fiducials "copper; size: 1.0mm; opening: 2.0mm; hoffset: 10mm; voffset: 2.5mm" \
  --text "simple; text: PROD_PANEL_REV_A; hoffset: 25mm; voffset: 2.5mm; height: 1.5mm" \
  hardware/device.kicad_pcb fab/panel.kicad_pcb
```

---

## 3. Parameter Category Reference

### A. `--layout` (Board Positioning)
- `type: grid` (or `tightgrid`): Regular matrix arrangement.
- `rows: <N>, cols: <M>`: Number of instances in Y and X directions.
- `space: <dim>`: Separation gap between adjacent boards (e.g. `2mm` for router bit path).
- `rotation: <angle>`: Rotate boards prior to tiling (e.g. `90deg` or `180deg`).
- `alternation: <none|rows|cols>`: Rotate alternate rows to optimize packing density.

### B. `--tabs` (Connection Tabs)
- `type: fixed`: Tabs placed at specified count along edges.
- `width: <dim>`: Width of connection tab (e.g. `3.0mm` to `4.0mm`).
- `vcount: <N>, hcount: <M>`: Number of tabs on vertical and horizontal board edges.
- `type: corner`: Places diagonal tabs at board corners for circular or contoured boards.

### C. `--cuts` (Separation Cuts)
- **Mousebites (Perforated Holes)**:
  - `type: mousebites`
  - `drill: <dim>`: Hole diameter (standard: `0.5mm`).
  - `spacing: <dim>`: Center-to-center distance between holes (standard: `0.8 - 1.0mm`).
  - `offset: <dim>`: Inset distance into the board edge (e.g. `0.2mm` recess leaves clean edge after de-paneling).
- **V-Cuts (V-Scoring)**:
  - `type: vcuts`
  - `clearance: <dim>`: Minimum copper clearance from V-groove line (standard: `0.5mm`).

### D. `--framing` (Waste Rails)
- `type: railstb`: Rails along Top and Bottom (most common for SMT conveyor belts).
- `type: fourrails`: Complete rectangular frame enclosing all 4 sides.
- `width: <dim>`: Width of frame rail (standard: `5.0mm`).
- `space: <dim>`: Gap between outermost boards and the frame rail.

### E. `--tooling` & `--fiducials`
- **Tooling Holes**:
  - `type: circle; size: 3.0mm`: Non-plated tooling holes located on diagonal frame corners.
- **Optical Fiducials**:
  - `type: copper; size: 1.0mm; opening: 2.0mm`: 1.0mm circular copper pad with 2.0mm solder mask clearance on rail corners.

---

## 4. Fabrication Exports (`kikit export`)

Export fabrication files directly from the generated panel:
```bash
# Export Gerbers and Drill for the panel
kikit export gerbers fab/panel.kicad_pcb fab/gerbers_panel/

# Export unified SMT Pick-and-Place (CPL) for all boards on panel
kikit export pcbnew-pos fab/panel.kicad_pcb fab/panel_cpl.csv
```
