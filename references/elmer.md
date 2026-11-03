# Elmer FEM Multiphysics Reference

*Finite Element Multiphysics suite developed by CSC (IT Center for Science).*

---

## 1. Supported Physics Modules

Elmer handles coupled multi-physics through dedicated solver modules:

| Physics Domain | Solver Name | Typical Hardware Use Case |
| :--- | :--- | :--- |
| **Heat Transfer** | `HeatSolver` | Heat conduction in multi-layer PCBs, thermal relief via arrays, heat dissipation inside enclosed plastic cases. |
| **Electrostatics** | `StatElecSolver` | Parasitic capacitance extraction between PCB traces, sensor electrode coupling. |
| **Magnetostatics** | `StatMagSolver` | Inductance of planar inductors, magnetic flux leakage from switching transformers. |
| **Solid Mechanics** | `StressAnalysis` | Stress distribution, snap-fit strain, drop test impact deformation. |
| **Navier-Stokes** | `FlowSolve` | Airflow convection cooling around heatsinks in ventilated enclosures. |

---

## 2. Mesh Conversion Flow (`ElmerGrid`)

Elmer requires geometry meshed into volume and boundary elements. Typically, meshes are authored in FreeCAD, Gmsh, or Salome:

```bash
# Convert a Gmsh 3D mesh (.msh) to Elmer mesh format
ElmerGrid 14 2 model.msh -autoclean -out mesh/
```
- Format code `14`: Gmsh format.
- Format code `2`: Elmer mesh directory (`mesh.header`, `mesh.nodes`, `mesh.elements`, `mesh.boundary`).
- `-autoclean`: Eliminates duplicate nodes and fixes degenerate elements.

---

## 3. Solver Input File (`case.sif`) Structure

The `.sif` file controls material assignments, equations, and boundary conditions:

```sif
Header
  CHECK KEYWORDS Warn
  Mesh DB "." "mesh"
  Include Path ""
  Results Directory "results"
End

Simulation
  Max Output Level = 5
  Coordinate System = Cartesian 3D
  Coordinate Mapping(3) = 1 2 3
  Simulation Type = Steady State
  Steady State Max Iterations = 1
  Output Intervals = 1
  Post File = "case.vtu"  ! Output format for ParaView visualization
End

Constants
  Gravity(4) = 0 -1 0 9.82
  Stefan Boltzmann = 5.670374e-8
  Permittivity of Vacuum = 8.854187e-12
End

Body 1
  Target Bodies(1) = 1
  Name = "PCB_Substrate"
  Equation = 1
  Material = 1
  Initial Condition = 1
End

Material 1
  Name = "FR4"
  Heat Conductivity = 0.3      ! W/(m*K)
  Density = 1850.0             ! kg/m^3
  Heat Capacity = 1200.0       ! J/(kg*K)
End

Equation 1
  Name = "Heat_Conduction"
  Active Solvers(1) = 1
End

Solver 1
  Equation = "Heat Equation"
  Procedure = "HeatSolve" "HeatSolver"
  Variable = "Temperature"
  Linear System Solver = Iterative
  Linear System Iterative Method = BiCGStab
  Linear System Max Iterations = 500
  Linear System Convergence Tolerance = 1.0e-8
  Linear System Preconditioning = ILU1
  Steady State Convergence Tolerance = 1.0e-5
End

Initial Condition 1
  Name = "Ambient_Start"
  Temperature = 298.15         ! 25°C in Kelvin
End

Boundary Condition 1
  Target Boundaries(1) = 2
  Name = "MCU_Heat_Source"
  Heat Flux = 15000.0          ! W/m^2 heat dissipation
End

Boundary Condition 2
  Target Boundaries(1) = 3
  Name = "Convective_Air_Cooling"
  Heat Transfer Coefficient = 10.0  ! W/(m^2*K) natural convection
  External Temperature = 298.15     ! Ambient temperature (K)
End
```

---

## 4. Headless Execution & Post-Processing

```bash
# Execute ElmerSolver in batch mode
ElmerSolver case.sif
```

Results are saved to `results/case.vtu`. Inspect with ParaView or Python `pyvista`:
```python
import pyvista as pv

mesh = pv.read("results/case.vtu")
temp = mesh["Temperature"]
print(f"Peak Junction Temperature: {temp.max() - 273.15:.1f} °C")
```
