---
doc_id: SSP-PRB-001
title: SunSpoke problem statement
project: SunSpoke
doc_type: Problem statement
version: "0.4"
status: Draft
date: '2026-10-02'
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
  change: Populate to TRL 2 (users, context, constraints, out of scope, prior work)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record SSP-DDR-001 (48 V on SwapCell, budget covers the bike kit only, pack priced in SwapCell); add checked sources to prior work
- version: "0.4"
  date: '2026-10-02'
  author: Amish Chadha
  change: "First region and partner type decided by Amish on 2026-10-02 (SSP-DEC-001)"
---

# SunSpoke problem statement

Most bicycles in rural sub-Saharan Africa are unpowered steel roadsters that carry people, water, firewood and goods over long, rough, hilly routes, and the electric alternatives on sale are either a whole new e-bike or a closed kit that local mechanics cannot repair and that assumes grid charging. Design with, not for: requirements must come from co-design sessions and field trials with the intended users through a local partner.

## The problem

The heavy single-speed roadster (28 in wheels, steel frame, rod or cable brakes, strong rear carrier) is the working vehicle of rural East, Central and Southern Africa and of many low-income regions elsewhere. Riders routinely carry 30 to 80 kg of goods or a passenger over 10 to 30 km a day on dirt roads. The limit is the rider's own power: hills and loads turn a 20 km trip into hours of walking and pushing.

Electric assist solves this, and e-bikes and conversion kits are already sold in the region. Three gaps remain:

1. **Fit.** Most kits are designed for modern aluminium bikes with 26 or 29 in wheels, disc brakes and threaded bottle-cage bosses. Roadsters have 28 in (ETRTO 635) rims, narrow steel dropouts, rod brakes and no mounting bosses. Buying a new e-bike to get assist throws away a bike the owner already has.
2. **Repair.** Closed kits use proprietary connectors, sealed displays and controller settings that need a laptop or app. When a part fails, the bike is parked until a spare arrives from a city. The roadside bicycle mechanic, who keeps every other bike running, is locked out.
3. **Charging.** Grid power is absent or unreliable in much of the rural region. Charging at a shop in town costs money and a trip. A single 100 W panel or a shared village charging hub could supply enough energy, but kits are not designed around slow solar charging.

SunSpoke is an open, bolt-on conversion kit that fits the roadsters people already own, can be fitted and repaired by a local bike mechanic with basic tools, and charges from one 100 W panel or a shared hub using a SwapCell-compatible pack.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Rural commuter | Reach work, school or market 10 to 30 km away without arriving exhausted | Dirt and gravel roads, hills, daily use |
| Small trader | Carry 30 to 80 kg of produce, water or goods to market, sometimes a passenger | Loaded rear carrier, stop-start riding, heat |
| Community health worker | Reliable daily rounds to scattered households with a medical kit | Long distances, schedule matters, often alone |
| Local bike mechanic | Fit, maintain and repair the kit with the tools and parts already in the shop, and earn from it | Roadside or market stall, hand tools, no welding in many cases |
| Village charging hub operator | Charge several packs a day from a shared solar array and track their condition | Hub with panels, dock and shade |

### Operating environment

- **Roads:** murram (laterite), gravel, sand and rutted dirt, with potholes, washboard and grades up to about 10 % on short climbs.
- **Loads:** rider 60 to 80 kg plus 30 to 80 kg on the carrier; bike about 20 to 23 kg before conversion.
- **Climate:** ambient 15 to 40 °C, with surfaces in sun reaching 60 °C or more; dust in the dry season; heavy rain, mud and shallow water crossings in the wet season.
- **Power:** limited or no grid; solar resource of about 4 to 6 peak sun hours per day across most of the region, lower in the rains.
- **Supply chain:** bicycle spares, generic e-bike parts and motorcycle electrical parts are available in towns; specialist parts are not.

## Constraints

- Garage-buildable prototype: the bike conversion kit costs $250 USD or less in parts. The solar charging set is costed separately, and the SwapCell pack is priced once in the SwapCell repo and excluded (decided by Amish, 2026-09-25; SSP-DDR-001).
- Bolt on to the donor bike with no welding, frame drilling or cutting.
- Fitting and repair possible with the tools a roadside bike mechanic already has.
- Standard, pluggable connectors and generic parts wherever possible, so a failed part can be swapped with one from the local market.
- Legal and safe assist: 250 W rated power and an assist cutoff speed in line with pedelec practice (in the EU, 250 W and a 25 km/h cut-off under Regulation (EU) No 168/2013, with EN 15194 as the product standard); SunSpoke defaults to 20 km/h (decided, SSP-DDR-001). National rules in target countries are still to be checked.
- Uses SwapCell interface v0.3 so packs can be shared across portfolio vehicles and charged at SwapCell docks. The system is 48 V on SwapCell (decided by Amish, 2026-09-25; SSP-DDR-001).

## Out of scope

- Building or selling complete bicycles.
- Designing the battery pack itself (that is SwapCell).
- The village charging hub and its dock (SwapCell and PowerBox cover these).
- Motorcycle-class speed or power (over 250 W rated or assist above 25 km/h).
- Cargo tricycles and trailers (see CargoMule and FlatTrike).

## Prior work

- **Commercial conversion kits.** Front hub, rear hub and mid-drive kits with 36 V and 48 V batteries are sold worldwide and in regional markets. They prove the technology and set the price floor, but are not designed for 28 in roadster wheels, rod brakes or local repair.
- **Regional e-bike ventures.** Several companies in East Africa assemble or sell e-bikes and electric motorcycles, some with battery swapping. They show demand and a working swap model, but most are closed products that need their own service network.
- **Rugged bicycles for rural use.** Purpose-built heavy-duty bicycles such as the World Bicycle Relief Buffalo bicycle show that design for rural loads and a single mechanic training curriculum works. World Bicycle Relief describes a heavy-gauge steel frame that carries 220 lb (about 100 kg) on the rear carrier, with frame, carrier, stand and wheels shared across models ([World Bicycle Relief, "The Bike"](https://worldbicyclerelief.org/the-bike/), checked 2026-09-25).
- **Pedelec rules.** In the EU a pedal cycle with assist up to 250 W that cuts off by 25 km/h is excluded from motor-vehicle type approval under Regulation (EU) No 168/2013 ([Wikipedia, "Pedelec"](https://en.wikipedia.org/wiki/Pedelec), checked 2026-09-25; secondary source). Rules in the first target country are not yet checked.
- **Bicycle taxis (boda-boda).** Bicycle taxis in East Africa show how much load and distance a roadster is asked to carry, and how important a local repair economy is.
- **Solar charging for small vehicles.** Solar e-bike charging stations and off-grid battery hubs exist in pilot form. The first-order numbers in SSP-PRC-001 show one 100 W panel can cover a typical day of assisted riding.

Two sources were checked on 2026-09-25 (above). The other entries are general descriptions without named sources; they stay unverified until a named source is checked.

## Open questions

- Which partner organization and which region first (for example an East African bike mechanic cooperative, a health worker program, or a university engineering department)? Decided 2026-10-02: western Kenya and eastern Uganda as the default region, where 28 in roadsters and bicycle taxis are common, with a bicycle mechanics' group or rural transport organization there as the partner type; the partner is named when the portfolio picks partners for this area (SSP-DEC-001).
- The 48 V system is decided (SSP-DDR-001). Field work should still record how common 36 V and 48 V spares are locally, which bears on the later 36 V low-cost variant.
- How much cargo and passenger carrying must the kit support, and does the pack location need to leave the rear carrier free? Assumed yes; to validate.
- What assist speed limit and registration rules apply in the first target country?

## Safety

> **Safety:** A conversion adds a lithium-ion pack of about 468 Wh, more speed and more mass to a bicycle with weak rod brakes and an old steel fork. The hazards (pack fire, dropout failure, braking, wet connectors) are set out in SSP-PRC-001.

## User research and co-design

This design is for communities the author is not part of, so requirements come from the people who will use it.

- [ ] Identify a local partner organization (Helpful Engineering network, NGO or university)
- [ ] Run co-design sessions with intended users; record who, where and what was learned
- [ ] Validate load, distance, terrain and cost assumptions in the field
- [ ] Revise requirements (REQ) from findings before freezing the design
