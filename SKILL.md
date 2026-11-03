---
name: hardware-product-design
description: Use when the user wants to design a physical electronic product end to end with free open-source tools - requirements, schematic and PCB layout (KiCad), 3D enclosure modeling (FreeCAD/CadQuery/OpenSCAD/build123d), circuit and thermal/mechanical simulation (ngspice, CalculiX, Elmer, openEMS), parameter tuning, firmware, and fabrication outputs (Gerbers, BOM, STEP, STL).
---

# Hardware Product Design (Open-Source Toolchain)

Design physical electronic products end-to-end as **version-controlled code and scripted models**.
In this skill, **PCB design always means schematic capture + board layout together**.
This file acts as the central router; detailed tool specifications, commands, and APIs live in `references/`.

---

## When to Use This Skill
- Designing a new electronic device from idea to fabrication-ready files.
- Creating or editing schematics, PCB layouts, 3D mechanical enclosures, BOMs, or circuit simulations.
- Tuning component values or physical design parameters against numerical specifications.

## Do Not Use This Skill When
- The task is pure software with no hardware component.
- The user requires proprietary tools (Altium, SolidWorks, Fusion 360, Ansys) — ask before proceeding.

---

## Toolchain & Reference Index

| Stage | Tools | Reference Guide |
| :--- | :--- | :--- |
| **Schematic + PCB** | KiCad 10 (`kicad-cli`, `pcbnew` Python API), Freerouting | [kicad.md](file:///C:/Users/Navan/.gemini/config/skills/hardware-product-design/references/kicad.md), [freerouting.md](file:///C:/Users/Navan/.gemini/config/skills/hardware-product-design/references/freerouting.md) |
| **Fab Automation** | KiBot, KiKit (panelization) | [kibot.md](file:///C:/Users/Navan/.gemini/config/skills/hardware-product-design/references/kibot.md), [kikit.md](file:///C:/Users/Navan/.gemini/config/skills/hardware-product-design/references/kikit.md) |
| **Circuit Simulation**| ngspice (batch mode, XSPICE), Qucs-S | [ngspice.md](file:///C:/Users/Navan/.gemini/config/skills/hardware-product-design/references/ngspice.md), [qucs-s.md](file:///C:/Users/Navan/.gemini/config/skills/hardware-product-design/references/qucs-s.md) |
| **3D Enclosure** | `build123d`, CadQuery, FreeCAD (`freecadcmd`), OpenSCAD | [build123d.md](file:///C:/Users/Navan/.gemini/config/skills/hardware-product-design/references/build123d.md), [cadquery.md](file:///C:/Users/Navan/.gemini/config/skills/hardware-product-design/references/cadquery.md), [freecad.md](file:///C:/Users/Navan/.gemini/config/skills/hardware-product-design/references/freecad.md), [openscad.md](file:///C:/Users/Navan/.gemini/config/skills/hardware-product-design/references/openscad.md) |
| **Thermal / Structural**| CalculiX (`ccx`), Elmer FEM | [calculix.md](file:///C:/Users/Navan/.gemini/config/skills/hardware-product-design/references/calculix.md), [elmer.md](file:///C:/Users/Navan/.gemini/config/skills/hardware-product-design/references/elmer.md) |
| **RF / Signal Integrity**| openEMS (FDTD 3D EM solver) | [openems.md](file:///C:/Users/Navan/.gemini/config/skills/hardware-product-design/references/openems.md) |
| **Firmware & Emulation**| PlatformIO CLI, Renode (bare-metal simulation) | [platformio.md](file:///C:/Users/Navan/.gemini/config/skills/hardware-product-design/references/platformio.md), [renode.md](file:///C:/Users/Navan/.gemini/config/skills/hardware-product-design/references/renode.md) |
| **Rendering & Slicing** | Blender (Cycles raytracing), PrusaSlicer / OrcaSlicer | [blender.md](file:///C:/Users/Navan/.gemini/config/skills/hardware-product-design/references/blender.md), [slicers.md](file:///C:/Users/Navan/.gemini/config/skills/hardware-product-design/references/slicers.md) |
| **Standards & Rules** | DFM, EMC/ESD pre-compliance, Mechanical tolerances | [dfm-guidelines.md](file:///C:/Users/Navan/.gemini/config/skills/hardware-product-design/references/dfm-guidelines.md), [emc-esd-rules.md](file:///C:/Users/Navan/.gemini/config/skills/hardware-product-design/references/emc-esd-rules.md), [enclosure-tolerances.md](file:///C:/Users/Navan/.gemini/config/skills/hardware-product-design/references/enclosure-tolerances.md) |

> [!IMPORTANT]
> **Pre-Flight Inventory**: Before starting, check installed tool versions against [VERSIONS.md](file:///C:/Users/Navan/.gemini/config/skills/hardware-product-design/references/VERSIONS.md). Report any missing tool to the user with installation instructions instead of silently substituting. Do not install anything without user consent.

---

## 10-Stage Product Workflow

Work in this order. Keep every stage scripted and reproducible; commit to git after each stage.

```mermaid
flowchart LR
    S1[1. Requirements] --> S2[2. Architecture] --> S3[3. Schematic] --> S4[4. Sim & Tune] --> S5[5. Layout & DRC]
    S5 --> S6[6. 3D Enclosure] --> S7[7. Thermal/FEA] --> S8[8. Firmware] --> S9[9. Fabrication] --> S10[10. Bring-up]
```

### 1. Requirements (`docs/requirements.md`)
- Define function, power budget (sleep, idle, peak), I/O buses, physical size limits, operating environment (temp, IP water/dust, drop), target cost (<$15 @ 1k), quantity, and certification needs (FCC/CE). Ask for critical missing constraints.
- **Features to use**: Power envelope matrix, thermal boundaries, mechanical sizing, target fab capability limits.
- **Pointer**: Read [dfm-guidelines.md](file:///C:/Users/Navan/.gemini/config/skills/hardware-product-design/references/dfm-guidelines.md) before setting fabrication constraints.

### 2. Architecture & Power Tree (`docs/architecture.md`)
- Select MCU, power conversion tree, sensors, connectors. Prefer parts in stock at common assemblers (e.g. JLCPCB basic parts) with verified KiCad symbols/footprints. Document trade-offs in `docs/architecture.md`.
- **Features to use**: Mermaid power tree diagrams (`flowchart TD`), component lifecycle checks (reject NRND/EOL), second-source verification.

### 3. Schematic Capture (`hardware/<project>.kicad_sch`)
- Capture full hierarchical schematic in KiCad. Add decoupling hierarchy ($0.1\,\mu\text{F} \parallel 10\,\mu\text{F}$), ESD arrays on external lines, reverse polarity protection, testpoints, and standardized debug/programming headers.
- **Features to use**: Hierarchical sheets, symbol libraries, custom net classes, net labels, text SPICE directives, ERC validation (`kicad-cli sch erc --severity-all --exit-code-violations`).
- **Pointer**: Read [kicad.md](file:///C:/Users/Navan/.gemini/config/skills/hardware-product-design/references/kicad.md) & [emc-esd-rules.md](file:///C:/Users/Navan/.gemini/config/skills/hardware-product-design/references/emc-esd-rules.md) before this stage.

### 4. Circuit Simulation & Parameter Tuning (`sim/`)
- Simulate power stages, analog filters, feedback loops, and timing in ngspice before layout. Run parameter sweeps, optimize values, snap to standard E-series, and execute Monte Carlo yield runs.
- **Features to use**: ngspice analyses (`.op`, `.dc`, `.ac`, `.tran`, `.noise`, `.pz`), `.param` expressions, `.step` sweeps, `.meas` automated metrics, Monte Carlo loops, B-sources, XSPICE mixed-mode.
- **Pointer**: Read [ngspice.md](file:///C:/Users/Navan/.gemini/config/skills/hardware-product-design/references/ngspice.md) & [qucs-s.md](file:///C:/Users/Navan/.gemini/config/skills/hardware-product-design/references/qucs-s.md) before this stage.

### 5. PCB Layout & Routing (`hardware/<project>.kicad_pcb`)
- Configure physical stackup (4-layer Signal-GND-Power-Signal recommended) and design rules first. Place mounting holes/connectors to match enclosure, place critical ICs and decoupling caps, then route (Freerouting for first pass; manual routing for power loops, differential pairs, and RF).
- **Features to use**: Board setup, net classes, differential pair routing ($90\,\Omega$), length tuning meanders, copper zones, teardrops, Freerouting CLI (`-de board.dsn -do board.ses`), DRC verification (`kicad-cli pcb drc --severity-all --exit-code-violations --refill-zones`).
- **Pointer**: Read [kicad.md](file:///C:/Users/Navan/.gemini/config/skills/hardware-product-design/references/kicad.md), [freerouting.md](file:///C:/Users/Navan/.gemini/config/skills/hardware-product-design/references/freerouting.md), & [dfm-guidelines.md](file:///C:/Users/Navan/.gemini/config/skills/hardware-product-design/references/dfm-guidelines.md) before this stage.

### 6. 3D Mechanical Enclosure (`mech/`)
- Export PCB as STEP (`kicad-cli pcb export step --subst-models`). Author parametric enclosure (`build123d`, `CadQuery`, `FreeCAD`, or `OpenSCAD`) around the board with clearances for connectors, LEDs, buttons, and screw bosses. Run programmatic collision checks.
- **Features to use**: Parametric solids, boss pilot holes ($0.8 \times D_s$), wall shelling, thread engagement, programmatic Boolean intersection interference checks (`solid.intersect(pcb)`), STEP/STL exports.
- **Pointer**: Read [build123d.md](file:///C:/Users/Navan/.gemini/config/skills/hardware-product-design/references/build123d.md), [cadquery.md](file:///C:/Users/Navan/.gemini/config/skills/hardware-product-design/references/cadquery.md), [freecad.md](file:///C:/Users/Navan/.gemini/config/skills/hardware-product-design/references/freecad.md), [openscad.md](file:///C:/Users/Navan/.gemini/config/skills/hardware-product-design/references/openscad.md), & [enclosure-tolerances.md](file:///C:/Users/Navan/.gemini/config/skills/hardware-product-design/references/enclosure-tolerances.md) before this stage.

### 7. Thermal, Mechanical & RF Verification (`sim/`)
- Estimate power dissipation per component ($T_j = T_a + P \cdot \theta_{ja}$). Run CalculiX (`ccx`) or Elmer FEM thermal/stress analysis for enclosed products $>2\,\text{W}$. Run openEMS for antenna return loss ($S_{11}$) and RF microstrip impedance.
- **Features to use**: CalculiX (`ccx -i jobname`) linear static and heat transfer, Elmer multi-physics (`HeatSolver`, `StatElecSolver`), openEMS FDTD mesh and S-parameters.
- **Pointer**: Read [calculix.md](file:///C:/Users/Navan/.gemini/config/skills/hardware-product-design/references/calculix.md), [elmer.md](file:///C:/Users/Navan/.gemini/config/skills/hardware-product-design/references/elmer.md), & [openems.md](file:///C:/Users/Navan/.gemini/config/skills/hardware-product-design/references/openems.md) before this stage.

### 8. Firmware Scaffolding & Virtual Bring-up (`firmware/`)
- Scaffold firmware with PlatformIO. Sync `include/pins.h` directly to KiCad schematic netlist. Implement baseline self-test (ADC voltage checks, I2C scanner, heartbeat LED). Run headless peripheral simulation in Renode.
- **Features to use**: `platformio.ini` multi-environment configuration, `pio run`, `pio test`, `pio check`, Renode `.resc` scripts and `.repl` platform definitions.
- **Pointer**: Read [platformio.md](file:///C:/Users/Navan/.gemini/config/skills/hardware-product-design/references/platformio.md) & [renode.md](file:///C:/Users/Navan/.gemini/config/skills/hardware-product-design/references/renode.md) before this stage.

### 9. Fabrication Release & Production Package (`fab/`)
- Generate Gerbers, Excellon drill (PTH/NPTH separate), pick-and-place CPL, and formatted BOM. Panelize with KiKit for volume assembly. Automate exports with KiBot. Slice enclosures for 3D printing and render photorealistic graphics in Blender.
- **Features to use**: `kicad-cli pcb export gerbers|drill|pos|step|pdf`, KiKit panelization (`--layout`, `--tabs`, `--cuts`, `--framing`), KiBot `.kibot.yaml` CI pipeline, PrusaSlicer/OrcaSlicer CLI (`--export-gcode`), Blender headless Cycles rendering.
- **Pointer**: Read [kicad.md](file:///C:/Users/Navan/.gemini/config/skills/hardware-product-design/references/kicad.md), [kikit.md](file:///C:/Users/Navan/.gemini/config/skills/hardware-product-design/references/kikit.md), [kibot.md](file:///C:/Users/Navan/.gemini/config/skills/hardware-product-design/references/kibot.md), [slicers.md](file:///C:/Users/Navan/.gemini/config/skills/hardware-product-design/references/slicers.md), & [blender.md](file:///C:/Users/Navan/.gemini/config/skills/hardware-product-design/references/blender.md) before this stage.

### 10. Prototype Bring-Up Plan (`docs/bringup.md`)
- Prepare staged first-article bring-up checklist: cold resistance short-circuit checks, current-limited power supply startup ($50\,\text{mA}$ limit), voltage rail DMM probing, oscilloscope ripple verification, and SWD/JTAG debug probe connection.

---

## Tuning (Parameter Optimization)
- **Define specs numerically first**: e.g. ripple $<50\,\text{mV}$, cutoff $1\,\text{kHz} \pm 5\%$, rise time $<2\,\text{ms}$, phase margin $>45^\circ$.
- **Parameterize and sweep**: Automate ngspice or CAD scripts using Python (`scipy.optimize` or `pymoo` for multi-objective Pareto frontiers).
- **Monte Carlo tolerance analysis**: Sweep 500+ runs across component bounds ($\pm 1\%$ resistors, $\pm 10\%$ caps) and temperature drifts. Report worst-case 3-sigma yield.
- **E-Series snapping**: Snap continuous optimization outputs to real standard values (E24/E96) via `scripts/e_series_snapper.py` and re-simulate.

---

## Project Directory Layout
```
project/
  docs/        requirements.md, architecture.md, bringup.md
  hardware/    KiCad project (.kicad_pro, .kicad_sch, .kicad_pcb), libraries/
  mech/        build123d/CadQuery/FreeCAD/OpenSCAD sources, STEP, STL
  sim/         ngspice netlists (.cir), Python drivers, results/
  firmware/    PlatformIO project (platformio.ini, include/pins.h, src/)
  fab/         Gerbers, Excellon drill, BOM (.csv/.xlsx), CPL (.csv), panels
  scripts/     Python automation (build, DRC/ERC runners, sweeps, exports)
```

---

## Non-Negotiable Engineering Rules
- **Verification First**: Never claim a design is correct without running ERC, DRC, and simulations. Present actual CLI exit codes and violation summaries.
- **Zero Hallucinated Parts**: Do not invent part numbers, footprints, or datasheet ratings. If unverified, ask the user to confirm.
- **Safety Critical Isolation**: Flag mains voltage ($>48\,\text{V}$), unbuffered Li-ion charging, high currents ($>5\,\text{A}$), and RF regulatory bounds. Recommend qualified review.
- **Script-First Automation**: Prioritize CLI and headless scripted actions over GUI steps. If a GUI action is unavoidable, supply exact numbered instructions.
- **One Question at a Time**: Ask at most one concise clarifying question at a time, only when the answer fundamentally changes the design.
- **Stage Ledger**: Summarize each turn with what was accomplished, what files changed, and what task is next.

---

## Updating This Skill

To maintain and refresh this skill as tools evolve:
1. **Re-Run Inventory**: Run the discovery script to detect newly installed tools, updated paths, or version bumps:
   ```bash
   where.exe kicad-cli freerouting kibot kikit ngspice freecadcmd openscad ElmerSolver ccx openEMS blender pio renode prusa-slicer orca-slicer
   ```
2. **Re-Check Help & Official Docs**: Run `<tool> --help` and review official documentation for deprecated or newly added subcommands and flags.
3. **Update References**: Add or revise features in `references/<tool>.md`. Mark any unverified command as `UNVERIFIED`.
4. **Update Version Manifest**: Record updated tool version numbers, installation paths, and verification dates in [VERSIONS.md](file:///C:/Users/Navan/.gemini/config/skills/hardware-product-design/references/VERSIONS.md).
