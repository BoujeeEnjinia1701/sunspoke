"""SunSpoke concept media (TRL 3), generated from the parametric model.

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Geometry comes from cad/src/model.py, so the media match the STEP files. The bicycle
lies in the XZ plane (X forward, Z up, Y across), rear axle at X = 0, ground at Z = 0.
The donor bicycle is grey; kit parts are colored. Flow values are from SSP-CAL-001.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from concept import Part, render_all
from model import build_parts

parts = [Part(n, shape, colour, bom, ex) if bom else Part(n, shape, colour, None)
         for n, shape, colour, bom, ex in build_parts()]

render_all(
    parts, project="SunSpoke", title="Roadster conversion kit concept", dwg_no="SSP-DWG-010", date="2026-09-25",
    key_figures=["250 W geared front hub, 48 V on SwapCell (decided)",
                 "SwapCell about 468 Wh: about 37 km loaded (SSP-CAL-001)",
                 "100 W panel: about 315 Wh/day stored at 4.5 sun hours",
                 "Added mass 6.65 kg with pack; torque arms both sides",
                 "Bike kit about $183; solar set about $86; pack excluded"],
    cut=False,
    flow={"title": "daily solar energy flow, Wh per day (estimates, 4.5 peak sun hours)", "unit": "Wh (est.)",
          "stages": [("Sun on 100 W panel", 450), ("Panel output", 360), ("Charger output", 331),
                     ("Stored in pack", 315), ("Pack output", 305), ("At the wheel", 229)],
          "losses": [(0, "Derating 20 %", 90), (1, "MPPT 8 %", 29),
                     (2, "Charging 5 %", 17), (3, "Pack loss 3 %", 9),
                     (4, "Drive 25 %", 76)]},
)
