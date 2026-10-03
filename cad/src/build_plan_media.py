"""SunSpoke prototype build plan pictures (SSP-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|layouts|joints|steps|wiring ...]
With no argument it draws everything. Every picture is drawn from cad/src/model.py
(build_components, cradle_parts), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png          the kit on the bike, pulled apart, numbered in build order
    docs/05-build-plan/cradle-parts.png      the receiver cradle's own parts, pulled apart
    docs/05-build-plan/solar-overview.png    the solar charging set, pulled apart
    cad/drawings/SSP-DWG-101 to 110          making sketches for the made components
    docs/05-build-plan/tray-layout.png       flat blank of the cradle tray with every hole and fold
    docs/05-build-plan/joint-NN.png          close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png           one picture per assembly step
    docs/05-build-plan/wiring.png            block-level wiring with wire sizes (matplotlib)
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
import model as M  # noqa: E402
from model import PARAMS as P  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-02"
G = M.geometry(P)
LV = M.saddle_levels(P)
LOC = M.cradle_location(P)
CP = M.cradle_parts(P)
CPO = dict(CP); CPO.update(M.gate_open(CP, P))
_C = None


def comps():
    global _C
    if _C is None:
        _C = M.build_components(P)
    return _C


COL = {"tray": "#94A3B8", "saddles": "#475569", "liners": "#111827", "bands": "#9CA3AF", "rails": "#E2E8F0", "catch": "#B45309",
       "stop": "#1D4ED8", "receptacle": "#1F2937", "gate": "#0F766E", "pad": "#111827", "hinge": "#6B7280", "latch": "#7C2D12",
       "keeper": "#6B7280", "adapter": "#7C3AED", "pack": "#C2410C", "tube": "#D6D3D1", "arm": "#D4A017", "motor": "#0F766E",
       "ctrl": "#115E59", "pas": "#0EA5E9", "bar": "#2563EB", "harness": "#111827", "panel": "#1E3A8A", "timber": "#A16207",
       "leg": "#92400E", "brace": "#CA8A04", "batten": "#78350F", "charger": "#16A34A", "cable": "#374151", "donor": "#D1D5DB", "blocks": "#7C2D12"}


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def S(*ks, src=None):
    src = src or comps()
    return M._fuse([src[k][0] for k in ks])


def L(*ks, d=None):
    d = d or CP
    return M._fuse([d[k] for k in ks])


def tube_local(x0=-330, x1=330):
    from build123d import Cylinder, Pos, Rot
    return Pos((x0 + x1) / 2, 0, 0) * Rot(0, 90, 0) * Cylinder(P["dt_r"], x1 - x0)


def zdir():
    a = math.radians(G["dt_ang"])
    return (-math.sin(a), 0, math.cos(a))


def xdir():
    a = math.radians(G["dt_ang"])
    return (math.cos(a), 0, math.sin(a))


def along(v, k):
    return tuple(k * c for c in v)


def add(*vs):
    return tuple(sum(c) for c in zip(*vs))


def front_blocks(side=None):
    """The wet-weather blocks on the front rim only (the rear wheel is not drawn in the pictures)."""
    fr = G["front"]
    y0, y1 = {None: (-100, 100), "L": (-100, 0), "R": (0, 100)}[side]
    return comps()["wet_blocks"][0] & M._box(fr[0] - 420, fr[0] + 420, y0, y1, fr[1] - 420, fr[1] + 420)


def front_wheel():
    fr = G["front"]
    return M.wheel(fr[0], fr[1], P["wheel_r"], hub_r=62, hub_y=25)


# ----------------------------------------------------------------- overviews
def overview():
    C = comps()
    zd = zdir()
    cr = ["tray", "saddles", "liners", "rails", "catch", "stop", "receptacle", "gate", "pad", "hinge", "hinge_leaf", "keeper", "latch"]
    D = M.donor_parts(P)
    donor = M._fuse([D[k] for k in ("frame", "fork", "stem_bars", "levers", "drive")])
    parts = [
        part("Receiver cradle, assembled on the bench", S(*cr), "#1D4ED8", along(zd, 130)),
        part("Band clamps (3) round the down tube", S("bands"), "#BE185D", along(zd, -90)),
        part("Host adapter and its lead", S("adapter", "inlet", "adapter_lead"), COL["adapter"], (-90, -60, -130)),
        part("Torque arms (2), joggled", S("arms"), COL["arm"], (150, -40, 70)),
        part("Motor wheel with axle nuts", S("motor", "axle_nuts") + front_wheel(), COL["motor"], (260, 0, -40)),
        part("Arm band clamps (2)", S("arm_clamps"), "#BE185D", (130, -60, 210)),
        part("Controller, pad and band clamps", S("controller", "ctrl_pad", "ctrl_bands"), COL["ctrl"], (-170, -60, 40)),
        part("Pedal-assist disc and sensor", S("pas_disc", "pas_sensor"), COL["pas"], (0, -100, -180)),
        part("Display and brake sensors", S("display", "brake_sensors"), "#4338CA", (40, 0, 170)),
        part("Wet-weather brake blocks (4; the front pair is drawn)", front_blocks(), COL["blocks"], (260, -150, -40)),
        part("Harness with fuse", S("harness"), COL["harness"], (0, 0, 0)),
        part("SwapCell pack (not part of the kit)", S("pack"), COL["pack"], add(along(zd, -330), along(xdir(), -40))),
        part("Donor roadster frame, fork and bars (yours)", donor, COL["donor"], (0, 0, 0)),
    ]
    bv.overview(parts, OUT / "overview.png", "SunSpoke prototype: the kit on the bike, pulled apart",
                subtitle="Numbered in build order. Seen from the left, a little in front and above. Rear wheel, carrier and saddle not drawn",
                elev=12, azim=-75, size=(12, 7.6), dpi=150, key=True)
    # the cradle's own parts, in the cradle frame
    cparts = [
        part("Tray (folded, drilled)", CP["tray"], COL["tray"], (0, 0, 0)),
        part("V-saddles (3) with rubber liners", L("saddles", "liners"), COL["saddles"], (0, 0, -70)),
        part("Slide strips (2)", CP["rails"], COL["rails"], (0, 0, 60)),
        part("Catch bar", CP["catch"], COL["catch"], (0, 0, 100)),
        part("End stop", CP["stop"], COL["stop"], (0, 0, 100)),
        part("SwapCell receptacle (bought)", CP["receptacle"], COL["receptacle"], (-60, 0, 180)),
        part("Gate with rubber pad", L("gate", "pad"), COL["gate"], (90, 0, 110)),
        part("Hinge (bought)", L("hinge", "hinge_leaf"), COL["hinge"], (150, 0, 40)),
        part("Over-centre draw latch and keeper (bought)", L("latch", "keeper"), COL["latch"], (40, -110, 140)),
        part("Host adapter and lead (bought)", L("adapter", "inlet", "adapter_lead"), COL["adapter"], (-80, 0, -20)),
        part("Band clamps (3), fitted on the bike", CP["bands"], COL["bands"], (0, 0, -150)),
    ]
    bv.overview(cparts, OUT / "cradle-parts.png", "Receiver cradle: its parts, pulled apart",
                subtitle="Drawn with the down tube's direction left to right (bottom bracket end on the left). Seen from the left, front and above",
                elev=26, azim=-62, size=(12, 7.2), dpi=150, key=True)
    # solar set
    F = M.Pos(P["panel_x"], 0, P["panel_z"]) * M.Rot(0, P["panel_tilt"], 0)
    st = C["stand"][0]
    sparts = [
        part("Top rails (2)", _stand_bit("rails"), COL["timber"], (0, 0, 120)),
        part("Legs (2 rear, 2 front)", _stand_bit("legs"), COL["leg"], (0, 0, 0)),
        part("Low braces (2)", _stand_bit("braces"), COL["brace"], (0, 0, -60)),
        part("Cross battens (2)", _stand_bit("battens"), COL["batten"], (0, -0, -120)),
        part("Solar panel, 100 W", S("panel"), COL["panel"], (0, 0, 330)),
        part("Boost charger", S("charger"), COL["charger"], (0, -160, 0)),
        part("Panel lead", S("panel_lead"), COL["cable"], (0, -220, 160)),
    ]
    bv.overview(sparts, OUT / "solar-overview.png", "Solar charging set: every component, pulled apart",
                subtitle="Numbered in build order. Seen from the front left and above. The 5 m charge cable runs from the charger to the bike",
                elev=22, azim=-55, size=(11, 7), dpi=150, key=True)
    return OUT / "overview.png"


def _stand_bit(which):
    """The stand's pieces, rebuilt from the same numbers model.py uses."""
    from build123d import Pos, Rot
    PX, PZ, T = P["panel_x"], P["panel_z"], P["panel_tilt"]
    pt_ = P["panel"][2]
    tb, ry = P["timber"], P["rail_y"]
    F = Pos(PX, 0, PZ) * Rot(0, T, 0)
    if which == "rails":
        return M._fuse([F * M._box(-350, 350, s * ry - tb / 2, s * ry + tb / 2, -pt_ / 2 - tb, -pt_ / 2) for s in (-1, 1)])
    xr = (F * Pos(-P["leg_u"], 0, 0)).position.X
    xf = (F * Pos(P["leg_u"], 0, 0)).position.X
    if which == "legs":
        out = []
        for uu in (-P["leg_u"], P["leg_u"]):
            lx = (F * Pos(uu, 0, 0)).position.X
            under = PZ - (lx - PX) * math.tan(math.radians(T)) - (pt_ / 2) / math.cos(math.radians(T))
            top = under - tb / 2 * math.tan(math.radians(T)) - 2
            for s in (-1, 1):
                y0 = s * (ry + tb / 2)
                out.append(M._box(lx - tb / 2, lx + tb / 2, min(y0, y0 + s * tb), max(y0, y0 + s * tb), 0, top))
        return M._fuse(out)
    if which == "braces":
        return M._fuse([M._box(xr - tb / 2, xf + tb / 2, *sorted((s * (ry - tb / 2), s * (ry + tb / 2))), 150, 150 + tb) for s in (-1, 1)])
    if which == "battens":
        bw, bt_ = P["batten"]
        out = []
        for lx, sg in ((xr, -1), (xf, 1)):
            xface = lx + sg * tb / 2
            out.append(M._box(min(xface, xface + sg * bt_), max(xface, xface + sg * bt_), -(ry + tb * 1.5), ry + tb * 1.5, 100, 100 + bw))
        return M._fuse(out)


# ----------------------------------------------------------------- making sketches
def sheets(only=None):
    from build123d import Pos, Rot, Plane
    zb, z0 = LV["zb"], LV["z0"]
    tube = part("Down tube", tube_local(-340, 340), COL["tube"])
    base = dict(project="SunSpoke", date=DATE)
    out = []

    def want(n):
        return only is None or n in only

    # 101 tray
    if want(101):
        out.append(bv.component_sheet(
            part("Tray", CP["tray"], COL["tray"]), [tube, part("Saddles", CP["saddles"], "#9CA3AF"), part("Stop", CP["stop"], "#9CA3AF"),
                                                    part("Pack", M.pack_local(P), "#E5E7EB")],
            dwg_no="SSP-DWG-101", title="SunSpoke cradle tray: making sketch", material="Aluminium sheet 3 mm, 5052-H32",
            view_shape=CP["tray"], inset_view=(28, -60),
            notes=["One blank, cut and folded: a base 470 x 98 mm with two guide tabs",
                   "  120 x 50 mm on each long edge at the bottom bracket end, and one",
                   "  latch ear tab 62 x 31 mm on the left edge at the head tube end.",
                   "Fold the three tabs up 90 degrees on the base's edges, inside radius",
                   "  about 4.5 mm (1.5 x thickness). Inside faces 92 mm apart.",
                   "Band slots: three pairs, 3 x 13 mm, 19 to 22 mm each side of the",
                   "  centre line, at 100 mm below, at, and 100 mm above the middle.",
                   "Air windows 68 x 44 mm either side of the middle slots.",
                   "Every other hole is on the layout picture: drill, countersink where",
                   "  it says, deburr. Base, guides and ear have no welds.",
                   "Fit: sits on the three V-saddles; the band clamps pass through",
                   "  the slots and over the base between them.",
                   "Check: the SwapCell envelope gauge drops between the guides with",
                   "  1 mm each side; the base lies flat within 1 mm over its length."],
            **base))
    # 102 V-saddle
    if want(102):
        sad = CP["saddles"] & M._box(-120, -80, -30, 30, -20, 40)
        out.append(bv.component_sheet(
            part("V-saddle", sad, COL["saddles"]), [part("Down tube", tube_local(-200, 0), COL["tube"]),
                                                    part("Tray", CP["tray"] & M._box(-200, 0, -60, 60, -10, 80), "#9CA3AF"),
                                                    part("Band", CP["bands"] & M._box(-200, 0, -60, 60, -40, 80), "#9CA3AF")],
            dwg_no="SSP-DWG-102", title="SunSpoke V-saddle (make 3): making sketch", material="Aluminium flat bar 35 x 12 mm, 6082 or 6061",
            view_shape=Pos(100, 0, -LV["sad_bot"]) * sad, inset_view=(-28, -60),
            notes=["Make three. Saw 40 mm lengths of 35 x 12 mm aluminium bar.",
                   "Cut a 120 degree V the full 40 mm length of one 40 x 35 face:",
                   "  27.7 mm wide at the face, 8 mm deep, centred. Saw just inside",
                   "  the scribed lines and file to them; 4 mm of solid stays above",
                   "  the point of the V.",
                   "Drill 4.2 mm and tap M5, 8 mm deep, in the flat top face, on the",
                   "  centre line, 8 mm from each end (24 mm apart).",
                   "Glue a 1.5 mm strip of rubber sheet into the V, both faces.",
                   "Fit: the V sits on the down tube, the tray on its flat top; two",
                   "  M5 countersunk screws down through the tray hold it.",
                   "Tubes of 28 to 32 mm seat on both faces of the V.",
                   "Check: on a 32 mm tube it does not rock, and the tube does not",
                   "  touch the bottom of the V."],
            **base))
    # 103 slide strip
    if want(103):
        rl = CP["rails"] & M._box(-200, 200, 0, 60, 0, 80)
        out.append(bv.component_sheet(
            part("Slide strip", rl, "#0F766E"), [part("Tray", CP["tray"], "#9CA3AF"), part("End stop", CP["stop"], "#9CA3AF")],
            dwg_no="SSP-DWG-103", title="SunSpoke slide strip (make 2): making sketch", material="HDPE (or UHMW-PE) bar 12 x 10 mm",
            view_shape=Pos(0, -40, -zb) * rl, inset_view=(30, -55),
            notes=["Make two. Cut 336 mm lengths of 12 x 10 mm HDPE bar.",
                   "Chamfer the top edges of both ends 2 x 45 degrees so the pack",
                   "  slides on without catching.",
                   "Fit: each strip lies on the tray along one edge, its outer face",
                   "  in line with the pack's side (35 to 45 mm from the centre line),",
                   "  starting 2 mm from the end stop.",
                   "Fix with three 4 mm countersunk self-tapping screws for",
                   "  plastic, up from under the tray, 10 mm deep, 120 mm apart.",
                   "The pack's back face slides on the two strips, 12 mm above",
                   "  the tray, so its latch clears the tray.",
                   "Check: screw heads below the tray's under face; strips straight."],
            **base))
    # 104 catch bar
    if want(104):
        out.append(bv.component_sheet(
            part("Catch bar", CP["catch"], COL["catch"]), [part("Tray", CP["tray"], "#9CA3AF"), part("Strips", CP["rails"], "#9CA3AF")],
            dwg_no="SSP-DWG-104", title="SunSpoke catch bar: making sketch", material="Steel flat bar 10 x 6 mm, S275 or mild steel",
            view_shape=Pos(-145, 0, -zb) * CP["catch"], inset_view=(35, -40),
            notes=["Cut a 50 mm length of 10 x 6 mm steel flat bar; deburr.",
                   "Drill 3.3 mm and tap M4, 6 mm deep (through), 10 mm from each",
                   "  end on the centre line (30 mm apart).",
                   "Paint or zinc spray it against rust.",
                   "Fit: lies flat on the tray across the centre line, its lower",
                   "  edge 140 mm above the middle of the tray (toward the head",
                   "  tube); two M4 countersunk screws up from under the tray.",
                   "The pack's spring latch drops in behind it: with the pack",
                   "  against the end stop the latch sits 3 mm short of the bar.",
                   "Check: it stands 6 mm proud of the tray and is square across."],
            **base))
    # 105 end stop
    if want(105):
        out.append(bv.component_sheet(
            part("End stop", CP["stop"], COL["stop"]), [part("Tray", CP["tray"], "#9CA3AF"), part("Receptacle", CP["receptacle"], "#9CA3AF")],
            dwg_no="SSP-DWG-105", title="SunSpoke end stop: making sketch", material="Aluminium sheet 3 mm, 5052-H32",
            view_shape=Pos(170, 0, -zb) * CP["stop"], inset_view=(22, -125),
            notes=["One blank folded into a wall with a foot and two side flanges.",
                   "Wall 92 mm wide x 72 mm tall; foot 27 mm deep; side flanges",
                   "  27 mm deep, 50 mm tall. Relieve the corners with 3 mm holes.",
                   "Plug notch in the wall, open at the top: 60 mm wide, down to",
                   "  25 mm above the tray. The pack's plug passes through it.",
                   "Holes: foot two 5.5 mm, 13 mm from the wall, 20 mm each side;",
                   "  each flange two 5.5 mm, 7 and 19 mm from the wall, 25 mm up;",
                   "  wall four 4.5 mm for the receptacle, 37 mm each side, 32 and",
                   "  56 mm up from the tray.",
                   "Fold the foot and flanges away from the pack side, 90 degrees.",
                   "Fit: foot bolted to the tray, flanges bolted inside the guides,",
                   "  M5 bolts with nyloc nuts; the pack's end bears on the wall.",
                   "Check: the wall is square to the tray within 1 degree."],
            **base))
    # 106 gate
    if want(106):
        out.append(bv.component_sheet(
            part("Gate", CP["gate"], COL["gate"]), [part("Tray", CP["tray"], "#9CA3AF"),
                                                     part("Latch", L("latch", "keeper", "hinge", "hinge_leaf"), "#9CA3AF")],
            dwg_no="SSP-DWG-106", title="SunSpoke gate: making sketch", material="Steel sheet 3 mm, mild steel, painted",
            view_shape=Pos(-175, 0, -zb) * CP["gate"], inset_view=(25, -35),
            notes=["Cut a plate 94 mm long x 25 mm tall with a 26 mm long, 16 mm tall",
                   "  tab on its left end (top corner); fold the tab 90 degrees",
                   "  toward the pack side: this is the flange that lies against the",
                   "  outside of the latch ear and carries the keeper.",
                   "Drill: two 4.5 mm holes for the hinge leaf, 18 mm each side of",
                   "  the centre of the plate, 10 mm up; two 3.5 mm in the flange",
                   "  for the keeper's rivets, 4 and 8 mm from its end, 8 mm up.",
                   "Glue a 3 mm rubber pad, 80 x 16 mm, on the pack face, 8 mm up.",
                   "Fit: the hinge holds its lower edge 6 mm above the tray; closed,",
                   "  the pad presses the pack's top end below the handle.",
                   "Folded down, it lies flat under the pack's path.",
                   "Check: it folds through 90 degrees without touching the pack."],
            **base))
    # 107 torque arm
    if want(107):
        arm_l, _ = M.torque_arm_local(P, 1)
        C = comps()
        out.append(bv.component_sheet(
            part("Torque arm", C["arms"][0], COL["arm"]), [part("Fork", C["fork"][0], "#9CA3AF"), part("Motor", C["motor"][0], "#D1D5DB"),
                                                           part("Clamps", C["arm_clamps"][0], "#9CA3AF")],
            dwg_no="SSP-DWG-107", title="SunSpoke torque arm (make 2, a left and a right): making sketch",
            material="Steel flat bar 20 x 5 mm, S275 or mild steel", view_shape=Rot(0, 0, 0) * arm_l, inset_view=(10, -20),
            notes=["Make two, mirror images. Cut 160 mm lengths of 20 x 5 mm bar.",
                   "Axle slot at one end: 10.0 mm wide (a snug fit on the motor's",
                   "  10 mm axle flats), open at the end, 23.4 mm deep, round-ended;",
                   "  the axle centre sits 15 mm in from the end.",
                   "  Saw the sides, then file to a 10 mm gauge.",
                   "Joggle: two bends, 12 and 28 mm from the axle centre, so the",
                   "  long part sits 8 mm further out than the slotted end. Bend",
                   "  in a vice over a 5 mm packing, one arm left-hand, one right.",
                   "Round and deburr both ends; paint or zinc spray.",
                   "Fit: the slotted end lies flat on the outside of the dropout,",
                   "  under the axle washer and nut; the long part lies on the outside",
                   "  of the fork blade, held 130 mm up by a band clamp.",
                   "Check: no shake on the axle flats; the long part touches the blade."],
            **base))
    # 108 top rail
    F = Pos(P["panel_x"], 0, P["panel_z"]) * Rot(0, P["panel_tilt"], 0)
    C = comps()
    if want(108):
        rail = _stand_bit("rails") & M._box(0, 5000, 0, 1000, -10, 2000)
        out.append(bv.component_sheet(
            part("Top rail", rail, COL["timber"]), [part("Legs", _stand_bit("legs"), "#9CA3AF"), part("Braces", _stand_bit("braces"), "#9CA3AF")],
            dwg_no="SSP-DWG-108", title="SunSpoke panel stand top rail (make 2): making sketch", material="Sawn timber 45 x 45 mm, treated",
            view_shape=F.inverse() * rail, inset_view=(20, -50),
            notes=["Make two. Cut 700 mm lengths of 45 x 45 mm treated timber.",
                   "Coach bolt holes: 9 mm through, side to side, 15 mm up from",
                   "  the rail's bottom face, 285 mm each side of the middle (one",
                   "  per leg).",
                   "Panel bolt holes: drill 6.5 mm down through the rail where the",
                   "  panel frame's own mounting holes fall (about 400 mm from",
                   "  the panel's centre line on each long side).",
                   "Fit: the panel's aluminium frame sits on the two rails; M6",
                   "  bolts through the frame and rail, washers and nuts below.",
                   "The rails slope at 15 degrees, the panel tilt.",
                   "Check: the two rails are the same length and drilled alike."],
            **base))
    if want(109):
        legs = _stand_bit("legs")
        rear = legs & M._box(P["panel_x"] - 400, P["panel_x"] - 200, 0, 1000, -10, 2000)
        out.append(bv.component_sheet(
            part("Rear leg", rear, COL["leg"]), [part("Rails", _stand_bit("rails"), "#9CA3AF"), part("Braces", _stand_bit("braces"), "#9CA3AF"),
                                                 part("Other legs", legs - rear, "#9CA3AF")],
            dwg_no="SSP-DWG-109", title="SunSpoke panel stand legs (2 rear, 2 front): making sketch", material="Sawn timber 45 x 45 mm, treated",
            view_shape=Pos(-rear.bounding_box().center().X, -rear.bounding_box().center().Y, 0) * rear, inset_view=(18, -60),
            notes=["Rear legs (drawn): cut two 668 mm long. Front legs: cut two",
                   "  520 mm long. Square ends; seal the end grain.",
                   "Each leg: one 9 mm hole 17 mm below its top end for the coach",
                   "  bolt into the top rail; two 9 mm holes, one above the other,",
                   "  162 and 183 mm up, for the low brace.",
                   "Fit: each leg lies against the outside face of the top rail",
                   "  and of the low brace, upright, its top just below the panel.",
                   "M8 x 100 coach bolts, washers and nuts inside: one at the rail,",
                   "  two at the brace, so each side frame is rigid.",
                   "Rear legs are the tall ones, on the high edge of the panel.",
                   "Check: each side frame lies flat and square when bolted."],
            **base))
    if want(110):
        braces = _stand_bit("braces")
        one = braces & M._box(0, 5000, 0, 1000, -10, 2000)
        out.append(bv.component_sheet(
            part("Low brace", one, COL["brace"]), [part("Legs", _stand_bit("legs"), "#9CA3AF"), part("Battens", _stand_bit("battens"), "#9CA3AF"),
                                                   part("Rails", _stand_bit("rails"), "#E5E7EB")],
            dwg_no="SSP-DWG-110", title="SunSpoke low brace (make 2) and cross batten (make 2): making sketch",
            material="Sawn timber 45 x 45 mm (brace), 45 x 20 mm (batten), treated",
            view_shape=Pos(-one.bounding_box().center().X, -one.bounding_box().center().Y, -150) * one, inset_view=(20, -55),
            notes=["Low braces (drawn): cut two 596 mm lengths of 45 x 45 mm.",
                   "  Two 9 mm holes at each end, 22 mm from the end, 12 mm in",
                   "  from the top and bottom faces, for the coach bolts.",
                   "Cross battens: cut two 935 mm lengths of 45 x 20 mm.",
                   "  Two 5 mm screw holes at each end, 22 mm from the end.",
                   "Fit: each brace lies inside its side frame's legs, 150 mm up,",
                   "  in line with the top rail above it. The battens join the two",
                   "  side frames across the back of the rear legs and the front of",
                   "  the front legs, 100 mm up, with 5 x 60 mm wood screws.",
                   "Check: the two side frames stand parallel, 935 mm apart outside."],
            **base))
    return out


# ----------------------------------------------------------------- tray layout (flat blank)
def layouts():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle, Circle, FancyBboxPatch
    INK, MUT, AC = "#111827", "#4B5563", "#0F766E"
    x0, x1 = P["base_x"]
    hw = P["base_half_w"]
    gx0, gx1 = P["guide_x"]
    ex0, ex1 = P["ear_x"]
    gh, eh = P["guide_h"], P["ear_h"]
    fig = plt.figure(figsize=(13, 7.6), dpi=150)
    ax = fig.add_axes([0.03, 0.08, 0.72, 0.8]); ax.set_aspect("equal"); ax.set_axis_off()
    # blank: base, guide tabs above and below, ear tab below (left side of the bike is drawn at the bottom)
    ax.add_patch(Rectangle((x0, -hw), x1 - x0, 2 * hw, fc="#F1F5F9", ec=INK, lw=1.1))
    for (a, b, y, h, lab) in ((gx0, gx1, hw, gh, "guide tab, right"), (gx0, gx1, -hw - gh, gh, "guide tab, left"),
                              (ex0, ex1, -hw - eh, eh, "latch ear tab, left")):
        ax.add_patch(Rectangle((a, y), b - a, h, fc="#F1F5F9", ec=INK, lw=1.1))
        ax.text((a + b) / 2, y + h / 2, lab, ha="center", va="center", fontsize=7, color=MUT)
    for (a, b, y) in ((gx0, gx1, hw), (gx0, gx1, -hw), (ex0, ex1, -hw)):
        ax.plot([a, b], [y, y], color=AC, lw=0.9, ls=(0, (6, 3)))
    ax.text(gx1 + 4, hw + 3, "fold up 90", fontsize=6.5, color=AC)
    ax.text(ex1 + 4, -hw - 7, "fold up 90", fontsize=6.5, color=AC)
    ax.axhline(0, xmin=0.02, xmax=0.98, color=MUT, lw=0.5, ls=(0, (8, 3, 2, 3)))
    for xs in P["saddle_x"]:
        for sg in (-1, 1):
            ax.add_patch(Rectangle((xs - 6.5, sg * P["slot_y"][0] if sg > 0 else -P["slot_y"][1]), 13, 3, fc="white", ec=INK, lw=0.8))
    for wx0, wx1 in P["window_x"]:
        ax.add_patch(FancyBboxPatch((wx0 + 4, -P["window_half_w"] + 4), wx1 - wx0 - 8, 2 * P["window_half_w"] - 8, boxstyle="round,pad=4",
                                    fc="white", ec=INK, lw=0.8))
    kinds = {}
    for what, hx, hy, hd, face in M.tray_holes(P):
        if face == "base":
            yy = hy
        elif face == "ear":
            yy = -hw - hy
        else:
            yy = None
        if face == "guide":
            for sg in (-1, 1):
                ax.add_patch(Circle((hx, sg * (hw + hy)), hd / 2, fc="white", ec=INK, lw=0.8))
        else:
            ax.add_patch(Circle((hx, yy), hd / 2, fc="white", ec=INK, lw=0.8))
        kinds.setdefault(what, []).append((hx, hy, hd, face))
    # x positions measured from the tray's bottom bracket end
    xs = sorted(set(round(h[1] - x0) for h in M.tray_holes(P)) | {round(xx - x0) for xx in P["saddle_x"]})
    for k, xx in enumerate(xs):
        yl = hw + gh + 12 + 9 * (k % 3)
        ax.plot([xx + x0, xx + x0], [hw + 2 if not (gx0 <= xx + x0 <= gx1) else hw + gh + 2, yl - 2], color=AC, lw=0.4, ls=":")
        ax.text(xx + x0, yl, f"{xx}", ha="center", va="bottom", fontsize=6.6, color=AC)
    ax.text(x0, hw + gh + 46, "Distances from the tray's lower end (the bottom bracket end), mm", fontsize=7.5, color=MUT)
    ax.text(x1 + 6, 0, "centre\nline", fontsize=6.5, color=MUT, va="center")
    ax.set_xlim(x0 - 12, x1 + 30); ax.set_ylim(-hw - eh - 30, hw + gh + 56)
    fig.text(0.03, 0.965, "Cradle tray: flat blank, folds and holes", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.03, 0.93, "Seen from above, as cut, before folding. Right side of the bike at the top. 3 mm aluminium. "
                         "Sizes to the outside of the folds; full-size figures in mm from the model.", fontsize=8.2, color=MUT, va="top")
    key = ["Base 470 x 98.", "Guide tabs 120 x 50, at 70 to 190.", "Latch ear tab 62 x 31, at 380 to 442.",
           "Band slots 3 x 13, 19 to 22 each side of the centre", "  line, centred at 170, 270 and 370.",
           "Air windows 68 x 44, either side of 270.", "",
           "Holes across the centre line (each side):",
           "  V-saddle screws 5.5, countersunk from above,", "    on the centre line, 12 each side of each slot pair",
           "  slide strip screws 4.5, at 40, countersunk below", "  catch bar screws 4.5, at 15, countersunk below",
           "  end stop foot bolts 5.5, at 20", "  host adapter screws 4.5, at 20", "  hinge screws 4.5, at 18", "",
           "In the folded tabs:", "  end stop flange bolts 5.5, 25 up, both guides", "  draw latch fixings 4.5, 23 up, latch ear",
           "", "Deburr every edge and hole."]
    fig.text(0.765, 0.86, "What each opening is (mm)", fontsize=9, fontweight="bold", color=INK, va="top")
    for i, t in enumerate(key):
        fig.text(0.765, 0.83 - i * 0.031, t, fontsize=7.6, color=INK, va="top")
    fig.text(0.03, 0.015, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    fig.text(0.97, 0.015, "github.com/BoujeeEnjinia1701/sunspoke", fontsize=7, color=AC, ha="right", family="monospace")
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "tray-layout.png", facecolor="white"); plt.close(fig)
    return OUT / "tray-layout.png"


# ----------------------------------------------------------------- joints
def joints(only=None):
    from build123d import Pos, Rot
    out = []
    zb, z0 = LV["zb"], LV["z0"]
    win = lambda sh, x0, x1, y0, y1, z0_, z1_: sh & M._box(x0, x1, y0, y1, z0_, z1_)  # noqa: E731

    def want(n):
        return only is None or n in only
    pk = M.pack_local(P)
    # 01 V-saddle and band, cut through the middle band, seen along the tube
    if want(1):
        bx = (-6, 6, -60, 60, -40, z0 + 30)
        out.append(bv.joint([
            part("Down tube (28 to 32 mm)", win(tube_local(), *bx), COL["tube"]),
            part("Rubber liner", win(CP["liners"], *bx), COL["liners"]),
            part("V-saddle", win(CP["saddles"], *bx), COL["saddles"]),
            part("Tray", win(CP["tray"], *bx), COL["tray"]),
            part("Band clamp, through the tray's slots", win(CP["bands"], *bx), "#64748B"),
            part("Slide strips", win(CP["rails"], *bx), "#CBD5E1"),
            part("Pack", win(pk, *bx), COL["pack"])],
            OUT / "joint-01.png", "Joint 1: V-saddle and band clamp on the down tube (cut through the middle band)",
            subtitle="Seen along the tube from the bottom bracket. The band pulls the tray and V down onto the tube; worm screw underneath",
            elev=0, azim=180.01, size=(8, 6)))
    # 02 end stop, receptacle and plug, cut on the centre line
    if want(2):
        bx = (-215, -125, 0, 29, zb - 4, z0 + 85)
        out.append(bv.joint([
            part("Tray", win(CP["tray"], *bx), COL["tray"]),
            part("End stop", win(CP["stop"], *bx), COL["stop"]),
            part("Receptacle (bought)", win(CP["receptacle"], *bx), COL["receptacle"]),
            part("Pack, with its plug", win(pk, *bx), COL["pack"])],
            OUT / "joint-02.png", "Joint 2: end stop, receptacle and the pack's plug (cut on the centre line)",
            subtitle="Seen from the left. The pack's end bears on the wall; its plug passes the notch into the receptacle, 1 mm short of the bottom",
            elev=8, azim=-90, size=(8, 6)))
    # 03 gate, hinge, pad and catch, cut on the centre line
    if want(3):
        bx = (95, 215, 0, 60, zb - 4, z0 + 50)
        out.append(bv.joint([
            part("Tray", win(CP["tray"], *bx), COL["tray"]),
            part("Catch bar", win(CP["catch"], *bx), COL["catch"]),
            part("Pack, with its spring latch", win(pk, *bx), COL["pack"]),
            part("Rubber pad", win(CP["pad"], *bx), COL["pad"]),
            part("Gate", win(CP["gate"], *bx), COL["gate"]),
            part("Hinge", win(L("hinge", "hinge_leaf"), *bx), COL["hinge"])],
            OUT / "joint-03.png", "Joint 3: gate, hinge and catch bar at the head tube end (cut on the centre line)",
            subtitle="Seen from the left. Closed, the gate's pad presses the pack's end below the handle; the pack's latch sits behind the catch bar",
            elev=8, azim=-90, size=(8, 6)))
    # 04 draw latch on the ear
    if want(4):
        bx = (95, 215, -75, 10, zb - 4, z0 + 45)
        out.append(bv.joint([
            part("Tray and latch ear", win(CP["tray"], *bx), COL["tray"]),
            part("Over-centre draw latch", win(CP["latch"], *bx), COL["latch"]),
            part("Keeper on the gate flange", win(CP["keeper"], *bx), COL["keeper"]),
            part("Gate and its flange", win(CP["gate"], *bx), COL["gate"])],
            OUT / "joint-04.png", "Joint 4: draw latch, keeper and gate flange on the left side",
            subtitle="Seen from the left, front and above. The latch hook pulls the gate flange toward the pack; its safety catch holds it closed",
            elev=18, azim=-70, size=(8, 6)))
    C = comps()
    # 05 torque arm at the axle (left side)
    fr = G["front"]
    if want(5):
        bx = (fr[0] - 60, fr[0] + 60, -90, -30, fr[1] - 50, fr[1] + 110)
        out.append(bv.joint([
            part("Fork blade and dropout (donor)", win(C["fork"][0], *bx), COL["donor"]),
            part("Motor axle with flats", win(C["motor"][0], *bx), COL["motor"]),
            part("Torque arm", win(C["arms"][0], *bx), COL["arm"]),
            part("Axle washer and nut", win(C["axle_nuts"][0], *bx), "#374151")],
            OUT / "joint-05.png", "Joint 5: torque arm on the left dropout",
            subtitle="Seen from the left and in front. The arm's slot fits the axle flats; it lies flat on the dropout, under the washer and nut",
            elev=12, azim=-70, size=(8, 6)))
    # 06 torque arm band clamp, cut across the blade
    if want(6):
        u, n = G["fork_u"], G["fork_n"]
        cpt = (fr[0] + u[0] * P["arm_len"], fr[1] + u[1] * P["arm_len"])
        sl = M._fork_local(P, -1, lambda: M._box(-40, 40, -100, -30, P["arm_len"] - 6, P["arm_len"] + 6))
        out.append(bv.joint([
            part("Fork blade (donor)", C["fork"][0] & sl, COL["donor"]),
            part("Torque arm", C["arms"][0] & sl, COL["arm"]),
            part("Band clamp round blade and arm", C["arm_clamps"][0] & sl, "#64748B"),
            part("Motor cable, tied over the clamp", C["harness"][0] & sl, COL["harness"])],
            OUT / "joint-06.png", "Joint 6: torque arm band clamp, 130 mm up the left blade (cut across the blade)",
            subtitle="Seen down the blade from above; the outside of the bike is at the lower left. The arm lies on the blade's outside; one band goes round both",
            elev=72, azim=-90 - 19.7, size=(8, 6)))
    # 07 controller on the seat tube, cut across
    if want(7):
        bb, st = G["bb"], G["seat_top"]
        sa = M._along(bb, st, 0.38)
        sv = (st[0] - bb[0], st[1] - bb[1]); ln = math.hypot(*sv); sv = (sv[0] / ln, sv[1] / ln)
        ang = math.degrees(math.atan2(sv[0], sv[1]))
        o = (sa[0] + sv[0] * 45, sa[1] + sv[1] * 45)
        sl = M.Pos(o[0], 0, o[1]) * Rot(0, ang, 0) * M._box(-40, 100, -60, 60, -10, 10)
        out.append(bv.joint([
            part("Seat tube (donor)", C["frame"][0] & sl, COL["donor"]),
            part("Rubber pad", C["ctrl_pad"][0] & sl, COL["pad"]),
            part("Controller", C["controller"][0] & sl, COL["ctrl"]),
            part("Band clamp", C["ctrl_bands"][0] & sl, "#64748B"),
            part("Harness", C["harness"][0] & sl, COL["harness"])],
            OUT / "joint-07.png", "Joint 7: controller on the seat tube (cut through the upper band)",
            subtitle="Seen down the seat tube from above. Rubber pad between tube and case; each band goes round tube and case",
            elev=70, azim=-90 - 21.4 + 180, size=(8, 6)))
    # 08 pedal-assist disc and sensor
    if want(8):
        bb = G["bb"]
        bx = (bb[0] - 70, bb[0] + 0.5, -60, 10, bb[1] - 50, bb[1] + 45)
        out.append(bv.joint([
            part("Bottom bracket, cup and lockring (donor)", win(C["frame"][0] + C["drive"][0], *bx), COL["donor"]),
            part("Sensor bracket and sensor", win(C["pas_sensor"][0], *bx), COL["pas"]),
            part("Magnet disc, clamped on the spindle", win(C["pas_disc"][0], *bx), "#0369A1")],
            OUT / "joint-08.png", "Joint 8: pedal-assist disc and sensor at the bottom bracket (cut through the spindle)",
            subtitle="Seen from in front; the left of the bike is on the left. Bracket ring under the lockring; 2.5 mm from the sensor face to the magnets",
            elev=0.01, azim=0.01, size=(8, 6)))
    # 09 brake sensor at the left lever
    if want(9):
        a = M.bar_point(912, -1)
        bx = (a.X - 40, a.X + 40, a.Y - 40, a.Y + 40, a.Z - 45, a.Z + 25)
        out.append(bv.joint([
            part("Handlebar (donor)", win(C["stem_bars"][0], *bx), COL["donor"]),
            part("Brake lever, clamp and pivot (donor)", win(C["levers"][0], *bx), "#9CA3AF"),
            part("Brake sensor on its bar clamp, magnet on the lever", win(C["brake_sensors"][0], *bx), COL["bar"])],
            OUT / "joint-09.png", "Joint 9: brake cut-off sensor at the left lever",
            subtitle="Seen from in front and below. The magnet is glued to the lever's pivot post; pulling the lever turns it away from the sensor",
            elev=-20, azim=-30, size=(8, 6)))
    # 10 stand: leg, top rail, brace and panel at the rear left corner
    if want(10):
        F = Pos(P["panel_x"], 0, P["panel_z"]) * Rot(0, P["panel_tilt"], 0)
        xr = (F * Pos(-P["leg_u"], 0, 0)).position.X
        bx = (xr - 120, xr + 120, -560, -330, 450, 800)
        out.append(bv.joint([
            part("Solar panel frame", win(C["panel"][0], *bx), COL["panel"]),
            part("Top rail", win(_stand_bit("rails"), *bx), COL["timber"]),
            part("Rear leg", win(_stand_bit("legs"), *bx), COL["leg"]),
            part("Boost charger", win(C["charger"][0], *bx), COL["charger"])],
            OUT / "joint-10.png", "Joint 10: rear leg, top rail and panel (left rear corner of the stand)",
            subtitle="Seen from the left and behind. The leg laps the rail's outside face on one coach bolt; the panel frame bolts down through the rail",
            elev=15, azim=-130, size=(8, 6)))
    # 11 wet-weather blocks on the rim, cut across the rim through the block
    if want(11):
        fr = G["front"]
        a = math.radians(P["wb_angle"])
        rx, rz = -math.sin(a), math.cos(a)
        bc = (fr[0] + P["wb_r"] * rx, fr[1] + P["wb_r"] * rz)
        sl = Pos(bc[0], 0, bc[1]) * Rot(0, math.degrees(math.atan2(rx, rz)), 0) * M._box(-6, 6, -50, 50, -30, 55)
        W0 = Pos(fr[0], 0, fr[1]) * Rot(90, 0, 0)
        r_ = P["wheel_r"]
        tyre_s = (W0 * M.Torus(r_ - 20, 20)) & sl
        rim_s = (W0 * (M.Cylinder(r_ - 38, 20) - M.Cylinder(r_ - 52, 22))) & sl
        out.append(bv.joint([
            part("Tyre", tyre_s, "#1F2937"),
            part("Rim (donor steel)", rim_s, "#9CA3AF"),
            part("Wet-weather blocks, one each side of the rim", C["wet_blocks"][0] & sl, COL["blocks"])],
            OUT / "joint-11.png", "Joint 11: wet-weather brake blocks on the front rim (cut across the rim through the blocks)",
            subtitle="Seen along the rim from the front. A block presses on each side face of the steel rim; the tyre sits outside the braking surface",
            elev=20, azim=0, size=(8, 6)))
    return out


# ----------------------------------------------------------------- assembly steps
def steps(only=None):
    from build123d import Pos
    out = []
    zb, z0 = LV["zb"], LV["z0"]
    C = comps()

    def want(n):
        return only is None or n in only

    def st(n, done, new, title, sub, **kw):
        if want(n):
            out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))

    def mv(p_, e):
        return Part(p_.name, p_.shape, p_.color, None, tuple(e), p_.alpha)
    tray = part("Tray", CP["tray"], COL["tray"])
    sad = part("V-saddles with liners", L("saddles", "liners"), COL["saddles"])
    # bench steps, cradle frame
    st(1, [tray], [mv(sad, (0, 0, -60))], "V-saddles onto the tray",
       "On the bench, seen from below. Two M5 countersunk screws down through the tray into each saddle's tapped holes", elev=-25, azim=-60)
    s2 = [tray, sad]
    st(2, s2, [mv(part("Slide strips (2)", CP["rails"], "#0EA5E9"), (0, 0, 50)),
               mv(part("Catch bar", CP["catch"], COL["catch"]), (0, 0, 70)),
               mv(part("End stop", CP["stop"], COL["stop"]), (-50, 0, 70)),
               mv(part("Receptacle", CP["receptacle"], COL["receptacle"]), (-110, 0, 0))],
       "slide strips, catch bar, end stop and receptacle",
       "Strips and bar on screws up from below; end stop on four M5 bolts; receptacle on four M4 bolts behind the wall",
       elev=28, azim=-60, label_done=False)
    s3 = s2 + [part("Fitted", L("rails", "catch", "stop", "receptacle"), "#D1D5DB")]
    st(3, s3, [mv(part("Hinge and gate with pad", L("hinge", "hinge_leaf", "gate", "pad"), COL["gate"]), (60, 0, 40)),
               mv(part("Draw latch on the ear, keeper on the gate", L("latch", "keeper"), COL["latch"]), (0, -70, 0))],
       "gate, hinge and draw latch", "Hinge: two M4 bolts in the tray, two in the gate. Latch: two M4 rivets or bolts in the ear; keeper on the gate flange",
       elev=25, azim=-55, label_done=False)
    s4 = s3 + [part("Fitted", L("hinge", "hinge_leaf", "gate", "pad", "latch", "keeper"), "#D1D5DB")]
    st(4, s4, [mv(part("Host adapter and lead", L("adapter", "inlet", "adapter_lead"), COL["adapter"]), (-60, 0, 60))],
       "host adapter and its lead to the receptacle", "Two M4 screws up through the tray into the adapter's inserts; plug the lead into the receptacle",
       elev=25, azim=-60, label_done=False)
    # on the bike
    D = M.donor_parts(P)
    donor_ctx = [part("Roadster", D["frame"] + D["fork"] + D["stem_bars"] + D["drive"], "#E5E7EB")]
    zd = zdir()
    cradle_all = S("tray", "saddles", "liners", "rails", "catch", "stop", "receptacle", "gate", "pad", "hinge", "hinge_leaf", "latch", "keeper",
                   "adapter", "inlet", "adapter_lead")
    frame_only = [part("Frame", D["frame"], "#D1D5DB")]
    st(5, frame_only, [mv(part("Receiver cradle", cradle_all, COL["tray"]), add(along(zd, 110), (0, -40, 0))),
                       mv(part("Band clamps (3)", S("bands"), "#BE185D"), (0, -130, 0))],
       "cradle onto the down tube", "Saddles on the tube, centred at 48 % of its length; three band clamps through the slots, screws underneath, tightened evenly",
       elev=20, azim=-62)
    fork = [part("Fork", D["fork"], "#D1D5DB")]
    st(6, fork, [mv(part("Motor wheel (rim and spokes not drawn)", S("motor"), COL["motor"]), (0, 0, -120)),
                 mv(part("Torque arms (2)", S("arms"), COL["arm"]), (0, -90, 0)),
                 mv(part("Washers and axle nuts", S("axle_nuts"), "#374151"), (0, -150, 0))],
       "motor wheel and torque arms into the fork", "Axle flats up into both dropout slots; an arm over each axle end, flat on the dropout; washer and nut, finger tight",
       elev=12, azim=-55)
    st(7, fork + [part("Motor and arms", S("motor", "arms", "axle_nuts"), "#D1D5DB")],
       [mv(part("Arm band clamps (2)", S("arm_clamps"), "#BE185D"), (0, -60, 60))],
       "band clamps round the blades and arms, then tighten the axle nuts",
       "Clamps 130 mm up each blade; then axle nuts to the motor maker's torque (typically 30 to 40 N m)", elev=12, azim=-55, label_done=False)
    st(8, frame_only, [mv(part("Controller and pad", S("controller", "ctrl_pad"), COL["ctrl"]), (110, -40, 40)),
                       mv(part("Band clamps (2)", S("ctrl_bands"), "#BE185D"), (0, -110, 0))],
       "controller onto the seat tube", "Pad against the front of the seat tube, controller on it, cable glands down; two band clamps round tube and case",
       elev=15, azim=-62)
    bbp = G["bb"]
    bb_ctx = [part("Frame and bottom bracket", (D["frame"] + D["drive"]) & M._box(bbp[0] - 130, bbp[0] + 130, -120, 120, bbp[1] - 130, bbp[1] + 120), "#D1D5DB")]
    st(9, bb_ctx, [mv(part("Sensor bracket and sensor", S("pas_sensor"), COL["pas"]), (0, -60, 0)),
                   mv(part("Magnet disc", S("pas_disc"), "#0369A1"), (0, -110, 0))],
       "pedal-assist sensor and disc", "Left crank off; bracket under the left lockring, sensor pointing down; disc on the spindle, magnets toward the sensor; crank back on",
       elev=15, azim=-125)
    bar_ctx = [part("Stem, bars and levers", D["stem_bars"] + D["levers"], "#D1D5DB")]
    st(10, bar_ctx, [mv(part("Display on its clamp", S("display"), COL["bar"]), (0, 0, 70)),
                     mv(part("Brake sensors and magnets", S("brake_sensors"), "#1D4ED8"), (0, 0, -70))],
       "display and brake cut-off sensors", "Display clamp left of the stem; a sensor clamp inboard of each lever; magnets glued to the lever posts",
       elev=22, azim=-40)
    kit_pre = S("tray", "saddles", "rails", "stop", "gate", "latch", "adapter", "bands", "motor", "arms", "arm_clamps", "controller",
                 "ctrl_bands", "pas_disc", "pas_sensor", "display", "brake_sensors") + front_wheel()
    kit_done = kit_pre + front_blocks()
    st(11, donor_ctx + [part("Kit fitted", kit_pre, "#D1D5DB")],
       [mv(part("Wet-weather block, left of the rim", front_blocks("L"), COL["blocks"]), (0, -90, 0)),
        mv(part("Wet-weather block, right of the rim", front_blocks("R"), COL["blocks"]), (0, 90, 0))],
       "wet-weather brake blocks", "Front pair shown; the rear pair fits the same way. Old block off its stirrup, new block on, set square to the rim face, 2 to 3 mm off the rim",
       elev=14, azim=-80, label_done=False)
    st(12, donor_ctx + [part("Kit fitted", kit_done, "#D1D5DB")],
       [mv(part("Harness, fuse and leads", S("harness"), COL["harness"]), (0, -140, 0))],
       "harness", "Left side of the tubes, cable ties every 150 mm, drip loops at every plug. Fuse out until the safety stops allow",
       elev=18, azim=-62, label_done=False)
    st(13, donor_ctx + [part("Kit fitted", kit_done + S("harness"), "#D1D5DB")],
       [mv(part("SwapCell pack", S("pack"), COL["pack"]), add(along(xdir(), 150), along(zd, 50), (0, -120, 0)))],
       "pack in, gate up, latch closed", "Gate folded down; pack in from the left, onto the strips, slid down onto the plug; gate up, latch closed and caught",
       elev=18, azim=-62, label_done=False)
    # solar set
    rails = part("Top rails", _stand_bit("rails"), COL["timber"])
    legs = part("Legs", _stand_bit("legs"), COL["leg"])
    braces = part("Low braces", _stand_bit("braces"), COL["brace"])
    st(14, [rails], [mv(legs, (0, -90, 0)), mv(braces, (0, 0, -90))], "the two side frames",
       "Each side: a rail and a brace, both inside two legs; one M8 coach bolt at each rail lap, two at each brace lap", elev=20, azim=-55)
    sides = [part("Side frames", _stand_bit("rails") + _stand_bit("legs") + _stand_bit("braces"), "#D1D5DB")]
    st(15, sides, [mv(part("Cross battens", _stand_bit("battens"), COL["batten"]), (0, 0, -80)),
                   mv(part("Solar panel", S("panel"), COL["panel"]), (0, 0, 200))],
       "battens, then the panel", "Battens across the rear and front legs, two screws at each end; panel on the rails, four M6 bolts through its frame",
       elev=22, azim=-55, label_done=False)
    st(16, sides + [part("Panel and battens", S("panel") + _stand_bit("battens"), "#D1D5DB")],
       [mv(part("Boost charger", S("charger"), COL["charger"]), (0, -120, 0)),
        mv(part("Panel lead", S("panel_lead"), COL["cable"]), (0, -60, 60))],
       "charger and panel lead", "Charger on the outside of the left rear leg, in the panel's shade, two screws; panel lead into its input",
       elev=18, azim=-50, label_done=False)
    return out


# ----------------------------------------------------------------- wiring
def wiring():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    fig = plt.figure(figsize=(12.5, 8.0), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 125); ax.set_ylim(0, 80); ax.set_axis_off()
    INK, MUT = "#111827", "#4B5563"
    ax.text(2, 78.4, "SunSpoke prototype: block-level wiring", fontsize=13, fontweight="bold", color=INK, va="top")
    ax.text(2, 75.0, "Bought parts joined by the harness; every joint is a keyed waterproof plug. Wire sizes are stranded copper.",
            fontsize=8.5, color=MUT, va="top")
    ax.text(2, 1.5, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    ax.text(123, 1.5, "github.com/BoujeeEnjinia1701/sunspoke", fontsize=7, color="#0F766E", ha="right", family="monospace")

    def blk(x, y, w, h, title, sub, color):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fc="white", ec=color, lw=1.8))
        ax.text(x + w / 2, y + h - 1.3, title, ha="center", va="top", fontsize=8.8, fontweight="bold", color=INK)
        ax.text(x + w / 2, y + h - 4.1, sub, ha="center", va="top", fontsize=7, color=MUT, linespacing=1.3)

    def wire(pts, color, lw=2.0):
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round", zorder=1)

    def lab(x, y, text, color, ha="left"):
        ax.text(x, y, text, fontsize=7, color=color, ha=ha, va="center", zorder=3, bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))
    RED, BLU, GRY, GRN = "#B91C1C", "#1D4ED8", "#6B7280", "#15803D"
    blk(3, 42, 17, 15, "SwapCell pack", "13S2P, 46.8 V,\n468 Wh, own BMS\nand fuse", "#C2410C")
    blk(27, 42, 17, 15, "Receptacle", "in the cradle;\n10 kOhm 1 %\ncoding resistor", "#1F2937")
    blk(27, 16, 17, 14, "Host adapter", "CAN host, charge\nhost; diode-OR\nsupply", "#7C3AED")
    blk(55, 40, 18, 17, "Controller", "48 V, 15 A, sine;\nmotor thermistor\nderate from 110 C", "#115E59")
    blk(86, 52, 17, 12, "Display unit", "level, charge,\nwalk button", "#2563EB")
    blk(106, 52, 16, 12, "Power switch", "on the display;\nINTERLOCK loop", "#2563EB")
    blk(86, 36, 17, 11, "Hub motor", "3 phases, 3 Hall,\nwinding NTC", "#0F766E")
    blk(106, 36, 16, 11, "Pedal-assist", "Hall sensor,\n12-magnet disc", "#0EA5E9")
    blk(86, 16, 17, 11, "Brake sensors", "left and right,\nmagnetic", "#1D4ED8")
    blk(3, 14, 17, 14, "Charge inlet", "keyed; from the\nboost charger by\nthe 5 m cable", "#16A34A")
    wire([(20, 51), (27, 51)], RED); lab(23.5, 53, "pack plug", RED, "center")
    wire([(44, 51), (55, 51)], RED); lab(49.5, 54.4, "PACK+ and -,\n2.5 mm2", RED, "center")
    ax.add_patch(FancyBboxPatch((47.6, 49.6), 3.8, 2.8, boxstyle="round,pad=0.1", fc="#FDE68A", ec="#B45309", lw=1.0, zorder=2))
    ax.text(49.5, 46.8, "20 A fuse", fontsize=7, color="#B45309", ha="center", fontweight="bold")
    wire([(73, 55), (86, 58)], BLU, 1.2); lab(79.5, 58.6, "display bus 0.25", BLU, "center")
    wire([(73, 47), (86, 44)], RED); lab(79.5, 47.6, "phases 1.5 mm2", RED, "center")
    wire([(73, 44.5), (86, 40.5)], GRY, 1.2); lab(79.5, 41.0, "Hall, NTC 0.25", GRY, "center")
    wire([(73, 42), (77.5, 42), (77.5, 32.5), (114, 32.5), (114, 36)], GRY, 1.2); lab(96, 32.5, "PAS 0.25", GRY, "center")
    wire([(73, 41), (76, 41), (76, 21.5), (86, 21.5)], GRY, 1.2); lab(80.5, 23.2, "brake 0.25", GRY, "center")
    wire([(40, 57), (40, 70), (111, 70), (111, 64)], GRN, 1.4)
    wire([(42, 57), (42, 68.5), (117, 68.5), (117, 64)], GRN, 1.4)
    lab(44, 66.6, "INTERLOCK loop through the power switch and the coding resistor, 0.25 mm2", GRN)
    wire([(33, 42), (33, 30)], BLU, 1.4); lab(33.6, 36, "CAN, 0.25 mm2", BLU)
    wire([(38, 42), (38, 30)], RED, 1.4); lab(38.6, 33.4, "PACK+ for the\nadapter, 0.5 mm2", RED)
    wire([(20, 21), (27, 21)], RED); lab(23.5, 23, "charge, 1.5 mm2", RED, "center")
    wire([(44, 24), (62, 24), (62, 40)], GRY, 1.2); lab(62.6, 30, "power-lock to\ncontroller, 0.25", GRY)
    ax.text(3, 9.2, "Safety: fuse out and pack out until the safety stops in section 6 of the plan allow. About 50 V DC: below the usual touch threshold, "
            "but a short can melt wire.", fontsize=7.4, color="#B45309", fontweight="bold")
    ax.text(3, 5.8, "Red: power. Blue: data. Green: SwapCell INTERLOCK wake loop. Grey: sensing and control. Plugs: IP65 keyed, dielectric grease, "
            "drip loop below each.", fontsize=7.2, color=MUT)
    out = OUT / "wiring.png"
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


if __name__ == "__main__":
    args = sys.argv[1:] or ["overview", "sheets", "layouts", "joints", "steps", "wiring"]
    fns = {"overview": overview, "sheets": sheets, "layouts": layouts, "joints": joints, "steps": steps, "wiring": wiring}
    what = [a for a in args if a in fns]
    nums = [int(a) for a in args if a.isdigit()] or None
    for w in what:
        r = fns[w](nums) if (nums and w in ("sheets", "joints", "steps")) else fns[w]()
        print(w, "->", r)
