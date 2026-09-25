"""SunSpoke general arrangement drawing SSP-DWG-001 (Rev P1).

Run from the repo root:  python cad/src/sheets.py
Builds cad/drawings/SSP-DWG-001.svg, .pdf and .png from the parametric model.
The solar charging set (items 10 to 13) is not shown; it is on the concept sheet SSP-DWG-010.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build123d import Compound  # noqa: E402
from drawing import Sheet, project_views  # noqa: E402
from model import PARAMS as P, build_parts, cradle_local, fit_checks, pack_local, receptacle_local  # noqa: E402

parts = build_parts()
bike = Compound([s for _, s, _, b, _ in parts if b is None or b <= 9])
work = ROOT / "cad/drawings/_views"
views = project_views(bike, work)
f = fit_checks()

s = Sheet(project="SunSpoke", title="General arrangement, kit on 28 in roadster", dwg_no="SSP-DWG-001",
          rev="P1", author="Amish Chadha", date="2026-09-25", concept=True,
          material="Kit parts per bom/bom.csv; donor roadster shown for context",
          revisions=[("P1", "Preliminary GA, SwapCell interface v0.3 (SSP-CAL-001)", "2026-09-25", "AC")])
s.add_ortho(views, ["front", "top", "right"])
s.add_svg(views["iso"], 276, 30, 140, 84, label="Isometric view", sublabel="Not to scale")
detail = project_views(Compound([cradle_local(), receptacle_local(), pack_local()]), work / "detail")
s.add_svg(detail["front"], 30, 200, 110, 40, scale=0.2, label="Detail A: cradle with pack, side view",
          sublabel="Scale 1:5; down tube axis horizontal, BB to the left")
s.add_svg(detail["right"], 150, 200, 60, 40, scale=0.2, label="Detail A: end view",
          sublabel="Scale 1:5; from the handle end")
s.add_notes("Key dimensions and interfaces (mm)", [
    f"Wheel 28 in (ETRTO 635), tyre radius {P['wheel_r']:.0f}; wheelbase {P['wheelbase']:.0f}",
    f"Motor 1: geared hub, {P['motor_d']:.0f} dia, {P['fork_spacing']:.0f} dropout spacing, {P['axle_flats']:.0f} axle flats",
    f"Torque arms 2: {P['arm_t']:.0f} x {P['arm_w']:.0f} steel, clamp {P['arm_len']:.0f} from axle, both sides",
    f"Cradle 4: band clamps for 28 to 32 dia down tube, {P['band_pitch']:.0f} pitch",
    f"Pack 6 centre at {P['pack_pos'] * 100:.0f} % of down tube ({f['dt_len']:.0f} long) from BB",
    f"SwapCell v0.3 envelope {P['pack_l']:.0f} x {P['pack_w']:.0f} x {P['pack_d']:.0f}, connector toward BB",
    f"Guides {P['guide_len']:.0f} long, {P['guide_clear']:.0f} clearance per side",
    f"Removal travel {f['travel']:.0f} free ({f['travel_needed']:.0f} needed); triangle clearance {f['clearance']:.0f}",
    "Latch class V1: over-centre lever, 330 N preload, detent",
    "INTERLOCK: 10 kOhm 1 % coding resistor in cradle, power",
    "  switch 8 in series (interface v0.3 item W)",
    "Controller 3 on seat tube; host adapter 5 below cradle",
    "Solar set 10 to 13 not shown (see SSP-DWG-010)",
    "PRELIMINARY, NOT FOR FABRICATION",
], x=276, y=128, width=140)
s.save(ROOT / "cad/drawings/SSP-DWG-001")
shutil.rmtree(work, ignore_errors=True)
print("wrote cad/drawings/SSP-DWG-001.svg, .pdf, .png")
