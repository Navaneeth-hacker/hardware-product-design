# PlatformIO Embedded Firmware Reference

*Next-generation open-source ecosystem for embedded development and IoT.*

---

## 1. Project Initialization & Structure

Initialize firmware projects headlessly from the command line:

```bash
# Initialize project for STM32F401 Blackpill using CMSIS / STM32Cube framework
pio project init --board blackpill_f401ce --framework stm32cube -d firmware/

# Initialize project for ESP32-S3 using ESP-IDF framework
pio project init --board esp32-s3-devkitc-1 --framework espidf -d firmware/

# Initialize project for Raspberry Pi Pico RP2040 using Arduino core
pio project init --board pico --framework arduino -d firmware/
```

Standard Project Layout:
```
firmware/
├── platformio.ini       # Build environments, dependencies, upload/debug flags
├── include/
│   └── pins.h           # Hardware pinout contract mapped to KiCad netlist
├── src/
│   └── main.c / .cpp
├── lib/                 # Private project-specific peripheral driver libraries
└── test/                # Unit test suites (Unity framework)
```

---

## 2. Configuration (`platformio.ini`)

Multi-target, multi-environment configuration:

```ini
[platformio]
default_envs = stm32_debug

[env]
monitor_speed = 115200
build_flags = 
    -Wall -Wextra
    -D PROJECT_REV_A

[env:stm32_debug]
platform = ststm32
board = blackpill_f401ce
framework = stm32cube
build_type = debug
debug_tool = stlink
upload_protocol = stlink
build_flags = 
    ${env.build_flags}
    -D DEBUG_CONSOLE=1

[env:stm32_release]
platform = ststm32
board = blackpill_f401ce
framework = stm32cube
build_type = release
lib_deps =
    bblanchon/ArduinoJson @ ^7.0.0
```

---

## 3. Headless Build, Test & Linting CLI

```bash
# 1. Compile firmware for default environment
pio run -d firmware/

# 2. Compile for specific target environment
pio run -d firmware/ -e stm32_release

# 3. Clean build artifacts
pio run -d firmware/ --target clean

# 4. Flash target MCU via JTAG/SWD probe (ST-Link, J-Link, CMSIS-DAP)
pio run -d firmware/ --target upload

# 5. Static Code Analysis & MISRA Checking (Clang-Tidy, Cppcheck)
pio check -d firmware/ --skip-packages

# 6. Execute Unit Tests on Target Hardware or Virtual Simulator
pio test -d firmware/ -e stm32_debug -v

# 7. Serial Monitor Console
pio device monitor -b 115200
```
