# Design For Manufacturing (DFM) Guidelines

Standard design rules for cost-effective PCB fabrication and automated SMT assembly (based on JLCPCB, PCBWay, and standard prototype fab capabilities).

---

## 1. PCB Fabrication Limits (Standard 2-Layer & 4-Layer)

| Parameter | Standard Fab Capability | Preferred / Safe Margin |
| :--- | :--- | :--- |
| **Minimum Trace Width** | 0.127 mm (5 mil) | 0.150 mm (6 mil) |
| **Minimum Trace Spacing** | 0.127 mm (5 mil) | 0.150 mm (6 mil) |
| **Minimum Via Drill Diameter** | 0.30 mm (12 mil) | 0.35 mm (14 mil) |
| **Minimum Via Pad Diameter** | 0.45 mm (18 mil) | 0.60 mm (24 mil) |
| **Minimum Annular Ring** | 0.13 mm (5 mil) | 0.15 mm (6 mil) |
| **Solder Mask Dam / Web** | 0.10 mm (4 mil) | 0.12 mm (5 mil) |
| **Solder Mask Expansion** | 0.05 mm (2 mil) | 0.05 mm (2 mil) |
| **Silkscreen Minimum Text Height** | 0.80 mm (32 mil) | 1.00 mm (40 mil) |
| **Silkscreen Line Width** | 0.15 mm (6 mil) | 0.18 mm (7 mil) |
| **Board Edge Clearance (Copper to Edge)** | 0.20 mm (8 mil) | 0.30 mm (12 mil) |
| **V-Cut Clearance (Copper to V-Cut Center)**| 0.40 mm (16 mil) | 0.50 mm (20 mil) |

---

## 2. Standard 4-Layer Stackup

Recommended for all mixed-signal, RF, or high-speed MCU designs (nominal board thickness $1.6\,\text{mm}$):

- **Layer 1 (Top Signal)**: Outer copper (1 oz, $35\,\mu\text{m}$) - High-speed signal routing, component placement.
- **Prepreg (Dielectric 1-2)**: ~0.21 mm thickness ($7628$ glass, $\varepsilon_r \approx 4.4$).
- **Layer 2 (Inner Plane 1)**: Solid continuous **Ground (GND)** plane ($0.5\,\text{oz}$, $17.5\,\mu\text{m}$).
- **Core (Dielectric 2-3)**: ~1.00 mm FR-4 dielectric.
- **Layer 3 (Inner Plane 2)**: **Power Plane (VCC/3V3)** and low-speed signal routing ($0.5\,\text{oz}$).
- **Prepreg (Dielectric 3-4)**: ~0.21 mm thickness.
- **Layer 4 (Bottom Signal)**: Outer copper (1 oz, $35\,\mu\text{m}$) - Secondary signals and ground flood.

---

## 3. SMT Assembly (PCBA) Rules

1. **Fiducial Markers**:
   - Place at least three 1.0 mm round bare copper fiducials (with 2.0 mm circular solder mask clearance) at non-symmetrical corners of the board.
   - For fine-pitch ICs (pitch $\le 0.5\,\text{mm}$ or QFN/BGA), place two local fiducials diagonally opposite the footprint.
2. **Component Orientation & Pin 1 Indicators**:
   - Every polarized component (diodes, electrolytic caps, ICs, LEDs) must have an unambiguous silkscreen marker visible after assembly.
   - For diodes: mark cathode clearly with a bar or band.
   - For ICs: dot or notch at Pin 1.
3. **Passive Component Sizing**:
   - Prefer **0603** ($1.6 \times 0.8\,\text{mm}$) or **0402** ($1.0 \times 0.5\,\text{mm}$) packages for basic passives. Avoid 0201 unless space is strictly constrained.
   - Ensure adequate solder mask between adjacent pads of 0402/0603 components to prevent solder bridging.
4. **Thermal Relief Pads**:
   - Connect through-hole pins and surface pads tied to large copper pours using 4-spoke thermal relief connections (spoke width $0.25 - 0.40\,\text{mm}$) to prevent heat siphoning during wave/reflow soldering.
