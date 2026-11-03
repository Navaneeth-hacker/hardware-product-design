# KiBot Automated Fabrication Pipeline Reference

*Comprehensive CI/CD build system for generating KiCad fabrication deliverables.*

---

## 1. Overview & Architecture

KiBot processes KiCad schematic (`.kicad_sch`) and board (`.kicad_pcb`) files against a declarative YAML configuration recipe (`.kibot.yaml`). It enforces preflight verification checks (ERC, DRC) and generates release outputs: Gerbers, drill files, assembly drawings, 3D renders, BOMs, and pick-and-place files formatted for specific manufacturing houses (JLCPCB, PCBWay).

---

## 2. Command Line Interface (CLI)

```bash
# Basic Execution
kibot -b hardware/board.kicad_pcb -e hardware/board.kicad_sch -c .kibot.yaml -d fab/

# List all outputs defined in configuration
kibot -c .kibot.yaml --list

# Skip preflight checks if already validated
kibot -b hardware/board.kicad_pcb -c .kibot.yaml -s run_erc,run_drc

# Generate full template configuration file
kibot --example
```

### Verified CLI Flags
| Flag | Long Argument | Purpose |
| :--- | :--- | :--- |
| `-b` | `--board <file.kicad_pcb>` | Input KiCad PCB file. |
| `-e` | `--schema <file.kicad_sch>`| Input KiCad schematic file. |
| `-c` | `--config <file.yaml>` | KiBot YAML configuration file. |
| `-d` | `--out-dir <dir>` | Base destination directory for all generated outputs. |
| `-s` | `--skip-pre <checks>` | Skip specific preflight tasks (e.g. `-s run_erc,run_drc` or `-s all`). |
| `--variant`| `--variant <name>` | Select assembly variant defined in project. |
| `--fail-on-warnings` | None | Treat warnings as fatal build errors (strict CI mode). |
| `-v` / `-vv` | `--verbose` | Increase log verbosity. |

---

## 3. Production Configuration Template (`.kibot.yaml`)

```yaml
kibot:
  version: 1

preflight:
  run_erc: true
  update_xml: true
  run_drc: true
  check_zone_fills: true
  ignore_unconnected: false

global:
  output: "%f-%i%I%v.%x"

outputs:
  # 1. Standard Gerbers
  - name: "gerbers"
    comment: "Production RS-274X Gerbers"
    type: gerber
    dir: gerbers
    options:
      use_protel_extensions: true
      create_gerber_job_file: true
      subtract_mask_from_silk: true
      output: "%f-%i.%x"
    layers:
      - F.Cu
      - B.Cu
      - In1.Cu
      - In2.Cu
      - F.Paste
      - B.Paste
      - F.SilkS
      - B.SilkS
      - F.Mask
      - B.Mask
      - Edge.Cuts

  # 2. Excellon Drill Files
  - name: "excellon_drill"
    comment: "PTH and NPTH drill files"
    type: excellon
    dir: gerbers
    options:
      metric_units: true
      pth_and_npth_single_file: false

  # 3. JLCPCB Assembly (PCBA) Position File
  - name: "jlcpcb_cpl"
    comment: "SMT Centroid Pick-and-Place for JLCPCB"
    type: position
    dir: assembly
    options:
      format: CSV
      units: millimeters
      separate_files_for_front_and_back: false
      only_smd: true

  # 4. Interactive HTML BOM
  - name: "ibom"
    comment: "Interactive HTML BOM for manual prototype assembly"
    type: ibom
    dir: assembly
    options:
      dark_mode: true
      highlight_pin1: true

  # 5. Photorealistic 3D Render
  - name: "render_3d"
    comment: "Top view 3D raytrace"
    type: render_3d
    dir: renders
    options:
      ray_tracing: true
      view: top
      width: 1920
      height: 1080
```
