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
