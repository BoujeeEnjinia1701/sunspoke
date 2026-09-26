# SunSpoke

![TRL 3](https://img.shields.io/badge/TRL-3%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Mobility and Logistics · **TRL:** 3 of 9 (proof of concept on paper) · **Prototype budget:** $250 USD for the bike kit (solar set costed separately; pack priced in SwapCell) · **Difficulty:** 3 of 5

Open, bolt-on electric conversion kit for existing steel bicycles, serviceable by local bike mechanics and charged from a single 100 W solar panel or a shared village hub, using a SwapCell-compatible battery.

![SunSpoke concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [General arrangement SSP-DWG-001 (PDF)](cad/drawings/SSP-DWG-001.pdf) · [Sizing note SSP-CAL-001](docs/04-calcs/01-sizing.md) · [Review note](docs/REVIEW.md)

## Concept rationale

The cheapest vehicle a rural household can electrify is the one it already owns. A bolt-on front hub kit leaves the roadster's chain, rear brake and carrier untouched, so the bicycle keeps working as a bicycle if anything electrical fails, and the parts that do fail are generic e-bike parts that a roadside mechanic can swap with spanners and a multimeter. Charging from one 100 W panel, or by swapping a shared SwapCell pack at a village hub, removes the dependence on a grid that many riders do not have.

Keeping the design open matters for the same reason. Closed kits lock the local mechanic out of repairs and settings; published drawings, a priced bill of materials and a plain wiring scheme let a workshop fit, service and adapt the kit, and let a small fabricator make the cradle and panel stand locally. Every part is chosen so the conversion can be done in a garage with hand tools and no welding.

## Burning platform

In 2023, 666 million people still had no access to electricity, and 85 percent of them, about 566 million, lived in sub-Saharan Africa ([World Bank, Tracking SDG 7: The Energy Progress Report 2025](https://www.worldbank.org/en/news/press-release/2025/06/25/energy-access-has-improved-yet-international-financial-support-still-needed-to-boost-progress-and-address-disparities)). Eighteen of the 20 countries with the largest access deficits are in that region. These are the same places where the unpowered steel roadster is the working vehicle for carrying people, water and produce over dirt roads.

For these riders, an e-bike that must be charged from a wall socket is not an option, and a new e-bike costs far more than the bicycle they already have. Assist that runs on a small solar panel and fits the existing bicycle turns hours of pushing a loaded bike uphill into a ride, without waiting for the grid to arrive.

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| Smallholder agriculture | Carrying produce, feed and water from farm to market on loaded roadsters |
| Community health services | Longer, more reliable daily rounds for health workers on rural routes |
| Informal transport | Bicycle taxis and goods carriers that already run on roadsters |
| Bicycle repair and retail | A new fitting and service trade for roadside mechanics |
| Off-grid energy | Village solar hubs that charge and swap SwapCell packs as a service |
| Last-mile logistics | Low-cost cargo delivery in towns where grid charging is unreliable |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| Uganda and Kenya | Bicycle taxis began at the Uganda-Kenya border in the 1980s and gave the boda-boda its name ([Wikipedia, "Boda boda"](https://en.wikipedia.org/wiki/Boda_boda), secondary source); heavy roadsters still carry goods and passengers on rural roads |
| Malawi, Tanzania and Zambia | Sub-Saharan Africa holds 18 of the 20 largest electricity access deficits ([World Bank, 2025](https://www.worldbank.org/en/news/press-release/2025/06/25/energy-access-has-improved-yet-international-financial-support-still-needed-to-boost-progress-and-address-disparities)); solar charging suits routes far from the grid |
| India and Bangladesh | Large rural populations still rely on steel single-speed bicycles for work trips, with a dense network of roadside repair shops |
| Andean and Central American highlands | Steep rural roads where a loaded bicycle is pushed more than ridden |
| Netherlands | About 56 percent of the 804,000 new bicycles sold in 2023 were e-bikes (RAI and BOVAG figures, reported by [DutchNews.nl](https://www.dutchnews.nl/2024/11/the-dutch-are-cycling-more-and-buying-more-e-bikes/)); a conversion kit lets owners of sturdy older bicycles join that shift without buying new |

## What sparked the idea

The idea traces back to the first patented electric bicycle. On December 31, 1895, Ogden Bolton Jr. was granted US Patent 552,271 for an "electrical bicycle" with a direct-current motor built into the hub of the rear wheel ([Google Patents, US552271A](https://patents.google.com/patent/US552271A/en)). The hub motor was the first answer to adding power to a bicycle without redesigning it, and more than a century later it is still the simplest one: a motor that replaces a wheel and bolts into the frame the rider already owns. SunSpoke takes that precedent to the steel roadsters of rural Africa, with a motor a local mechanic can lace into a standard rim and a battery that charges from the sun.

## Problem

Most bicycles in rural Africa are unpowered steel roadsters, and commercial e-bikes are too costly and hard to charge where grid power is scarce. Design with, not for: requirements must come from co-design sessions and field trials with the intended users through a local partner.

## Concept

Open, bolt-on electric conversion kit for existing steel bicycles, serviceable by local bike mechanics and charged from a single 100 W solar panel or a shared village hub, using a SwapCell-compatible battery.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- 250 W geared front hub motor wheel, 48 V
- 48 V SwapCell pack (SwapCell interface v0.3; 48 V decided by Amish, 2026-09-25)
- Sealed controller with a motor thermistor input that derates instead of cutting out (decided by Amish, 2026-09-25)
- Handlebar power switch in the SwapCell INTERLOCK loop
- Pedal-assist sensor
- SwapCell receiver cradle with band clamps (no welding) and host adapter
- 100 W solar panel with MPPT charger
- Weatherproof wiring harness

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> Check that the donor frame and fork can take a hub motor's torque; fit torque arms. Contains a lithium battery pack. Use a BMS with cell-level protection, fuse the pack, and charge on a non-combustible surface.

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (SSP-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `SSP-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

A project of the [Design Molecule](https://designmolecule.com) lab.
