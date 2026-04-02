# PCB Design

## Master's Project — Electrowetting Control System
Designed a multi-board PCB system for controlling electrodes in an electrowetting
application. This was the primary technical deliverable of the master's project.

## Boards Designed

**Boost Converter Board**
Stepped up voltage for the electrowetting electrodes using a boost converter topology.
Designed for the high voltage requirements of electrode actuation.

**Main Control Board**
Central board managing all sensors and peripherals. Communication via I2C and SPI.
STM32 based MCU. USB communication with correct pullup resistor selection.
Debugging via SWD/JTAG using ST-Link.

**Power Delivery Board**
Dedicated power management board supplying the system.

## Design and Manufacturing
- All boards designed in KiCad
- Components selected from JLCPCB library for assembly compatibility
- BOM and pick and place files generated from KiCad for JLCPCB manufacturing
- Boards manufactured and assembled by JLCPCB

## EMC Considerations
Design-side EMC awareness applied throughout — loop sizes, return paths,
ferrite cages, filters, ringing and coupling noise. This is design-side
knowledge, not accredited compliance testing.

## Programming and Debugging
- All MCUs STM32 based, programmed using STM32CubeIDE
- SWD/JTAG debugging via ST-Link
- STM32CubeIDE also used during PCB design for pin allocation and peripheral configuration

## Honest Framing
This was a master's project that was not completed due to health reasons toward
the end. The PCB design and bring-up work was real and substantial — three boards
designed, manufactured and assembled. The project did not reach final validation.
Do not omit the context but do not let it overshadow the genuine technical work done.