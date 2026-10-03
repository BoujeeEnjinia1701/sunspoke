# BOM notes

**The SwapCell pack (item 6) is not included in the kit cost.** By Amish's portfolio rule of 2026-09-25, a SwapCell pack is priced once in the SwapCell repo ($414 in prototype parts, SWC-CAL-001) and excluded from each dependent kit budget. It is listed here so the numbering matches the exploded view and the full system cost is visible.

Every line is priced. Prices are indicative estimates with a supplier type, not quotes from named suppliers; they are checked by `docs/04-calcs/sizing.py` (SSP-CAL-001 section 11).

| Group | Items | Cost (USD) |
| --- | --- | --- |
| Bike conversion kit | 1 to 5, 7 to 9, 14, 15 | 208 |
| Solar charging set, costed separately | 10 to 13 | 90 |
| Kit plus solar set, pack excluded | 1 to 5, 7 to 15 | 298 |
| SwapCell pack (priced in SwapCell) | 6 | 414 |
| Full system for one rider with own panel | all | 712 |

R12 was redefined by Amish's decision of 2026-09-25 (SSP-DDR-001): the bike kit must cost USD 250 or less, and the solar set is costed separately. Value-engineering target: USD 250 (`budget_usd`, a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 208 (USD 42 under the target). Generic parts make up about 84 % of the kit plus solar set cost.

On 2026-09-25 Amish accepted the remaining recommendations (SSP-DDR-002): the motor now has a built-in winding thermistor ($70 to $72) and the controller a thermistor input with a current derate ($22 to $25), so the bike kit rose from $183 to $188. The handlebar power switch in the INTERLOCK loop (item 8) was already costed.

On 2026-10-01 the design was made constructable (SSP-DDR-003): line 2 (torque arms) became a made part at USD 6; line 4 (cradle) rose from USD 28 to USD 33 for the aluminium tray, V-saddles, a third band clamp, the hinge and the draw latch; line 12 (panel stand) from USD 10 to USD 14 for timber and coach bolts; line 14 (hardware) from USD 8 to USD 11 for four more band clamps and the controller pad. The bike kit rose from USD 188 to USD 196 and the solar set from USD 86 to USD 90.

Decided by Amish on 2026-10-02 (SSP-DEC-001): the kit includes wet-weather brake blocks suited to steel rims, front and rear. They are now line 15 of `bom.csv`: two pairs at USD 6 a pair, USD 12 in all. The basis is an indicative price for a generic replacement block of the kind sold for rod and caliper rim brakes, not a quote. The assumed wet friction of 0.25 is also not verified; it is replaced by the maker's data or by a wet braking test (TRL 4, on hold). The blocks replace the donor blocks, so they add 0.10 kg to the kit in the mass count to be safe, and the bike kit rose from USD 196 to USD 208. The reference motor for line 1 is a widely sold 250 W front geared hub such as one of Bafang's, with 10 mm axle flats unless the donor survey shows 3/8 in slots are the norm, in which case a motor whose flats fit them is looked for first.
