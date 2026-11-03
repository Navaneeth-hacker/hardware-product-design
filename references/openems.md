# openEMS Electromagnetic & RF Field Solver Reference

*Finite-Difference Time-Domain (FDTD) full-wave 3D electromagnetic field solver.*

---

## 1. Overview & RF Applications

openEMS simulates Maxwell's equations in the time domain. Key applications in hardware product design:
- **Trace Impedance & Return Paths**: Extracting characteristic impedance ($Z_0$) and signal integrity for microstrip and stripline transmission lines.
- **Antenna Design**: Matching networks, return loss ($S_{11}$), bandwidth, and 3D radiation patterns for PCB antennas (2.4 GHz BLE/Wi-Fi meander, inverted-F / IFA, patch antennas).
- **Crosstalk & Coupling**: Near-field coupling ($S_{21}$) between adjacent high-speed traces and switching converters.
- **Filter Performance**: S-parameter extraction ($S_{11}$, $S_{21}$, $S_{12}$, $S_{22}$) for microstrip filters and power dividers.

---

## 2. Python Scripting Workflow (`openEMS` + `CSXCAD`)

```python
import os
import numpy as np
from CSXCAD import ContinuousStructure
from openEMS import openEMS

# 1. Initialize FDTD and CSX Structures
openEMS_grid = openEMS(EndCriteria=1e-5)
CSX = ContinuousStructure()

# 2. Define Frequency Range & Excitation
f0 = 2.45e9  # 2.45 GHz center frequency
fc = 1.0e9   # 1.0 GHz bandwidth
openEMS_grid.SetGaussExcite(f0, fc)

# 3. Define Boundary Conditions
# PML (Perfect Matched Layer) absorbs outgoing waves (free space radiation)
openEMS_grid.SetBoundaryCond(['PML_8', 'PML_8', 'PML_8', 'PML_8', 'PML_8', 'PML_8'])

# 4. Define Materials
# Substrate (FR4: er=4.4, tand=0.02)
fr4 = CSX.AddMaterial('FR4', epsilon=4.4)
# Conductor (Copper)
copper = CSX.AddMetal('Copper')

# 5. Add Geometry Primitives
# Substrate Box: 50mm x 30mm x 1.6mm
fr4.AddBox(priority=1, start=[-25, -15, 0], stop=[25, 15, 1.6])
# Ground Plane on Bottom Face
copper.AddBox(priority=10, start=[-25, -15, 0], stop=[25, 15, 0])
# Microstrip Trace on Top Face (width 3.0mm for ~50 Ohm)
copper.AddBox(priority=10, start=[-25, -1.5, 1.6], stop=[25, 1.5, 1.6])

# 6. Setup Mesh (Discretization)
# Rule of thumb: max cell size <= lambda / 20 in dielectric
lambda_min = 3e8 / ((f0 + fc) * np.sqrt(4.4))
max_res = lambda_min / 20.0 * 1000  # in mm
CSX.AddGrid('x', np.arange(-30, 30, max_res))
CSX.AddGrid('y', np.arange(-20, 20, max_res))
CSX.AddGrid('z', np.arange(-5, 10, max_res))

# 7. Add Ports (MSL Port for S-Parameters)
port = openEMS_grid.AddMSLPort(
    port_nr=1,
    metal_material=copper,
    start=[-20, -1.5, 1.6],
    stop=[-15, 1.5, 0],
    dir='x',
    excite=1.0
)

# 8. Run Headless Simulation
sim_dir = "sim/openems_microstrip"
os.makedirs(sim_dir, exist_ok=True)
openEMS_grid.Run(sim_dir)

# 9. Extract S-Parameters ($S_{11}$)
port.CalcPort(sim_dir, np.linspace(f0 - fc, f0 + fc, 201))
s11_db = 20 * np.log10(np.abs(port.uf_ref / port.uf_inc))
print(f"Minimum S11: {s11_db.min():.2f} dB at 2.45 GHz")
```

---

## 3. Far-Field Antenna Radiation Pattern

Extract 3D gain, directivity, and radiation efficiency:
```python
# Setup Far-field recording box (Nf2F: Near-field to Far-field transformation)
nf2ff = openEMS_grid.CreateNF2FFBox()

# Post-processing after run
theta = np.linspace(0, np.pi, 181)
phi = np.linspace(0, 2*np.pi, 361)
E_far = nf2ff.CalcNF2FF(sim_dir, f0, theta, phi)
directivity_dbi = 10 * np.log10(E_far.Dmax)
print(f"Antenna Peak Directivity: {directivity_dbi:.2f} dBi")
```
