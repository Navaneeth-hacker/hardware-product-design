# Electromagnetic Compatibility (EMC) & ESD Pre-Compliance Rules

Guidelines for designing circuits that pass FCC Part 15 Class B and CE RED emissions and immunity tests on the first board turn.

---

## 1. Ground Plane Continuity & Return Paths

- **Golden Rule**: High-frequency return current flows directly underneath the signal trace in the ground plane to minimize the enclosed loop area.
- **Never Split Reference Planes Under Signals**: Do not route traces across splits or voids in the ground plane. If a trace hops layers, place a ground return via immediately adjacent to the signal via ($\le 1\,\text{mm}$ center-to-center).
- **Ground Stitching**: For multi-layer boards, stitch copper fills together around the perimeter of the board at $\lambda/20$ intervals (approx. every $3 - 5\,\text{mm}$).

---

## 2. Decoupling Capacitor Placement & Loop Inductance

- Every power pin on microcontrollers, transceivers, and switching ICs requires dedicated decoupling.
- **Placement Sequence**: Power Rail $\rightarrow$ Bulk Capacitor ($4.7\,\mu\text{F}$) $\rightarrow$ Local Ceramic ($0.1\,\mu\text{F}$) $\rightarrow$ IC Pin.
- **Via Discipline**: Place the capacitor pads directly along the trace before entering the IC pin, with ground vias connected directly at the capacitor ground pad. Never route past the IC pin to reach the capacitor.

---

## 3. Electrostatic Discharge (ESD) Protection

- All external connectors (USB, audio jacks, buttons, programming headers, expansion ports) must have bidirectional or unidirectional TVS protection.
- **Placement**: Place TVS protection diodes **at the connector entrance**, before any series resistors, chokes, or IC pins.
- **Trace Routing**: The high-speed signal must enter the TVS diode pad directly. Do not stub to a TVS diode placed far away on the trace.
- **Ground Return**: Connect the TVS ground pin directly to the connector shield and chassis/digital ground using low-inductance vias.

---

## 4. Differential Pairs & High-Speed Traces (USB 2.0 / USB 3.0)

- **Target Impedance**:
  - USB 2.0 Full/High Speed: $90\,\Omega \pm 10\%$ differential impedance ($45\,\Omega$ single-ended).
- **Length Matching**:
  - Skew between $D+$ and $D-$ traces must be less than $1.25\,\text{mm}$ (approx. $8\,\text{ps}$ delay).
- **Isolation**:
  - Maintain $3\times$ dielectric height spacing from other high-speed or noisy signals (e.g. clock lines, switching nodes).
- **Common Mode Choke**:
  - Add an optional 0603 common-mode choke footprint in series with $D+/D-$ for USB interfaces failing radiated emissions.

---

## 5. Switching Regulators (Buck / Boost Converters)

- **Identify the High di/dt Loop**:
  - For a Buck converter: Input capacitor $\rightarrow$ High-side switch $\rightarrow$ Low-side switch/diode $\rightarrow$ Input capacitor ground.
  - Keep this loop perimeter under $10\,\text{mm}$ total length.
- **Switching Node (SW)**:
  - The SW pin copper area must be only as large as necessary to carry the current. Excessive copper turns the switching node into a broadcasting antenna.
- **Feedback Trace (FB)**:
  - Route the feedback trace far away from the inductor and SW node, preferably on the opposite side of a ground shielding plane.
