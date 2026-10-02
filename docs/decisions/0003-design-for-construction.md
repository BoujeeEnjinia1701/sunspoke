---
doc_id: SSP-DDR-003
title: SunSpoke design for construction
project: SunSpoke
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
---

# 0003: Design for construction

- **Date:** 2026-10-01
- **Status:** Draft. Every change in Table 1 was made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review. The items in Table 3 are Proposed, awaiting Amish.

## Context

On 2026-09-30 Amish asked for every repo to have an illustrated build plan and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The TRL 3 model of SunSpoke (SSP-DDR-001, SSP-DDR-002) was a massing model with correct interfaces. Checking it part by part with build123d showed that many kit parts overlapped their neighbours, floated with no fixing, or could not be made as drawn, and that the pack could not be taken out of the cradle because the lever's hinge block stood in its path.

The changes keep what SunSpoke does: the same 250 W front hub motor, 48 V SwapCell pack on the down tube at the same place, the same controller, sensors, display, harness, charging route and solar set; no welding, drilling or cutting of the donor frame or fork; SwapCell interface v0.3 items W, C and V; and the same safety case. Every change is in `cad/src/model.py`, which now runs 57 constructability checks (`python cad/src/model.py --check`): parts that must touch do touch, parts that must not touch are apart by at least the stated clearance, and the pack slides out, lifts and comes away with nothing in its path. All 57 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The cradle base was a flat 4 mm plate whose "saddle" block cut 6 mm into the down tube; nothing could seat it on a round tube. | Three V-saddles (40 mm lengths of 35 x 12 mm aluminium bar, a 120 degree V with a 1.5 mm rubber liner) under a tray folded from 3 mm 5052 aluminium. Each saddle is held by two M5 countersunk screws through the tray. | A V seats on any round tube from 28 to 32 mm (R5) and lets the band press the cradle on squarely. Aluminium instead of the concept's folded steel keeps the cradle at 1.10 kg; in steel the tray alone would have weighed about 1.3 kg and R6 would fail. |
| P2 | The two band clamps were drawn as rings round the tube that passed through the base; a band cannot go through a plate. | Each band passes down through a pair of 3 x 13 mm slots in the tray, round the V-saddle and the underside of the tube, and back over the tray; the worm screw sits under the tube. Three band clamps (at the middle and 100 mm each side) instead of two. | This is how a band holds a plate to a tube without drilling the frame. A real band wraps only about 150 degrees of the tube, not a full turn, so with two bands the 25 g rotation margin would fall from 1.40 to about 0.96; three bands give 1.44 (SSP-CAL-001 v0.3 section 8). |
| P3 | The end stop was a solid 30 x 104 x 90 mm block with the receptacle drawn inside it. | A folded 3 mm aluminium end stop: a wall with an open-topped notch for the pack's plug, a foot on the tray and two side flanges bolted inside the guides. The bought SwapCell receptacle bolts behind the wall on four M4 bolts; the plug stops 1 mm short of its bottom. The guides are the tray's own folded side tabs. | Every part is sheet that can be cut, folded and drilled by hand. Held on three edges, the wall sees about 62 MPa at 25 g, a factor of 3.1 on yield. The open notch avoids a thin strip of metal spanning the window. |
| P4 | The V1 lever was three loose blocks (hinge, pad and handle, up to 5 mm apart), its pad 4 mm short of the pack, and the hinge block stood across the pack's path, so the pack could not slide out. | A drop-down gate (3 mm steel) on a stainless butt hinge at the tray's top end, with a 3 mm rubber pad that presses the pack's top end below the handle, closed by a bought adjustable over-centre draw latch with a safety catch on a folded ear on the tray's left side; the latch hook pulls a keeper on the gate's folded flange. Opened, the gate folds flat under the pack's path. | Keeps latch class V1: an over-centre lever, 330 N preload (the latch pulls about 314 N), a detent (the safety catch). Nothing stands in the pack's path once the gate is down. One hinge and one latch, both bought. |
| P5 | The slide rails were solid steel bars with no fixing; the latch catch was a loose block. | Two 12 x 10 mm HDPE slide strips on three self-tapping screws each from under the tray; a 10 x 6 mm steel catch bar on two M4 countersunk screws. | Low friction for the pack, no screw heads on the sliding faces; the pack's latch still sits 3 mm short of the catch. |
| P6 | The host adapter floated 4 mm above the tube beyond the end of the base. | The tray runs 70 mm past the end stop and the adapter sits on it, two M4 screws up into its inserts, with a short lead to the receptacle. | Uses the tray; keeps the adapter where the concept put it, 7.5 mm clear of the chainring. |
| P7 | The torque arms passed 2 mm into the fork blades; their clips were rings on the blades not joined to the arms; the fork had no dropouts and the axle was shorter than its nuts needed. | Joggled arms from 20 x 5 mm steel bar: a 10 mm slot open at the end that fits the axle flats and lies flat on the outside of the dropout under the washer and nut, and an 8 mm joggle so the long part lies on the outside of the blade, held 130 mm up by one band clamp round blade and arm. The donor's 6 mm dropouts with 10 mm slots and a 150 mm axle are now in the model. | The arm bears on the dropout face and the blade, as a torque arm must, and can be made with a hacksaw, file and vice. The lever arm stays 130 mm, so SSP-CAL-001 section 7 is unchanged. |
| P8 | The controller floated 4 mm in front of the seat tube with no fixing. | A 4 mm rubber pad on the front of the seat tube and two 12 mm band clamps round the tube and the controller case. | No drilling of the frame; the pad stops the case rattling and chafing the paint. |
| P9 | The pedal-assist disc sat on nothing (its bore was 36 mm on a 16 mm spindle), touched the left chainstay, and there was no Hall sensor. | A split disc that clamps on the spindle 10 mm outboard of the bottom bracket shell, and the Hall sensor on a ring bracket that fits under the left lockring, 2.5 mm from the magnets. The chainstays now meet the shell, not the space beside it. | This is how bolt-on pedal-assist sensors fit a cup-and-cone bottom bracket; the crank comes off but the spindle stays. |
| P10 | The handlebar display box cut 2.5 mm into the bar; the brake sensors were boxes centred on the grip section of the bar. | The display on its own bar clamp left of the stem; each brake sensor on a small bar clamp inboard of its lever, with a magnet glued to the lever's pivot post. | Fits rod or cable levers without changing them. It also puts the sensors where the appearance model (`cad/src/product_model.py`) already showed them (review note, 2026-09-26, proposal 3). |
| P11 | The harness ran through open space and through the cradle. | Routed along the left side of the down tube near the bottom bracket, the seat tube, the top tube and the head tube, down the front of the left fork blade (over the torque arm's band) and up the stem; cable ties every 150 mm; the 20 A fuse holder on the lead from the adapter. | Every run lies on a tube, clear of the cradle, wheel, cranks and chainring by the checked distances. |
| P12 | The panel stand's legs ran 14 to 22 mm into the panel, nothing joined the leg tops, nothing held the panel, and the charger floated. | A timber A-frame from 45 x 45 mm sawn timber: two top rails under the panel at its 15 degree tilt, two tall rear and two short front legs lapped on the rails' outside faces with M8 coach bolts, two low braces and two cross battens. The panel bolts through its own frame holes into the rails; the charger screws to the left rear leg in the panel's shade. | The BOM allowed steel angle or timber; timber needs no welding and only a saw and drill, and matches the appearance model (review note, 2026-09-26, proposal 4). |
| P13 | The front wheel's spokes ran from the hub centre through the motor shell. | Spokes from the motor's two flanges to the rim (context only). | Shows the wheel as a mechanic laces it. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Pack position | The V-saddles lift the pack 7 mm; it still sits at 48 % of the down tube. Clearance in the triangle 121 mm (was 123 mm); free travel 165 mm for the 143 mm needed. | Follows P1. |
| Swap sequence | Open the latch, fold the gate down, press the pack's release and slide the pack 143 mm up the tube, lift 45 mm, take it out to the left. Fitting is the reverse. | Follows P4; the concept did not state one, and its own lever blocked the pack. |
| Mass | Kit 3.93 kg (was 3.80 kg); added mass with pack 6.78 kg, 0.22 kg under R6's 7 kg (SSP-CAL-001 v0.3 section 2). | P1 to P8. |
| Retention | Axial margin at 25 g 7.7 (was 6.8); rotation margin 1.44 (was 1.40); end stop factor 3.1 on yield. | P1 to P4. |
| Cost | BOM line 2 USD 6 (now a made part), line 4 USD 28 to 33, line 12 USD 10 to 14, line 14 USD 8 to 11. Bike kit USD 196 (was USD 188), USD 54 under the USD 250 value-engineering target; solar set USD 90 (was USD 86). | Parts added for construction. |
| Drawings | SSP-DWG-001 Rev P3; making sketches SSP-DWG-101 to 110 added. | Follows the model. |
| Documents | SSP-CAL-001 v0.3, SSP-REQ-001 v0.5, SSP-PRC-001 v0.5: mass, cost, retention and fit figures updated. No requirement changed status. | Follows the model. |
| Unchanged | Motor, torque arm lever arm, controller, pack, charging, solar yield, range, hill climb and braking results (each within rounding of v0.2). | |

*Table 3. Proposed, awaiting Amish.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | The pack swap now has two hand movements at the cradle (open the latch, fold the gate) where the concept showed one lever. | (a) gate and draw latch as modelled; (b) design a single lever that also folds the gate (a linkage, more parts, not yet designed). | (a) for the prototype; review after the first swap trials at TRL 4. |
| A2 | Timber for the panel stand (also proposal 4 of 2026-09-26). | (a) timber, as modelled; (b) steel angle, bolted. | (a): no welding, local materials, and it is what the renders show. |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan SSP-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`); open decisions are in the design decisions register SSP-DEC-001.
- Requirement status is unchanged: none not met; R3, R4 and R11 at risk; R7, R9, R10 and R13 not verifiable at TRL 3; the rest met on paper (SSP-CAL-001 v0.3).
- The photoreal renders (`media/render-*.png`), `media/card.png`, `media/social-preview.png` and the appearance model `cad/src/product_model.py` still show the concept cradle, lever, torque arms and stand; they need updating on Amish's Mac, where Blender is.
- The fork must take the motor's 10 mm axle flats without filing (decision 15 of SSP-DDR-001 is still open); the build plan asks for a donor fork that does.
