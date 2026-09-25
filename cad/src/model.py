"""SunSpoke parametric model (build123d), TRL 3.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl, and prints the fit checks
quoted in SSP-CAL-001 (pack clearance in the main triangle, extraction travel).

Massing-plus detail: correct interfaces (SwapCell interface v0.3 envelope, cradle,
latch class V1 lever, fork and torque arms, 28 in wheel) and main dimensions; not
fabrication detail. The donor roadster is a context model.

Axes: the bicycle lies in the XZ plane (X forward, Z up, Y across the bike), rear
axle at X = 0, ground at Z = 0. Dimensions in mm.
"""
import math
from pathlib import Path

from build123d import (Box, Compound, Cylinder, Location, Plane, Pos, Rot, Solid, Torus, Vector,
                       export_step, export_stl)

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # Donor roadster, 28 in (ETRTO 635)
    "wheel_r": 355.0, "wheelbase": 1150.0,
    "bb_x": 430.0, "bb_z": 290.0,
    "seat_top_x": 225.0, "seat_top_z": 815.0,
    "head_bot_x": 1030.0, "head_bot_z": 690.0,
    "head_top_x": 975.0, "head_top_z": 840.0,
    "tube_r": 14.3,           # 28.6 mm top and seat tubes
    "dt_r": 16.0,             # down tube radius (R5 range 28 to 32 mm diameter)
    "fork_spacing": 100.0,    # front dropout spacing (R5)
    "fork_blade_r": 11.0,
    # Motor (item 1)
    "motor_d": 150.0, "motor_w": 80.0, "axle_flats": 10.0,
    # Torque arms (item 2)
    "arm_len": 130.0, "arm_w": 20.0, "arm_t": 5.0,
    # SwapCell envelope (interface v0.3)
    "pack_l": 340.0, "pack_w": 90.0, "pack_d": 80.0,
    "plug_w": 56.0, "plug_d": 34.0, "plug_h": 18.0, "plug_offset": 8.0,
    "handle_w": 84.0, "handle_d": 22.0, "handle_h": 35.0,
    "latch_w": 36.0, "latch_from_top": 45.0, "latch_proud": 10.0, "latch_h": 24.0,
    # Cradle (item 4)
    "pack_pos": 0.48,         # pack centre along the down tube, fraction from the bottom bracket
    "base_t": 4.0, "rail_h": 12.0, "rail_w": 10.0,
    "guide_len": 120.0, "guide_t": 6.0, "guide_h": 50.0, "guide_clear": 1.0,
    "stop_len": 30.0, "band_pitch": 220.0, "band_w": 22.0,
    "lever_len": 90.0,
    # Host adapter (item 5) and controller (item 3)
    "adapter": (50.0, 70.0, 35.0), "controller": (150.0, 62.0, 42.0),
    # Solar set (items 10 to 13)
    "panel": (670.0, 1000.0, 35.0), "panel_x": 2250.0, "panel_tilt": 15.0,
}


def _tube(p1, p2, r, y=0.0):
    a = Vector(p1[0], y, p1[1]); b = Vector(p2[0], y, p2[1]); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def _tube3(a, b, r):
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def _along(p1, p2, t):
    return (p1[0] + (p2[0] - p1[0]) * t, p1[1] + (p2[1] - p1[1]) * t)


def geometry(p=PARAMS):
    """Key points of the donor frame."""
    g = {"rear": (0.0, p["wheel_r"]), "front": (p["wheelbase"], p["wheel_r"]),
         "bb": (p["bb_x"], p["bb_z"]), "seat_top": (p["seat_top_x"], p["seat_top_z"]),
         "head_bot": (p["head_bot_x"], p["head_bot_z"]), "head_top": (p["head_top_x"], p["head_top_z"])}
    bb, hb = g["bb"], g["head_bot"]
    g["dt_ang"] = math.degrees(math.atan2(hb[1] - bb[1], hb[0] - bb[0]))
    g["dt_len"] = math.hypot(hb[0] - bb[0], hb[1] - bb[1])
    g["dt_mid"] = _along(bb, hb, p["pack_pos"])
    return g


def cradle_location(p=PARAMS):
    """Local frame of the cradle: x along the down tube (up), z away from the tube into the triangle."""
    g = geometry(p)
    m = g["dt_mid"]
    return Pos(m[0], 0, m[1]) * Rot(0, -g["dt_ang"], 0)


def wheel(cx, cz, r):
    tyre = Pos(cx, 0, cz) * Rot(90, 0, 0) * Torus(r - 20, 20)
    rim = Pos(cx, 0, cz) * Rot(90, 0, 0) * (Cylinder(r - 38, 20) - Cylinder(r - 52, 22))
    spokes = None
    for k in range(12):
        t = math.radians(k * 30)
        s = _tube3((cx, 0, cz), (cx + (r - 50) * math.cos(t), 0, cz + (r - 50) * math.sin(t)), 2.0)
        spokes = s if spokes is None else spokes + s
    return tyre + rim + spokes


def pack_local(p=PARAMS):
    """SwapCell pack in the cradle frame: back face (latch side) down on the rails, connector toward the BB."""
    L, W, D = p["pack_l"], p["pack_w"], p["pack_d"]
    z0 = p["dt_r"] + p["base_t"] + p["rail_h"]          # back face
    zc = z0 + D / 2
    body = Pos(0, 0, zc) * Box(L, W, D)
    zp = zc - p["plug_offset"]                          # plug offset toward the back face
    plug = Pos(-L / 2 - p["plug_h"] / 2, 0, zp) * Box(p["plug_h"], p["plug_w"], p["plug_d"])
    handle = Pos(L / 2 + p["handle_h"] / 2, 0, zp) * (
        Box(p["handle_h"], p["handle_w"], p["handle_d"]) - Pos(-5, 0, 0) * Box(26, p["handle_w"] - 22, p["handle_d"] + 2))
    pawl = Pos(L / 2 - p["latch_from_top"], 0, z0 - p["latch_proud"] / 2) * Box(p["latch_h"], p["latch_w"], p["latch_proud"])
    return body + plug + handle + pawl


def cradle_local(p=PARAMS):
    """Receiver cradle with band clamps, guides, end stop, receptacle, latch catch and V1 lever."""
    L, W = p["pack_l"], p["pack_w"]
    r, bt, rh = p["dt_r"], p["base_t"], p["rail_h"]
    zb = r + bt
    base = Pos(0, 0, r + bt / 2) * Box(L + 60, W + 14, bt) + Pos(0, 0, r - 2) * Box(L + 40, 30, 8)
    rails = None
    for s in (-1, 1):
        rl = Pos(0, s * (W / 2 - p["rail_w"] / 2), zb + rh / 2) * Box(L, p["rail_w"], rh)
        rails = rl if rails is None else rails + rl
    gy = W / 2 + p["guide_clear"] + p["guide_t"] / 2
    gx = -L / 2 + p["guide_len"] / 2
    guides = (Pos(gx, gy, zb + p["guide_h"] / 2) * Box(p["guide_len"], p["guide_t"], p["guide_h"])
              + Pos(gx, -gy, zb + p["guide_h"] / 2) * Box(p["guide_len"], p["guide_t"], p["guide_h"]))
    sx = -L / 2 - p["stop_len"] / 2
    stop = Pos(sx, 0, zb + 45) * Box(p["stop_len"], W + 14, 90)
    zc = zb + rh + p["pack_d"] / 2 - p["plug_offset"]
    stop -= Pos(-L / 2 - p["plug_h"] / 2 + 0.5, 0, zc) * Box(p["plug_h"] + 1, p["plug_w"] + 4, p["plug_d"] + 4)
    catch = Pos(L / 2 - p["latch_from_top"] + 20, 0, zb + 3) * Box(10, 50, 6)
    # Latch class V1: hinge block beyond the top end, pad bearing on the top end next to the back face
    lever = (Pos(L / 2 + 20, 0, zb + 12) * Box(20, 60, 24)
             + Pos(L / 2 + 4, 0, zb + rh + 9) * Box(8, 60, 18)
             + Pos(L / 2 + 30 + p["lever_len"] / 2, 0, zb + 18) * Box(p["lever_len"], 20, 8))
    bands = None
    for s in (-1, 1):
        b = Pos(s * p["band_pitch"] / 2, 0, 0) * Rot(0, 90, 0) * (Cylinder(r + 5, p["band_w"]) - Cylinder(r, p["band_w"] + 2))
        bands = b if bands is None else bands + b
    return base + rails + guides + stop + catch + lever + bands


def receptacle_local(p=PARAMS):
    L = p["pack_l"]
    zc = p["dt_r"] + p["base_t"] + p["rail_h"] + p["pack_d"] / 2 - p["plug_offset"]
    return Pos(-L / 2 - p["plug_h"] - 4, 0, zc) * Box(8, p["plug_w"] + 2, p["plug_d"] + 2)


def build_parts(p=PARAMS):
    """Return a list of (name, shape, colour, bom_item or None, explode_offset)."""
    g = geometry(p)
    R = p["wheel_r"]
    rear, front, bb, st, hb, ht = g["rear"], g["front"], g["bb"], g["seat_top"], g["head_bot"], g["head_top"]
    tr = p["tube_r"]
    fy = p["fork_spacing"] / 2

    # ---------------- donor bicycle (context, no BOM number)
    frame = (_tube(bb, st, tr) + _tube(st, ht, tr) + _tube(bb, hb, p["dt_r"]) + _tube(hb, ht, 18)
             + _tube(bb, rear, 9, 45) + _tube(bb, rear, 9, -45)
             + _tube(st, rear, 8, 45) + _tube(st, rear, 8, -45)
             + _tube((210, 850), (205, 900), 13))
    fork = (_tube(hb, front, p["fork_blade_r"], fy) + _tube(hb, front, p["fork_blade_r"], -fy)
            + Pos(hb[0], 0, hb[1]) * Box(40, p["fork_spacing"] + 10, 20))
    stem = _tube(ht, (950, 960), 12)
    bars = (_tube3((950, -300, 960), (950, 300, 960), 11)
            + _tube3((950, 300, 960), (820, 330, 945), 11) + _tube3((950, -300, 960), (820, -330, 945), 11))
    saddle = Pos(200, 0, 925) * Box(260, 150, 55)
    carrier = (Pos(-60, 0, 800) * Box(420, 170, 12)
               + _tube3((-230, 60, 795), (0, 60, R), 6) + _tube3((-230, -60, 795), (0, -60, R), 6))
    cranks = (_tube3((bb[0], -75, bb[1]), (bb[0] + 60, -75, bb[1] - 160), 9)
              + _tube3((bb[0], 75, bb[1]), (bb[0] - 60, 75, bb[1] + 160), 9)
              + Pos(bb[0], 45, bb[1]) * Rot(90, 0, 0) * Cylinder(100, 5))
    bike = frame + fork + stem + bars + saddle + carrier + cranks
    wheels = wheel(*rear, R) + wheel(*front, R)

    # ---------------- kit
    motor = (Pos(front[0], 0, front[1]) * Rot(90, 0, 0) * Cylinder(p["motor_d"] / 2, p["motor_w"] - 20)
             + Pos(front[0], 0, front[1]) * Rot(90, 0, 0) * Cylinder(p["axle_flats"] / 2 + 1, p["fork_spacing"] + 30))
    fd = (hb[0] - front[0], hb[1] - front[1]); fl = math.hypot(*fd)
    end = (front[0] + fd[0] / fl * p["arm_len"], front[1] + fd[1] / fl * p["arm_len"])
    fang = math.degrees(math.atan2(fd[1], fd[0]))
    arms = None
    for s in (-1, 1):
        y = s * (fy + p["fork_blade_r"] + p["arm_t"] / 2 + 1)
        mid = _along(front, end, 0.5)
        plate = Pos(mid[0], y, mid[1]) * Rot(0, -fang, 0) * Box(p["arm_len"] + 20, p["arm_t"], p["arm_w"])
        clip = Pos(end[0], s * fy, end[1]) * Rot(0, -fang, 0) * Rot(0, 90, 0) * (
            Cylinder(p["fork_blade_r"] + 3, 14) - Cylinder(p["fork_blade_r"], 16))
        arms = plate + clip if arms is None else arms + plate + clip

    loc = cradle_location(p)
    cradle = loc * cradle_local(p)
    receptacle = loc * receptacle_local(p)
    pack = loc * pack_local(p)
    ax, ay, az = p["adapter"]
    adapter = loc * Pos(-p["pack_l"] / 2 - p["stop_len"] - 10 - ax / 2, 0, p["dt_r"] + p["base_t"] + az / 2) * Box(ax, ay, az)

    sa = _along(bb, st, 0.38)
    st_ang = math.degrees(math.atan2(st[1] - bb[1], st[0] - bb[0]))
    cx, cy, cz = p["controller"]
    controller = Pos(sa[0] + 42, 0, sa[1]) * Rot(0, -st_ang, 0) * Box(cx, cy, cz)
    pas = Pos(bb[0], -58, bb[1]) * Rot(90, 0, 0) * (Cylinder(38, 8) - Cylinder(18, 10))
    hbar = (Pos(950, -120, 975) * Box(55, 45, 30)
            + Pos(860, -318, 950) * Box(35, 22, 22) + Pos(860, 318, 950) * Box(35, 22, 22))
    w_lo = (sa[0] + 80, -30, sa[1] - 60); w_bb = (bb[0] + 60, -30, bb[1] + 60)
    w_hd = (hb[0] - 20, -30, hb[1] - 10); w_ax = (front[0] - 10, -60, front[1] + 40)
    harness = (_tube3(w_lo, w_bb, 5) + _tube3(w_bb, w_hd, 5) + _tube3(w_hd, w_ax, 5)
               + _tube3(w_hd, (ht[0] - 10, -30, ht[1] + 60), 5)
               + _tube3((ht[0] - 10, -30, ht[1] + 60), (950, -120, 960), 5))

    PX, TILT = p["panel_x"], p["panel_tilt"]
    panel = Pos(PX, 0, 620) * Rot(0, TILT, 0) * Box(*p["panel"])
    stand = None
    for dx, zt in ((-300, 700), (300, 540)):
        for dy in (-440, 440):
            leg = _tube3((PX + dx, dy, 0), (PX + dx * 0.95, dy, zt), 14)
            stand = leg if stand is None else stand + leg
    stand = stand + _tube3((PX - 300, -440, 150), (PX + 300, -440, 150), 10) \
        + _tube3((PX - 300, 440, 150), (PX + 300, 440, 150), 10)
    charger = Pos(PX + 20, -500, 360) * Box(120, 70, 45)
    a0 = (loc * Pos(-p["pack_l"] / 2 - p["stop_len"] - 10 - ax / 2, -ay / 2, p["dt_r"] + az / 2)).position
    cable = (_tube3((PX + 20, -520, 340), (PX - 300, -200, 40), 4)
             + _tube3((PX - 300, -200, 40), (a0.X, -200, 40), 4)
             + _tube3((a0.X, -200, 40), (a0.X, a0.Y, a0.Z), 4))

    return [
        ("Donor roadster frame, fork and bars", bike, "#6B7280", None, (0, 0, 0)),
        ("Donor wheels", wheels, "#1F2937", None, (0, 0, 0)),
        ("Front hub motor, 250 W geared", motor, "#0F766E", 1, (260, -300, 0)),
        ("Torque arms (pair)", arms, "#D4A017", 2, (380, -520, 200)),
        ("Controller, sealed", controller, "#115E59", 3, (-300, -450, -60)),
        ("SwapCell receiver cradle, V1 lever", cradle + receptacle, "#94A3B8", 4, (0, -300, 170)),
        ("Host adapter (CAN, charge port)", adapter, "#7C3AED", 5, (120, -700, -260)),
        ("SwapCell pack (not in kit cost)", pack, "#C2410C", 6, (-40, -650, 480)),
        ("Pedal-assist sensor", pas, "#0EA5E9", 7, (0, -360, -60)),
        ("Handlebar control and brake cut-off", hbar, "#2563EB", 8, (160, -120, 300)),
        ("Wiring harness with fuse", harness, "#111827", 9, (0, -300, -260)),
        ("Solar panel, 100 W", panel, "#1E3A8A", 10, (-600, -2600, -300)),
        ("Boost MPPT charger", charger, "#16A34A", 11, (-600, -2900, -700)),
        ("Panel stand (local make)", stand, "#A16207", 12, (-600, -2600, -700)),
        ("Charge cable", cable, "#374151", 13, (500, -900, -450)),
    ]


def fit_checks(p=PARAMS):
    """Clearance of the pack in the main triangle and free travel along the down tube for removal."""
    g = geometry(p)
    bb, st, hb, ht = g["bb"], g["seat_top"], g["head_bot"], g["head_top"]
    others = (_tube(bb, st, p["tube_r"]) + _tube(st, ht, p["tube_r"]) + _tube(hb, ht, 18))
    loc = cradle_location(p)
    pack = loc * pack_local(p)
    clear = pack.distance_to(others)
    u = Vector(math.cos(math.radians(g["dt_ang"])), 0, math.sin(math.radians(g["dt_ang"])))
    lo, hi = 0.0, 600.0
    for _ in range(14):
        mid = (lo + hi) / 2
        moved = Pos(u.X * mid, 0, u.Z * mid) * pack
        lo, hi = (mid, hi) if moved.distance_to(others) > 0.5 else (lo, mid)
    need = p["guide_len"] + p["plug_h"] + 5
    return {"dt_len": g["dt_len"], "clearance": clear, "travel": lo, "travel_needed": need}


KIT_ITEMS = {1, 2, 3, 4, 5, 7, 8, 9}


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    (root / "step").mkdir(exist_ok=True); (root / "stl").mkdir(exist_ok=True)
    parts = build_parts()
    kit = Compound([s for _, s, _, b, _ in parts if b in KIT_ITEMS])
    receiver = Compound([cradle_local(), receptacle_local(), pack_local()])
    asm = Compound([s for _, s, _, _, _ in parts])
    for name, shape in (("sunspoke-kit", kit), ("sunspoke-cradle-with-pack", receiver), ("sunspoke-assembly", asm)):
        export_step(shape, str(root / "step" / f"{name}.step"))
        export_stl(shape, str(root / "stl" / f"{name}.stl"))
        bb = shape.bounding_box()
        print(f"{name:26s} {bb.size.X:7.1f} x {bb.size.Y:7.1f} x {bb.size.Z:7.1f} mm")
    f = fit_checks()
    print(f"down tube length {f['dt_len']:.0f} mm")
    print(f"pack clearance to top tube, seat tube and head tube {f['clearance']:.0f} mm")
    print(f"free travel along the down tube for removal {f['travel']:.0f} mm (needed {f['travel_needed']:.0f} mm)")
