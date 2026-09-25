# BOM notes

**The SwapCell pack (item 6) is not included in the kit cost.** By Amish's portfolio rule of 2026-09-25, a SwapCell pack is priced once in the SwapCell repo ($414 in prototype parts, SWC-CAL-001) and excluded from each dependent kit budget. It is listed here so the numbering matches the exploded view and the full system cost is visible.

Every line is priced. Prices are indicative estimates with a supplier type, not quotes from named suppliers; they are checked by `docs/04-calcs/sizing.py` (SSP-CAL-001 section 11).

| Group | Items | Cost (USD) |
| --- | --- | --- |
| Bike conversion kit | 1 to 5, 7 to 9, 14 | 183 |
| Solar charging set, costed separately | 10 to 13 | 86 |
| Kit plus solar set, pack excluded | 1 to 5, 7 to 14 | 269 |
| SwapCell pack (priced in SwapCell) | 6 | 414 |
| Full system for one rider with own panel | all | 683 |

R12 was redefined by Amish's decision of 2026-09-25 (SSP-DDR-001): the bike kit must cost $250 or less, and the solar set is costed separately. The bike kit meets this with $67 margin. `budget_usd` in `project.yaml` stays at $250. Generic parts make up about 84 % of the kit plus solar set cost.
