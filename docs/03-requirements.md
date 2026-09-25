---
doc_id: SSP-REQ-001
title: SunSpoke requirements
project: SunSpoke
doc_type: Requirements
version: "0.2"
status: Draft
date: '2026-09-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-24'
  author: Amish Chadha
  change: First measurable requirements for TRL 2
---

# SunSpoke requirements

These are first-pass requirements for the concept. Targets are proposals for review, not yet validated with users, and will be checked by calculation at TRL 3 and revised after co-design sessions (see SSP-PRB-001).

The **design load case** used throughout is a 75 kg rider, 25 kg of cargo on the rear carrier, a 22 kg roadster and about 6.5 kg of kit and pack: about 130 kg in total, on a dry dirt road.

| ID | Requirement | Target | Verification (TRL 3 or later) |
| --- | --- | --- | --- |
| R1 | Pedal-assist power within pedelec limits | 250 W rated continuous motor output; assist only while pedaling; assist cuts off at 25 km/h or lower | Motor and controller datasheets; controller settings |
| R2 | Range per charge in the design load case | 30 km or more on a dirt road with the rider pedaling at about 70 W | Energy calculation; later field ride with a logger |
| R3 | Climb a loaded hill | 8 % grade for 500 m at 8 km/h or more in the design load case, rider at 80 W, without motor over-temperature cutout at 35 °C ambient | Force and thermal calculation; later hill test |
| R4 | Fit to the donor bike without fabrication | No welding, drilling or cutting of the frame or fork; fitted in 90 min or less by a trained local mechanic with basic tools (spanners to 18 mm, hex keys, spoke key, screwdriver, file) | Fitting sequence review; later timed fitting trials |
| R5 | Fit the common roadster | 28 in (ETRTO 635) front wheel, 100 mm front dropout spacing, round down tube 28 to 32 mm, rod or cable brakes | Survey of donor bikes with the partner; model check |
| R6 | Keep the bike rideable and liftable | Added mass 7 kg or less including the pack; bike still stands on its kickstand and can be pushed with the system off | Mass estimate; later weighing |
| R7 | Survive dust, rain and heat | Controller, host adapter and connectors IP65; motor IP54 or better; ride through heavy rain and 150 mm of standing water; operate at 0 to 45 °C ambient | Datasheets and design review; later spray and dust tests |
| R8 | Charge from one 100 W solar panel | Energy for 20 km or more of loaded assist per day at 4.5 peak sun hours; full recharge (10 to 100 %) of the pack in 2 days or less | Solar yield calculation |
| R9 | Repairable by a local mechanic | Every electrical joint pluggable with keyed connectors; any single kit part swapped in 20 min or less at the roadside; basic faults diagnosed with a multimeter and a printed fault chart; 70 % or more of kit cost in generic parts available in regional towns | Design review; parts availability survey with the partner |
| R10 | Safe assist control | Brake cut-off on both brake levers; assist stops within 0.5 s of braking or of pedaling stopping; pack output fused; torque arms on both fork dropouts | Design review; later bench test |
| R11 | Stop safely with the added mass and speed | Design load case stops from 20 km/h in 9 m or less on a dry dirt road | Braking calculation; later field test with the donor brakes |
| R12 | Affordable | Kit including the solar charging set, pack excluded, $250 or less in parts | Priced BOM (`bom/bom.csv`) |

## Assumptions

- Rolling resistance coefficient about 0.02 on a dry dirt road; drag area about 0.6 m² for an upright rider with cargo.
- The rider supplies about 70 W while cruising and 80 W on a climb.
- 4.5 peak sun hours per day is a mid-range value for most of sub-Saharan Africa outside the rainy season; 4 hours is used as the low case.
- Pack capacity follows the SwapCell interface v0.2 (about 468 Wh). A separate 36 V pack option is assessed in SSP-PRC-001.
- A 25 km/h assist limit follows EN 15194; a lower limit may be proposed after field input on braking.
