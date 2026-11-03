# Hardware Product Design

An open-source-toolchain skill for designing physical electronic products from requirements through prototyping and fabrication. It provides a central workflow and tool router in [`SKILL.md`](SKILL.md), detailed guides in [`references/`](references/), and small Python command-line utilities in [`scripts/`](scripts/).

This repository is a design reference and set of engineering helpers, not a complete hardware project or a packaged application. Use the workflow and tools that fit the product; verify design outputs with the relevant engineering tools before relying on them.

## What it covers

- Requirements, system architecture, schematics, and PCB layout with KiCad
- Circuit simulation and component-value tuning with ngspice and Qucs-S
- Parametric enclosure design with build123d, CadQuery, FreeCAD, or OpenSCAD
- Thermal, structural, and electromagnetic analysis
- Firmware workflows with PlatformIO and Renode
- Fabrication exports, panelization, rendering, and 3D-print slicing
- DFM, EMC/ESD, and enclosure-tolerance considerations

The recommended end-to-end sequence is: requirements → architecture → schematic → simulation and tuning → PCB layout and DRC → enclosure → verification → firmware → fabrication release → prototype bring-up. See [`SKILL.md`](SKILL.md) for stage-by-stage guidance and engineering rules.

## Repository layout

```text
.
├── SKILL.md
├── references/       Tool guides, standards, and tool-version inventory
└── scripts/
    ├── e_series_snapper.py
    ├── kicad_automation.py
    └── thermal_calculator.py
```

## Using the skill

Read [`SKILL.md`](SKILL.md) first. It describes when to use the skill, how to select the relevant reference guides, and what information and checks belong in each design stage. Before starting tool-dependent work, check [`references/VERSIONS.md`](references/VERSIONS.md) and confirm the installed tools are available. The listed installations and versions are specific to the machine on which that inventory was recorded.

Each guide under [`references/`](references/) covers a tool or engineering topic. For example:

- PCB design and routing: [`kicad.md`](references/kicad.md), [`freerouting.md`](references/freerouting.md)
- Simulation: [`ngspice.md`](references/ngspice.md), [`qucs-s.md`](references/qucs-s.md)
- Enclosures: [`build123d.md`](references/build123d.md), [`cadquery.md`](references/cadquery.md), [`freecad.md`](references/freecad.md), [`openscad.md`](references/openscad.md)
- Design constraints: [`dfm-guidelines.md`](references/dfm-guidelines.md), [`emc-esd-rules.md`](references/emc-esd-rules.md), [`enclosure-tolerances.md`](references/enclosure-tolerances.md)

## Python utilities

The scripts use only the Python standard library. Run them with Python 3 from the repository root; use `python` or the appropriate Python executable for your system.

### Thermal and trace calculator

[`scripts/thermal_calculator.py`](scripts/thermal_calculator.py) estimates junction temperature, required heatsink-to-ambient thermal resistance, or PCB trace width.

```sh
python scripts/thermal_calculator.py junction --power 2 --rja 30 --ambient 25
python scripts/thermal_calculator.py heatsink --power 5 --rjc 2 --ambient 40
python scripts/thermal_calculator.py trace --current 2 --rise 10 --copper 1
```

Add `--internal` to the `trace` command for an internal PCB layer. These are estimates; confirm thermal design and trace sizing against applicable standards, manufacturer data, and the actual board construction.

### E-series value snapper

[`scripts/e_series_snapper.py`](scripts/e_series_snapper.py) snaps a positive target value to the nearest supported E12, E24, or E96 nominal value and reports relative error.

```sh
python scripts/e_series_snapper.py --value 4732.5 --series E96 --unit Ohm
```

### KiCad automation

[`scripts/kicad_automation.py`](scripts/kicad_automation.py) wraps KiCad CLI operations for schematic ERC, board DRC, and fabrication exports. It requires `kicad-cli` to be on `PATH` or installed in one of the Windows locations searched by the script.

```sh
python scripts/kicad_automation.py erc path\to\design.kicad_sch
python scripts/kicad_automation.py drc path\to\design.kicad_pcb
python scripts/kicad_automation.py export path\to\design.kicad_pcb --out fab
```

The export command writes Gerbers, drill files, a component-placement CSV, and a STEP model to the output directory. Review ERC/DRC results and inspect all manufacturing outputs before release.

## Safety and verification

Calculations and documented workflows are aids, not certification or proof of a safe design. Follow the verification rules in [`SKILL.md`](SKILL.md), validate with the relevant simulation and design checks, and obtain qualified review for hazardous voltages, high currents, battery charging, or regulated RF designs. Do not install tools without user consent.
