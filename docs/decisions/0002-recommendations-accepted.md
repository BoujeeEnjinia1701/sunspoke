---
doc_id: SSP-DDR-002
title: SunSpoke recommendations accepted
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
  change: Record Amish's acceptance of all open recommendations and what changed in the repo
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted (items 16, 17 and 18 of SSP-DDR-001); items 14 and 15 remain proposed, awaiting Amish

## Context

After the TRL 3 session, SSP-DDR-001 left five items open. Three carried a recommendation (items 16, 17 and 18) and two did not (items 14 and 15). On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." This record lists what that decides for SunSpoke, what changed in the repo, and what stays open. TRL 4 remains on hold by Amish's instruction, and the project stays at TRL 3.

## Options considered

The options and recommendations are in SSP-DDR-001 (Table 2), SSP-CAL-001 v0.1 sections 4 and 6, and `docs/REVIEW.md` (session 2026-09-25, TRL 3). They are not repeated here.

## Decision

*Table 1. Newly decided items.*

| # (SSP-DDR-001) | Item | Decision | What changed in the repo |
| --- | --- | --- | --- |
| 16 | Handlebar power switch in series with the INTERLOCK coding resistor; host adapter powered from legacy discharge or the charge inlet | Decided by Amish, 2026-09-25: go with recommendation (adopt) | R10 in SSP-REQ-001 v0.4 now requires the switch in the INTERLOCK loop; SSP-PRC-001 v0.4 records it as decided. The switch was already costed in BOM item 8 and shown on SSP-DWG-001, so cost and geometry are unchanged |
| 17 | Motor temperature input on the controller so an overheat becomes a derate, not a cutout (R3) | Decided by Amish, 2026-09-25: go with recommendation (controller with a thermistor input; motor with a winding thermistor) | R3 restated in SSP-REQ-001 v0.4 (derate from 110 °C, winding at or below 120 °C, no abrupt cutout). BOM item 1 $70 to $72 (built-in 10 kΩ NTC thermistor), item 3 $22 to $25 (thermistor input and derate); bike kit $183 to $188. SSP-CAL-001 v0.2 adds a derate calculation. SSP-DWG-001 notes updated, Rev P1 to P2 |
| 18 | Raise with the SwapCell project that a pack in legacy discharge (state 5) should move to heartbeat discharge (mode 2) without opening the output | Decided by Amish, 2026-09-25: go with recommendation (raise with SwapCell) | Listed under cross-repo actions in `docs/REVIEW.md`. The interface is governed in the swapcell repo and is not changed here |

### Effect on requirements and budget

- `budget_usd` stays at $250. The budget decision (SSP-DDR-001 item 2) already redefined R12 to cover the bike kit only; the bike kit is now $188, still inside the target with $62 margin.
- R3 stays **at risk**. With the derate, the base case runs the 500 m design climb at full assist (derating would start only after about 697 m). In the hot-motor case derating starts after about 225 m, and on a climb that does not end the loaded bike slows to about 3.7 km/h instead of stalling. A named motor's thermal data are still needed.
- No requirement is shown to be not met.

### Items still open

*Table 2. Proposed, awaiting Amish (no recommendation to accept).*

| # (SSP-DDR-001) | Item | Status |
| --- | --- | --- |
| 14 | First co-design partner and region | Proposed, awaiting Amish. No recommendation; partners are chosen per area later |
| 15 | Whether light filing of the donor fork slots (about 0.24 mm per side) is acceptable with torque arms fitted (R4) | Proposed, awaiting Amish. No recommendation until the donor survey |

## Consequences

- SSP-REQ-001 and SSP-PRC-001 move to v0.4, SSP-CAL-001 to v0.2, SSP-DDR-001 to v0.2, and SSP-DWG-001 to Rev P2.
- Specifying and testing the derate on real hardware (thermistor calibration, derate curve, hill test) is TRL 4 work and is on hold by Amish's instruction. Nothing past TRL 3 was started.
