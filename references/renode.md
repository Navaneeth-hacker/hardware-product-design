# Renode System Emulation & Virtual Bring-Up Reference

*Virtual development framework for multi-node embedded networks and bare-metal MCUs.*

---

## 1. Overview & Virtual Bring-Up

Renode emulates physical microcontrollers (ARM Cortex-M0/M3/M4/M7, RISC-V, ESP32), memory mappings, and peripheral buses (UART, I2C, SPI, CAN, Ethernet) directly from compiled ELF binaries. This enables continuous integration testing of firmware **before physical PCBs are manufactured**.

---

## 2. Command Line Execution (Headless CI Mode)

```bash
# 1. Run Renode headless with a test script and auto-exit
renode --disable-gui --console -e "i @sim/scripts/bringup.resc; start; emu Sleep 5; quit"

# 2. Run Renode headless exposing Monitor CLI on network socket (Port 1234)
renode --disable-gui -P 1234 -e "i @sim/scripts/bringup.resc; start"

# 3. Clean CI execution with no ANSI color escape codes
renode --disable-gui --console -p -e "i @sim/scripts/automated_test.resc"
```

### Verified CLI Flags
| Flag | Description |
| :--- | :--- |
| `--disable-gui` (or `--disable-xwt`) | Disables all graphical windows, analyzers, and monitor popups. |
| `--console` | Runs the Renode monitor directly inside the current terminal console. |
| `-e "<COMMAND>"` | Executes a Monitor command at startup (can be repeated). |
| `-P <PORT>` | Opens a network socket for remote Telnet monitor interaction (e.g. `-P 1234`). |
| `-p` | Strips terminal color formatting for clean CI log files. |

---

## 3. Platform Description (`.repl`)

Defines the hardware memory map, registers, interrupts, and peripherals matching the schematic:

```repl
// --- stm32f4_custom.repl ---
using "platforms/cpus/stm32f401.repl"

// External I2C Temperature Sensor on I2C1 bus
sensor_temp: Sensors.TMP102 @ i2c1 0x48
    Temperature: 28.5

// Status LED on GPIO Port C Pin 13
led_status: Miscellaneous.LED @ gpioPortC 13
```

---

## 4. Renode Script (`.resc`)

Orchestrates machine initialization, loads firmware binaries, and configures GDB debug stubs:

```resc
# --- bringup.resc ---
# 1. Clear previous emulation
mach clear

# 2. Create Machine
mach create "MyBoard"
machine LoadPlatformDescription @sim/platforms/stm32f4_custom.repl

# 3. Route UART1 output to terminal console
showAnalyzer sysbus.usart1

# 4. Load compiled firmware ELF
sysbus LoadELF @firmware/.pio/build/stm32_debug/firmware.elf

# 5. Enable GDB Server on Port 3333
machine StartGdbServer 3333

# 6. Start Emulation
echo "Starting virtual board emulation..."
start
```
