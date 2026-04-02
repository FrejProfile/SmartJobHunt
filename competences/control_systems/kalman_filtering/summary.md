# Kalman Filtering and Sensor Fusion

## Amfitech In-company Project (2024)
15 ECTS project implementing a sequential Extended Kalman Filter for the
Amfitrack magnetic tracking system.

## The Problem
The system uses 4 magnetic emitters to estimate the position of a receiver.
Each emitter contributes a position estimate but with varying reliability
depending on distance, orientation and interference. Naively fusing all
estimates equally degrades accuracy.

## The Solution
Modelled the noise characteristics of each emitter through a lookup table
mapping signal conditions to uncertainty values. This gave a principled way
to assign trust to each emitter's position estimate proportional to its
current reliability.

A sequential Extended Kalman Filter was used to fuse the four estimates one
at a time, each weighted by its modelled uncertainty. The result was a more
accurate and precise position estimate than equal weighting would produce.

## Implementation
- Algorithm developed entirely in MATLAB — no Simulink
- Data collection scripts written in Python
- Data gathered through both dynamic and static experiments
- Lookup table built from empirical noise characterisation
- Amfitech later converted the algorithm to run on their STM32 based sensor,
  likely in embedded Python or C — this conversion was done by them after
  the project concluded

## Honest Framing
This was a university in-company project in terms of formal framing, but the
work was integrated into Amfitech's commercial product after completion. The
algorithm solved a real problem they needed solved and did not have time to
do themselves. This was not a toy project — the output had real commercial value.

Frame as: an in-company project whose results were adopted into a commercial
product. Do not claim a full industry engineering position, but do not
undersell the real-world impact of the work either.

## Related
- `competences/control_systems/signal_processing/summary.md` — theoretical
  foundation for the estimation approach
- `competences/professional/summary.md` — professional context