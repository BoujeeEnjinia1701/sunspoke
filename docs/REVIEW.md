# Review note: SunSpoke

## Session 2026-09-24: /populate to a strong TRL 2

### What was done

- `docs/01-problem.md` (SSP-PRB-001 v0.2): problem, users (commuters, traders, health workers, mechanics, hub operators), operating environment, constraints, out of scope, prior work without links, open questions; co-design checklist kept.
- `docs/03-requirements.md` (SSP-REQ-001 v0.2): 12 measurable requirements (R1 to R12) with targets, a defined design load case and assumptions.
- `docs/02-concept.md` (SSP-PRC-001 v0.2): how it works, numbered components, energy per km, range, hill climb, solar yield, fork torque and torque arms, cost, design choices, safety, open questions.
- `cad/src/concept_media.py`: massing model of a 28 in roadster (frame from tubes, fork, bars, carrier, wheels) with the kit parts colored and a separate 100 W panel on a stand; 1.75 m scale figure.
- `media/`: hero, blueprint sheet (PNG, PDF, SVG), exploded view with BOM callouts, daily solar energy flow diagram, `model.glb` and `viewer.html`. No cutaway (the inside does not carry the idea).
- `bom/bom.csv`: 14 lines with indicative prices, numbered to match the exploded view; `bom/bom-notes.md` states that the pack is **not** included in the kit cost.
- `README.md`: hero image and links line added.
- `docs/pdf/`: branded PDFs of the three controlled documents.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Pack energy, design load case (130 kg, dirt road) | about 12 Wh/km | |
| Range on SwapCell (about 420 Wh usable) | about 35 km loaded, about 60 km light | R2 met |
| Range on alternative 36 V 10 Ah pack | about 27 km loaded | R2 not met |
| Power on 8 % grade at 8 km/h | about 290 W needed, about 330 W available | R3 met on power; motor heating unverified |
| Added mass | about 6.5 kg with pack | R6 met, thin margin |
| One 100 W panel, 4.5 sun hours | about 315 Wh/day stored, about 25 km of loaded riding | R8 met |
| SwapCell recharge 10 to 100 % | about 1.3 days (1.2 to 1.5) | R8 met |
| Torque arm load | about 300 N total at 130 mm, versus about 4 kN on bare dropout faces | R10 by design |
| Kit cost, solar set included, pack excluded | about $261 (bike kit about $175, solar set about $86) | **R12 not met, about 4 % over** |
| SwapCell pack (not in kit cost) | about $370 prototype parts | |

Requirements not met or at risk:

- **R12 (cost) not met:** about $261 against $250.
- **R4 (no fabrication, 90 min fit) at risk:** roadster fork slots may be narrower than the motor's 10 mm axle flats, so fitting may need filing.
- **R11 (stopping distance) unverified:** about 9 m needs about 2.5 m/s² deceleration, which loaded rod brakes may not reach, especially wet.
- **R3 thermal part unverified:** a 250 W geared hub near peak torque on a long climb in 35 °C heat may overheat.
- **R2 would not be met** if the 36 V pack option is chosen.

### Proposed, awaiting Amish

1. **System voltage (pitch-level).** The scaffold assumed 36 V, but SwapCell is 48 V class (about 46.8 V nominal, 54.6 V full). Option A: 48 V motor and controller on SwapCell (meets range, shares packs, keeps pitch; pack about $370, needs a CAN host adapter). Option B: 36 V kit with its own generic pack (cheaper, simpler, misses R2, drops SwapCell). Recommendation: A, with B kept as a later low-cost variant.
2. **Budget.** Options: (a) treat the solar set as optional when a village hub exists, so the bike kit (about $175) meets $250; (b) cut cost (a local-made cradle, cheaper panel) to reach $250; (c) raise `budget_usd` to $300. Recommendation: (a) and redefine R12 as "bike kit $250 or less; solar set costed separately". `project.yaml` is unchanged.
3. Geared front hub motor rather than direct drive, rear hub or mid-drive.
4. Pack in the main triangle on the down tube rather than on the rear carrier.
5. Motor laced locally into a 28 in rim rather than a pre-built wheel.
6. Assist cutoff at 20 km/h by default rather than 25 km/h.
7. Pedal assist plus 6 km/h walk assist; no throttle.
8. Charge on the bike through the cradle, with the host adapter acting as the SwapCell charge host.
9. First partner and region for co-design.

### Safety concerns

- About 468 Wh lithium-ion pack: BMS, fused output, charging in shade on a non-combustible surface, no charging of damaged or wet packs.
- Fork dropout failure from motor reaction torque: torque arms on both sides are mandatory; filed or cracked dropouts must not be converted; fork fatigue is unverified.
- Braking: about 2 to 3 times the kinetic energy of an unassisted loaded roadster, with rod and rim brakes that are weak in the wet.
- Water in connectors causing sudden loss of assist or shorts; front-wheel spin on loose ground with a rear load.

### Problems and notes

- The README "Key components" list still says "36 V 10 Ah pack (SwapCell compatible)", from the scaffold. This session only inserted the hero and links as instructed. Update it once decision 1 is made.
- The SwapCell interface requires a host heartbeat for both discharge and charge, so off-the-shelf controllers and chargers need the host adapter (item 5). Any need to change the SwapCell interface should be raised with that project, not changed here.
- The legacy `cad/src/model.py` placeholder is untouched (TRL 3 work).

### Recommended next step

Review this note and the media, then decide items 1 and 2. If approved, run `/advance-trl3` to check the energy, hill, thermal, braking and fork load estimates by calculation and produce the parametric model and drawing sheet.

## Session 2026-09-25: TRL 3

Authority: on 2026-09-25 Amish wrote "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." He also approved the SwapCell interface v0.3 additions (wake, charge-discharge mode, latch vibration rating) and the rule that shared SwapCell packs are priced once and excluded from each kit budget. TRL 4 is on hold by his instruction.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (SSP-DDR-001 v0.1): decided and open items (below).
- `docs/04-calcs/01-sizing.md` (SSP-CAL-001 v0.1) with `docs/04-calcs/sizing.py` and `docs/04-calcs/results.csv`: mass, energy and range, hill and motor heating, solar, SwapCell items W, C and V, torque arms, cradle retention, pack fit, braking, cost, and a status for every requirement.
- `cad/src/model.py`: parametric build123d model (donor roadster, motor, torque arms, SwapCell envelope, cradle with V1 lever and receptacle, host adapter, controller, solar set) with fit checks; exports `cad/step/` and `cad/stl/` (`sunspoke-kit`, `sunspoke-cradle-with-pack`, `sunspoke-assembly`).
- `cad/src/sheets.py` and `cad/drawings/SSP-DWG-001` (SVG, PDF, PNG): general arrangement at Rev P1 with a 1:5 cradle detail, "PRELIMINARY, NOT FOR FABRICATION". SSP-DWG-001 was free (the concept sheet is SSP-DWG-010).
- `bom/bom.csv` and `bom/bom-notes.md`: every line priced with a supplier type; cradle $22 to $28 (V1 lever, coding resistor), host adapter $12 to $14 (charge inlet); pack $414 from SWC-CAL-001, excluded.
- `docs/01-problem.md`, `docs/02-concept.md`, `docs/03-requirements.md` moved to v0.3 (decisions, corrected numbers, new R13, R1 and R12 redefined, status column).
- `cad/src/concept_media.py` now draws from the model; all media refreshed and checked (flow labels shortened to stop overlap; exploded callouts moved apart). Temporary `media/_views*` folders deleted.
- `project.yaml`: `trl: 3`, `trl_target: 3`, evidence listed; `budget_usd` unchanged at 250. `README.md`: TRL 3 badge, budget line, drawing and calc links, key components. The README no longer had a literal "36 V 10 Ah" line (it read "48 V SwapCell pack (proposed, see precis)"); it now states 48 V as decided.
- Citations: two sources checked with web search on 2026-09-25 and added to SSP-PRB-001 (World Bicycle Relief "The Bike" page; Wikipedia "Pedelec" for Regulation (EU) No 168/2013, a secondary source). The other prior-work entries remain unsourced general descriptions and are flagged as unverified.

### Requirements (SSP-CAL-001)

| ID | Status | Value |
| --- | --- | --- |
| (none) | **Not met** | No requirement is shown to be not met |
| R3 | At risk | Motor winding about 100 °C at the top of the 500 m climb from 35 °C (base), about 139 °C in a hotter-motor case; 204 W and 32.5 N·m needed |
| R4 | At risk | 10 mm axle flats may need about 0.24 mm filed per side from 9.53 mm roadster slots |
| R11 | At risk | 8.5 m dry from 20 km/h (9 % margin); 21.7 m wet |
| R7, R9, R10, R13 | Not verifiable at TRL 3 | Sealing, swap time, cut-off timing, V1 retention (rotation margin 1.40 at 25 g) |
| R1, R5 | Met (specification, on paper) | 250 W, 20 km/h default, walk assist; pack fits the triangle with 164 mm removal travel |
| R2 | Met | 37 km design case (23 km with 80 kg cargo) |
| R6 | Met | 6.65 kg |
| R8 | Met | 27 km/day; 1.3 days to recharge |
| R12 | Met (redefined) | Bike kit $183; solar set $86 separately; pack $414 in SwapCell |

The model check found that the TRL 2 pack position (52 % up the down tube) left only 135 mm of removal travel against 143 mm needed; the pack now sits at 48 %.

### Decisions recorded (Decided by Amish, 2026-09-25: go with recommendation)

48 V on SwapCell (Option A; 36 V only as a later variant); budget kept at $250 with R12 redefined to the bike kit and the solar set costed separately; geared front hub; pack on the down tube; local lacing; 20 km/h default cut-off; pedal assist plus walk assist, no throttle; charge on the bike with the host adapter as charge host; SwapCell interface v0.3 items W, C and V; SwapCell pack priced once and excluded.

### Still awaiting Amish

1. First co-design partner and region (no recommendation; picked per area later).
2. Whether light slot filing is acceptable with torque arms (R4; no recommendation until the donor survey).
3. New proposal: handlebar power switch in series with the INTERLOCK coding resistor, host adapter powered from legacy discharge or the charge inlet. Recommendation: adopt.
4. New proposal: controller with a motor thermistor input so R3 becomes a derate, not a cutout. Recommendation: adopt.
5. For the SwapCell project, not changed here: interface v0.3 should state that a pack in legacy discharge (state 5) moves to heartbeat discharge (mode 2) without opening the output.

### Safety concerns

- Wet braking: about 22 m from 20 km/h with rod brakes on steel rims, versus 8.5 m dry. R11 covers only dry roads; a wet target and better blocks should be considered.
- Motor overheating on long loaded climbs in heat; a cutout on a hill can stall a loaded bike.
- Pack retention: V1 lever and clamp torque are safety-critical; rotation margin at 25 g is only about 1.4 on paper.
- Fork dropouts: torque arms mandatory; filed or cracked dropouts must not be converted; fork fatigue unverified.
- 468 Wh lithium-ion pack: charge in shade on a non-combustible surface; no damaged or wet packs.

### TRL 4 material

None found. `build-log/` holds only its README; `electronics/` and `firmware/` are empty. Nothing beyond TRL 3 was created.

### Recommended next step

Amish reviews SSP-DDR-001 open items 1 to 4 and forwards item 5 to the SwapCell project. Paper work that stays within TRL 3: pick a named 250 W geared hub and controller and rerun R3 with datasheet values, and define the donor survey questions (slot width, down tube diameter, frame size) with the partner once chosen.

TRL 4 is on hold by Amish's instruction. For the record only, TRL 4 would need: a bench-built kit on a donor roadster, a lab test report (TST, `environment: lab`) covering motor temperature on a loaded climb profile, brake cut-off timing, stopping distance dry and wet, cradle vibration and shock to latch class V1, and IP checks, plus build log entries.
