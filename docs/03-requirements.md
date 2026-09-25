---
doc_id: SSP-REQ-001
title: SunSpoke requirements
project: SunSpoke
doc_type: Requirements
version: "0.3"
status: Draft
date: '2026-09-25'
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
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record SSP-DDR-001 (R1 20 km/h default and walk assist, R12 redefined to the bike kit, new R13 for SwapCell interface v0.3); status column from SSP-CAL-001
---

# SunSpoke requirements

These requirements were checked by calculation in SSP-CAL-001 at TRL 3. None is shown to be not met; R3, R4 and R11 are at risk, and R7, R9, R10 and R13 cannot be verified until hardware exists (TRL 4, on hold by Amish's instruction). Targets are not yet validated with users and will be revised after co-design sessions (see SSP-PRB-001). Changes in v0.3 follow Amish's decisions of 2026-09-25 (SSP-DDR-001).

The **design load case** used throughout is a 75 kg rider, 25 kg of cargo on the rear carrier, a 22 kg roadster and about 6.65 kg of kit and pack: about 130 kg (128.65 kg) in total, on a dry dirt road.

*Table 1. Requirements with status from SSP-CAL-001.*

| ID | Requirement | Target | Verification (TRL 3 or later) | Status (SSP-CAL-001) |
| --- | --- | --- | --- | --- |
| R1 | Pedal-assist power within pedelec limits | 250 W rated continuous motor output; pedal assist only, no throttle, plus a 6 km/h walk assist; assist cuts off at 20 km/h by default, adjustable only by the mechanic and never above 25 km/h | Motor and controller datasheets; controller settings | Met (by specification) |
| R2 | Range per charge in the design load case | 30 km or more on a dirt road with the rider pedaling at about 70 W | Energy calculation; later field ride with a logger | Met (37 km) |
| R3 | Climb a loaded hill | 8 % grade for 500 m at 8 km/h or more in the design load case, rider at 80 W, without motor over-temperature cutout at 35 °C ambient | Force and thermal calculation; later hill test | At risk |
| R4 | Fit to the donor bike without fabrication | No welding, drilling or cutting of the frame or fork; fitted in 90 min or less by a trained local mechanic with basic tools (spanners to 18 mm, hex keys, spoke key, screwdriver, file) | Fitting sequence review; later timed fitting trials | At risk |
| R5 | Fit the common roadster | 28 in (ETRTO 635) front wheel, 100 mm front dropout spacing, round down tube 28 to 32 mm, rod or cable brakes | Survey of donor bikes with the partner; model check | Met (on paper) |
| R6 | Keep the bike rideable and liftable | Added mass 7 kg or less including the pack; bike still stands on its kickstand and can be pushed with the system off | Mass estimate; later weighing | Met (6.65 kg) |
| R7 | Survive dust, rain and heat | Controller, host adapter and connectors IP65; motor IP54 or better; ride through heavy rain and 150 mm of standing water; operate at 0 to 45 °C ambient | Datasheets and design review; later spray and dust tests | Not verifiable at TRL 3 |
| R8 | Charge from one 100 W solar panel | Energy for 20 km or more of loaded assist per day at 4.5 peak sun hours; full recharge (10 to 100 %) of the pack in 2 days or less | Solar yield calculation | Met (27 km/day, 1.3 days) |
| R9 | Repairable by a local mechanic | Every electrical joint pluggable with keyed connectors; any single kit part swapped in 20 min or less at the roadside; basic faults diagnosed with a multimeter and a printed fault chart; 70 % or more of kit cost in generic parts available in regional towns | Design review; parts availability survey with the partner | Not verifiable at TRL 3 (84 % generic) |
| R10 | Safe assist control | Brake cut-off on both brake levers; assist stops within 0.5 s of braking or of pedaling stopping; pack output fused; torque arms on both fork dropouts | Design review; later bench test | Not verifiable at TRL 3 |
| R11 | Stop safely with the added mass and speed | Design load case stops from 20 km/h in 9 m or less on a dry dirt road | Braking calculation; later field test with the donor brakes | At risk (8.5 m dry) |
| R12 | Affordable | Bike conversion kit (items 1 to 5, 7 to 9, 14) $250 or less in parts; the solar charging set is costed separately; the SwapCell pack is excluded and priced once in SwapCell | Priced BOM (`bom/bom.csv`) | Met ($183) |
| R13 | Build to SwapCell interface v0.3 | Cradle receptacle fits the 10 kΩ ±1 % INTERLOCK coding resistor (item W); host adapter acts as the vehicle host for modes 2, 3 and 4 within the pack's published limits (item C); cradle is a latch class V1 vehicle receiver with at least 330 N preload (item V) | Design review against SWC-PRC-001 v0.3; later vibration and shock test | Not verifiable at TRL 3 |

## Assumptions

- Rolling resistance coefficient about 0.02 on a dry dirt road; drag area about 0.6 m² for an upright rider with cargo.
- The rider supplies about 70 W while cruising and 80 W on a climb.
- 4.5 peak sun hours per day is a mid-range value for most of sub-Saharan Africa outside the rainy season; 4 hours is used as the low case.
- Pack capacity follows SwapCell interface v0.3 and SWC-CAL-001 (about 466 Wh at 0.2C, 90 % usable). The 48 V system on SwapCell is decided (SSP-DDR-001); a 36 V kit is only a later low-cost variant.
- The 25 km/h ceiling follows EU pedelec practice (Regulation (EU) No 168/2013 excludes pedal cycles with assist up to 250 W that cuts off at 25 km/h; EN 15194 is the matching product standard). The 20 km/h default is decided (SSP-DDR-001) and is supported by the braking result in SSP-CAL-001.
- R12 covers only the bike kit. The solar set (about $86) is costed separately because a rider who charges at a village hub does not need it.

> **Safety:** R6, R10, R11 and R13 are safety requirements for a bicycle carrying a 468 Wh lithium-ion pack at up to 20 km/h. Braking in the wet (about 22 m from 20 km/h in SSP-CAL-001) falls far short of the dry target, and pack retention and fork loads are unverified. No conversion may be ridden before these are verified by test, which is TRL 4 work and on hold.
