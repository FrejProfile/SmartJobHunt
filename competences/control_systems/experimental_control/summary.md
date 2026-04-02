# Experimental Control

Master's level course at SDU Sønderborg. Distinct from pure theory courses —
all work was implemented and validated on real physical systems in the lab.

## Systems Worked On

**Rotating Spring System**
Coupled rotating masses with springs. Parameter identification and controller design.

**Flying Wing**
Two rotors on different axes. Attitude control of an inherently unstable system.
Required careful modelling and robust controller design.

**Balancing Pendulum**
Classic unstable system. Required state estimation and fast controller response
to maintain balance.

**Water Tank System**
Multiple connected tanks with nonlinear dynamics due to tank geometry.
Nonlinear system requiring linearisation around operating point.

## Workflow for Each System
1. Data gathering experiments to identify system parameters
2. System modelling in MATLAB/Simulink including parameter fitting
3. State estimator design where necessary — Kalman filter for systems
   where full state was not directly measurable
4. Controller design and implementation
5. Validation on physical hardware

## Controllers Used
- PID — proportional, integral, derivative
- PD — proportional, derivative
- LQR — Linear Quadratic Regulator, optimal state feedback
- LQI — LQR with integral action for steady state error rejection

## Honest Framing
This was coursework, not an industry project. The value is hands-on experience
implementing and validating controllers on real physical systems rather than
purely in simulation. Each system presented different modelling and control challenges.