# FPGA and VHDL

All projects implemented on Zedboards (Xilinx Zynq — dual core ARM + FPGA fabric).
Toolchain: Vivado for hardware design, Vitis HLS for high level synthesis.

## Digital Design and Signal Processing (Bachelor)
Implemented a Kalman filter in VHDL for state estimation on FPGA.
Validated through a simulated wheeled robot running on the computer.
Foundation course for hardware description and digital logic design.

## Hardware/Software Co-Design of Embedded Systems (Master)
Took a machine learning algorithm and offloaded compute intensive loops
and bottlenecks from the processor (PS) to the FPGA fabric (PL) using
Vitis HLS. Focus was on identifying bottlenecks and accelerating them
in hardware while keeping control flow on the processor.

## Advanced Machine Learning (Master)
Offloaded part of a neural network from processor to FPGA.
Similar PS/PL partitioning approach — accelerating the inference
critical path in hardware.

## Honest Framing
Three courses across bachelor and master's level gives a solid foundation
in FPGA development and hardware/software partitioning. Not a specialist
but comfortable with the full toolchain from hardware description through
to HLS based acceleration. All work was coursework, not industry projects.