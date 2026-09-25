---
doc_id: SSP-PRC-001
title: SunSpoke design precis
project: SunSpoke
doc_type: Design precis
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
  change: Populate to TRL 2 (architecture, first-order numbers, fork torque, safety, media)
---

# SunSpoke design precis

SunSpoke converts a steel roadster bicycle into a pedal-assist e-bike with a 250 W geared front hub motor, a sealed controller and a SwapCell pack clamped inside the main triangle, all bolted on with no welding, and charges the pack from one 100 W solar panel or a shared village hub. First-order numbers suggest a 48 V build on the SwapCell pack gives about 35 km of loaded range, that one panel stores about 315 Wh on a 4.5 sun-hour day (enough for about 25 km of loaded riding), and that the kit with its solar set costs about $261 in parts with the pack excluded, about 4 % over the $250 target.

![Hero render](../media/hero.png)

*Figure 1. SunSpoke fitted to a 28 in roadster, with the 100 W solar charging set and a 1.75 m person for scale. Kit parts are colored; the donor bicycle is grey.*

## How it works

1. **Charge.** A 100 W panel on a simple stand feeds a boost MPPT charger that raises the panel's roughly 18 V to the pack's charge voltage. A 5 m cable lets the panel sit in sun while the bike and pack stay in shade. Alternatively the rider swaps the pack at a village hub that has a SwapCell dock.
2. **Store.** A SwapCell pack (13S2P, about 46.8 V nominal, about 468 Wh) slides into a receiver cradle clamped to the down tube and latches. It enables its output only when the interlock closes and the host adapter sends a valid CAN heartbeat, as the SwapCell interface requires.
3. **Sense.** A split-disc pedal-assist sensor at the crank detects pedaling. Magnetic sensors on both brake levers detect braking.
4. **Control.** A sealed 48 V, 15 A sine-wave controller on the seat tube drives the motor only while the rider pedals and no brake is applied, up to a set assist speed. A small handlebar unit sets the assist level and shows pack charge.
5. **Drive.** A 250 W geared hub motor, laced by a local mechanic into a standard 28 in (ETRTO 635) rim, replaces the front wheel. Torque arms on both fork blades carry the motor's reaction torque so it does not act on the thin dropouts alone.

Front drive leaves the roadster's chain, freewheel or coaster brake and rear carrier untouched, which is what makes a bolt-on fit and local repair realistic.

![Energy flow](../media/flow.png)

*Figure 2. Daily solar energy flow from one 100 W panel at 4.5 peak sun hours, in Wh per day. All values are estimates.*

## Main components

Numbers match the exploded view (Figure 3) and `bom/bom.csv`.

| # | Component | Proposed choice | Notes |
| --- | --- | --- | --- |
| 1 | Front hub motor wheel | 48 V, 250 W geared hub, 100 mm spacing, laced into a 28 in steel rim | Donor tyre and tube reused. Voltage proposed, awaiting Amish |
| 2 | Torque arms | Steel plate arms keyed to the axle flats, clamped to each fork blade | Mandatory on both sides |
| 3 | Controller | 48 V, 15 A limit, sine-wave, potted or IP65 | Pedal-assist and brake cut-off inputs; generic part |
| 4 | SwapCell receiver cradle | Folded steel cradle with SwapCell guides, latch catch and connector; two lined band clamps | Clamps to 28 to 32 mm down tubes; no welding |
| 5 | Host adapter | Microcontroller with CAN transceiver, interlock loop, potted box | Sends the heartbeat SwapCell needs before it enables output |
| 6 | SwapCell pack | 13S2P, about 468 Wh, 340 x 90 x 80 mm, about 2.8 kg | Not in kit cost (see `bom/bom-notes.md`) |
| 7 | Pedal-assist sensor | Split 12-magnet disc and Hall sensor | Fits without pulling the crank |
| 8 | Handlebar control and brake cut-off | LED level and charge display, power switch, two clamp-on lever sensors | Works with rod or cable brake levers |
| 9 | Wiring harness | Keyed waterproof connectors, 20 A fuse, spiral wrap | Every joint pluggable (R9) |
| 10 | Solar panel | 100 W monocrystalline, about 1,000 x 670 mm | Can be shared at a hub |
| 11 | Boost MPPT charger | 15 to 25 V in, CC/CV to 54.6 V at up to 2 A out | Must also act as a SwapCell charge host (open question) |
| 12 | Panel stand | Local steel angle or timber A-frame, 10 to 20 degree tilt | Local make |
| 13 | Charge cable | 5 m outdoor cable with keyed plug to the cradle charge port | Pack charges in shade |

![Exploded view](../media/exploded.png)

*Figure 3. Exploded view with numbered callouts matching the BOM. The solar charging set is shown displaced below the bike.*

## First-order numbers

All values are estimates for concept review and will be checked at TRL 3. The design load case is about 130 kg total (75 kg rider, 25 kg cargo, 22 kg roadster, about 6.5 kg of kit and pack) on a dry dirt road.

### Energy use per kilometer

Assumptions: rolling resistance coefficient 0.02 (dirt road), drag area 0.6 m², air density 1.2 kg/m³, cruising at 18 km/h, a 30 % allowance for hills, rough surface and stop-start riding, rider supplying 70 W, and motor plus controller efficiency of 75 %.

| Quantity | Estimate | Basis |
| --- | --- | --- |
| Rolling resistance | about 25.5 N | 0.02 x 130 kg x 9.81 m/s² |
| Aerodynamic drag at 18 km/h | about 9 N | 0.5 x 1.2 x 0.6 x (5 m/s)² |
| Road energy at the wheel | about 9.6 Wh/km, about 12.5 Wh/km with the 30 % allowance | 34.5 N over 1 km |
| Rider contribution | about 3.9 Wh/km | 70 W at 18 km/h |
| Motor energy at the wheel | about 8.6 Wh/km | 12.5 minus 3.9 |
| **Pack energy, design case** | **about 12 Wh/km** | 8.6 / 0.75, rounded up |
| Pack energy, light case | about 7 Wh/km | Rider only, good road, no cargo |

### Range and hills

| Quantity | Estimate | Basis | Requirement |
| --- | --- | --- | --- |
| Usable pack energy, SwapCell | about 420 Wh | 468 Wh x 90 % usable window | |
| Range, SwapCell, design case | about 35 km | 420 Wh / 12 Wh/km | R2 (30 km) met |
| Range, SwapCell, light case | about 60 km | 420 Wh / 7 Wh/km | |
| Range, alternative 36 V 10 Ah pack | about 27 km design, about 46 km light | 360 Wh x 90 % | R2 not met |
| Force on an 8 % grade at 8 km/h | about 129 N | Grade 102 N, rolling 25.5 N, drag 1.5 N | |
| Power needed on the grade | about 290 W at the wheel | 129 N x 2.22 m/s | |
| Power available | about 330 W | 250 W motor plus 80 W rider | R3 met on power; motor heating unverified |
| Wheel torque on the grade | about 46 N·m, of which the motor supplies about 40 N·m | 129 N x 0.355 m wheel radius | Near the peak of a typical 250 W geared hub |
| Added mass | about 3.7 kg of kit plus 2.8 kg pack, about 6.5 kg | Motor wheel +1.2 kg over the donor wheel, cradle 0.9, controller 0.5, harness 0.4, others 0.7 | R6 (7 kg) met, margin thin |

### Solar charging

Assumptions: one 100 W panel, 4.5 peak sun hours (4 to 5 h range), 20 % derating for cell temperature in the heat, dust, wiring and non-ideal tilt, 92 % boost MPPT charger efficiency, 95 % cell charging efficiency and 3 % loss in pack resistance on discharge.

| Quantity | Estimate | Basis | Requirement |
| --- | --- | --- | --- |
| Panel output | about 360 Wh/day (320 to 400) | 100 W x 4.5 h x 0.8 | |
| Stored in pack | about 315 Wh/day (280 to 350) | x 0.92 x 0.95 | |
| Peak charge current | about 1.5 A | About 74 W into about 50 V; about 0.15 C, gentle on cells | |
| Daily loaded range from one panel | about 25 km (23 to 28) | 305 Wh at the pack terminals / 12 Wh/km | R8 (20 km) met |
| Days to recharge SwapCell, 10 to 100 % | about 1.3 days (1.2 to 1.5) | 420 Wh / 315 Wh per day | R8 (2 days) met |
| Days to recharge 36 V 10 Ah pack | about 1.0 day | 324 Wh / 315 Wh per day | |

One panel therefore supports a typical day of loaded riding, but a rider who uses the full 35 km range every day will run down over several days. A village hub with more panels, or a second pack, closes that gap.

### Fork and frame torque

The motor pushes against its own axle. The reaction torque, up to about 40 N·m at peak in the design case, tries to spin the axle in the fork dropouts. The axle carries 10 mm flats that bear on the slot faces over a lever of only about 5 mm each side, so the contact force on the dropout faces is of the order of 4 kN. That is enough to spread or crack thin stamped dropouts over time, and roadster fork slots are often narrower than 10 mm, so fitting may need the slot filed wider, which weakens them further.

Torque arms move the reaction to a clamp about 130 mm up each fork blade, cutting the force to about 300 N in total, about 150 N per arm when two are fitted. Torque arms on both sides are therefore part of the kit, not an option, and whether slot filing is acceptable is an open question (R4). Braking and pothole loads on the fork also rise with the heavier front wheel and higher speed; the roadster fork's fatigue margin is unverified.

### Cost

| Group | Indicative cost | Requirement |
| --- | --- | --- |
| Bike conversion kit (items 1 to 5, 7 to 9, 14) | about $175 | |
| Solar charging set (items 10 to 13) | about $86 | |
| **Kit total, pack excluded** | **about $261** | R12 ($250) not met, about 4 % over |
| SwapCell pack (item 6, not in kit cost) | about $370 prototype parts | |

## Key design choices

Every choice below is **Proposed, awaiting Amish**.

- **System voltage and pack.** The scaffold assumed a 36 V 10 Ah pack, but the SwapCell interface (v0.2) is a 48 V class pack, about 46.8 V nominal and up to 54.6 V, which a 36 V controller cannot accept.
  - Option A: a 48 V motor and controller that use SwapCell directly. Meets R2 (about 35 km), shares packs and docks with other portfolio vehicles, keeps the pitch; but the pack costs about $370 and the kit needs a CAN host adapter.
  - Option B: a 36 V kit with its own generic 36 V 10 Ah pack (about $130 to $160 indicative). Cheaper and simpler, with common local spares, but misses R2 (about 27 km) and drops SwapCell compatibility, which changes the pitch.
  - Recommendation: Option A, with Option B recorded as a low-cost variant for later. Proposed, awaiting Amish.
- **Front geared hub motor.** Front drive leaves the roadster's drivetrain, rear brake and carrier untouched and is the easiest bolt-on. Alternatives: a direct-drive front hub (tougher and quieter, but about 5 kg and harder on the fork), a rear hub (better traction when loaded, but clashes with coaster brakes and single-speed freewheels) or a mid-drive (best on hills, but needs bottom bracket work and wears the chain). Recommendation: geared front hub. Proposed, awaiting Amish.
- **Pack in the main triangle on the down tube.** This keeps the rear carrier free for goods and passengers and keeps mass low and central. The alternative is a cradle on the rear carrier, which is easier to fit on small frames but takes carrying space and raises the center of mass. Recommendation: down tube. Proposed, awaiting Amish.
- **Motor laced locally into a 28 in rim.** Local lacing uses a skill the mechanic already has and a rim the market already stocks; a pre-built wheel is simpler to fit but in a size that may not match the donor tyre. Recommendation: local lacing with a lacing card. Proposed, awaiting Amish.
- **Assist speed limit.** 25 km/h follows EN 15194, but a loaded roadster with rod brakes is marginal at that speed. Recommendation: 20 km/h default, adjustable only by the mechanic. Proposed, awaiting Amish.
- **Pedal assist only, plus walk assist.** No throttle, to stay a pedelec and keep speeds modest, with a 6 km/h walk-assist button for pushing a loaded bike up steep hills. Proposed, awaiting Amish.
- **Charge on the bike.** The charger plugs into the cradle's charge port and the host adapter acts as the SwapCell charge host, so no dock is needed at home; hub docks remain an option. Proposed, awaiting Amish.
- **Budget.** The kit with solar set is about $11 over the $250 target. Options are in `docs/REVIEW.md`. The `project.yaml` budget is unchanged. Proposed, awaiting Amish.

## Safety

> **Safety:** SunSpoke carries a lithium-ion pack of about 468 Wh, drives a loaded bicycle faster than its rider alone, and puts new loads on an old steel fork. Treat each of these as a hazard at every stage.

- **Lithium pack.** A cell in thermal runaway vents flammable, toxic gas and can ignite its neighbors. Use only a pack with a BMS and cell-level protection (SwapCell provides this), fuse the pack output (item 9), charge on a non-combustible surface in shade and away from sleeping areas, never charge a pack that is damaged, swollen or has been submerged, and keep the pack out of direct sun when parked. Charging below 0 °C or above 45 °C must be blocked by the BMS.
- **Fork dropout failure.** A spun axle can rip the motor cable and let the wheel leave the fork, which throws the rider over the bars. Torque arms on both sides are mandatory, axle nuts need a set torque and a check at every service, and a fork with cracked, bent or heavily filed dropouts must not be converted. Fork fatigue under the heavier wheel is unverified.
- **Braking with added speed and mass.** At 20 km/h the design load case carries about 2 kJ of kinetic energy, roughly 2 to 3 times that of the same bike at an unassisted 12 to 14 km/h. Rod and rim brakes lose much of their grip in rain and mud. Brake cut-off sensors on both levers, a conservative assist limit, and a brake check and pad or block replacement at fitting are part of the kit; stopping distance (R11) is unverified. Braking with only the front brake on loose ground can wash out the front wheel.
- **Wiring in rain.** The system is about 50 V DC, below the usual touch-safety threshold, but water in connectors causes corrosion, shorts and sudden loss of assist. Use keyed IP65 connectors with dielectric grease, drip loops, and routing that keeps the motor cable exit facing down and away from water. The fuse protects against a pinched cable shorting to the frame.
- **Traction.** With cargo on the rear carrier, the front wheel carries little weight and a front motor can spin on sand or wet laterite. Assist ramp-up must be soft.

## Open questions for TRL 3

- Confirm motor voltage and pack option (Option A or B above) with Amish and the partner.
- Measure donor fork dropout slot widths, thickness and axle sizes on a sample of local roadsters; decide whether slot filing is acceptable with torque arms.
- Check motor temperature on a long loaded climb at 35 °C ambient (R3); consider a thermal sensor input to the controller.
- Estimate stopping distance with typical rod and cable brakes, dry and wet (R11), and decide the assist limit.
- Define how the host adapter and solar charger act as SwapCell hosts (heartbeat, charge request, interlock) within the SwapCell interface v0.2, and flag any conflict to the SwapCell project rather than change the interface here.
- Confirm that a low-cost boost charger with input-voltage tracking gives near-MPPT yield from one 18 V panel.
- Close the $11 cost gap or propose a budget change.
- Choose the first partner and region for co-design and fitting trials.

Concept media: [blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html).
