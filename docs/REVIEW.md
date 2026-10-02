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

### Still awaiting Amish (items 3 to 5 decided later the same day, see the next session)

1. First co-design partner and region (no recommendation; picked per area later).
2. Whether light slot filing is acceptable with torque arms (R4; no recommendation until the donor survey).
3. Handlebar power switch in series with the INTERLOCK coding resistor, host adapter powered from legacy discharge or the charge inlet. Decided by Amish, 2026-09-25: go with recommendation (SSP-DDR-002).
4. Controller with a motor thermistor input so R3 becomes a derate, not a cutout. Decided by Amish, 2026-09-25: go with recommendation (SSP-DDR-002).
5. Decided by Amish, 2026-09-25: go with recommendation (raise with SwapCell; cross-repo action, SSP-DDR-002). For the SwapCell project, not changed here: interface v0.3 should state that a pack in legacy discharge (state 5) moves to heartbeat discharge (mode 2) without opening the output.

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

## Session 2026-09-25: recommendations accepted

Authority: on 2026-09-25 Amish wrote "i accept all your recommendations, go with them across all repos." Every open item with a recommendation is now "Decided by Amish, 2026-09-25: go with recommendation", recorded in `docs/decisions/0002-recommendations-accepted.md` (SSP-DDR-002 v0.1). Items without a recommendation stay open. TRL stays at 3.

### Decisions applied and what changed

| Item (SSP-DDR-001) | Decision | Change, before and after |
| --- | --- | --- |
| 16, power switch in the INTERLOCK loop | Adopt | R10 now requires the switch; already costed in BOM item 8 and shown on the drawing, so no cost or geometry change |
| 17, motor thermistor and controller derate | Adopt | BOM item 1 $70 to $72, item 3 $22 to $25; bike kit $183 to $188 (margin $67 to $62); generic share 84 % to 85 %. R3 restated: derate from 110 °C, winding at or below 120 °C, no abrupt cutout. New CAL result: derate starts after 697 m of the 8 % climb (base case, so the 500 m design climb runs at full assist) or 225 m (hot case); sustained 4.7 or 3.7 km/h on an unending climb |
| 18, legacy-to-heartbeat transition | Raise with SwapCell | Cross-repo action below; nothing changed here |

`budget_usd` stays at $250 (the budget decision of SSP-DDR-001 already redefined R12 to the bike kit). Documents changed: SSP-REQ-001 v0.3 to v0.4, SSP-PRC-001 v0.3 to v0.4, SSP-CAL-001 v0.1 to v0.2, SSP-DDR-001 v0.1 to v0.2, SSP-DWG-001 Rev P1 to P2 (notes only; geometry unchanged), new SSP-DDR-002 v0.1. `bom/bom.csv`, `bom/bom-notes.md`, `docs/04-calcs/sizing.py` and `results.csv`, `cad/src/sheets.py` and `concept_media.py` (blueprint cost) updated; STEP, STL, drawings, media and PDFs regenerated.

Other work this session: all generated files re-rendered so the footer reads designmolecule.com; README gains "Concept rationale", "Burning platform", "Where it could be used" and "What sparked the idea" (the 1895 Bolton hub-motor bicycle patent, US 552,271).

### Requirement status (SSP-CAL-001 v0.2)

| Status | Requirements |
| --- | --- |
| Not met | None |
| At risk | R3 (100 °C base, 139 °C hot case; hot case now derates after 225 m instead of cutting out), R4 (slot filing about 0.24 mm per side), R11 (8.5 m dry, 21.7 m wet) |
| Not verifiable at TRL 3 | R7, R9 (85 % generic), R10, R13 |
| Met | R1, R2 (37 km), R5, R6 (6.65 kg), R8 (27 km/day, 1.3 days), R12 (bike kit $188) |

### Still awaiting Amish

1. First co-design partner and region (no recommendation).
2. Whether light slot filing is acceptable with torque arms (R4; no recommendation until the donor survey).

### Cross-repo actions

- **SwapCell:** interface v0.3 should state that a pack in legacy discharge (state 5) moves to heartbeat discharge (mode 2) without opening the output (SSP-DDR-001 item 18, decided). Not changed here.

### TRL 4

TRL 4 remains on hold by Amish's instruction. Choosing and calibrating a real thermistor derate curve and a hill test are TRL 4 work and were not started. `trl: 3`, `trl_target: 3`.

## Session 2026-09-26: sources strengthened

README "Where it could be used" country table, per Amish's instruction of 2026-09-26 ("Fix the weaker sources"). Every link below was fetched and checked against the claim it supports.

| Row | Old source | New source |
| --- | --- | --- |
| Uganda and Kenya | Wikipedia, "Boda boda" (alone) | *Daily Monitor* (Uganda), May 25, 2017; row now states only the Busia "border, border" origin it reports (the "1980s" date is dropped) |
| Malawi, Tanzania and Zambia | World Bank 2025 press release, which names no countries | Row renamed "Wider sub-Saharan Africa"; same World Bank source, now matching what it says |
| India and Bangladesh | None | Replaced by "India": TERI, *Benefits of Cycling in India* (2020), reporting Census of India bicycle ownership and rural work-trip share |
| Andean and Central American highlands | None | Replaced by "Haiti": World Bank press release, October 18, 2024 (access about 47.1 percent in 2021; solar mini-grid financing) |
| Netherlands | DutchNews.nl (alone) | BOVAG and RAI Vereniging press release, February 26, 2024 (804,000 bicycles, about 56 percent e-bikes); DutchNews.nl kept alongside |

"What sparked the idea" already rests on the primary patent record (Google Patents, US552271A); rechecked, unchanged. No controlled document changed. Still open: `docs/01-problem.md` prior-work line on pedelec rules cites Wikipedia alone; it is outside this session's scope and should cite Regulation (EU) No 168/2013 on EUR-Lex at the next revision.

## Session 2026-09-26: product appearance model and photoreal renders

Amish chose this repo for the first batch of product renders on 2026-09-26. This session adds `cad/src/product_model.py`, an appearance model for photoreal renders, and points the README hero at `media/render-hero.png` (with an exploded render link); the render files are produced separately.

### What product_model.py adds

- `product_parts()`: 96 parts (66 shell, 15 internal, 14 accessory, 1 context), each with colour, material class, BOM line and explode offset. All main dimensions and interfaces come from `PARAMS`, `geometry()`, `cradle_location()`, `pack_local()` and `receptacle_local()` in `model.py`.
- Donor roadster, shown as part of the product: lugged black enamel frame, fork, chrome stem and swept bars with ribbed grips and brake levers, sprung leather saddle, tube carrier, chainring, chain and block pedals, and 36-spoke wheels.
- Item 1: brushed hub motor with ribbed drum, spoke flanges, side covers and screws, a teal band, rating label, keyed axle, axle nuts and the cable exit, laced into the front rim.
- Item 2: keyed torque arms with band clips and bolts on both fork blades.
- Items 4 and 6: the cradle with guides, end stop and receptacle; the teal V1 preload lever with grip and pivot pin; stainless band clamps with rubber liners and screws; and the SwapCell pack with dark end caps, carry handle, accent stripe, label and a four-segment charge gauge (three segments lit).
- Item 5: potted host adapter with a parting line, the keyed charge inlet, a lit status light and a label.
- Item 3: finned aluminium controller with sealed end caps, glands, a name plate and straps to the seat tube.
- Items 7 to 9: magnet disc and Hall sensor; handlebar display with lit assist and charge segments, power switch, walk-assist button and two brake-lever sensors; harness with cable ties and a sealed fuse holder behind a clear cover.
- Items 10 to 13: panel with aluminium frame, 24 cells, busbars and junction box; timber A-frame stand with coach bolts; finned boost charger with a lit charge light; panel lead; and the 5 m charge cable with its plug in the charge inlet.
- Context: the shared clay mannequin (1.75 m) in the "ride" pose, placed on the bike's bottom bracket, with the torso and arm angles set so the hands close on the grips and the feet land on the pedals.
- `TITLE` and three `RENDER_VIEWS`: "hero" (front right, about 18 deg elevation, rider and solar set), "exploded" (front right, about 28 deg), and "detail" (front right, about 12 deg: the hub motor wheel, fork and torque arms without the rider).

### Where the appearance model differs from model.py

Each is render-only; `model.py`, the STEP files and SSP-DWG-001 are unchanged.

1. **Cranks turned to vertical** so the rider's feet sit on the pedals (cranks rotate; no dimension changes). Proposed, awaiting Amish. Recommendation: accept.
2. **Saddle top raised about 12 mm** (to about 964 mm) to meet the mannequin's seat point. Proposed, awaiting Amish. Recommendation: accept; it is within normal saddle-height adjustment.
3. **Brake cut-off sensors moved about 45 mm forward and 32 mm lower** (to X = 905 mm, Z = 918 mm, under the bar at the lever pivots) so the rider's hands clear them; `model.py` places them on the grip section. Proposed, awaiting Amish. Recommendation: move the envelopes in `model.py` to match at the next drawing revision.
4. **Panel stand drawn as square timber** (36 mm legs, 28 x 24 mm rails) instead of round tube, plus a small upright for the charger, which floats in `model.py`. The BOM allows steel angle or timber. Proposed, awaiting Amish. Recommendation: accept, and add the charger upright to `model.py` at the next revision.
5. **Hero scene shows the rider seated while the pack charges** from the panel (the adapter's mode 4, bike on while charging). This reads as a waiting rider rather than riding. Proposed, awaiting Amish. Options: keep it; or pose a standing owner beside the parked bike. Recommendation: keep it for one image that shows the whole system; revisit if the render reads oddly.

### TRL

This is an appearance model only: no tolerances, fabrication detail or build instructions were added. `trl: 3` and `trl_target: 3` are unchanged, and TRL 4 remains on hold by Amish's instruction.

## Session 2026-09-27: kit 1.5.0 and image quality

- Kit 1.5.0 synced: STANDARDS v1.5 (sections 12 to 15: product renders, storefront images and image quality, public release, authorship and signing), `.kit/cards.py`, `.kit/image_qc.py`, `.kit/release_gate.py`, issue templates, and the `/render-product` and `/release` commands. `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Every `media/render-*.png` recaptioned from its original render with the new layout: the title, concept label and repository sit in a band above the render and the view note in a band below it, each line wrapped to the image width, so no text overlaps other text or the render or runs off the image. `media/card.png` and `media/social-preview.png` regenerated with the same rules.
- `python .kit/image_qc.py` and `python .kit/release_gate.py` pass. trl stays 3.

## Session 2026-10-01: kit 1.7.0, design made constructable, build plan

Authority: Amish's instruction of 2026-09-30 to give every repo the approved build plan and to "fix the design assumptions to match and be physically feasible as you draw the illustrations", with open decisions in a separate register (SSP-DEC-001), and his 2026-10-01 guidance that `budget_usd` is a value-engineering target. Kit 1.7.0 installed (`.kit/`, `.claude/commands/`, `CLAUDE.md`).

### Design changes made for construction (SSP-DDR-003, Draft, open for Amish's review)

1. Cradle base: the concept's flat plate cut into the down tube; now a folded 3 mm 5052 aluminium tray on three 120 degree aluminium V-saddles with rubber liners (aluminium, not steel, to hold the cradle at 1.10 kg).
2. Band clamps: drawn as rings through the plate; now three band clamps (was two), each through two slots in the tray, round the saddle and under the tube. The real band path wraps about 150 degrees of the tube, so a third band was needed to keep the 25 g rotation margin (1.44, was 1.40).
3. End stop: a solid block with the receptacle inside it; now a folded aluminium end stop with an open-topped plug notch, bolted to the tray and guides, the receptacle bolted behind it.
4. V1 lever: three loose blocks whose hinge stood in the pack's path, so the pack could not come out; now a drop-down gate with a rubber pad on a butt hinge, closed by an over-centre draw latch with a safety catch (330 N preload, latch pull about 314 N).
5. Slide rails and catch: loose steel bars; now HDPE slide strips and a steel catch bar on screws from below.
6. Host adapter: floating beyond the base; now on a 70 mm extension of the tray with a lead to the receptacle.
7. Torque arms: ran into the fork blades, clips not joined; now joggled 20 x 5 mm steel arms with an open 10 mm slot on the axle flats, held by a band clamp round blade and arm. Donor dropouts and a 150 mm axle added to the model.
8. Controller: floating; now on a rubber pad with two band clamps round the seat tube.
9. Pedal-assist sensor: disc on nothing, no sensor; now a disc clamped on the spindle and a Hall sensor on a bracket under the left lockring.
10. Display and brake sensors: cut into the bar; now each on its own bar clamp, magnets on the levers (matches proposal 3 of 2026-09-26).
11. Harness: through open space and the cradle; now routed along the left side of the tubes.
12. Panel stand: legs ran into the panel, nothing held it; now a bolted timber A-frame, panel bolted to its rails, charger on the rear leg.
13. Front wheel spokes now run from the motor's flanges (context).

`cad/src/model.py` now runs 57 constructability checks (`--check`), including the pack's removal path; all pass.

### Key results (SSP-CAL-001 v0.3)

| Quantity | Before | Now |
| --- | --- | --- |
| Added mass with pack (R6, 7 kg) | 6.65 kg | 6.78 kg (0.22 kg margin) |
| Retention at 25 g: axial / rotation margin | 6.8 / 1.40 | 7.7 / 1.44 |
| End stop at 25 g | (solid block) | about 62 MPa, factor 3.1 on yield |
| Pack clearance in the triangle; free travel | 123 mm; 164 mm | 121 mm; 165 mm (143 needed), path checked |
| Bike kit cost (value-engineering target USD 250) | USD 188 | USD 196, USD 54 under the target |
| Solar set cost | USD 86 | USD 90 |

No requirement changed status: none not met; R3, R4 and R11 at risk; R7, R9, R10 and R13 not verifiable at TRL 3.

### Files

- New: `docs/05-build-plan.md` (SSP-BLD-001 v0.1), `docs/06-design-decisions.md` (SSP-DEC-001 v0.1), `docs/decisions/0003-design-for-construction.md` (SSP-DDR-003 v0.1), `cad/src/build_plan_media.py`, `cad/drawings/SSP-DWG-101` to `110`, `docs/05-build-plan/` (3 overviews, tray layout, wiring, 10 joints, 15 steps).
- Updated: `cad/src/model.py`, `cad/src/sheets.py` (SSP-DWG-001 Rev P3), `cad/src/concept_media.py`, `cad/step/`, `cad/stl/`, `media/` concept media and `model.glb`, `bom/bom.csv` (lines 2, 4, 7, 8, 12, 14), `bom/bom-notes.md`, `docs/04-calcs/sizing.py` and `results.csv`, SSP-CAL-001 v0.3, SSP-REQ-001 v0.5, SSP-PRC-001 v0.5, `project.yaml` (`design_state: constructable`, new evidence), `README.md`.

### Proposed, awaiting Amish

All in the design decisions register: accept SSP-DDR-003 (decision 1); the two-movement pack swap (2); timber stand (3); plus the open items carried over (fork slot filing, co-design partner, appearance-model proposals 1, 2, 3 and 5 of 2026-09-26, wet braking, motor data).

### Stale media (made on Amish's Mac)

The design changed visibly at the cradle, lever, torque arms and panel stand, so `media/render-hero.png`, `media/render-exploded.png`, `media/render-detail.png`, `media/card.png`, `media/social-preview.png` and the appearance model `cad/src/product_model.py` are stale and need regenerating on the Mac. They were not regenerated here.

### Safety

Unchanged hazards (lithium pack, retention, fork dropouts, wet braking, motor heat). The build plan adds seven safety stops (S1 to S7); first rides are TRL 4 tests on a closed, dry site. Retention depends on the three band clamps being at torque and the latch's safety catch being on.

### Recommended next step

Amish reviews SSP-DDR-003 and the register. TRL 4 (building to the plan) remains on hold; trl stays 3.
