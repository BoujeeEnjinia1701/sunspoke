# SunSpoke

![TRL 2](https://img.shields.io/badge/TRL-2%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Mobility and Logistics · **TRL:** 2 of 9 (concept formulated) · **Prototype budget:** about $250 USD · **Difficulty:** 3 of 5

Open, bolt-on electric conversion kit for existing steel bicycles, serviceable by local bike mechanics and charged from a single 100 W solar panel or a shared village hub, using a SwapCell-compatible battery.

## Problem

Most bicycles in rural Africa are unpowered steel roadsters, and commercial e-bikes are too costly and hard to charge where grid power is scarce. Design with, not for: requirements must come from co-design sessions and field trials with the intended users through a local partner.

## Concept

Open, bolt-on electric conversion kit for existing steel bicycles, serviceable by local bike mechanics and charged from a single 100 W solar panel or a shared village hub, using a SwapCell-compatible battery.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- 250 W front hub motor wheel
- 36 V 10 Ah pack (SwapCell compatible)
- Sealed controller
- Pedal-assist sensor
- Universal clamp mounts (no welding)
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

Part of the open hardware portfolio at [amishchadha.com](https://amishchadha.com).
