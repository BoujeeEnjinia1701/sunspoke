"""SunSpoke product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders of the conversion kit fitted to a steel roadster:
a brushed geared hub motor laced into the 28 in front rim with side covers, cover screws, axle
nuts, a teal band and its cable exit; keyed torque arms with band clamps on both fork blades;
the SwapCell pack in its receiver cradle, with end caps, a carry handle, a lit charge gauge, a
label and the teal V1 preload lever; lined band clamps with clamp screws; the finned, sealed
controller strapped to the seat tube; the potted host adapter with its charge inlet and the
charge plug fitted; the pedal-assist magnet disc and sensor; the handlebar display with lit
level segments, the walk-assist button and the two brake-lever sensors; the harness with
cable ties and a clear fuse holder; and the 100 W solar set (panel with cells and busbars,
timber stand, finned boost charger with a lit charge light, and the 5 m charge cable).
The donor roadster (lugged frame, fork, wheels, sprung saddle, bars, carrier and drivetrain)
counts as part of the product in these renders. Context is a clay rider (1.75 m) in the "ride"
pose, hands on the grips and feet on the pedals.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every main dimension and interface comes from PARAMS, geometry(), cradle_location(),
pack_local(), cradle_local() and receptacle_local() in model.py. Axes as model.py: X forward,
Z up, Y across the bike (the camera side is -Y, the bike's right), rear axle at X = 0, ground
at Z = 0. Render-only differences from model.py are listed in docs/REVIEW.md, session
2026-09-26.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
sys.path.insert(0, str(_HERE.parents[1] / ".kit"))

from build123d import (Axis, Box, Compound, Cylinder, Location, Plane, Pos, RegularPolygon, Rot, Solid,
                       Sphere, Torus, Vector, extrude, fillet)
from model import PARAMS, geometry, cradle_location, pack_local, receptacle_local  # noqa: F401

TITLE = "SunSpoke: solar-charged e-bike conversion kit for steel roadster bicycles"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "accessory", "context"], "explode": False, "el": 18, "az": -55,
     "note": "Product render from the front right and above (about 18 deg elevation); rider on the converted "
             "roadster, hub motor at the front, SwapCell pack in the frame, controller on the seat tube, and "
             "the 100 W panel at right charging the pack through the charge inlet"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): hub motor wheel and torque "
             "arms, SwapCell pack and cradle, host adapter, controller, pedal-assist sensor, handlebar unit, "
             "harness, and the solar panel, stand, charger and cable"},
    {"name": "detail", "groups": ["internal"], "explode": False, "el": 12, "az": -62,
     "note": "Detail from the front right, slightly above (about 12 deg elevation): 250 W hub motor laced into "
             "the 28 in rim, torque arms clamped to both fork blades, axle nuts and motor cable exit"},
]

# Rider pose: "ride" with arm and torso overrides so the hands close on the swept-back grips
# (grip centre X = 850 mm) of the model.py roadster bars; feet land on the pedals.
RIDER_H = 1750.0
RIDER_POSE = dict(torso_lean=28.1, shoulder_flex_l=52.2, shoulder_flex_r=52.2, elbow_flex_l=16.0,
                  elbow_flex_r=16.0, shoulder_abd_l=27.8, shoulder_abd_r=27.8)

# Colours (restrained product palette; kit accent)
C_FRAME = "#22262C"      # gloss black roadster enamel
C_CHROME = "#C4C9CF"
C_LUG = "#2E333A"
C_TYRE = "#1B1D20"
C_RIM = "#B8BEC6"
C_SPOKE = "#A9AFB6"
C_SADDLE = "#5B4332"
C_ACCENT = "#0F766E"
C_ACCENT_D = "#0B5F59"
C_MOTOR = "#AEB5BD"
C_COVER = "#3A3F46"
C_ZINC = "#B6A770"
C_PACK = "#E6E8EB"
C_PACK_END = "#2B2F36"
C_DARK = "#2B2F36"
C_BLACK = "#16181C"
C_CRADLE = "#5F6670"
C_ALU = "#9EA5AD"
C_LABEL = "#F4F4F2"
C_LED_G = "#22C55E"
C_LED_T = "#2DD4BF"
C_LED_OFF = "#2A3A36"
C_GLASS = "#DCEBF5"
C_CELL = "#1B2A4A"
C_BACKSHEET = "#E7E9EC"
C_TIMBER = "#A57C52"
C_CABLE = "#1F2226"
C_CLAY = "#9CA3AF"


# ---------------------------------------------------------------- helpers
def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _box(cx, cy, cz, sx, sy, sz):
    return Pos(cx, cy, cz) * Box(sx, sy, sz)


def _ycyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(90, 0, 0) * Cylinder(r, h)


def _rod(a, b, r):
    a, b = Vector(*a), Vector(*b)
    d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def _pipe(points, r):
    """Round tube through `points` with spherical joints (clean bends)."""
    out = None
    for a, c in zip(points, points[1:]):
        seg = _rod(a, c, r)
        out = seg if out is None else out + seg
    for q in points[1:-1]:
        out += Pos(*q) * Sphere(r)
    return out


def _beam(a, b, w, h):
    """Rectangular beam w x h from a to b (h measured along world Y where possible)."""
    a, b = Vector(*a), Vector(*b)
    d = (b - a).normalized()
    ref = Vector(0, 1, 0) if abs(d.Y) < 0.9 else Vector(1, 0, 0)
    xd = ref.cross(d).normalized()
    mid = (a + b) * 0.5
    return Location(Plane(origin=mid, x_dir=xd, z_dir=d)) * Box(w, h, (b - a).length)


def _ring_y(x, y, z, r_out, r_in, w):
    return Pos(x, y, z) * Rot(90, 0, 0) * (Cylinder(r_out, w) - Cylinder(r_in, w + 2))


def _hex_y(x, y, z, af, t):
    return Pos(x, y - t / 2, z) * Rot(-90, 0, 0) * extrude(RegularPolygon(af / 1.732, 6), amount=t)


def _comp(shapes):
    shapes = [s for s in shapes if s is not None]
    return shapes[0] if len(shapes) == 1 else Compound(shapes)


def _edges_par(s, axis):
    return s.edges().filter_by(axis)


def _along(p, q, t):
    return tuple(p[i] + (q[i] - p[i]) * t for i in range(len(p)))


def _local_face_edges(shape, loc_dir):
    return shape.faces().sort_by(loc_dir)[-1].edges()


# ---------------------------------------------------------------- wheels
def _wheel(cx, cz, R, hub_r, hub_y, cross_deg, n=36):
    """Tyre, rim, valve and n spokes from flanges at +/-hub_y (radius hub_r) to the rim centre line."""
    tyre = Pos(cx, 0, cz) * Rot(90, 0, 0) * Torus(R - 20, 20)
    rim = Pos(cx, 0, cz) * Rot(90, 0, 0) * (Cylinder(R - 38, 20) - Cylinder(R - 52, 22))
    rim = _fillet_try(rim, rim.edges(), [2.0, 1.0])
    valve = _rod((cx, 0, cz + R - 52), (cx, 0, cz + R - 80), 3.0)
    spokes = []
    for k in range(n):
        a = math.radians(k * 360.0 / n + 5)
        side = 1 if k % 2 == 0 else -1
        lead = 1 if (k // 2) % 2 == 0 else -1
        b = a + math.radians(lead * cross_deg)
        p0 = (cx + hub_r * math.cos(b), side * hub_y, cz + hub_r * math.sin(b))
        p1 = (cx + (R - 54) * math.cos(a), side * 3.0, cz + (R - 54) * math.sin(a))
        spokes.append(_rod(p0, p1, 1.0))
    return tyre, rim, valve, _comp(spokes)


# ---------------------------------------------------------------- the model
def product_parts(P=PARAMS):
    g = geometry(P)
    R = P["wheel_r"]
    rear, front, bb, st, hb, ht = g["rear"], g["front"], g["bb"], g["seat_top"], g["head_bot"], g["head_top"]
    tr = P["tube_r"]
    fy = P["fork_spacing"] / 2
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    def T(p1, p2, r, y=0.0):
        return _rod((p1[0], y, p1[1]), (p2[0], y, p2[1]), r)

    # ============================================================ donor roadster (product body, no BOM)
    frame = [T(bb, st, tr), T(st, ht, tr), T(bb, hb, P["dt_r"]), T(hb, ht, 18),
             T(bb, rear, 9, 45), T(bb, rear, 9, -45), T(st, rear, 8, 45), T(st, rear, 8, -45),
             _ycyl(bb[0], 0, bb[1], 21, 72)]                                 # bottom bracket shell
    for s in (-1, 1):                                                        # rear dropouts
        frame.append(_box(rear[0] + 6, s * 45, rear[1] + 4, 40, 6, 34))
    add("Roadster frame (steel, black enamel)", _comp(frame), C_FRAME, "painted", None, "shell", (0, 0, 0))

    # lugs and head set, a slightly larger sleeve at each joint
    hd = Vector(ht[0] - hb[0], 0, ht[1] - hb[1]).normalized()
    lugs = [_rod((hb[0] - hd.X * 4, 0, hb[1] - hd.Z * 4), (hb[0] + hd.X * 24, 0, hb[1] + hd.Z * 24), 21),
            _rod((ht[0] - hd.X * 24, 0, ht[1] - hd.Z * 24), (ht[0] + hd.X * 4, 0, ht[1] + hd.Z * 4), 21)]
    sd = Vector(st[0] - bb[0], 0, st[1] - bb[1]).normalized()
    lugs.append(_rod((st[0] - sd.X * 40, 0, st[1] - sd.Z * 40), (st[0] + sd.X * 6, 0, st[1] + sd.Z * 6), 17))
    add("Frame lugs and head set", _comp(lugs), C_LUG, "painted", None, "shell", (0, 0, 0))

    # seat post, sprung leather saddle (top meets the rider's seat point)
    post = _rod((st[0] - sd.X * 10, 0, st[1] - sd.Z * 10), (205, 0, 915), 12.5)
    rails = _comp([_rod((150, s * 22, 925), (285, s * 16, 935), 4) for s in (-1, 1)])
    add("Seat post and saddle rails", _comp([post, rails]), C_CHROME, "metal", None, "shell", (0, 0, 0))
    springs = []
    for s in (-1, 1):
        for k in range(6):
            springs.append(Pos(150, s * 40, 912 + 4.5 * k) * Torus(11, 2.2))
    add("Saddle springs", _comp(springs), C_CHROME, "metal", None, "shell", (0, 0, 0))
    sad = (Pos(160, 0, 945) * Cylinder(78, 26)) + (Pos(300, 0, 945) * Cylinder(26, 26))
    sad += _box(230, 0, 945, 140, 70, 26)
    try:
        from build123d import make_hull, Circle, Sketch  # noqa: F401
        outline = make_hull((Pos(160, 0) * Circle(78)).edges() + (Pos(302, 0) * Circle(24)).edges())
        sad = Pos(0, 0, 932) * extrude(outline, amount=32)
    except Exception:
        pass
    sad = _fillet_try(sad, sad.faces().sort_by(Axis.Z)[-1].edges(), [12.0, 9.0, 6.0])
    sad = _fillet_try(sad, sad.faces().sort_by(Axis.Z)[0].edges(), [3.0, 1.5])
    add("Leather saddle", sad, C_SADDLE, "rubber", None, "shell", (0, 0, 0))

    # rear carrier: tube frame with slats and stays (model.py platform envelope)
    carr = [_rod((-270, s * 80, 800), (150, s * 80, 800), 6) for s in (-1, 1)]
    carr += [_rod((x, -80, 800), (x, 80, 800), 6) for x in (-270, 150)]
    carr += [_rod((x, -80, 802), (x, 80, 802), 3.5) for x in (-190, -110, -30, 50)]
    carr += [_rod((-230, s * 60, 795), (0, s * 60, R), 6) for s in (-1, 1)]
    carr += [_rod((150, s * 70, 800), (st[0] - sd.X * 30, s * 16, st[1] - sd.Z * 30), 4) for s in (-1, 1)]
    add("Rear carrier", _comp(carr), C_FRAME, "painted", None, "shell", (0, 0, 0))

    # fork, stem, bars, grips, brake levers
    fork = [T(hb, front, P["fork_blade_r"], fy), T(hb, front, P["fork_blade_r"], -fy)]
    crown = Pos(hb[0], 0, hb[1]) * Box(46, P["fork_spacing"] + 16, 22)
    crown = _fillet_try(crown, crown.edges(), [6.0, 4.0, 2.0])
    fork.append(crown)
    for s in (-1, 1):
        fork.append(_box(front[0] + 4, s * (fy + 2), front[1] + 6, 26, 5, 30))  # fork ends
    add("Roadster fork", _comp(fork), C_FRAME, "painted", None, "internal", (0, 0, 0))
    stem = _comp([T(ht, (950, 960), 12), _ycyl(950, 0, 960, 16, 44)])
    bars = _comp([_rod((950, -300, 960), (950, 300, 960), 11), Pos(950, 300, 960) * Sphere(11),
                  Pos(950, -300, 960) * Sphere(11),
                  _rod((950, 300, 960), (820, 330, 945), 11), _rod((950, -300, 960), (820, -330, 945), 11)])
    add("Stem and swept handlebar", _comp([stem, bars]), C_CHROME, "metal", None, "shell", (0, 0, 0))
    grips = []
    for s in (-1, 1):
        a, b = (882, s * 322.6, 951.3), (815, s * 331.2, 944.4)
        gr = _rod(a, b, 15.0) + Pos(*b) * Sphere(15.5)
        for k in range(6):                      # grip ribs
            q = _along(a, b, 0.12 + 0.13 * k)
            gr += Location(Plane(origin=q, z_dir=(Vector(*b) - Vector(*a)).normalized())) * Torus(15.0, 1.2)
        grips.append(gr)
    add("Handlebar grips", _comp(grips), C_BLACK, "rubber", None, "shell", (0, 0, 0))
    levers = []
    for s in (-1, 1):
        levers.append(_rod((905, s * 311, 948), (905, s * 311, 930), 5) + Pos(905, s * 311, 930) * Sphere(6))
        levers.append(_rod((905, s * 311, 930), (835, s * 327, 921), 4.5) + Pos(835, s * 327, 921) * Sphere(5))
    add("Brake levers", _comp(levers), C_CHROME, "metal", None, "shell", (0, 0, 0))

    # drivetrain: cranks set to the rider's pedal positions (cranks rotate), chainring, chain, pedals
    bbv = (bb[0], bb[1])
    crk = [_rod((bbv[0], -75, bbv[1]), (bbv[0], -75, bbv[1] - 170), 9), _rod((bbv[0], 75, bbv[1]), (bbv[0], 75, bbv[1] + 170), 9),
           _ycyl(bbv[0], 0, bbv[1], 10, 150)]
    for s, dz in ((-1, -170), (1, 170)):
        crk.append(_rod((bbv[0], s * 75, bbv[1] + dz), (bbv[0], s * 150, bbv[1] + dz), 5))
    add("Cranks and pedal spindles", _comp(crk), C_CHROME, "metal", None, "shell", (0, 0, 0))
    ring = _ring_y(bbv[0], 45, bbv[1], 100, 80, 4)
    for k in range(5):
        a = math.radians(90 + 72 * k)
        ring += _rod((bbv[0], 45, bbv[1]), (bbv[0] + 84 * math.cos(a), 45, bbv[1] + 84 * math.sin(a)), 7)
    ring += _ring_y(rear[0], 45, rear[1], 35, 14, 4)
    add("Chainring and rear sprocket", ring, C_CHROME, "metal", None, "shell", (0, 0, 0))
    c1, c2 = Vector(bbv[0], 0, bbv[1]), Vector(rear[0], 0, rear[1])
    R1, R2 = 103.0, 38.0
    dv = c2 - c1
    L = dv.length
    du = dv.normalized()
    dp = Vector(-du.Z, 0, du.X)
    cb = (R1 - R2) / L
    sb = math.sqrt(1 - cb * cb)
    chain = [_ring_y(c1.X, 45, c1.Z, R1 + 3, R1 - 3, 6), _ring_y(c2.X, 45, c2.Z, R2 + 3, R2 - 3, 6)]
    for sgn in (-1, 1):
        n = du * cb + dp * (sgn * sb)
        p1, p2 = c1 + n * R1, c2 + n * R2
        chain.append(_rod((p1.X, 45, p1.Z), (p2.X, 45, p2.Z), 3.2))
    add("Chain", _comp(chain), "#4B5058", "metal", None, "shell", (0, 0, 0))
    peds = []
    for s, dz in ((-1, -170), (1, 170)):
        pb = _box(bbv[0], s * 128, bbv[1] + dz, 90, 80, 24)
        pb = _fillet_try(pb, _edges_par(pb, Axis.Y), [6.0, 4.0])
        for k in range(4):
            pb -= _box(bbv[0] - 33 + 22 * k, s * 128, bbv[1] + dz + 12, 8, 70, 4)
        peds.append(pb)
    add("Rubber block pedals", _comp(peds), C_BLACK, "rubber", None, "shell", (0, 0, 0))

    # rear wheel and hub
    tyre_r, rim_r, valve_r, spokes_r = _wheel(rear[0], rear[1], R, 32, 30, 36)
    add("Rear tyre", tyre_r, C_TYRE, "rubber", None, "shell", (0, 0, 0))
    add("Rear rim and valve", _comp([rim_r, valve_r]), C_RIM, "metal", None, "shell", (0, 0, 0))
    add("Rear spokes", spokes_r, C_SPOKE, "metal", None, "shell", (0, 0, 0))
    rhub = _ycyl(rear[0], 0, rear[1], 18, 90) + _ring_y(rear[0], 30, rear[1], 34, 17, 4) \
        + _ring_y(rear[0], -30, rear[1], 34, 17, 4) + _ycyl(rear[0], 0, rear[1], 6, 140)
    rhub += _hex_y(rear[0], 56, rear[1], 15, 8) + _hex_y(rear[0], -56, rear[1], 15, 8)
    add("Rear hub and axle nuts", rhub, C_CHROME, "metal", None, "shell", (0, 0, 0))

    # ============================================================ item 1: hub motor wheel (front)
    EW = (170, -430, 0)
    fx, fz = front
    tyre_f, rim_f, valve_f, spokes_f = _wheel(fx, fz, R, 78, 27, 22)
    add("Front tyre (donor, reused)", tyre_f, C_TYRE, "rubber", 1, "internal", EW)
    add("Front rim, 28 in steel, and valve", _comp([rim_f, valve_f]), C_RIM, "metal", 1, "internal", EW)
    add("Front spokes, 13G", spokes_f, C_SPOKE, "metal", 1, "internal", EW)
    mw = P["motor_w"] - 20
    shell = Pos(fx, 0, fz) * Rot(90, 0, 0) * Cylinder(P["motor_d"] / 2, mw)
    shell = _fillet_try(shell, shell.edges(), [7.0, 5.0, 3.0])
    for k in range(24):                      # cooling ribs on the drum
        a = math.radians(k * 15)
        shell -= Pos(fx + 75 * math.cos(a), 0, fz + 75 * math.sin(a)) * Rot(90, 0, 0) * Cylinder(1.6, mw - 26)
    add("Hub motor shell, 250 W geared", shell, C_MOTOR, "metal", 1, "internal", EW)
    fl = _ring_y(fx, 27, fz, 81, 60, 3) + _ring_y(fx, -27, fz, 81, 60, 3)
    for sgn in (-1, 1):
        for k in range(18):
            a = math.radians(5 + k * 20 + (10 if sgn > 0 else 0))
            fl -= _ycyl(fx + 78 * math.cos(a), sgn * 27, fz + 78 * math.sin(a), 1.4, 6)
    add("Hub motor spoke flanges", fl, C_MOTOR, "metal", 1, "internal", EW)
    covers = []
    for sgn in (-1, 1):
        c = _ycyl(fx, sgn * (mw / 2 + 1.0), fz, 60, 2.0)
        c = _fillet_try(c, c.edges(), [0.8, 0.4])
        c += _ycyl(fx, sgn * (mw / 2 + 5), fz, 22, 8)
        covers.append(c)
    add("Hub motor side covers", _comp(covers), C_COVER, "painted", 1, "internal", EW)
    band = _ring_y(fx, 0, fz, 75.8, 73, 10)
    add("Hub motor accent band", band, C_ACCENT, "painted", 1, "internal", EW)
    scr = []
    for sgn in (-1, 1):
        for k in range(6):
            a = math.radians(30 + 60 * k)
            s = _ycyl(fx + 48 * math.cos(a), sgn * (mw / 2 + 2.6), fz + 48 * math.sin(a), 3.2, 1.4)
            scr.append(s)
    add("Hub motor cover screws", _comp(scr), C_CHROME, "metal", 1, "internal", EW)
    lab = _box(fx, -(mw / 2 + 2.3), fz - 36, 40, 0.6, 10)
    add("Hub motor rating label", lab, C_LABEL, "paper", 1, "internal", EW)
    axle = _ycyl(fx, 0, fz, P["axle_flats"] / 2 + 1, P["fork_spacing"] + 30)
    axle -= _box(fx, 0, fz + 6.5, 20, 200, 2) + _box(fx, 0, fz - 6.5, 20, 200, 2)
    nuts = [_hex_y(fx, s * 72, fz, 15, 7) for s in (-1, 1)] + [_ring_y(fx, s * 67.5, fz, 10, 6, 2) for s in (-1, 1)]
    add("Motor axle, 10 mm flats", axle, C_CHROME, "metal", 1, "internal", EW)
    add("Axle nuts and washers", _comp(nuts), C_CHROME, "metal", 14, "internal", (170, -520, 0))
    mcab = _pipe([(fx, -36, fz - 2), (fx - 4, -48, fz + 14), (fx - 10, -60, fz + 40)], 4.0)
    mcab += _ycyl(fx, -34, fz - 2, 7, 6)
    add("Motor cable exit", mcab, C_CABLE, "rubber", 1, "internal", EW)

    # ============================================================ item 2: torque arms
    fdv = (hb[0] - front[0], hb[1] - front[1])
    fln = math.hypot(*fdv)
    end = (front[0] + fdv[0] / fln * P["arm_len"], front[1] + fdv[1] / fln * P["arm_len"])
    fang = math.degrees(math.atan2(fdv[1], fdv[0]))
    arms, clamps = [], []
    for s in (-1, 1):
        y = s * (fy + P["fork_blade_r"] + P["arm_t"] / 2 + 1)
        mid = _along(front, end, 0.5)
        pl = Pos(mid[0], y, mid[1]) * Rot(0, -fang, 0) * Box(P["arm_len"], P["arm_t"], P["arm_w"])
        pl += _ycyl(front[0], y, front[1], P["arm_w"] / 2, P["arm_t"]) + _ycyl(end[0], y, end[1], P["arm_w"] / 2, P["arm_t"])
        pl -= _ycyl(end[0], y, end[1], 3.5, 10)
        arms.append(pl)
        cl = Pos(end[0], s * fy, end[1]) * Rot(0, -fang, 0) * Rot(0, 90, 0) * (
            Cylinder(P["fork_blade_r"] + 2.5, 14) - Cylinder(P["fork_blade_r"], 16))
        cl += _ycyl(end[0], y + s * 1, end[1], 7, 3)
        clamps.append(cl)
        clamps.append(_ycyl(end[0], y + s * 6, end[1], 4.5, 4) + _hex_y(end[0], y - s * 7, end[1], 8, 4))
    add("Torque arms (pair)", _comp(arms), C_ZINC, "metal", 2, "internal", (200, -600, 90))
    add("Torque arm band clips and bolts", _comp(clamps), C_CHROME, "metal", 2, "internal", (200, -600, 90))

    # ============================================================ items 4 and 6: cradle and SwapCell pack
    loc = cradle_location(P)
    Lp, Wp, Dp = P["pack_l"], P["pack_w"], P["pack_d"]
    r, bt, rh = P["dt_r"], P["base_t"], P["rail_h"]
    zb = r + bt
    EC = (0, -300, 170)
    base = Pos(0, 0, r + bt / 2) * Box(Lp + 60, Wp + 14, bt)
    base = _fillet_try(base, _edges_par(base, Axis.Z), [8.0, 5.0])
    base += Pos(0, 0, r - 2) * Box(Lp + 40, 30, 8)
    for sgn in (-1, 1):
        base += Pos(0, sgn * (Wp / 2 - P["rail_w"] / 2), zb + rh / 2) * Box(Lp, P["rail_w"], rh)
    gy = Wp / 2 + P["guide_clear"] + P["guide_t"] / 2
    gx = -Lp / 2 + P["guide_len"] / 2
    for sgn in (-1, 1):
        gd = Pos(gx, sgn * gy, zb + P["guide_h"] / 2) * Box(P["guide_len"], P["guide_t"], P["guide_h"])
        gd = _fillet_try(gd, gd.faces().sort_by(Axis.Z)[-1].edges(), [2.5, 1.5])
        base += gd
    sx = -Lp / 2 - P["stop_len"] / 2
    stop = Pos(sx, 0, zb + 45) * Box(P["stop_len"], Wp + 14, 90)
    stop = _fillet_try(stop, stop.faces().sort_by(Axis.Z)[-1].edges(), [5.0, 3.0])
    zc = zb + rh + Dp / 2 - P["plug_offset"]
    stop -= Pos(-Lp / 2 - P["plug_h"] / 2 + 0.5, 0, zc) * Box(P["plug_h"] + 1, P["plug_w"] + 4, P["plug_d"] + 4)
    base += stop
    base += Pos(Lp / 2 - P["latch_from_top"] + 20, 0, zb + 3) * Box(10, 50, 6)
    base += Pos(Lp / 2 + 20, 0, zb + 12) * Box(20, 60, 24)
    add("SwapCell receiver cradle (folded steel)", loc * base, C_CRADLE, "painted", 4, "shell", EC)
    rec = receptacle_local(P)
    add("Cradle receptacle, 10 kOhm coding", loc * rec, C_BLACK, "plastic", 4, "shell", EC)
    # V1 preload lever: pad, arm and grip (accent)
    lev = Pos(Lp / 2 + 4, 0, zb + rh + 9) * Box(8, 60, 18)
    arm = Pos(Lp / 2 + 30 + P["lever_len"] / 2, 0, zb + 18) * Box(P["lever_len"], 20, 8)
    arm = _fillet_try(arm, _edges_par(arm, Axis.Z), [3.5, 2.0])
    lev += arm
    add("V1 preload lever", loc * lev, C_ACCENT, "painted", 4, "shell", EC)
    lgrip = Pos(Lp / 2 + 30 + P["lever_len"] - 18, 0, zb + 18) * Box(36, 24, 12)
    lgrip = _fillet_try(lgrip, lgrip.edges(), [4.0, 2.0])
    add("Lever grip", loc * lgrip, C_BLACK, "rubber", 4, "shell", EC)
    pin = Pos(Lp / 2 + 20, 0, zb + 12) * Rot(90, 0, 0) * Cylinder(4, 70)
    add("Lever pivot pin", loc * pin, C_CHROME, "metal", 4, "shell", EC)
    bands, liners, bscr = [], [], []
    for sgn in (-1, 1):
        x = sgn * P["band_pitch"] / 2
        bands.append(Pos(x, 0, 0) * Rot(0, 90, 0) * (Cylinder(r + 5, P["band_w"]) - Cylinder(r + 1.5, P["band_w"] + 2)))
        liners.append(Pos(x, 0, 0) * Rot(0, 90, 0) * (Cylinder(r + 1.5, P["band_w"] + 3) - Cylinder(r, P["band_w"] + 5)))
        lug = Pos(x, 0, -r - 7) * Box(P["band_w"], 16, 8)
        bscr.append(lug + Pos(x, 0, -r - 7) * Rot(90, 0, 0) * Cylinder(3, 26)
                    + Pos(x, -15, -r - 7) * Rot(90, 0, 0) * Cylinder(5, 4))
    add("Stainless band clamps", loc * _comp(bands), C_CHROME, "metal", 4, "shell", EC)
    add("Band clamp rubber liners", loc * _comp(liners), C_BLACK, "rubber", 4, "shell", EC)
    add("Band clamp screws", loc * _comp(bscr), C_CHROME, "metal", 14, "shell", (0, -330, 120))

    # pack: light body between dark end caps, handle, charge gauge, label, accent stripe
    EPk = (0, -560, 420)
    z0 = zb + rh
    pz = z0 + Dp / 2
    cap_l = 34.0
    body = Pos(0, 0, pz) * Box(Lp - 2 * cap_l, Wp, Dp)
    body = _fillet_try(body, _edges_par(body, Axis.X), [10.0, 7.0, 4.0])
    add("SwapCell pack body", loc * body, C_PACK, "plastic", 6, "shell", EPk)
    caps = []
    for sgn in (-1, 1):
        c = Pos(sgn * (Lp / 2 - cap_l / 2 + 0.5), 0, pz) * Box(cap_l - 1, Wp, Dp)
        c = _fillet_try(c, _edges_par(c, Axis.X), [10.0, 7.0, 4.0])
        c = _fillet_try(c, c.faces().sort_by(Axis.X)[-1 if sgn > 0 else 0].edges(), [5.0, 3.0, 1.5])
        caps.append(c)
    add("SwapCell pack end caps", loc * _comp(caps), C_PACK_END, "plastic", 6, "shell", EPk)
    zp = pz - P["plug_offset"]
    plug = Pos(-Lp / 2 - P["plug_h"] / 2, 0, zp) * Box(P["plug_h"], P["plug_w"], P["plug_d"])
    pawl = Pos(Lp / 2 - P["latch_from_top"], 0, z0 - P["latch_proud"] / 2) * Box(P["latch_h"], P["latch_w"], P["latch_proud"])
    add("SwapCell plug and latch pawl", loc * _comp([plug, pawl]), C_BLACK, "plastic", 6, "shell", EPk)
    hdl = Pos(Lp / 2 + P["handle_h"] / 2, 0, zp) * (
        Box(P["handle_h"], P["handle_w"], P["handle_d"]) - Pos(-5, 0, 0) * Box(26, P["handle_w"] - 22, P["handle_d"] + 2))
    hdl = _fillet_try(hdl, _edges_par(hdl, Axis.Z), [4.0, 2.5, 1.5])
    add("SwapCell carry handle", loc * hdl, C_BLACK, "rubber", 6, "shell", EPk)
    stripe = Pos(0, -Wp / 2 - 0.2, pz + 20) * Box(Lp - 2 * cap_l - 20, 0.4, 6)
    add("SwapCell accent stripe", loc * stripe, C_ACCENT, "painted", 6, "shell", EPk)
    plab = Pos(-30, -Wp / 2 - 0.2, pz - 6) * Box(120, 0.4, 34)
    add("SwapCell pack label", loc * plab, C_LABEL, "paper", 6, "shell", EPk)
    ink = (Pos(-65, -Wp / 2 - 0.45, pz + 2) * Box(40, 0.3, 10) + Pos(-10, -Wp / 2 - 0.45, pz + 4) * Box(56, 0.3, 3)
           + Pos(-10, -Wp / 2 - 0.45, pz - 4) * Box(56, 0.3, 2) + Pos(-30, -Wp / 2 - 0.45, pz - 16) * Box(104, 0.3, 2))
    add("SwapCell label print", loc * ink, C_DARK, "paper", 6, "shell", EPk)
    zt = z0 + Dp                                             # top face (into the triangle)
    gauge = Pos(Lp / 2 - cap_l - 40, 0, zt + 0.8) * Box(46, 14, 1.6)
    gauge = _fillet_try(gauge, _edges_par(gauge, Axis.Z), [2.0, 1.0])
    add("Charge gauge window", loc * gauge, C_BLACK, "screen", 6, "shell", EPk)
    for k in range(4):
        seg = Pos(Lp / 2 - cap_l - 55 + 10 * k, 0, zt + 1.8) * Box(7, 8, 0.6)
        lit = k < 3
        add(f"Charge gauge segment {k + 1}" + (" (lit)" if lit else ""), loc * seg,
            C_LED_G if lit else C_LED_OFF, "emissive" if lit else "plastic", 6, "shell", EPk)

    # ============================================================ item 5: host adapter with charge inlet
    ax_, ay_, az_ = P["adapter"]
    axl = -Lp / 2 - P["stop_len"] - 10 - ax_ / 2
    EA = (80, -450, -220)
    ad = Pos(axl, 0, r + az_ / 2) * Box(ax_, ay_, az_)
    ad = _fillet_try(ad, _edges_par(ad, Axis.Y), [6.0, 4.0, 2.0])
    ad = _fillet_try(ad, ad.faces().sort_by(Axis.Z)[-1].edges(), [2.0, 1.0])
    ad -= Pos(axl, 0, r + az_ - 8) * (Box(ax_ + 2, ay_ + 2, 0.8) - Box(ax_ - 1.2, ay_ - 1.2, 2))
    add("Host adapter, potted", loc * ad, C_DARK, "plastic", 5, "shell", EA)
    inlet = Pos(axl, -ay_ / 2 - 3, r + az_ / 2) * Rot(90, 0, 0) * Cylinder(12, 6)
    inlet -= Pos(axl, -ay_ / 2 - 6, r + az_ / 2) * Rot(90, 0, 0) * Cylinder(8, 2)
    add("Charge inlet, keyed", loc * inlet, C_ACCENT, "plastic", 5, "shell", EA)
    ledA = Pos(axl + 16, 0, r + az_ + 0.6) * Sphere(2.6) & Pos(axl + 16, 0, r + az_ + 1) * Box(6, 6, 2)
    add("Adapter status light (lit)", loc * ledA, C_LED_T, "emissive", 5, "shell", EA)
    alab = Pos(axl - 4, 0, r + az_ + 0.2) * Box(26, 40, 0.4)
    add("Adapter label", loc * alab, C_LABEL, "paper", 5, "shell", EA)

    # ============================================================ item 3: controller on the seat tube
    sa = _along(bb, st, 0.38)
    st_ang = math.degrees(math.atan2(st[1] - bb[1], st[0] - bb[0]))
    cx, cy, cz = P["controller"]
    cl = Pos(sa[0] + 42, 0, sa[1]) * Rot(0, -st_ang, 0)
    EK = (-250, -380, -40)
    cbody = Box(cx - 24, cy, cz)
    cbody = _fillet_try(cbody, _edges_par(cbody, Axis.X), [5.0, 3.0])
    for k in range(5):                                        # fins on the face away from the tube
        cbody -= Pos(0, -20 + 10 * k, -cz / 2) * Box(cx - 40, 3.2, 8)
    add("Controller case, finned aluminium", cl * cbody, C_ALU, "metal", 3, "shell", EK)
    ends = []
    for sgn in (-1, 1):
        e = Pos(sgn * (cx / 2 - 6.5), 0, 0) * Box(13, cy + 2, cz + 2)
        e = _fillet_try(e, _edges_par(e, Axis.X), [6.0, 4.0])
        ends.append(e)
    add("Controller end caps, sealed", cl * _comp(ends), C_BLACK, "plastic", 3, "shell", EK)
    glands = []
    for dy in (-16, 0, 16):
        glands.append(Pos(-cx / 2 - 5, dy, 0) * Rot(0, 90, 0) * Cylinder(5.5, 10))
    add("Controller cable glands", cl * _comp(glands), C_DARK, "plastic", 3, "shell", EK)
    clab = Pos(10, -cy / 2 - 0.2, 4) * Box(60, 0.4, 14)
    add("Controller name plate", cl * clab, C_ACCENT, "painted", 3, "shell", EK)
    straps = []
    nrm = Vector(sd.Z, 0, -sd.X)                               # from the seat tube toward the controller
    for dx in (-40, 40):
        pcen = Vector(sa[0], 0, sa[1]) + sd * dx
        straps.append(Location(Plane(origin=pcen, z_dir=sd)) * (Cylinder(tr + 2.5, 14) - Cylinder(tr, 16)))
        straps.append(Location(Plane(origin=pcen + nrm * 22, x_dir=nrm, z_dir=sd)) * Box(16, 14, 14))
    add("Controller straps", _comp(straps), C_BLACK, "rubber", 3, "shell", EK)

    # ============================================================ item 7: pedal-assist sensor
    EPs = (0, -260, -120)
    disc = _ring_y(bb[0], -58, bb[1], 38, 18, 6)
    add("Pedal-assist magnet disc", disc, C_BLACK, "plastic", 7, "shell", EPs)
    mags = [_ycyl(bb[0] + 31 * math.cos(math.radians(30 * k)), -61.8, bb[1] + 31 * math.sin(math.radians(30 * k)), 3.6, 2)
            for k in range(12)]
    add("Pedal-assist magnets", _comp(mags), C_CHROME, "metal", 7, "shell", EPs)
    hall = _box(bb[0] - 30, -58, bb[1] + 44, 18, 12, 14)
    hall = _fillet_try(hall, hall.edges(), [2.0, 1.0])
    hall += _box(bb[0] - 30, -52, bb[1] + 58, 10, 4, 20)
    add("Pedal-assist Hall sensor", hall, C_DARK, "plastic", 7, "shell", EPs)

    # ============================================================ item 8: handlebar display, walk button, brake sensors
    EH = (120, -160, 260)
    disp = _box(950, -120, 982, 55, 45, 22)
    disp = _fillet_try(disp, _edges_par(disp, Axis.Z), [8.0, 5.0])
    disp = _fillet_try(disp, disp.faces().sort_by(Axis.Z)[-1].edges(), [3.0, 2.0])
    disp += _ycyl(950, -120, 960, 14, 22)
    add("Handlebar display unit", disp, C_DARK, "plastic", 8, "shell", EH)
    win = _box(944, -120, 993.3, 34, 34, 0.6)
    add("Display window", win, C_BLACK, "screen", 8, "shell", EH)
    for k in range(5):
        lit = k < 3
        seg = _box(935 + 7.5 * k, -113, 993.8, 5, 12, 0.5)
        add(f"Assist level segment {k + 1}" + (" (lit)" if lit else ""), seg,
            C_LED_T if lit else C_LED_OFF, "emissive" if lit else "plastic", 8, "shell", EH)
    batt = _box(944, -130, 993.8, 30, 5, 0.5)
    add("Pack charge bar (lit)", batt, C_LED_G, "emissive", 8, "shell", EH)
    pbtn = _box(970, -120, 993.5, 7, 16, 3)
    pbtn = _fillet_try(pbtn, pbtn.edges(), [1.2, 0.6])
    add("Power switch (INTERLOCK loop)", pbtn, C_ACCENT, "rubber", 8, "shell", EH)
    walk = _ycyl(950, -262, 972, 9, 12) + _ycyl(950, -262, 960, 13, 18)
    add("Walk-assist button pod", walk, C_DARK, "plastic", 8, "shell", EH)
    wcap = _ycyl(950, -262, 978, 6, 4) & _box(950, -262, 981, 14, 14, 6)
    add("Walk-assist button", wcap, C_ACCENT, "rubber", 8, "shell", EH)
    bsens = []
    for s in (-1, 1):
        b = _box(905, s * 311, 918, 30, 20, 18)
        b = _fillet_try(b, b.edges(), [3.0, 1.5])
        bsens.append(b)
    add("Brake cut-off sensors", _comp(bsens), C_DARK, "plastic", 8, "shell", (80, -120, 160))

    # ============================================================ item 9: harness with fuse
    EHn = (0, -220, -300)
    w_lo = (sa[0] + 80, -30, sa[1] - 60)
    w_bb = (bb[0] + 60, -30, bb[1] + 60)
    w_hd = (hb[0] - 20, -30, hb[1] - 10)
    w_ax = (front[0] - 10, -60, front[1] + 40)
    w_up = (ht[0] - 10, -30, ht[1] + 60)
    harness = _pipe([w_lo, w_bb, w_hd, w_ax], 5) + _pipe([w_hd, w_up, (950, -120, 960)], 5)
    add("Wiring harness, spiral wrapped", harness, C_CABLE, "rubber", 9, "shell", EHn)
    ties = []
    for a, b, t in ((w_bb, w_hd, 0.25), (w_bb, w_hd, 0.55), (w_bb, w_hd, 0.85), (w_hd, w_ax, 0.4), (w_hd, w_ax, 0.8),
                    (w_hd, w_up, 0.5)):
        q = Vector(*_along(a, b, t))
        d = (Vector(*b) - Vector(*a)).normalized()
        ties.append(Location(Plane(origin=q, z_dir=d)) * Torus(6.5, 1.3))
    add("Cable ties", _comp(ties), C_BLACK, "plastic", 14, "shell", EHn)
    fq = Vector(*_along(w_bb, w_hd, 0.4))
    fz_ = Location(Plane(origin=fq + Vector(0, -14, 0), z_dir=(Vector(*w_hd) - Vector(*w_bb)).normalized()))
    fbase = fz_ * Box(22, 12, 44)
    fbase = _fillet_try(fbase, fbase.edges(), [2.5, 1.5])
    add("Fuse holder, sealed", fbase, C_DARK, "plastic", 9, "shell", EHn)
    fcov = fz_ * Pos(0, -7, 0) * Box(18, 3, 36)
    fcov = _fillet_try(fcov, fcov.edges(), [1.2, 0.6])
    add("Fuse holder clear cover", fcov, C_GLASS, "clear", 9, "shell", EHn)
    fuse = fz_ * Pos(0, -4.6, 0) * Box(12, 1.2, 18)
    add("Blade fuse, 20 A", fuse, "#EAB308", "plastic", 9, "shell", EHn)

    # ============================================================ items 10 to 13: solar set
    PX, TILT = P["panel_x"], P["panel_tilt"]
    pw, pd, pt = P["panel"]
    ES = (0, 0, 330)
    ploc = Pos(PX, 0, 620) * Rot(0, TILT, 0)
    frm = Box(pw, pd, pt) - Pos(0, 0, 4) * Box(pw - 24, pd - 24, pt)
    frm = _fillet_try(frm, _edges_par(frm, Axis.Z), [3.0, 1.5])
    add("Solar panel frame, anodised aluminium", ploc * frm, C_CHROME, "metal", 10, "accessory", ES)
    back = Pos(0, 0, pt / 2 - 5) * Box(pw - 24, pd - 24, 2)
    add("Solar panel backsheet", ploc * back, C_BACKSHEET, "plastic", 10, "accessory", ES)
    cells, bus = [], []
    cw_, gap = 150.0, 6.0
    for i in range(4):
        for j in range(6):
            x = -1.5 * (cw_ + gap) + i * (cw_ + gap)
            y = -2.5 * (cw_ + gap) + j * (cw_ + gap)
            c = Pos(x, y, pt / 2 - 3.6) * Box(cw_, cw_, 0.8)
            c = _fillet_try(c, _edges_par(c, Axis.Z), [8.0, 4.0])
            cells.append(c)
        for b in (-50, 0, 50):
            bus.append(Pos(-1.5 * (cw_ + gap) + i * (cw_ + gap) + b, 0, pt / 2 - 3.05) * Box(1.6, 6 * cw_ + 5 * gap, 0.3))
    add("Solar cells, monocrystalline", ploc * Compound(cells), C_CELL, "screen", 10, "accessory", ES)
    add("Cell busbars", ploc * Compound(bus), "#C9CED6", "metal", 10, "accessory", ES)
    jb = Pos(-200, 0, -pt / 2 - 10) * Box(80, 100, 20)
    jb = _fillet_try(jb, jb.edges(), [3.0, 1.5])
    add("Panel junction box", ploc * jb, C_BLACK, "plastic", 10, "accessory", ES)

    stand = []
    for dx, zt_ in ((-300, 700), (300, 540)):
        for dy in (-440, 440):
            stand.append(_beam((PX + dx, dy, 0), (PX + dx * 0.95, dy, zt_), 36, 36))
    for dy in (-440, 440):
        stand.append(_beam((PX - 300, dy, 150), (PX + 300, dy, 150), 28, 24))
    stand.append(_beam((PX - 300, -440, 420), (PX - 300, 440, 420), 28, 24))
    stand.append(_beam((PX + 20, -452, 150), (PX + 20, -452, 400), 40, 8))
    add("Panel stand, timber A-frame", _comp(stand), C_TIMBER, "wood", 12, "accessory", (0, 0, 0))
    bolts = []
    for dx in (-300, 300):
        for dy in (-440, 440):
            bolts.append(Pos(PX + dx, dy - math.copysign(19, dy), 150) * Rot(90, 0, 0) * Cylinder(6, 4))
    add("Stand coach bolts", _comp(bolts), C_CHROME, "metal", 14, "accessory", (0, 0, 0))

    chx, chy, chz = PX + 20, -500, 360
    chb = _box(chx, chy, chz, 120, 70, 45)
    chb = _fillet_try(chb, _edges_par(chb, Axis.Y), [5.0, 3.0])
    for k in range(6):
        chb -= _box(chx - 37.5 + 15 * k, chy - 35, chz, 5, 6, 35)
    add("Boost MPPT charger case", chb, C_ALU, "metal", 11, "accessory", (0, -260, 60))
    che = []
    for sgn in (-1, 1):
        e = _box(chx + sgn * 64, chy, chz, 10, 72, 47)
        e = _fillet_try(e, _edges_par(e, Axis.X), [4.0, 2.0])
        che.append(e)
    add("Charger end caps", _comp(che), C_BLACK, "plastic", 11, "accessory", (0, -260, 60))
    led = Pos(chx + 40, chy - 36, chz + 16) * Sphere(3.2) & _box(chx + 40, chy - 37, chz + 16, 8, 4, 8)
    add("Charger charge light (lit)", led, C_LED_G, "emissive", 11, "accessory", (0, -260, 60))
    chl = _box(chx - 10, chy - 35.3, chz - 12, 60, 0.6, 12)
    add("Charger label", chl, C_ACCENT, "painted", 11, "accessory", (0, -260, 60))

    # panel lead (part of the panel) and the 5 m charge cable to the charge inlet
    jbw = (ploc * Pos(-200, 40, -pt / 2 - 20)).position
    lead = _pipe([(jbw.X, jbw.Y, jbw.Z), (jbw.X, -380, jbw.Z - 20), (chx + 69, -470, chz + 10)], 3.5)
    add("Panel lead", lead, C_CABLE, "rubber", 10, "accessory", ES)
    a_in = (loc * Pos(axl, -ay_ / 2 - 6, r + az_ / 2)).position
    a_out = (loc * Pos(axl, -ay_ / 2 - 40, r + az_ / 2)).position
    cab = _pipe([(chx - 69, chy + 10, chz - 10), (chx - 110, chy + 30, chz - 60), (PX - 300, -330, 20),
                 (PX - 700, -260, 6), (a_in.X + 40, -150, 6), (a_out.X, a_out.Y, a_out.Z - 60), (a_out.X, a_out.Y, a_out.Z)], 4.0)
    add("Charge cable, 5 m", cab, C_CABLE, "rubber", 13, "accessory", (0, -120, 0))
    cplug = _ycyl(a_in.X, (a_in.Y + a_out.Y) / 2, a_in.Z, 10.5, abs(a_out.Y - a_in.Y))
    cplug = _fillet_try(cplug, cplug.edges(), [2.0, 1.0])
    add("Charge plug, keyed", cplug, C_BLACK, "rubber", 13, "accessory", (0, -120, 0))

    # ============================================================ context: rider (clay)
    try:
        from context_parts import mannequin, mannequin_landmarks
        lm = mannequin_landmarks(RIDER_H, "ride", **RIDER_POSE)
        bx, by, bz = lm["bb"]
        # mannequin faces -Y; turn it to face +X (the bike's forward), then put its bottom bracket on ours
        rider = Pos(bb[0] + by, 0 - bx, bb[1] - bz) * Rot(0, 0, 90) * mannequin(RIDER_H, "ride", **RIDER_POSE)
        add("Rider, 1.75 m (clay mannequin)", rider, C_CLAY, "clay", None, "context", (0, 0, 0))
    except ImportError:
        pass
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:42s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:9.2f} cm3")
