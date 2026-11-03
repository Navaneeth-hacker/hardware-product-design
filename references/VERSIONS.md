# Tool Inventory & Version Tracking

Last audit date: November 2026  
Platform: Windows 11 (x86_64)  
Workspace directory: `C:\Users\Navan`  
Skill directory: `C:\Users\Navan\.gemini\config\skills\hardware-product-design`

---

## 1. Installed Tools (Verified on Local System)

| Tool | Component | Installed Version | Executable Path / Location | Verification Method |
| :--- | :--- | :--- | :--- | :--- |
| **KiCad** | `kicad-cli` | `10.0.6` | `C:\Program Files\KiCad\10.0\bin\kicad-cli.exe` | Verified via `kicad-cli version` |
| **KiCad GUI** | `pcbnew`, `eeschema` | `10.0.6` | `C:\Program Files\KiCad\10.0\bin\kicad.exe` | Verified via `kicad-cli --version` |
| **KiCad Python** | `pcbnew` Python API | `10.0.6` | `C:\Program Files\KiCad\10.0\bin\python.exe` | Verified via `import pcbnew; pcbnew.GetBuildVersion()` |
| **FreeCAD** | `freecadcmd` | `1.1.4 (Rev 20260928)` | `C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe` | Verified via `freecadcmd.exe --version` |
| **CalculiX** | `ccx` (FEA Solver) | `2.22` | `C:\Program Files\FreeCAD 1.1\bin\ccx.exe` | Verified via `ccx.exe -v` (bundled in FreeCAD) |
| **Gmsh** | `gmsh` (Mesh Generator) | Bundled | `C:\Program Files\FreeCAD 1.1\bin\gmsh.exe` | Verified binary in FreeCAD bin |
| **Blender** | `blender` | `5.2.2 LTS` | `C:\Program Files\Blender Foundation\Blender 5.2\blender.exe` | Verified via `blender.exe --version` & `bpy` API |
| **ngspice (dll)** | `ngspice.dll` | Bundled in KiCad | `C:\Program Files\KiCad\10.0\bin\ngspice.dll` | Verified DLL in KiCad bin |
| **Python 3** | System Python | `3.13.14` | System PATH | Verified via `python --version` |
| **NumPy** | Python package | `2.5.4` (Sys) / `1.26.4` (FC) | System Python & FreeCAD Python | Verified via `import numpy; numpy.__version__` |
| **SciPy** | Python package | `1.18.1` (Sys) / `1.16.3` (FC)| System Python & FreeCAD Python | Verified via `import scipy; scipy.__version__` |

---

## 2. Missing Tools & Installation Instructions

The following tools are not yet installed on this system. **Do not install anything without user consent.**

### `ngspice` (Standalone CLI)
- **Status**: MISSING standalone CLI `ngspice.exe` (KiCad bundles `ngspice.dll` internally for schematic simulation).
- **How to install**:
  - Download official Windows 64-bit release from SourceForge: `https://sourceforge.net/projects/ngspice/files/ng-spice-rework/`
  - Unpack to `C:\tools\ngspice` and add `C:\tools\ngspice\Spice64\bin` to user PATH.
  - Or via Chocolatey: `choco install ngspice`
  - Or via Scoop: `scoop install ngspice`

### `build123d` & `cadquery` (Python CAD)
- **Status**: MISSING in Python environment.
- **How to install**:
  - `python -m pip install "build123d>=0.11.1"`
  - `python -m pip install "cadquery>=2.5.0"`
  - *Note: Requires `cadquery-ocp` OpenCascade kernel wheel.*

### `openscad`
- **Status**: MISSING.
- **How to install**:
  - Download installer from `https://openscad.org/downloads.html`
  - Or via Winget: `winget install OpenSCAD.OpenSCAD`
  - Or via Scoop: `scoop install openscad`

### `freerouting`
- **Status**: MISSING.
- **How to install**:
  - Requires Java Runtime Environment (JRE 17+ or 21+).
  - Download `freerouting-executable.jar` from `https://github.com/freerouting/freerouting/releases`.
  - Save to `C:\tools\freerouting\freerouting.jar` and invoke with `java -jar freerouting.jar`.

### `kibot` & `kikit`
- **Status**: MISSING.
- **How to install**:
  - KiBot: `python -m pip install kibot` (requires KiCad Python or Linux container/WSL for best compatibility).
  - KiKit: `python -m pip install kikit` (works directly with KiCad PCB files).

### `ElmerSolver` & `ElmerGrid`
- **Status**: MISSING.
- **How to install**:
  - Download Windows installer from CSC: `http://www.nic.funet.fi/pub/sci/physics/elmer/bin/windows/`
  - Run `Elmerfem-gui-mpi-Windows-AMD64.exe` to install to `C:\Program Files\Elmer 9.0`.

### `openEMS`
- **Status**: MISSING.
- **How to install**:
  - Download Windows 64-bit binaries from `https://openems.de/start/download.php`
  - Extract and run `setup.m` or configure Python bindings: `pip install openEMS CSXCAD`.

### `qucs-s`
- **Status**: MISSING.
- **How to install**:
  - Download Windows installer from `https://ra3xdh.github.io/` or GitHub releases: `https://github.com/ra3xdh/qucs_s/releases`.
  - Connects to `ngspice` as simulation backend.

### `platformio`
- **Status**: MISSING.
- **How to install**:
  - Install via pip: `python -m pip install -U platformio`
  - Or standalone installer: `curl -fsSL -o get-platformio.py https://raw.githubusercontent.com/platformio/platformio-core-installer/master/get-platformio.py && python get-platformio.py`

### `renode`
- **Status**: MISSING.
- **How to install**:
  - Download Windows MSI installer from `https://github.com/renode/renode/releases`.
  - Or via Scoop: `scoop install renode`.

### `orcaslicer` / `prusa-slicer`
- **Status**: MISSING.
- **How to install**:
  - PrusaSlicer: `winget install Prusa3D.PrusaSlicer` or download from `https://www.prusa3d.com/page/prusaslicer_424/`. Provides `prusa-slicer-console.exe`.
  - OrcaSlicer: `winget install SoftFever.OrcaSlicer` or download from `https://github.com/SoftFever/OrcaSlicer/releases`.
