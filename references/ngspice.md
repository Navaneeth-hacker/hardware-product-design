# ngspice Comprehensive Simulation Reference

*Verified against official ngspice 43/44 syntax and KiCad bundled simulation engine.*

---

## 1. Analysis Types Overview

| Analysis | Directive Syntax | Purpose / When to Use | Typical Output Variables |
| :--- | :--- | :--- | :--- |
| **Operating Point** | `.op` | DC bias point, quiescent currents, node voltages. Always run first to confirm transistor operating regions. | `V(node)`, `I(Vsource)` |
| **DC Transfer Sweep**| `.dc SRC VSTART VSTOP VINCR` | Input-output transfer characteristics, voltage regulator dropout, comparator thresholds. | `V(out)` vs `V(in)` |
| **AC Small-Signal** | `.ac dec NP FSTART FSTOP` | Frequency response, filter transfer functions, gain and phase margins (Bode plot), audio band analysis. | `vdb(out)`, `cph(out)`, `vp(out)` |
| **Transient** | `.tran TSTEP TSTOP [TSTART [TMAX]]` | Time-domain behavior, switching waveforms, ripple voltage, turn-on inrush current, digital clock edges. | `V(out)` vs `time` |
| **Noise** | `.noise V(OUT) SRC dec NP FSTART FSTOP` | Total output noise and input-referred noise spectral density over frequency. Crucial for sensor AFEs. | `onoise_spectrum`, `inoise_spectrum`, `onoise_total` |
| **Transfer Function**| `.tf V(OUT) SRC` | Small-signal DC gain, input resistance, and output resistance without full AC sweep. | `Transfer_function`, `Input_impedance`, `Output_impedance` |
| **Pole-Zero** | `.pz IN_POS IN_NEG OUT_POS OUT_NEG vol pz`| Computes poles and zeros of transfer function to verify unconditional stability. | Complex poles/zeros $(s = \sigma + j\omega)$ |
| **Sensitivity** | `.sens V(OUT)` | DC small-signal sensitivity of output voltage with respect to every resistor, capacitor, and source. | Normalized sensitivity coefficients |
| **Distortion** | `.disto dec NP FSTART FSTOP [F2/F1]` | Harmonic distortion (HD2, HD3) and intermodulation products for audio/analog signal paths. | `hd2`, `hd3`, `sim2`, `dim2` |

---

## 2. Advanced Directives & Measurement

### Parameters & Sweeps (`.param`, `.step`)
- **Parameter Declaration**:
  ```spice
  .param Rval=10k Cval=100n Cutoff={1/(2*pi*Rval*Cval)}
  R1 in out {Rval}
  C1 out 0   {Cval}
  ```
- **Stepping Values**:
  ```spice
  .step param Rval 1k 50k 5k
  ```

### Automated Measurements (`.meas`)
Extract scalar metrics directly from simulation curves:
- **Measure Cutoff Frequency ($-3\,\text{dB}$ point)**:
  ```spice
  .meas ac f_3db when vdb(out)=-3
  ```
- **Measure Peak-to-Peak Ripple**:
  ```spice
  .meas tran v_ripple PP v(vout) from=5m to=10m
  ```
- **Measure Rise Time (10% to 90%)**:
  ```spice
  .meas tran t_rise trig v(out) val=0.33 rise=1 targ v(out) val=2.97 rise=1
  ```
- **Average Current / Power Consumption**:
  ```spice
  .meas tran avg_power avg {v(vcc)*i(Vmeas)} from=1m to=10m
  ```

---

## 3. Monte Carlo & Tolerance Analysis

Using `.control` blocks with pseudo-random distributions to simulate 500+ production board iterations:

```spice
* Low-pass filter Monte Carlo 100 runs
V1 in 0 dc 0 ac 1
R1 in out 10k
C1 out 0 100n
.param Rnom=10k Cnom=100n

.control
  let mc_runs = 100
  let run = 1
  let f_cut = vector(mc_runs)
  
  dowhile run <= mc_runs
    * Resistor 1% gaussian, Cap 10% uniform
    alter R1 = Rnom * (1 + 0.01 * gauss(0))
    alter C1 = Cnom * (1 + 0.10 * (2*unif(0)-1))
    
    run
    meas ac fc when vdb(out)=-3
    let f_cut[run-1] = fc
    let run = run + 1
  end
  
  echo "--- Monte Carlo Complete ---"
  print f_cut
  wrdata mc_results.csv f_cut
.endc
```

---

## 4. Temperature Sweeps

Test circuit performance over industrial temperature envelopes:
```spice
.temp -40 -20 0 25 50 85 105
.tran 10u 10m
```
Individual component temperature coefficients:
```spice
R1 in out 10k tc1=100e-6 tc2=1e-9  ; 100 ppm/°C linear, 1 ppb/°C quadratic
```

---

## 5. Non-Linear Behavioral Sources (B-Sources)

Arbitrary algebraic voltage and current generators:
- **Instantaneous Non-Linear Voltage Source**:
  ```spice
  B1 out 0 V = V(in) > 2.5 ? 5.0 : 0.0                      ; Ideal comparator
  B2 out 0 V = V(ctrl) * sin(2 * pi * 1000 * time)         ; Modulator
  B3 out 0 V = sqrt(pow(V(a), 2) + pow(V(b), 2))           ; True RMS vector sum
  ```
- **Non-Linear Current Source**:
  ```spice
  Bload vcc 0 I = 0.05 + 0.5 * (time > 2m)                 ; Dynamic load step (50mA to 550mA at t=2ms)
  ```

---

## 6. XSPICE Mixed-Mode Simulation

Enables analog circuits to interact with digital logic gates, D-flip-flops, state machines, and ADC/DAC converters without CPU-heavy analog approximations:
```spice
* A-device: 8-bit Analog-to-Digital Converter
a_adc in clk_in [b7 b6 b5 b4 b3 b2 b1 b0] adc_8bit
.model adc_8bit adc_bridge(in_low=0.5 in_high=2.5 rise_delay=10n)

* Digital Logic Gate (AND gate)
a_and [b7 b6] and_out my_and
.model my_and d_and(rise_delay=5n fall_delay=5n)
```

---

## 7. Batch Mode Execution & Data Export

Run simulations headlessly in automated scripts:
```bash
# 1. Batch mode execution with raw binary output
ngspice -b -r sim/results/output.raw -o sim/results/sim.log sim/circuits/power_stage.cir

# 2. Exporting CSV directly inside a .control block
.control
  run
  set filetype=ascii
  wrdata sim/results/transient.csv v(vin) v(vout) i(L1)
.endc
```

Parsing `.raw` files in Python:
```python
from PySpice.Spice.Parser import SpiceParser
from PySpice.Spice.Netlist import Circuit
# or read CSV directly with polars/pandas
import polars as pl
df = pl.read_csv("sim/results/transient.csv", separator=" ")
```
