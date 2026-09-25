---
doc_id: SSP-CAL-001
title: SunSpoke sizing calculations
project: SunSpoke
doc_type: Calculation note
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First TRL 3 sizing note (mass, energy and range, hill and motor heating, solar, SwapCell interface v0.3 items, fork and torque arms, cradle retention, braking, cost)
---

# SunSpoke sizing calculations

The 48 V SunSpoke kit on a SwapCell pack meets its range, mass, solar charging and cost requirements on paper: about 37 km of loaded range against 30 km, 6.65 kg added against 7 kg, about 27 km of riding per day from one 100 W panel, and a bike kit of about $183 against the redefined $250 target. No requirement is shown to be not met. Three are **at risk**: R3 (motor winding reaches about 100 °C at the top of the design climb in the base case but about 139 °C in a hotter-motor case), R4 (roadster fork slots may need filing) and R11 (dry stopping distance about 8.5 m against 9 m, a 9 % margin, and about 22 m in the wet). Sealing, repair time, cut-off timing and SwapCell latch class V1 retention (R7, R9, R10, R13) cannot be verified until hardware exists, which is TRL 4 work and on hold by Amish's instruction.

Every number in this note is printed by `docs/04-calcs/sizing.py` (run from the repo root: `python docs/04-calcs/sizing.py`), which also writes `docs/04-calcs/results.csv`. The cost figures are read from `bom/bom.csv`. Fit checks in section 9 are printed by `python cad/src/model.py`. All values are first-principles estimates; nothing here is measured. SwapCell values follow SwapCell interface v0.3 and SWC-CAL-001.

## 1. Assumptions

*Table 1. Inputs. All are assumptions for a paper design.*

| Input | Value | Basis |
| --- | --- | --- |
| Design load case | 75 kg rider, 25 kg cargo, 22 kg roadster, kit and pack (section 2) | SSP-REQ-001 |
| Rolling resistance, drag area, air density | Crr 0.020 on dry dirt; CdA 0.60 m²; 1.2 kg/m³ | Upright rider with cargo |
| Cruise | 18 km/h, rider 70 W, 30 % allowance for hills, rough surface and stop-start | SSP-REQ-001 |
| Motor plus controller efficiency, cruise | 75 % | Small geared hub at part load |
| Wheel radius | 0.355 m | 28 in (ETRTO 635) with tyre |
| SwapCell pack | 466 Wh at 0.2C (452 Wh with minimum cells), 46.8 V, 110 mΩ, 2.85 kg; 90 % usable window | SWC-CAL-001 |
| Motor | 48 V, 250 W geared hub, about 200 rpm no-load at 48 V, gear efficiency 90 %, winding 0.45 Ω, 15 W iron and gear loss, 40 N·m peak | Typical slow-wound 250 W geared hub; to confirm against a named motor |
| Motor thermal | 600 J/K stator and winding, 1.2 K/W winding to ambient while riding, 120 °C practical limit (nylon planetary gears) | Assumed; hot case 0.60 Ω, 450 J/K, 1.5 K/W |
| Solar | 100 W panel, 4.5 peak sun hours (4.0 low), 80 % derating, 92 % boost MPPT, 95 % cell charging, 97 % pack output | SSP-PRC-001 |
| Torque arms | 5 x 20 mm mild steel (250 MPa yield), clamp 130 mm from the axle; flats lever 5 mm on bare dropouts | |
| Donor dropout slot | 9.53 mm (3/8 in) | Assumption until the donor survey |
| Cradle retention | 3.5 kg receiver design pack plus 1.0 kg cradle; 8 g vibration and 25 g shock (latch class V1); band tension 1.5 kN, liner friction 0.40, centroid 70 mm above the tube axis | SwapCell interface v0.3 item V |
| Braking | 0.5 s application delay; 250 N clamp per block from a 100 N hand force; block on steel rim 0.40 dry and 0.12 wet; braking radius 0.310 m | Rod brakes on steel rims |

## 2. Mass (R6)

*Table 2. Added mass.*

| Part | Mass (kg) |
| --- | --- |
| Motor wheel, increase over the donor front wheel | 1.20 |
| Torque arms and band clips | 0.30 |
| Controller | 0.50 |
| Receiver cradle, band clamps and V1 lever | 1.00 |
| Host adapter and charge port | 0.15 |
| Pedal-assist sensor | 0.10 |
| Handlebar control and brake sensors | 0.15 |
| Wiring harness and fuse | 0.40 |
| **Kit** | **3.80** |
| SwapCell pack (SWC-CAL-001) | 2.85 |
| **Added mass** | **6.65 (14.7 lb)** |

R6 (7 kg) is met with 0.35 kg margin. The design load case totals 128.65 kg, rounded to "about 130 kg" in the requirements.

## 3. Energy per kilometer and range (R2)

On a dry dirt road at 18 km/h the design case sees 25.2 N of rolling resistance and 9.0 N of drag, 12.36 Wh/km at the wheel with the 30 % allowance. The rider supplies 3.89 Wh/km, so the motor supplies 8.47 Wh/km and the pack about **11.3 Wh/km**. The TRL 2 figure of 12 Wh/km was rounded up and is superseded.

*Table 3. Range on one SwapCell pack (419 Wh usable with nominal cells).*

| Case | Mass (kg) | Pack energy (Wh/km) | Range (km) |
| --- | --- | --- | --- |
| Design: 25 kg cargo, dirt, 18 km/h | 128.7 | 11.3 | 37 (36 with minimum cells) |
| Light: no cargo, graded murram (Crr 0.015, 20 % allowance) | 103.7 | 5.6 | 75 |
| Heavy: 80 kg cargo, rough dirt (Crr 0.025), 15 km/h | 183.7 | 18.5 | 23 |

R2 (30 km in the design case) is met. A trader carrying 80 kg on rough roads gets about 23 km, so R2 depends on the load case chosen with users. At cruise the pack delivers about 203 W and 4.3 A, which heats it by only about 2.1 W; at the controller's 15 A limit the pack makes about 25 W, far inside SwapCell's 20 A rating.

## 4. Hill climb and motor heating (R3)

On the 8 % grade at 8 km/h the loaded bike needs 127.6 N (grade 100.6 N, rolling 25.2 N, drag 1.8 N), or 284 W at the wheel. With the rider at 80 W the motor supplies **204 W** and **32.5 N·m**, about 81 % of the assumed 40 N·m peak, at about 15.8 A motor current. R3 is met on power and torque. On a 10 % grade the same 330 W gives about 7.8 km/h.

At this low speed the motor is only about 62 % efficient and loses about 127 W. From a cruise temperature of about 68 °C at 35 °C ambient, the winding reaches about **100 °C** at the top of the 500 m climb (225 s), 20 K below the assumed 120 °C limit; the limit would be reached after about 919 m. In the hot case (0.60 Ω winding, 450 J/K, 1.5 K/W, a smaller hub) it reaches about **139 °C**, over the limit. R3 is therefore **at risk**: the result turns on motor data that a named motor datasheet, and later a test, must supply. A controller with a motor temperature input would turn an overheat into a derate instead of a cutout.

## 5. Solar charging (R8) and charge-discharge mode

*Table 4. Daily energy from one 100 W panel (Figure 2 of SSP-PRC-001 uses the mid case).*

| Stage | Mid, 4.5 h (Wh/day) | Low, 4.0 h (Wh/day) |
| --- | --- | --- |
| Sun on panel | 450 | 400 |
| Panel output after 20 % derating | 360 | 320 |
| Charger output (92 %) | 331 | 294 |
| Stored in pack (95 %) | 315 | 280 |
| Pack output (97 %) | 305 | 271 |
| Daily loaded range | 27.0 km | 24.0 km |
| Days to recharge 10 to 100 % (421 Wh) | 1.34 | 1.51 |

R8 (20 km per day and 2 days to recharge) is met in both cases. The peak charge power into the pack is about 74 W, or 1.47 A (0.15C).

**Charge-discharge mode (SwapCell interface v0.3 item C).** When the rider switches the bike on while it charges, the host adapter requests mode 4, so the display and lights run from the pack. With a 4 W load the net charge current is about 1.39 A, 28 % of SwapCell's 5 A standard charge limit. When the bike is off, the adapter requests mode 3 (charge only).

## 6. SwapCell wake and host power (item W)

The cradle receptacle loops INTERLOCK to SGND through the 10 kΩ ±1 % coding resistor that interface v0.3 requires. With the pack's 100 kΩ pull-up from 3.3 V the node sits at 0.30 V and draws 30 µA, inside the pack's 8.0 to 12.5 kΩ acceptance window, so a sleeping pack wakes with no supply from the bike.

The handlebar power switch sits in series with the coding resistor. Switching on closes the loop and wakes the pack; switching off opens it, and the pack opens its output within 1 ms, which also gives the rider a hard off. The host adapter is powered from PACK+ (after the pack enables legacy discharge 2 s after a valid loop) or from the charge inlet, through a diode-OR. If the adapter fails, the pack still runs the bike in legacy discharge-only mode at 15 A, which matches the controller's limit, so the rider is not stranded; charging then needs a working adapter or a hub dock. This relies on the pack moving from legacy discharge (state 5) to heartbeat discharge (mode 2) without opening the output; interface v0.3 does not state that transition explicitly, so it is flagged to the SwapCell project (SSP-DDR-001), not changed here.

## 7. Fork dropouts and torque arms (R4, R10)

At the assumed 40 N·m motor peak, bare dropouts would carry about 4,000 N on each slot face (20 N·m per side over a 5 mm lever). Torque arms clamped 130 mm up each blade carry about 308 N in total, 154 N per arm clamp, and the 5 x 20 mm arm sees about 60 MPa in bending at the axle, a safety factor of about 4.2 on mild steel yield. On the design climb the reaction torque is 32.5 N·m. Torque arms on both sides stay mandatory (R10).

If the donor slot is 3/8 in (9.53 mm), the 10 mm axle flats need about 0.24 mm filed from each slot face. That is small, but it is fabrication on the donor fork, which R4 forbids, and whether it is acceptable with torque arms fitted is open (R4 **at risk**). Fork fatigue under the heavier wheel is not calculated.

## 8. Cradle retention, latch class V1 (item V)

SwapCell class V1 asks the vehicle receiver to hold the pack with no release under 8 g vibration and 25 g shocks, preloading it against its end stop with at least 330 N through an over-centre lever. At a 50 N hand force that needs a lever ratio of 6.6 or more, which the cradle's lever is sized to. For the receiver design mass of 3.5 kg plus the 1.0 kg cradle, 8 g gives about 353 N and 25 g about 1,104 N. The two lined band clamps resist axial slip up to about 7,540 N (margin 6.8 at 25 g) but resist rotation about the down tube only up to about 108 N·m against a 77 N·m moment from a 25 g lateral shock, a margin of about 1.40. The clamps must be tightened to their stated torque and checked at service; a V-shaped saddle under the cradle base helps. Retention cannot be verified at TRL 3.

## 9. Fit in the main triangle (R5)

The parametric model (`cad/src/model.py`) places the pack on a 721 mm down tube with its centre at 48 % of the tube length from the bottom bracket. At that position the pack clears the top tube, seat tube and head tube by 123 mm, and it can slide 164 mm up the tube before touching the frame, against 143 mm needed to clear the 120 mm guides and the 18 mm plug before lifting it out sideways. At the TRL 2 position (52 %) the free travel was only 135 mm, so the pack could not be removed; the model was corrected. Smaller frames need this check on the donor survey.

## 10. Braking (R11)

From 20 km/h the bike covers 2.78 m during a 0.5 s application delay, so stopping in 9 m needs 2.48 m/s². Both rod brakes on dry steel rims give about 2.72 m/s² and a stopping distance of about **8.5 m** (9 % margin on deceleration); from 25 km/h the dry distance is about 12.4 m. In the wet, block friction on steel rims falls to about 0.12 and the distance rises to about 21.7 m. The loaded bike at 20 km/h carries about 1,985 J, about 2.5 times the 795 J of the unconverted bike at 13 km/h. R11 is specified dry and is **at risk** on a thin margin; the wet case is a safety concern whatever the requirement says. The 20 km/h default assist limit (decided) is supported by this result.

## 11. Cost (R12)

*Table 5. Cost from `bom/bom.csv` (indicative prices).*

| Group | Items | Cost (USD) |
| --- | --- | --- |
| Bike conversion kit | 1 to 5, 7 to 9, 14 | 183 |
| Solar charging set, costed separately | 10 to 13 | 86 |
| Kit plus solar set, pack excluded | | 269 |
| SwapCell pack, priced once in SwapCell (SWC-CAL-001) | 6 | 414 |
| Full system for one rider with own panel | all | 683 |

Under the redefined R12 (bike kit $250 or less; solar set costed separately; pack excluded), R12 is met with $67 margin. Generic parts make up about 84 % of the kit plus solar set cost (R9 asks for 70 %). The cradle rose from $22 to $28 (V1 lever, coding resistor) and the host adapter from $12 to $14 (charge inlet and diode-OR).

## 12. Results against requirements

*Table 6. Requirement status. Not met: none. Items at risk and not verifiable are listed first.*

| ID | Value (SSP-CAL-001) | Target | Status |
| --- | --- | --- | --- |
| R3 | 100 °C winding at the top of 500 m from 35 °C (139 °C in the hot case); 32.5 N·m; 204 W motor | 8 % for 500 m at 8 km/h, no over-temperature cutout at 35 °C | At risk |
| R4 | Slot filing about 0.24 mm per side on a 9.53 mm slot; fitting time not calculable | No fabrication; 90 min or less | At risk |
| R11 | 8.5 m dry (9 % margin); 21.7 m wet | 9 m or less from 20 km/h, dry dirt | At risk |
| R7 | IP ratings by part selection only | IP65 electronics, IP54 motor, 150 mm water, 0 to 45 °C | Not verifiable at TRL 3 |
| R9 | Generic parts 84 % of kit cost; swap time not calculable | Pluggable joints, 20 min swap, 70 % generic | Not verifiable at TRL 3 |
| R10 | Arm clamp 154 N each, arm safety factor 4.2; 0.5 s cut-off needs a bench test | Brake cut-off, 0.5 s stop, fuse, torque arms | Not verifiable at TRL 3 |
| R13 | Coding node 0.30 V; mode 4 net 1.39 A; clamp rotation margin 1.40 at 25 g | SwapCell interface v0.3 items W, C and V1 | Not verifiable at TRL 3 |
| R1 | 250 W rated motor, 20 km/h cut-off, pedal assist and 6 km/h walk assist | 250 W; 25 km/h or lower; assist only when pedaling | Met (by specification) |
| R2 | 37 km (36 km with minimum cells) | 30 km or more | Met |
| R5 | Cradle for 28 to 32 mm tubes; motor for 100 mm spacing and 635 rim; pack fits the main triangle in the model | Common roadster | Met (on paper) |
| R6 | 6.65 kg | 7 kg or less | Met |
| R8 | 27 km/day; recharge 1.3 days (1.5 at 4 h) | 20 km/day; 2 days or less | Met |
| R12 | Bike kit $183; solar set $86 costed separately | Bike kit $250 or less | Met |

## 13. Checks against earlier documents

The TRL 2 figures in SSP-PRC-001 v0.2 were checked against this script and corrected in v0.3: pack energy 12 to 11.3 Wh/km, design range 35 to 37 km, light-case range 60 to 75 km (the light case is now defined), daily range from one panel 25 to 27 km, added mass 6.5 to 6.65 kg (pack 2.8 to 2.85 kg, host adapter and V1 lever added), pack cost $370 to $414 (SWC-CAL-001), kit plus solar set $261 to $269, wheel torque on the grade 46 to 45.3 N·m and motor torque 40 to 32.5 N·m (the TRL 2 figure used the whole wheel torque less a rounded rider share), and the pack position on the down tube 52 % to 48 % (section 9). The 36 V pack option (Option B) is no longer assessed; it remains a later low-cost variant.

> **Safety:** These calculations concern a 468 Wh lithium-ion pack, a loaded bicycle at up to 20 km/h with weak wet brakes, and new loads on an old steel fork. They are paper estimates and do not replace inspection of each donor bike or testing. Nothing may be built or ridden from this note; building and testing are TRL 4 work and on hold.
