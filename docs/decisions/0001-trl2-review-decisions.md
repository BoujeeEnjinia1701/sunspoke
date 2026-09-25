---
doc_id: SSP-DDR-001
title: SunSpoke TRL 2 review decisions
project: SunSpoke
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's 2026-09-25 decisions on the TRL 2 review and the SwapCell interface v0.3 items
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted (items 1 to 8 and 10 to 13); items 14 to 18 remain proposed, awaiting Amish

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-24) listed nine items as "Proposed, awaiting Amish", and SSP-PRC-001 v0.2 marked every key design choice the same way. On 2026-09-25 Amish reviewed the review points for every portfolio repo and wrote: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." He also approved three cross-cutting additions to the SwapCell interface and a portfolio rule for pricing shared packs.

This record lists what that instruction decides and what it leaves open because there was no recommendation to accept. TRL 4 is on hold by Amish's instruction.

## Options considered

The options for each item are in `docs/REVIEW.md` (2026-09-24) and SSP-PRC-001 v0.2. They are not repeated here.

## Decision

*Table 1. Decided items.*

| # | Item | Decision | Where it now lives |
| --- | --- | --- | --- |
| 1 | System voltage and pack | Decided by Amish, 2026-09-25: go with recommendation. Option A: 48 V motor and controller on the SwapCell pack. Option B (36 V kit with its own pack) is kept only as a later low-cost variant | SSP-PRC-001 v0.3, SSP-REQ-001 v0.3, `README.md` |
| 2 | Budget | Decided by Amish, 2026-09-25: go with recommendation (a). Keep `budget_usd: 250`; redefine R12 as "bike kit $250 or less; solar set costed separately"; the pack is excluded | SSP-REQ-001 v0.3 R12, `project.yaml` unchanged |
| 3 | Motor type | Decided by Amish, 2026-09-25: go with recommendation. Geared front hub motor | SSP-PRC-001 v0.3 |
| 4 | Pack location | Decided by Amish, 2026-09-25: go with recommendation. Pack in the main triangle on the down tube | SSP-PRC-001 v0.3, SSP-DWG-001 |
| 5 | Wheel build | Decided by Amish, 2026-09-25: go with recommendation. Motor laced locally into a 28 in rim, with a lacing card | SSP-PRC-001 v0.3 |
| 6 | Assist speed limit | Decided by Amish, 2026-09-25: go with recommendation. 20 km/h default, adjustable only by the mechanic, never above 25 km/h | SSP-REQ-001 v0.3 R1 |
| 7 | Assist modes | Decided by Amish, 2026-09-25: go with recommendation. Pedal assist plus a 6 km/h walk assist; no throttle | SSP-REQ-001 v0.3 R1 |
| 8 | Charging | Decided by Amish, 2026-09-25: go with recommendation. Charge on the bike through the cradle charge port, with the host adapter acting as the SwapCell charge host; hub docks remain an option | SSP-PRC-001 v0.3 |
| 10 | SwapCell interface v0.3 item W (wake) | Decided by Amish, 2026-09-25 (cross-cutting approval). The cradle fits the 10 kΩ INTERLOCK coding resistor | SSP-PRC-001 v0.3, SSP-REQ-001 v0.3 R13 |
| 11 | SwapCell interface v0.3 item C (charge-discharge mode) | Decided by Amish, 2026-09-25 (cross-cutting approval). The host adapter requests mode 4 when the bike is switched on while charging | SSP-PRC-001 v0.3, R13 |
| 12 | SwapCell interface v0.3 item V (latch vibration rating) | Decided by Amish, 2026-09-25 (cross-cutting approval). The cradle is a class V1 vehicle receiver with an over-centre preload lever | SSP-PRC-001 v0.3, R13, SSP-DWG-001 |
| 13 | Shared pack pricing | Decided by Amish, 2026-09-25 (cross-cutting): the SwapCell pack is priced once in the SwapCell repo ($414, SWC-CAL-001) and excluded from this kit's budget | `bom/bom.csv`, `bom/bom-notes.md`, R12 |

Item 9 of the TRL 2 list (first partner and region) had no recommendation and is item 14 below.

### Items that remain open

*Table 2. Open items, Proposed, awaiting Amish.*

| # | Item | Status |
| --- | --- | --- |
| 14 | First co-design partner and region | Proposed, awaiting Amish. No recommendation was made; portfolio rule: partners are chosen per area later |
| 15 | Whether light filing of the donor fork slots (about 0.24 mm per side) is acceptable with torque arms fitted (R4) | Proposed, awaiting Amish. No recommendation yet; needs the donor survey |
| 16 | Handlebar power switch wired in series with the INTERLOCK coding resistor, and host adapter powered from legacy discharge or the charge inlet (SSP-CAL-001 section 6) | New engineering proposal from this session, awaiting Amish. Recommendation: adopt |
| 17 | Motor temperature input on the controller to derate instead of cutting out (R3) | New engineering proposal, awaiting Amish. Recommendation: specify a controller with a thermistor input |
| 18 | Clarification to raise with the SwapCell project: the pack should move from legacy discharge (state 5) to heartbeat discharge (mode 2) without opening the output | Flag for SwapCell; not changed here. The interface is governed in the swapcell repo |

## Consequences

- SunSpoke builds to SwapCell interface v0.3 and cites items W, C and V. A new requirement R13 records this.
- R1 now states the 20 km/h default cut-off, the walk assist and the ban on a throttle. R12 is redefined; `budget_usd` stays at 250.
- SSP-PRB-001, SSP-PRC-001 and SSP-REQ-001 move to v0.3. TRL is set to 3. No TRL 4 work is started.
