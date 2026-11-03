# Qucs-S Circuit & RF Simulation Reference

*GUI schematic and multi-engine simulation interface supporting ngspice, Qucsator, and Xyce backends.*

---

## 1. Overview & Advantages

Qucs-S (Qucs with SPICE) bridges the intuitive GUI schematic capture of Qucs with industrial SPICE simulation backends (principally **ngspice**):
- **Universal Simulation Engine**: Allows switching between ngspice (transient/noise), Qucsator (S-parameter RF networks), and Xyce (large-scale parallel transient).
- **RF & Microwave Blocks**: Dedicated microstrip lines, coupled lines, attenuators, bias tees, and S-parameter multiport blocks.
- **Harmonic Balance (HB)**: Nonlinear RF frequency-domain analysis for power amplifiers, mixers, and oscillators (when paired with compatible solver engines).

---

## 2. Supported Analyses

| Analysis Type | Backend Engine | Application |
| :--- | :--- | :--- |
| **S-Parameter Simulation** | Qucsator / ngspice | Multi-port network analysis, return loss ($S_{11}$), insertion loss ($S_{21}$), Smith chart plotting. |
| **DC & AC Sweep** | ngspice | Bias point verification, frequency response, Bode plots. |
| **Transient Analysis** | ngspice | Time-domain waveform analysis, clock jitter, switching transitions. |
| **Noise Analysis** | ngspice | Noise figure (NF) and equivalent noise temperature across frequency. |
| **Parameter Sweep** | ngspice / Qucsator | Sweeping component values, bias voltages, or temperatures across sub-simulations. |

---

## 3. Headless & Batch Execution

Qucs-S schematics (`.sch`) can be exported to standard ngspice netlists for headless automated simulation in CI/CD pipelines:

```bash
# 1. Export SPICE netlist from Qucs-S schematic (GUI or script converter)
# 2. Run simulation headlessly with ngspice
ngspice -b -r sim/results/rf_filter.raw -o sim/results/rf_filter.log sim/circuits/rf_filter.cir
```

### Typical S-Parameter Simulation Netlist Snippet
```spice
* 2-Port S-Parameter Analysis in ngspice
V1 in 0 dc 0 port 1 z0=50
R1 in out 50
C1 out 0 10p
P2 out 0 port 2 z0=50

.control
  sp dec 100 1Meg 1G 50
  wrdata sim/results/sparam.csv s_1_1 s_2_1
.endc
.end
```
