# Enclosure Design & Mechanical Tolerances

Rules for designing 3D enclosures that mate cleanly with KiCad PCBs and standard hardware fasteners.

---

## 1. Process Clearance Tolerances (Diametral & Surface)

When modeling housings around a physical PCB, apply clearances based on the fabrication process:

| Process | Typical Machine | PCB Edge Clearance | Connector Hole Clearance | Snap-Fit Interference |
| :--- | :--- | :--- | :--- | :--- |
| **FDM 3D Printing** | Prusa MK4, Bambu Lab X1 | $+0.40\,\text{mm}$ | $+0.40\,\text{mm}$ | $0.25 - 0.35\,\text{mm}$ |
| **SLA / Resin** | Formlabs, Elegoo | $+0.20\,\text{mm}$ | $+0.20\,\text{mm}$ | $0.15 - 0.20\,\text{mm}$ |
| **SLS Nylon** | EOS, Formlabs Fuse | $+0.30\,\text{mm}$ | $+0.30\,\text{mm}$ | $0.25\,\text{mm}$ |
| **CNC Aluminum** | 3-axis mill | $+0.15\,\text{mm}$ | $+0.15\,\text{mm}$ | N/A (bolt / gasket) |
| **Injection Mold** | Steel / Aluminum tool | $+0.20\,\text{mm}$ | $+0.20\,\text{mm}$ | $0.30\,\text{mm}$ (1° draft) |

---

## 2. Fastener Boss Sizing (Self-Tapping & Threaded Inserts)

### A. Thermoplastic Self-Tapping Screws (Plastite / Delta PT)

For screws driven directly into 3D printed or molded plastic:

- **Screw Nominal Diameter ($D_s$)**: e.g., M2 ($2.0\,\text{mm}$), M2.5 ($2.5\,\text{mm}$), M3 ($3.0\,\text{mm}$).
- **Pilot Hole Diameter ($D_h$)**: $0.80 \times D_s$ (e.g. for M2: $1.60\,\text{mm}$; for M3: $2.40\,\text{mm}$).
- **Boss Outer Diameter ($D_b$)**: $2.0 \times D_s$ to $2.2 \times D_s$ (e.g. for M2: $4.0 - 4.4\,\text{mm}$).
- **Thread Engagement Depth**: At least $2.5 \times D_s$ (e.g. for M2: $\ge 5.0\,\text{mm}$).

### B. Heat-Set Brass Threaded Inserts

For reusable machine screws (standard M2, M2.5, M3 socket head cap screws):

- **Hole Taper**: 8° taper or straight hole according to the insert vendor spec.
- **Hole Diameter**: Outer diameter of insert body before knurling (typically nominal $+0.1\,\text{mm}$).
- **Wall Thickness Around Insert**: Minimum $1.5 \times$ hole radius to prevent boss cracking during insertion.

---

## 3. Wall Thickness & Structural Guidelines

- **FDM 3D Printing**:
  - Minimum wall thickness: $1.6\,\text{mm}$ (4 perimeter walls with a 0.4mm nozzle).
  - Recommended general wall: $2.0 - 2.4\,\text{mm}$.
- **Cantilever Snap-Fits**:
  - Keep beam strain below 2% for PLA/PETG ($1.5\%$ for brittle materials).
  - Taper beam thickness from base to tip to distribute bending stress evenly.
  - Add generous fillet radius ($R \ge 0.5 \times t$) at the root of the snap beam to eliminate stress concentration.

---

## 4. PCB Mounting Hole Standard Clearances

- **M2 Screw**: Hole in PCB = $2.2\,\text{mm}$ diameter. Keep-out zone around hole = $4.5\,\text{mm}$ (screw head + washer clearance).
- **M2.5 Screw**: Hole in PCB = $2.7\,\text{mm}$ diameter. Keep-out zone = $5.5\,\text{mm}$.
- **M3 Screw**: Hole in PCB = $3.2\,\text{mm}$ diameter. Keep-out zone = $6.5\,\text{mm}$.
- No surface-mount components, vias, or traces may enter the mounting hole keep-out zone on any copper layer.
