---
doc_id: SSP-DEC-001
title: SunSpoke design decisions register
project: SunSpoke
doc_type: Design decisions register
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: Register opened with the build plan; open decisions from the decision records, the review note and the design for construction
  - version: "0.2"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Amish approved the recommendations for all eleven open decisions (SSP-DDR-003 accepted); moved to decisions made; To confirm items 1 and 2 updated"
---

# SunSpoke design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/` or in the review note; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

None. All open decisions were decided on 2026-10-02.

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The motor's axle has 10 mm flats (or, if the donor survey shows 3/8 in slots are the norm, flats that fit them; decided 2026-10-02), an M12 thread and enough length for three threads past the nut over the dropout, torque arm and washer | The torque arms and dropouts are sized to it | SSP-DDR-003, P7 |
| 2 | The donor's dropout slots take the 10 mm flats without filing (never file the fork, decided 2026-10-02), its down tube is round and 28 to 32 mm, and the step from dropout face to blade outside is about 8 mm | The saddles, torque arm slot and joggle are sized to these | SSP-DDR-003, P1 and P7 |
| 3 | The donor's bottom bracket is cup-and-cone with a left lockring | The pedal-assist bracket fits under it | SSP-DDR-003, P9 |
| 4 | The draw latch: adjustable hook, safety catch, 500 N working load or more, over centre with 50 N or less at its lever | It sets the V1 preload of 330 N | SSP-DDR-003, P4; SSP-CAL-001 section 8 |
| 5 | The band clamp torque that gives 1.5 kN of band tension | The cradle retention margins assume it | SSP-CAL-001 section 8 |
| 6 | The SwapCell receptacle's flange and hole pattern | The end stop's four holes are drawn for a 37 x 24 mm pattern | SSP-DDR-003, P3 |
| 7 | The host adapter's base inserts (two, 40 mm apart) and the controller case size | The tray holes and the band clamps are sized to them | SSP-DDR-003, P6 and P8 |
| 8 | The panel's mounting hole positions on its frame | The stand's rail holes are drilled to match | SSP-DDR-003, P12 |
| 9 | The pack moves from legacy discharge (state 5) to heartbeat discharge (mode 2) without opening its output | The bike relies on it if the adapter is slow to start; raised with SwapCell | SSP-DDR-002, item 18 |
| 10 | A low-cost boost charger with input-voltage tracking gives near-MPPT yield from one 18 V panel | R8 assumes 92 % | SSP-PRC-001, open questions |

## Value engineering

Value-engineering target: USD 250 for the bike kit (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 196 for the bike kit (USD 54 under the target). The solar set is costed separately at USD 90, and the SwapCell pack (USD 414) is priced once in the SwapCell project. Main cost drivers and savings worth trying:

- The largest lines are the motor wheel (USD 72), the receiver cradle (USD 33), the controller (USD 25), the harness (USD 15), the host adapter (USD 14) and the handlebar display and brake sensors (USD 14).
- Making the design constructable added USD 8 to the bike kit (cradle USD 28 to 33, hardware USD 8 to 11) and USD 4 to the solar set (stand USD 10 to 14).
- Savings worth trying: buy the receptacle, draw latch and hinge in batches with other SwapCell vehicle receivers; fold the tray from 2 mm aluminium if the retention and end stop margins still hold; a shared panel and stand at a village hub removes the USD 90 solar set for riders who swap packs there.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | 48 V on the SwapCell pack; budget kept at USD 250 with R12 covering the bike kit and the solar set costed separately; geared front hub; pack on the down tube; local lacing; 20 km/h default cut-off; pedal assist and walk assist, no throttle; charge on the bike; SwapCell interface v0.3 items W, C and V; pack priced once in SwapCell | Amish: go with recommendation | SSP-DDR-001, items 1 to 13 |
| 2026-09-25 | Handlebar power switch in the INTERLOCK loop; motor thermistor with a controller derate instead of a cutout; raise the legacy-to-heartbeat transition with SwapCell | Amish: "i accept all your recommendations, go with them across all repos." | SSP-DDR-002, items 16 to 18 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | SSP-DDR-003 (Draft, open for review: open decision 1) |
| 2026-10-01 | Treat `budget_usd` as a value-engineering target, not a limit | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens" | STANDARDS section 18; this register's Value engineering section |
| 2026-10-02 | Design for construction accepted: the changes P1 to P13 as made (open item 1) | Amish: "i approve your recommendations for all 555 open decisions." | SSP-DDR-003, Table 1 |
| 2026-10-02 | Pack swap: gate and draw latch as modelled (option a) for the prototype, reviewed after the first swap trials (open item 2) | Amish: "i approve your recommendations for all 555 open decisions." | SSP-DDR-003, A1 |
| 2026-10-02 | Panel stand in timber (option a) (open item 3) | Amish: "i approve your recommendations for all 555 open decisions." | SSP-DDR-003, A2; review note 2026-09-26, proposal 4 |
| 2026-10-02 | Donor fork slots are never filed for now: donors are chosen whose slots take 10 mm flats, and if the donor survey shows 3/8 in slots are the norm, a motor whose axle flats fit them is looked for first (open item 4) | Amish: "i approve your recommendations for all 555 open decisions." | SSP-DDR-001, item 15 |
| 2026-10-02 | Default region western Kenya and eastern Uganda, where 28 in roadsters and bicycle taxis are common, with a bicycle mechanics' group or rural transport organization there as the partner type; the partner is named when the portfolio picks partners for this area (open item 5) | Amish: "i approve your recommendations for all 555 open decisions." | SSP-DDR-001, item 14 |
| 2026-10-02 | Vertical cranks in the renders accepted (open item 6) | Amish: "i approve your recommendations for all 555 open decisions." | Review note 2026-09-26, proposal 1 |
| 2026-10-02 | Saddle raised about 12 mm in the renders accepted (open item 7) | Amish: "i approve your recommendations for all 555 open decisions." | Review note 2026-09-26, proposal 2 |
| 2026-10-02 | Brake sensors under the bar beside the levers accepted, as `model.py` already has them (SSP-DDR-003, P10) (open item 8) | Amish: "i approve your recommendations for all 555 open decisions." | Review note 2026-09-26, proposal 3 |
| 2026-10-02 | Seated rider kept in the hero render, revisited if it reads oddly (open item 9) | Amish: "i approve your recommendations for all 555 open decisions." | Review note 2026-09-26, proposal 5 |
| 2026-10-02 | Wet braking treated as a safety item: a wet stopping target is added to R11, wet-weather brake blocks suited to steel rims go in the kit, and trials keep a no-wet-riding rule until a wet braking test meets the target (open item 10) | Amish: "i approve your recommendations for all 555 open decisions." | SSP-PRC-001, open questions; SSP-CAL-001 section 10; SSP-REQ-001 R11 |
| 2026-10-02 | Reference motor: a widely sold 250 W front geared hub, such as one of Bafang's; its maker is asked for winding resistance, thermal capacity and gear temperature limit and R3 is rerun; the winding resistance is measured at TRL 4 if the data are not published (open item 11) | Amish: "i approve your recommendations for all 555 open decisions." | SSP-PRC-001, open questions |
