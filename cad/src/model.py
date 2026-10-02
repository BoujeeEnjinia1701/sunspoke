"""SunSpoke parametric model (build123d), TRL 3, constructable design (SSP-DDR-003).

Run from the repo root:
    python cad/src/model.py            export STEP and STL into cad/step and cad/stl, print the fit checks
    python cad/src/model.py --check    run the constructability checks (touch, clear, removal path)

Every kit part is modelled as it is made or bought, at its place on the donor roadster, with the
faces that touch its neighbours: the receiver cradle (folded aluminium tray, V-saddles, band clamps,
slide strips, end stop, receptacle, catch bar, drop-down gate with an over-centre draw latch), the
joggled torque arms, the controller with its band clamps, the pedal-assist disc and sensor bracket,
the handlebar display and brake sensors, the routed harness and the timber panel stand.
The donor roadster is a context model; its dropouts, bottom bracket and brake levers are drawn
because kit parts fix to them.

Axes: the bicycle lies in the XZ plane (X forward, Z up, Y across the bike, +Y to the rider's
right), rear axle at X = 0, ground at Z = 0. Dimensions in mm. Cradle parts are drawn in the
cradle frame (x up the down tube, z away from the tube into the main triangle, y across) and
placed by cradle_location().
"""
import math
import sys
from pathlib import Path

from build123d import (Box, Compound, Cylinder, Plane, Polyline, Pos, Rot, Solid, Torus, Vector,
                       export_step, export_stl, extrude, make_face)

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
    "fork_spacing": 100.0,    # front dropout spacing (R5), inside faces of the dropouts
    "fork_blade_r": 11.0, "blade_y": 53.0, "dropout_t": 6.0,
    "bb_shell_w": 68.0, "bb_shell_r": 20.0, "spindle_r": 8.0,
    # Motor wheel (item 1)
    "motor_d": 150.0, "motor_w": 80.0, "axle_flats": 10.0, "axle_r": 6.0, "axle_len": 150.0,
    # Torque arms (item 2): 5 x 20 flat bar, joggled 8 mm so the upper part lies on the blade
    "arm_len": 130.0, "arm_w": 20.0, "arm_t": 5.0, "arm_joggle": (12.0, 28.0), "arm_ends": (-15.0, 145.0),
    # SwapCell envelope (interface v0.3)
    "pack_l": 340.0, "pack_w": 90.0, "pack_d": 80.0,
    "plug_w": 56.0, "plug_d": 34.0, "plug_h": 18.0, "plug_offset": 8.0,
    "handle_w": 84.0, "handle_d": 22.0, "handle_h": 35.0,
    "latch_w": 36.0, "latch_from_top": 45.0, "latch_proud": 10.0, "latch_h": 24.0,
    # Receiver cradle (item 4)
    "pack_pos": 0.48,         # pack centre along the down tube, fraction from the bottom bracket
    "liner_t": 1.5,           # rubber liner in the V-saddles
    "v_half": 60.0,           # half angle of the 120 degree V, from the vertical
    "saddle": (40.0, 35.0, 12.0), "saddle_v_depth": 8.0,   # length, width, height
    "saddle_x": (-100.0, 0.0, 100.0),                       # one V-saddle and one band clamp at each
    "base_t": 3.0, "base_x": (-270.0, 200.0), "base_half_w": 49.0,
    "rail_h": 12.0, "rail_w": 10.0,
    "guide_x": (-200.0, -80.0), "guide_t": 3.0, "guide_h": 50.0, "guide_clear": 1.0,
    "slot_y": (19.0, 22.0), "band_w": 12.0, "band_t": 0.8,
    "stop_t": 3.0, "stop_h": 72.0, "stop_foot": 27.0,
    "window_x": ((-80.0, -12.0), (12.0, 80.0)), "window_half_w": 22.0,
    "ear_x": (110.0, 172.0), "ear_h": 31.0,
    "gate_t": 3.0, "gate_z": (6.0, 31.0), "pad_t": 3.0,
    # Legacy concept names kept for cad/src/product_model.py (appearance model, to be updated on the Mac)
    "guide_len": 120.0, "guide_h_old": 50.0, "stop_len": 30.0, "band_pitch": 200.0, "lever_len": 90.0,
    # Host adapter (item 5) and controller (item 3)
    "adapter": (50.0, 70.0, 35.0), "controller": (150.0, 62.0, 42.0), "ctrl_pad_t": 4.0,
    # Solar set (items 10 to 13); timber stand in 45 x 45 mm sawn timber
    "panel": (670.0, 1000.0, 35.0), "panel_x": 2250.0, "panel_z": 620.0, "panel_tilt": 15.0,
    "timber": 45.0, "rail_y": 400.0, "leg_u": 285.0, "batten": (45.0, 20.0),
}

C_DONOR, C_WHEEL = "#6B7280", "#1F2937"
SLOT_END = 3.4      # centre of the slot's round end above the axle centre, so the 12 mm thread clears it


# ------------------------------------------------------------------ helpers
def _tube(p1, p2, r, y=0.0):
    a = Vector(p1[0], y, p1[1]); b = Vector(p2[0], y, p2[1]); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def _tube3(a, b, r):
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def _along(p1, p2, t):
    return (p1[0] + (p2[0] - p1[0]) * t, p1[1] + (p2[1] - p1[1]) * t)


def _fuse(shapes):
    out = None
    for s in shapes:
        if s is not None:
            out = s if out is None else out + s
    return out


def _hull2d(pts):
    pts = sorted(set((round(x, 4), round(y, 4)) for x, y in pts))
    if len(pts) < 3:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, hi = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(hi) >= 2 and cross(hi[-2], hi[-1], p) <= 0:
            hi.pop()
        hi.append(p)
    return lo[:-1] + hi[:-1]


def _circle_pts(cx, cy, r, n=72, outside=False):
    r = r / math.cos(math.pi / n) if outside else r
    return [(cx + r * math.cos(2 * math.pi * k / n), cy + r * math.sin(2 * math.pi * k / n)) for k in range(n)]


def _prism(pts2d, plane, width):
    """Closed polygon in plane coordinates, extruded symmetrically along the plane normal."""
    w = Polyline(*[plane.from_local_coords((x, y, -width / 2)) for x, y in pts2d], close=True)
    return extrude(make_face(w), width, dir=plane.z_dir)


def band_loop(core_pts, plane, width, t):
    """A worm-drive band pulled tight round everything in core_pts (plane coordinates)."""
    inner = _hull2d(core_pts)
    outer = _hull2d([q for p in inner for q in _circle_pts(p[0], p[1], t, 16)])
    return _prism(outer, plane, width) - _prism(inner, plane, width + 2)


def _box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


# ------------------------------------------------------------------ donor geometry
def geometry(p=PARAMS):
    """Key points of the donor frame."""
    g = {"rear": (0.0, p["wheel_r"]), "front": (p["wheelbase"], p["wheel_r"]),
         "bb": (p["bb_x"], p["bb_z"]), "seat_top": (p["seat_top_x"], p["seat_top_z"]),
         "head_bot": (p["head_bot_x"], p["head_bot_z"]), "head_top": (p["head_top_x"], p["head_top_z"])}
    bb, hb = g["bb"], g["head_bot"]
    g["dt_ang"] = math.degrees(math.atan2(hb[1] - bb[1], hb[0] - bb[0]))
    g["dt_len"] = math.hypot(hb[0] - bb[0], hb[1] - bb[1])
    g["dt_mid"] = _along(bb, hb, p["pack_pos"])
    fr, hb = g["front"], g["head_bot"]
    L = math.hypot(hb[0] - fr[0], hb[1] - fr[1])
    g["fork_u"] = ((hb[0] - fr[0]) / L, (hb[1] - fr[1]) / L)       # up the fork blade
    g["fork_n"] = (g["fork_u"][1], -g["fork_u"][0])                   # across the blade, forward
    return g


def cradle_location(p=PARAMS):
    """Local frame of the cradle: x along the down tube (up), z away from the tube into the triangle."""
    g = geometry(p)
    m = g["dt_mid"]
    return Pos(m[0], 0, m[1]) * Rot(0, -g["dt_ang"], 0)


def _fork_local(p, side, shape_fn):
    """Build a shape in fork-local coordinates (n, y, u): x = n, y = y, z = u, then place it."""
    g = geometry(p)
    fr, u = g["front"], g["fork_u"]
    ang = math.degrees(math.atan2(u[0], u[1]))      # tilt of the blade from vertical, toward -X
    return Pos(fr[0], 0, fr[1]) * Rot(0, ang, 0) * shape_fn()


def saddle_levels(p=PARAMS, r=None):
    """Heights above the down tube axis (cradle z) set by the V-saddles."""
    r = p["dt_r"] if r is None else r
    s = math.sin(math.radians(p["v_half"]))
    apex = (r + p["liner_t"]) / s
    land = p["saddle"][2] - p["saddle_v_depth"]
    zbb = apex + land                       # underside of the tray
    zb = zbb + p["base_t"]                  # top of the tray
    return {"apex": apex, "zbb": zbb, "zb": zb, "z0": zb + p["rail_h"], "sad_bot": zbb - p["saddle"][2]}


# ------------------------------------------------------------------ SwapCell pack and receiver (cradle frame)
def pack_local(p=PARAMS):
    """SwapCell pack in the cradle frame: back face (latch side) down on the slide strips, connector toward the BB."""
    L, W, D = p["pack_l"], p["pack_w"], p["pack_d"]
    z0 = saddle_levels(p)["z0"]
    zc = z0 + D / 2
    body = Pos(0, 0, zc) * Box(L, W, D)
    zp = zc - p["plug_offset"]
    plug = Pos(-L / 2 - p["plug_h"] / 2, 0, zp) * Box(p["plug_h"], p["plug_w"], p["plug_d"])
    handle = Pos(L / 2 + p["handle_h"] / 2, 0, zp) * (
        Box(p["handle_h"], p["handle_w"], p["handle_d"]) - Pos(-5, 0, 0) * Box(26, p["handle_w"] - 22, p["handle_d"] + 2))
    pawl = Pos(L / 2 - p["latch_from_top"], 0, z0 - p["latch_proud"] / 2) * Box(p["latch_h"], p["latch_w"], p["latch_proud"])
    return body + plug + handle + pawl


def _plug_z(p):
    return saddle_levels(p)["z0"] + p["pack_d"] / 2 - p["plug_offset"]


def receptacle_local(p=PARAMS):
    """SwapCell receptacle housing (bought) bolted behind the end stop wall, with a pocket for the plug."""
    L = p["pack_l"]
    zp = _plug_z(p)
    x_wall = -L / 2 - p["stop_t"]
    body = _box(x_wall - 22, x_wall, -31, 31, zp - 19, zp + 19) + _box(x_wall - 3, x_wall, -40, 40, zp - 19, zp + 19)
    pocket = _box(-L / 2 - p["plug_h"] - 1, x_wall + 1, -29, 29, zp - 18, zp + 18)
    return body - pocket


def tray_holes(p=PARAMS):
    """Fixing holes in the tray: (what, x along the tube, y or height, diameter, face).
    face 'base' holes go down through the base (y across); 'ear' and 'guide' holes go across through
    the folded walls (second number is the height above the base top)."""
    L = p["pack_l"]
    h = []
    for xs in p["saddle_x"]:
        h += [("V-saddle screw, countersunk from above", xs + dx, 0.0, 5.5, "base") for dx in (-12, 12)]
    for xr in (-120.0, 0.0, 120.0):
        h += [("Slide strip screw, countersunk from below", xr, sg * 40.0, 4.5, "base") for sg in (-1, 1)]
    cx = L / 2 - p["latch_from_top"] + p["latch_h"] / 2 + 3 + 5
    h += [("Catch bar screw, countersunk from below", cx, sg * 15.0, 4.5, "base") for sg in (-1, 1)]
    h += [("End stop foot bolt", -186.0, sg * 20.0, 5.5, "base") for sg in (-1, 1)]
    axc = p["base_x"][0] + 8 + p["adapter"][0] / 2
    h += [("Host adapter screw", axc, sg * 20.0, 4.5, "base") for sg in (-1, 1)]
    kx = L / 2 + p["pad_t"] + p["gate_t"] + 1.5
    h += [("Hinge screw", kx + 13, sg * 18.0, 4.5, "base") for sg in (-1, 1)]
    h += [("Draw latch rivet or screw", x, 23.0, 4.5, "ear") for x in (117.0, 137.0)]
    h += [("End stop flange bolt", x, 25.0, 5.5, "guide") for x in (-192.0, -180.0)]
    return h


def cradle_parts(p=PARAMS):
    """Every part of the receiver (item 4) and host adapter (item 5), in the cradle frame, closed."""
    L, W = p["pack_l"], p["pack_w"]
    r = p["dt_r"]
    lv = saddle_levels(p)
    zbb, zb, z0 = lv["zbb"], lv["zb"], lv["z0"]
    xb0, xb1 = p["base_x"]
    hw = p["base_half_w"]
    t = p["base_t"]
    gi = W / 2 + p["guide_clear"]                    # 46: inside face of the guides and ears
    out = {}

    # --- tray: base with band slots, screw holes and air windows; guides and latch ear folded up
    base = _box(xb0, xb1, -hw, hw, zbb, zb)
    for xs in p["saddle_x"]:
        for s in (-1, 1):
            base -= _box(xs - 6.5, xs + 6.5, s * p["slot_y"][0], s * p["slot_y"][1], zbb - 1, zb + 1) if s > 0 else \
                _box(xs - 6.5, xs + 6.5, -p["slot_y"][1], -p["slot_y"][0], zbb - 1, zb + 1)
        for dx in (-12, 12):
            base -= Pos(xs + dx, 0, zb - 2) * Cylinder(2.7, 8)
    for (wx0, wx1) in p["window_x"]:
        base -= _box(wx0, wx1, -p["window_half_w"], p["window_half_w"], zbb - 1, zb + 1)
    holes_base, holes_side = None, None
    for what, hx, hy, hd, face in tray_holes(p):
        if face == "base" and not what.startswith("V-saddle"):
            c = Pos(hx, hy, (zbb + zb) / 2) * Cylinder(hd / 2, t + 2)
            holes_base = c if holes_base is None else holes_base + c
        elif face in ("ear", "guide"):
            for sg in ((-1,) if face == "ear" else (-1, 1)):
                c = Pos(hx, sg * (gi + t / 2), zb + hy) * Rot(90, 0, 0) * Cylinder(hd / 2, t + 2)
                holes_side = c if holes_side is None else holes_side + c
    base -= holes_base
    gx0, gx1 = p["guide_x"]
    guides = _box(gx0, gx1, gi, hw, zb, zb + p["guide_h"]) + _box(gx0, gx1, -hw, -gi, zb, zb + p["guide_h"])
    ex0, ex1 = p["ear_x"]
    ear = _box(ex0, ex1, -hw, -gi, zb, zb + p["ear_h"])
    out["tray"] = base + guides + ear - holes_side

    # --- V-saddles with rubber liners
    sl, sw, sh = p["saddle"]
    tn = math.tan(math.radians(p["v_half"]))
    apex = lv["apex"]
    sad_bot = lv["sad_bot"]
    vd = p["saddle_v_depth"]

    def v_prism(apex_z, depth, length, xc):
        hw_ = depth * tn
        pts = [(-hw_ - 30 * tn, apex_z - depth - 30), (0, apex_z), (hw_ + 30 * tn, apex_z - depth - 30)]
        pl = Plane(origin=(xc, 0, 0), x_dir=(0, 1, 0), z_dir=(1, 0, 0))
        return _prism(pts, pl, length)
    saddles, liners = [], []
    for xs in p["saddle_x"]:
        blk = _box(xs - sl / 2, xs + sl / 2, -sw / 2, sw / 2, sad_bot, zbb)
        cut = v_prism(apex, vd, sl + 2, xs)
        for dx in (-12, 12):
            blk -= Pos(xs + dx, 0, zbb - 4) * Cylinder(2.1, 8)          # M5 tapped, 8 deep
        saddles.append(blk - cut)
        sh_ = p["liner_t"] / math.cos(math.radians(90 - p["v_half"]))
        lin = (v_prism(apex, vd, sl, xs) - v_prism(apex - sh_, vd, sl + 2, xs)) & _box(xs - sl / 2, xs + sl / 2, -sw / 2, sw / 2, sad_bot, zbb)
        liners.append(lin)
    out["saddles"] = _fuse(saddles)
    out["liners"] = _fuse(liners)

    # --- band clamps through the slots, round the tube and the saddle
    bands = []
    for xs in p["saddle_x"]:
        ys = p["slot_y"][0] + 0.5
        core = _circle_pts(0, 0, r, outside=True) + [(-sw / 2, sad_bot), (sw / 2, sad_bot), (-ys, zbb), (ys, zbb), (-ys, zb), (ys, zb)]
        pl = Plane(origin=(xs, 0, 0), x_dir=(0, 1, 0), z_dir=(1, 0, 0))
        loop = band_loop(core, pl, p["band_w"], p["band_t"])
        housing = _box(xs - 7, xs + 7, -6, 6, -r - p["band_t"] - 9, -r - p["band_t"])
        bands.append(loop + housing)
    out["bands"] = _fuse(bands)

    # --- slide strips (HDPE) and catch bar
    rails = None
    for s in (-1, 1):
        y0, y1 = sorted((s * (W / 2 - p["rail_w"]), s * W / 2))
        rl = _box(-L / 2 + 2, L / 2 - 2, y0, y1, zb, z0)
        rails = rl if rails is None else rails + rl
    for what, hx, hy, hd, face in tray_holes(p):
        if what.startswith("Slide strip"):
            rails -= Pos(hx, hy, zb + 5) * Cylinder(1.6, 10)                # pilot for the self-tapping screw
    out["rails"] = rails
    cx = L / 2 - p["latch_from_top"] + p["latch_h"] / 2 + 3      # 3 mm past the pawl
    catch = _box(cx, cx + 10, -25, 25, zb, zb + 6)
    for sg in (-1, 1):
        catch -= Pos(cx + 5, sg * 15, zb + 3) * Cylinder(1.65, 8)
    out["catch"] = catch

    # --- end stop: folded 3 mm aluminium, wall with plug window, two side flanges, a foot
    st = p["stop_t"]
    xw = -L / 2
    zp = _plug_z(p)
    wall = _box(xw - st, xw, -gi, gi, zb, zb + p["stop_h"]) - _box(xw - st - 1, xw + 1, -30, 30, zp - 19, zb + p["stop_h"] + 1)
    flanges = _box(gx0, xw - st, gi - st, gi, zb, zb + p["guide_h"]) + _box(gx0, xw - st, -gi, -gi + st, zb, zb + p["guide_h"])
    foot = _box(gx0, xw - st, -gi + st, gi - st, zb, zb + st)
    stop = wall + flanges + foot
    for what, hx, hy, hd, face in tray_holes(p):
        if what.startswith("End stop foot"):
            stop -= Pos(hx, hy, zb + st / 2) * Cylinder(hd / 2, st + 2)
        if what.startswith("End stop flange"):
            for sg in (-1, 1):
                stop -= Pos(hx, sg * (gi - st / 2), zb + hy) * Rot(90, 0, 0) * Cylinder(hd / 2, st + 2)
    for sg in (-1, 1):
        for hz in (zp - 12, zp + 12):
            stop -= Pos(xw - st / 2, sg * 37, hz) * Rot(0, 90, 0) * Cylinder(2.25, st + 2)
    out["stop"] = stop
    out["receptacle"] = receptacle_local(p)

    # --- host adapter on the tray's lower extension, lead to the receptacle, charge inlet on its left side
    ax, ay, az = p["adapter"]
    axc = xb0 + 8 + ax / 2
    out["adapter"] = _box(axc - ax / 2, axc + ax / 2, -ay / 2, ay / 2, zb, zb + az)
    out["inlet"] = Pos(axc, -ay / 2 - 9, zb + az / 2) * Rot(90, 0, 0) * Cylinder(9, 18)
    out["adapter_lead"] = _tube3((xw - st - 22, 0, zp - 10), (axc + ax / 2, 0, zb + az - 8), 4)

    # --- drop-down gate, rubber pad, hinge, over-centre draw latch and keeper
    gz0, gz1 = zb + p["gate_z"][0], zb + p["gate_z"][1]
    xg0 = L / 2 + p["pad_t"]
    xg1 = xg0 + p["gate_t"]
    gate = _box(xg0, xg1, -hw, gi - 1, gz0, gz1) + _box(150, xg1, -hw - 3, -hw, zb + 15, gz1)
    for sg in (-1, 1):
        gate -= Pos(xg0 + p["gate_t"] / 2, sg * 18, gz0 + 10) * Rot(0, 90, 0) * Cylinder(2.25, p["gate_t"] + 2)
    for kx_ in (154, 158):
        gate -= Pos(kx_, -hw - 1.5, zb + 23) * Rot(90, 0, 0) * Cylinder(1.75, 5)
    out["gate"] = gate
    out["pad"] = _box(L / 2, xg0, -40, 40, z0 + 2, z0 + 18)
    kx = xg1 + 1.5                                   # hinge knuckle axis
    out["hinge"] = Pos(kx, 0, zb + 2.5) * Rot(90, 0, 0) * Cylinder(2.5, 60) + _box(kx, kx + 20, -30, 30, zb, zb + 1.5)
    out["hinge_leaf"] = _box(xg1, xg1 + 1.5, -30, 30, zb + 5, zb + 25)
    yk = -hw - 3                                     # outer face of the gate flange
    out["keeper"] = _box(152, 160, yk - 4, yk, zb + 18, zb + 28)
    out["latch"] = (_box(112, 142, -hw - 10, -hw, zb + 16, zb + 30)
                    + _box(142, 162, yk - 6, yk - 4, zb + 22, zb + 25) + _box(160, 162, yk - 4, yk - 1, zb + 22, zb + 25))
    return out


def gate_open(parts, p=PARAMS):
    """The gate, pad, keeper and hinge leaf folded down flat toward the head tube (pack out)."""
    zb = saddle_levels(p)["zb"]
    kx = p["pack_l"] / 2 + p["pad_t"] + p["gate_t"] + 1.5
    rot = Pos(kx, 0, zb + 2.5) * Rot(0, 90, 0) * Pos(-kx, 0, -(zb + 2.5))
    return {k: rot * parts[k] for k in ("gate", "pad", "keeper", "hinge_leaf")}


def cradle_local(p=PARAMS):
    """The whole receiver in the cradle frame (closed), for drawings."""
    c = cradle_parts(p)
    return _fuse([c[k] for k in ("tray", "saddles", "liners", "bands", "rails", "catch", "stop", "gate", "pad",
                                 "hinge", "hinge_leaf", "keeper", "latch")])


# ------------------------------------------------------------------ donor roadster (context)
def wheel(cx, cz, r, hub_r=0.0, hub_y=0.0):
    tyre = Pos(cx, 0, cz) * Rot(90, 0, 0) * Torus(r - 20, 20)
    rim = Pos(cx, 0, cz) * Rot(90, 0, 0) * (Cylinder(r - 38, 20) - Cylinder(r - 52, 22))
    spokes = None
    for k in range(12):
        t = math.radians(k * 30)
        y0 = hub_y * (1 if k % 2 else -1)
        s = _tube3((cx + hub_r * math.cos(t), y0, cz + hub_r * math.sin(t)),
                   (cx + (r - 50) * math.cos(t), 0, cz + (r - 50) * math.sin(t)), 2.0)
        spokes = s if spokes is None else spokes + s
    return tyre + rim + spokes


def donor_parts(p=PARAMS):
    """Context: the roadster the kit bolts to. Returns a dict of shapes."""
    g = geometry(p)
    R = p["wheel_r"]
    rear, front, bb, st, hb, ht = g["rear"], g["front"], g["bb"], g["seat_top"], g["head_bot"], g["head_top"]
    tr = p["tube_r"]
    by = p["blade_y"]
    u, n = g["fork_u"], g["fork_n"]
    out = {}
    out["frame"] = (_tube(bb, st, tr) + _tube(st, ht, tr) + _tube(bb, hb, p["dt_r"]) + _tube(hb, ht, 18)
                    + _tube3((bb[0], 25, bb[1]), (rear[0], 45, rear[1]), 9) + _tube3((bb[0], -25, bb[1]), (rear[0], -45, rear[1]), 9)
                    + _tube(st, rear, 8, 45) + _tube(st, rear, 8, -45)
                    + _tube((210, 850), (205, 900), 13)
                    + Pos(bb[0], 0, bb[1]) * Rot(90, 0, 0) * Cylinder(p["bb_shell_r"], p["bb_shell_w"]))
    # fork: blades end 30 mm up from the axle in a 6 mm dropout plate slotted 10 mm for the axle flats
    blade_end = (front[0] + u[0] * 30, front[1] + u[1] * 30)
    fork = Pos(hb[0], 0, hb[1]) * Box(40, 2 * (by + 12), 20)
    for s in (-1, 1):
        fork = fork + _tube(hb, blade_end, p["fork_blade_r"], s * by)

        def dropout():
            y0 = p["fork_spacing"] / 2
            pl = _box(-12, 12, y0, y0 + p["dropout_t"], -14, 40) - _box(-p["axle_flats"] / 2, p["axle_flats"] / 2, y0 - 1, y0 + p["dropout_t"] + 1, -15, SLOT_END)
            pl = pl - Pos(0, y0 + p["dropout_t"] / 2, SLOT_END) * Rot(90, 0, 0) * Cylinder(p["axle_flats"] / 2, p["dropout_t"] + 2)
            return pl if s > 0 else pl.mirror(Plane.XZ)
        fork = fork + _fork_local(p, s, dropout)
    out["fork"] = fork
    out["stem_bars"] = (_tube(ht, (950, 960), 12)
                        + _tube3((950, -300, 960), (950, 300, 960), 11)
                        + _tube3((950, 300, 960), (820, 330, 945), 11) + _tube3((950, -300, 960), (820, -330, 945), 11))
    # brake levers (rod brakes): a clamp on each bar end, a pivot post and the lever blade under the grip
    lev = []
    for s in (-1, 1):
        a, b = bar_point(905, s), _bar_dir(s)
        lev.append(_tube3(tuple(a - b * 8), tuple(a + b * 8), 14) - _tube3(tuple(a - b * 9), tuple(a + b * 9), 11))
        lev.append(_tube3((a.X, a.Y, a.Z - 13.5), (a.X, a.Y, 930), 5))
        lev.append(_tube3((a.X, a.Y, 930), (835, s * 327, 921), 4.5))
    out["levers"] = _fuse(lev)
    out["saddle_seat"] = Pos(200, 0, 925) * Box(260, 150, 55)
    out["carrier"] = (Pos(-60, 0, 800) * Box(420, 170, 12)
                      + _tube3((-230, 60, 795), (0, 60, R), 6) + _tube3((-230, -60, 795), (0, -60, R), 6))
    hw = p["bb_shell_w"] / 2
    out["drive"] = (_tube3((bb[0], -75, bb[1]), (bb[0] + 60, -75, bb[1] - 160), 9)
                    + _tube3((bb[0], 75, bb[1]), (bb[0] - 60, 75, bb[1] + 160), 9)
                    + Pos(bb[0], 45, bb[1]) * Rot(90, 0, 0) * Cylinder(100, 5)
                    + Pos(bb[0], 0, bb[1]) * Rot(90, 0, 0) * Cylinder(p["spindle_r"], 150)
                    # left adjustable cup and lockring, outside the shell
                    + Pos(bb[0], -hw - 4, bb[1]) * Rot(90, 0, 0) * (Cylinder(17, 8) - Cylinder(10, 9))
                    + Pos(bb[0], -hw - 1.5 - 2, bb[1]) * Rot(90, 0, 0) * (Cylinder(22, 4) - Cylinder(17, 5)))
    out["wheels"] = wheel(*rear, R) + wheel(*front, R, hub_r=62, hub_y=25)
    return out


def _bar_dir(s):
    a, b = Vector(950, s * 300, 960), Vector(820, s * 330, 945)
    return (b - a).normalized()


def bar_point(x, s):
    """Point on the centre line of the swept part of the bar at a given X (s = side)."""
    a, b = Vector(950, s * 300, 960), Vector(820, s * 330, 945)
    t = (950 - x) / 130
    return a + (b - a) * t


def torque_arm_local(p=PARAMS, s=1):
    """Torque arm and axle nut in fork-local coordinates (x across the blade, y out to the side,
    z up the blade, axle at the origin). s = +1 right, -1 left (mirror image)."""
    a0, a1 = p["arm_ends"]
    j0, j1 = p["arm_joggle"]
    t = p["arm_t"]
    y_in = p["fork_spacing"] / 2 + p["dropout_t"]    # 56: outer face of the dropout
    y_bl = p["blade_y"] + p["fork_blade_r"]          # 64: outside of the blade
    prof = [(a0, y_in), (j0, y_in), (j1, y_bl), (a1, y_bl), (a1, y_bl + t), (j1, y_bl + t), (j0, y_in + t), (a0, y_in + t)]
    pl = Plane(origin=(0, 0, 0), x_dir=(0, 0, 1), z_dir=(-1, 0, 0))    # local x = u, local y = y, normal = n
    arm = _prism(prof, pl, p["arm_w"])
    arm -= _box(-p["axle_flats"] / 2, p["axle_flats"] / 2, y_in - 1, y_in + t + 1, a0 - 1, SLOT_END)
    arm -= Pos(0, y_in + t / 2, SLOT_END) * Rot(90, 0, 0) * Cylinder(p["axle_flats"] / 2, t + 2)
    nut = (Pos(0, y_in + t + 1, 0) * Rot(90, 0, 0) * (Cylinder(10, 2) - Cylinder(p["axle_r"], 3))
           + Pos(0, y_in + t + 6, 0) * Rot(90, 0, 0) * (Cylinder(9.5, 8) - Cylinder(p["axle_r"], 9)))
    return (arm, nut) if s > 0 else (arm.mirror(Plane.XZ), nut.mirror(Plane.XZ))


# ------------------------------------------------------------------ kit parts on the bike
def build_components(p=PARAMS, gate_closed=True):
    """Every kit and donor part at its place, by name: {name: (shape, colour, bom item or None)}."""
    g = geometry(p)
    rear, front, bb, st, hb, ht = g["rear"], g["front"], g["bb"], g["seat_top"], g["head_bot"], g["head_top"]
    C = {}
    D = donor_parts(p)
    C["frame"] = (D["frame"], C_DONOR, None)
    C["fork"] = (D["fork"], C_DONOR, None)
    C["stem_bars"] = (D["stem_bars"], C_DONOR, None)
    C["levers"] = (D["levers"], "#9CA3AF", None)
    C["saddle_seat"] = (D["saddle_seat"], C_DONOR, None)
    C["carrier"] = (D["carrier"], C_DONOR, None)
    C["drive"] = (D["drive"], C_DONOR, None)
    C["wheels"] = (D["wheels"], C_WHEEL, None)

    # ---------------- item 1: hub motor, axle with flats, nuts and washers
    fy = p["fork_spacing"] / 2

    def motor_local():
        shell = Rot(90, 0, 0) * Cylinder(p["motor_d"] / 2, p["motor_w"] - 20)
        flanges = Rot(90, 0, 0) * (Pos(0, 0, 25) * Cylinder(66, 3) + Pos(0, 0, -25) * Cylinder(66, 3))
        cones = Rot(90, 0, 0) * (Pos(0, 0, (30 + fy) / 2) * Cylinder(9, fy - 30) + Pos(0, 0, -(30 + fy) / 2) * Cylinder(9, fy - 30))
        axle = (Rot(90, 0, 0) * Cylinder(p["axle_r"], p["axle_len"])) & Box(p["axle_flats"], p["axle_len"] + 2, 20)
        return shell + flanges + cones + axle
    C["motor"] = (_fork_local(p, 1, motor_local), "#0F766E", 1)
    a0, a1 = p["arm_ends"]
    j0, j1 = p["arm_joggle"]
    t = p["arm_t"]
    y_in = fy + p["dropout_t"]                       # 56: outer face of the dropout
    y_bl = p["blade_y"] + p["fork_blade_r"]          # 64: outside of the blade

    arms, nuts, clamps = [], [], []
    for s in (-1, 1):
        a_, n_ = torque_arm_local(p, s)
        arms.append(_fork_local(p, s, lambda a_=a_: a_))
        nuts.append(_fork_local(p, s, lambda n_=n_: n_))

        def clamp(s=s):
            yb = s * p["blade_y"]
            core = _circle_pts(0, yb, p["fork_blade_r"], outside=True) + [(-p["arm_w"] / 2, s * y_bl), (p["arm_w"] / 2, s * y_bl),
                                                             (-p["arm_w"] / 2, s * (y_bl + t)), (p["arm_w"] / 2, s * (y_bl + t))]
            pl = Plane(origin=(0, 0, p["arm_len"]), x_dir=(1, 0, 0), z_dir=(0, 0, 1))
            loop = band_loop(core, pl, 12, 0.8)
            hous = _box(-6, 6, s * (y_bl + t + 0.8) if s > 0 else -(y_bl + t + 0.8 + 9), (y_bl + t + 0.8 + 9) if s > 0 else -(y_bl + t + 0.8),
                        p["arm_len"] - 7, p["arm_len"] + 7)
            return loop + hous
        clamps.append(_fork_local(p, s, clamp))
    C["arms"] = (_fuse(arms), "#D4A017", 2)
    C["arm_clamps"] = (_fuse(clamps), "#9CA3AF", 2)
    C["axle_nuts"] = (_fuse(nuts), "#374151", 1)

    # ---------------- items 4 and 5: receiver cradle, pack, host adapter
    loc = cradle_location(p)
    cp = cradle_parts(p)
    if not gate_closed:
        cp.update(gate_open(cp, p))
    for k, col, item in (("tray", "#94A3B8", 4), ("saddles", "#64748B", 4), ("liners", "#111827", 4), ("bands", "#9CA3AF", 4),
                         ("rails", "#F1F5F9", 4), ("catch", "#475569", 4), ("stop", "#64748B", 4), ("receptacle", "#1F2937", 4),
                         ("gate", "#0F766E", 4), ("pad", "#111827", 4), ("hinge", "#9CA3AF", 4), ("hinge_leaf", "#9CA3AF", 4), ("keeper", "#9CA3AF", 4),
                         ("latch", "#115E59", 4), ("adapter", "#7C3AED", 5), ("inlet", "#4C1D95", 5), ("adapter_lead", "#111827", 9)):
        C[k] = (loc * cp[k], col, item)
    C["pack"] = (loc * pack_local(p), "#C2410C", 6)

    # ---------------- item 3: controller on a rubber pad, two band clamps round the seat tube
    sa = _along(bb, st, 0.38)
    sv = Vector(st[0] - bb[0], 0, st[1] - bb[1]).normalized()
    fwd = Vector(-sv.Z, 0, sv.X) if sv.X < 0 else Vector(sv.Z, 0, -sv.X)      # perpendicular, pointing forward
    if fwd.X < 0:
        fwd = -fwd
    cx_, cy_, cz_ = p["controller"]
    tr = p["tube_r"]
    pad_t = p["ctrl_pad_t"]
    ang = math.degrees(math.atan2(sv.X, sv.Z))
    base_pt = Vector(sa[0], 0, sa[1])

    def onseat(shape, off):          # off: distance in front of the seat tube axis
        return Pos(*(base_pt + fwd * off)) * Rot(0, ang, 0) * shape
    C["controller"] = (onseat(Box(cz_, cy_, cx_), tr + pad_t + cz_ / 2), "#115E59", 3)
    C["ctrl_pad"] = (onseat(Box(pad_t, 40, 120), tr + pad_t / 2), "#111827", 3)
    cb = []
    for d in (-45, 45):
        o = base_pt + sv * d
        pl = Plane(origin=o, x_dir=fwd, z_dir=sv)
        core = _circle_pts(0, 0, tr, outside=True) + [(tr + pad_t + cz_, -cy_ / 2), (tr + pad_t + cz_, cy_ / 2), (tr, -20), (tr, 20)]
        loop = band_loop(core, pl, 12, 0.8)
        hous = Pos(*(o - fwd * (tr + 0.8 + 4.5))) * Rot(0, ang, 0) * Box(9, 12, 14)
        cb.append(loop + hous)
    C["ctrl_bands"] = (_fuse(cb), "#9CA3AF", 3)

    # ---------------- item 7: pedal-assist disc on the spindle, sensor on a bracket under the left lockring
    hw = p["bb_shell_w"] / 2
    disc = Pos(bb[0], -hw - 12, bb[1]) * Rot(90, 0, 0) * (Cylinder(38, 4) - Cylinder(p["spindle_r"], 5))
    hubc = Pos(bb[0], -hw - 16.5, bb[1]) * Rot(90, 0, 0) * (Cylinder(14, 5) - Cylinder(p["spindle_r"], 6))
    mags = _fuse([Pos(bb[0] + 32 * math.cos(math.radians(k * 30)), -hw - 9.5, bb[1] + 32 * math.sin(math.radians(k * 30)))
                  * Rot(90, 0, 0) * Cylinder(3, 1) for k in range(12)])
    C["pas_disc"] = (disc + hubc + mags, "#0EA5E9", 7)
    ring = Pos(bb[0], -hw - 0.75, bb[1]) * Rot(90, 0, 0) * (Cylinder(25, 1.5) - Cylinder(17, 2))
    tab = _box(bb[0] - 6, bb[0] + 6, -hw - 1.5, -hw, bb[1] - 40, bb[1] - 23)
    sensor = _box(bb[0] - 6, bb[0] + 6, -hw - 6.5, -hw - 1.5, bb[1] - 40, bb[1] - 26)
    C["pas_sensor"] = (ring + tab + sensor, "#0369A1", 7)

    # ---------------- item 8: display on its own bar clamp, brake sensors on bar clamps beside each lever
    disp_y = -120
    dclamp = _tube3((950, disp_y - 10, 960), (950, disp_y + 10, 960), 13.5) - _tube3((950, disp_y - 11, 960), (950, disp_y + 11, 960), 11)
    disp = _box(922.5, 977.5, disp_y - 22.5, disp_y + 22.5, 973.5, 1003.5)
    C["display"] = (dclamp + disp, "#2563EB", 8)
    bs = []
    for s in (-1, 1):
        a, d = bar_point(925, s), _bar_dir(s)
        bs.append(_tube3(tuple(a - d * 6), tuple(a + d * 6), 13) - _tube3(tuple(a - d * 7), tuple(a + d * 7), 11))
        bs.append(_box(a.X - 6, a.X + 14, a.Y - 7, a.Y + 7, a.Z - 13 - 14, a.Z - 12.5))
        m = bar_point(905, s)
        bs.append(Pos(m.X + 5 + 1, m.Y, a.Z - 20) * Rot(0, 90, 0) * Cylinder(4, 2))   # magnet on the lever post
    C["brake_sensors"] = (_fuse(bs), "#1D4ED8", 8)

    # ---------------- item 9: harness, routed on the left side of the tubes and held by cable ties
    cr = 4.0
    sd = -(tr + cr)                       # left side of the seat and top tubes
    dd = -(p["dt_r"] + cr)

    def on_tube(a, b, t_):
        return (a[0] + (b[0] - a[0]) * t_, a[1] + (b[1] - a[1]) * t_)
    lv_ = saddle_levels(p)
    axl = p["base_x"][0] + 8
    st_low = on_tube(bb, st, 0.10)
    ctl_lo = on_tube(bb, st, 0.38 - 75 / g_len(bb, st))
    ctl_hi = on_tube(bb, st, 0.38 + 75 / g_len(bb, st))
    st_top = on_tube(bb, st, 0.93)
    tt_end = on_tube(st, ht, 0.92)
    A = [tuple((loc * Pos(*q)).position) for q in ((axl, -20, lv_["zb"] + 15), (axl - 18, -20, lv_["zb"] + 15),
                                                     (axl - 34, dd, 0.0))]
    pts_a = A + [(st_low[0], sd, st_low[1]), (ctl_lo[0], sd, ctl_lo[1])]
    pts_b = [(ctl_hi[0], sd, ctl_hi[1]), (st_top[0], sd, st_top[1]), (tt_end[0], sd, tt_end[1] - 4), (ht[0] - 4, -22, ht[1] - 20),
             (hb[0] - 4, -22, hb[1] + 10)]
    harness = []
    for pts in (pts_a, pts_b):
        for q0, q1 in zip(pts[:-1], pts[1:]):
            harness.append(_tube3(q0, q1, cr))
    # motor cable down the front of the left blade, over the band clamp; bar leads up the stem
    u, n = g["fork_u"], g["fork_n"]
    by = p["blade_y"]
    c0 = (hb[0] - 4, -22, hb[1] + 10)
    off = p["fork_blade_r"] + 1.0 + cr
    m_top = (hb[0] - u[0] * 40 + n[0] * off, -by, hb[1] - u[1] * 40 + n[1] * off)
    m_bot = (front[0] + u[0] * 40 + n[0] * off, -by, front[1] + u[1] * 40 + n[1] * off)
    m_end = (front[0] + n[0] * 16, -(p["fork_spacing"] / 2 + p["dropout_t"] + 22), front[1] + n[1] * 16)
    harness += [_tube3(c0, m_top, cr), _tube3(m_top, m_bot, cr), _tube3(m_bot, m_end, cr)]
    s_top = (950 - 12 - cr, -6, 940)
    harness += [_tube3((ht[0] - 4, -22, ht[1] - 20), (ht[0] - 16, -16, ht[1] + 40), cr), _tube3((ht[0] - 16, -16, ht[1] + 40), s_top, cr)]
    for s in (-1, 1):
        a = bar_point(925, s)
        harness.append(_tube3(s_top, (950 - 4, s * 60, 960 - 11 - cr), cr))
        harness.append(_tube3((950 - 4, s * 60, 960 - 11 - cr), (a.X, a.Y - s * 10, a.Z - 13 - cr), cr))
    harness.append(_tube3((950 - 4, -60, 960 - 11 - cr), (950, -120, 960 - 11 - cr), cr))
    # pedal-assist lead up the seat tube
    pas = [(bb[0] + 9, -hw - 4, bb[1] - 33), (bb[0] - 28, -hw - 4, bb[1] - 34), (bb[0] - 50, -hw - 4, bb[1] + 2),
           (st_low[0] - 8, sd - 1, st_low[1] - 10), (st_low[0], sd, st_low[1])]
    for q0, q1 in zip(pas[:-1], pas[1:]):
        harness.append(_tube3(q0, q1, 3))
    va, vb = Vector(*pts_a[1]), Vector(*pts_a[2])
    fuse = _tube3(tuple(va + (vb - va) * 0.35), tuple(va + (vb - va) * 0.85), 7)      # sealed 20 A fuse holder
    C["harness"] = (_fuse(harness) + fuse, "#111827", 9)

    # ---------------- items 10 to 13: panel, timber stand, charger, cable
    PX, PZ, TILT = p["panel_x"], p["panel_z"], p["panel_tilt"]
    pw, pl_, pt_ = p["panel"]
    F = Pos(PX, 0, PZ) * Rot(0, TILT, 0)
    C["panel"] = (F * Box(pw, pl_, pt_) + F * _box(-200, -120, -330, -270, -pt_ / 2 - 20, -pt_ / 2), "#1E3A8A", 10)
    tb = p["timber"]
    ry = p["rail_y"]
    stand = []
    rails = [F * _box(-350, 350, s * ry - tb / 2, s * ry + tb / 2, -pt_ / 2 - tb, -pt_ / 2) for s in (-1, 1)]
    stand += rails
    legs = []
    for uu in (-p["leg_u"], p["leg_u"]):
        c = F * Pos(uu, 0, -pt_ / 2 - tb / 2)
        lx = c.position.X
        under = PZ - (lx - PX) * math.tan(math.radians(TILT)) - (pt_ / 2) / math.cos(math.radians(TILT))
        top = under - tb / 2 * math.tan(math.radians(TILT)) - 2
        for s in (-1, 1):
            y0 = s * (ry + tb / 2)
            legs.append(_box(lx - tb / 2, lx + tb / 2, min(y0, y0 + s * tb), max(y0, y0 + s * tb), 0, top))
    stand += legs
    xr = (F * Pos(-p["leg_u"], 0, 0)).position.X
    xf = (F * Pos(p["leg_u"], 0, 0)).position.X
    for s in (-1, 1):
        y0, y1 = sorted((s * (ry - tb / 2), s * (ry + tb / 2)))
        stand.append(_box(xr - tb / 2, xf + tb / 2, y0, y1, 150, 150 + tb))
    bw, bt_ = p["batten"]
    for uu, sgn in ((-p["leg_u"], -1), (p["leg_u"], 1)):
        lx = (F * Pos(uu, 0, 0)).position.X
        xface = lx + sgn * tb / 2
        stand.append(_box(min(xface, xface + sgn * bt_), max(xface, xface + sgn * bt_), -(ry + tb * 1.5), ry + tb * 1.5, 100, 100 + bw))
    C["stand"] = (_fuse(stand), "#A16207", 12)
    rear_leg_x = (F * Pos(-p["leg_u"], 0, 0)).position.X
    ch = _box(rear_leg_x - 35, rear_leg_x + 35, -(ry + tb * 1.5) - 45, -(ry + tb * 1.5), 330, 450)
    C["charger"] = (ch, "#16A34A", 11)
    jb = (F * Pos(-160, -300, -pt_ / 2 - 20)).position
    lead = _tube3((jb.X, jb.Y, jb.Z), (rear_leg_x, -(ry + tb * 1.5) - 22, 450), 3.5)
    inlet = (loc * Pos(p["base_x"][0] + 8 + p["adapter"][0] / 2, -p["adapter"][1] / 2 - 18, saddle_levels(p)["zb"] + p["adapter"][2] / 2)).position
    cable = (_tube3((rear_leg_x, -(ry + tb * 1.5) - 22, 330), (rear_leg_x, -(ry + tb * 1.5) - 22, 20), 4)
             + _tube3((rear_leg_x, -(ry + tb * 1.5) - 22, 20), (inlet.X + 40, -250, 20), 4)
             + _tube3((inlet.X + 40, -250, 20), (inlet.X + 40, -250, inlet.Z - 120), 4)
             + _tube3((inlet.X + 40, -250, inlet.Z - 120), (inlet.X, inlet.Y, inlet.Z), 4))
    C["panel_lead"] = (lead, "#374151", 10)
    C["cable"] = (cable, "#374151", 13)
    return C


def g_len(a, b):
    return math.hypot(b[0] - a[0], b[1] - a[1])


# ------------------------------------------------------------------ concept media parts list
GROUPS = [  # (label, component keys, colour, bom item, explode offset)
    ("Donor roadster frame, fork and bars", ["frame", "fork", "stem_bars", "levers", "saddle_seat", "carrier", "drive"], "#6B7280", None, (0, 0, 0)),
    ("Donor wheels", ["wheels"], "#1F2937", None, (0, 0, 0)),
    ("Front hub motor, 250 W geared", ["motor", "axle_nuts"], "#0F766E", 1, (260, -300, 0)),
    ("Torque arms (pair)", ["arms", "arm_clamps"], "#D4A017", 2, (380, -520, 200)),
    ("Controller, sealed", ["controller", "ctrl_pad", "ctrl_bands"], "#115E59", 3, (-300, -450, -60)),
    ("SwapCell receiver cradle, V1 latch", ["tray", "saddles", "liners", "bands", "rails", "catch", "stop", "receptacle", "gate", "pad",
                                            "hinge", "hinge_leaf", "keeper", "latch"], "#94A3B8", 4, (0, -300, 170)),
    ("Host adapter (CAN, charge port)", ["adapter", "inlet"], "#7C3AED", 5, (120, -700, -260)),
    ("SwapCell pack (not in kit cost)", ["pack"], "#C2410C", 6, (-40, -650, 480)),
    ("Pedal-assist sensor", ["pas_disc", "pas_sensor"], "#0EA5E9", 7, (0, -360, -60)),
    ("Handlebar control and brake cut-off", ["display", "brake_sensors"], "#2563EB", 8, (160, -120, 300)),
    ("Wiring harness with fuse", ["harness", "adapter_lead"], "#111827", 9, (0, -300, -260)),
    ("Solar panel, 100 W", ["panel", "panel_lead"], "#1E3A8A", 10, (-600, -2600, -300)),
    ("Boost MPPT charger", ["charger"], "#16A34A", 11, (-600, -2900, -700)),
    ("Panel stand (local make)", ["stand"], "#A16207", 12, (-600, -2600, -700)),
    ("Charge cable", ["cable"], "#374151", 13, (500, -900, -450)),
]


def build_parts(p=PARAMS, C=None):
    """Return a list of (name, shape, colour, bom_item or None, explode_offset) for concept media and drawings."""
    C = C or build_components(p)
    return [(name, _fuse([C[k][0] for k in keys]), col, bom, ex) for name, keys, col, bom, ex in GROUPS]


# ------------------------------------------------------------------ checks
def _gap(a, b):
    return a.distance_to(b)


def _overlap(a, b):
    try:
        return (a & b).volume
    except Exception:
        return 0.0


def fit_checks(p=PARAMS):
    """Pack clearance in the main triangle and the removal path: gate down, slide up the tube, lift out."""
    g = geometry(p)
    D = donor_parts(p)
    frame_bits = D["frame"] + D["fork"]
    loc = cradle_location(p)
    cp = cradle_parts(p)
    cp.update(gate_open(cp, p))
    fixed = loc * _fuse([cp[k] for k in ("tray", "saddles", "bands", "rails", "catch", "stop", "receptacle", "gate", "pad",
                                          "hinge", "hinge_leaf", "keeper", "latch", "adapter")])
    pk = pack_local(p)
    zb = saddle_levels(p)["zb"]
    pk_free = pk - _box(-200, 200, -60, 60, zb - 5, zb + p["rail_h"] - 0.01)     # the pawl retracted by the release
    pack = loc * pk
    clear = pack.distance_to(_tube(g["bb"], g["seat_top"], p["tube_r"]) + _tube(g["seat_top"], g["head_top"], p["tube_r"])
                             + _tube(g["head_bot"], g["head_top"], 18))
    need = p["guide_x"][1] - p["guide_x"][0] + p["plug_h"] + 5
    worst = 0.0
    for k in range(0, int(need) + 1, 11):
        moved = loc * Pos(k + 0.5, 0, 0.2) * pk_free
        worst = max(worst, _overlap(moved, fixed), _overlap(moved, frame_bits))
    lift = 45.0
    lift_ok = True
    for dz, dy in [(lift * f / 4, 0) for f in range(1, 5)] + [(lift, -40 * k) for k in range(1, 6)]:
        moved = loc * Pos(need + 0.5, dy, dz + 0.2) * pk_free
        if _overlap(moved, fixed) > 1e-3 or _overlap(moved, frame_bits) > 1e-3:
            lift_ok = False
    lo, hi = 0.0, 600.0
    for _ in range(12):
        mid = (lo + hi) / 2
        moved = loc * Pos(mid, 0, 0.2) * pk_free
        lo, hi = (mid, hi) if moved.distance_to(frame_bits) > 0.5 else (lo, mid)
    return {"dt_len": g["dt_len"], "clearance": clear, "travel": lo, "travel_needed": need,
            "slide_overlap": worst, "lift_ok": lift_ok}


def constructability_checks(p=PARAMS):
    """(name, kind, value, limit, ok). kind 'touch': parts that must bear on each other (gap 0.05 mm or
    less, no overlap); 'clear': parts that must not touch (gap at least the limit)."""
    C = build_components(p)
    S = {k: v[0] for k, v in C.items()}
    loc = cradle_location(p)
    cp = cradle_parts(p)
    tube = _tube(geometry(p)["bb"], geometry(p)["head_bot"], p["dt_r"])
    res = []

    def touch(name, a, b, tol=0.05):
        gp, ov = _gap(a, b), _overlap(a, b)
        res.append((name, "touch", gp, ov, gp <= tol and ov < 0.5))

    def clear(name, a, b, lim):
        gp = _gap(a, b)
        res.append((name, "clear", gp, lim, gp >= lim - 1e-6))
    L = loc
    touch("V-saddle liners on the down tube", L * cp["liners"], tube)
    touch("Liners in the V-saddles", cp["liners"], cp["saddles"])
    touch("V-saddles under the tray", cp["saddles"], cp["tray"])
    touch("Band clamps on the down tube", L * cp["bands"], tube)
    touch("Band clamps over the tray", cp["bands"], cp["tray"])
    touch("Slide strips on the tray", cp["rails"], cp["tray"])
    touch("Pack on the slide strips", pack_local(p), cp["rails"])
    touch("Catch bar on the tray", cp["catch"], cp["tray"])
    clear("Pack pawl to catch bar (3 mm)", pack_local(p), cp["catch"], 2.9)
    touch("End stop on the tray", cp["stop"], cp["tray"])
    touch("Pack on the end stop", pack_local(p), cp["stop"])
    touch("Receptacle on the end stop", cp["receptacle"], cp["stop"])
    clear("Plug in the receptacle pocket", pack_local(p) - Pos(-p["pack_l"] / 2 - 9, 0, 0) * Box(0.01, 1, 1), cp["receptacle"], 0.9)
    clear("Pack to the guides (1 mm each side)", pack_local(p), cp["tray"] - _box(-400, 400, -60, 60, -50, saddle_levels(p)["zb"] + 0.01), 0.95)
    touch("Adapter on the tray", cp["adapter"], cp["tray"])
    touch("Gate pad on the pack", cp["pad"], pack_local(p))
    touch("Gate pad on the gate", cp["pad"], cp["gate"])
    touch("Hinge leaf on the gate", cp["hinge_leaf"], cp["gate"])
    touch("Hinge leaf on its knuckle", cp["hinge_leaf"], cp["hinge"])
    touch("Hinge on the tray", cp["hinge"], cp["tray"])
    touch("Gate flange on the latch ear", cp["gate"], cp["tray"])
    touch("Keeper on the gate flange", cp["keeper"], cp["gate"])
    touch("Latch on the ear", cp["latch"], cp["tray"])
    touch("Latch hook on the keeper", cp["latch"], cp["keeper"])
    clear("Gate below the pack handle", cp["gate"], pack_local(p), 1.0)
    for k in ("saddles", "bands", "stop", "adapter", "receptacle"):
        clear(f"Cradle {k} clear of the chainring and cranks", L * cp[k], S["drive"], 3.0)
    touch("Torque arms on the dropouts", S["arms"], S["fork"], 0.05)
    touch("Axle flats in the torque arm slots", S["arms"], S["motor"], 0.05)
    touch("Axle flats in the dropout slots", S["motor"], S["fork"], 0.05)
    touch("Axle nuts on the torque arms", S["axle_nuts"], S["arms"])
    touch("Arm band clamps on the fork blades", S["arm_clamps"], S["fork"], 0.05)
    clear("Motor shell clear of the fork", S["motor"] - _fork_local(p, 1, lambda: Rot(90, 0, 0) * Cylinder(20, 300)), S["fork"], 3.0)
    touch("Controller pad on the seat tube", S["ctrl_pad"], S["frame"])
    touch("Controller on its pad", S["controller"], S["ctrl_pad"])
    touch("Controller bands on the seat tube", S["ctrl_bands"], S["frame"], 0.05)
    clear("Controller clear of the pack", S["controller"], S["pack"], 20.0)
    touch("Pedal-assist disc on the spindle", S["pas_disc"], S["drive"])
    touch("Sensor bracket under the lockring", S["pas_sensor"], S["drive"])
    clear("Sensor to disc gap (2 mm or more)", S["pas_sensor"], S["pas_disc"], 2.0)
    clear("Disc clear of the cup and left crank", S["pas_disc"], S["drive"] - Pos(geometry(p)["bb"][0], 0, geometry(p)["bb"][1]) * Rot(90, 0, 0) * Cylinder(9, 140), 1.5)
    touch("Display clamp on the bar", S["display"], S["stem_bars"])
    touch("Brake sensor clamps on the bar", S["brake_sensors"], S["stem_bars"])
    clear("Brake sensors clear of the levers", S["brake_sensors"] - _fuse([Pos(bar_point(905, s).X + 6, bar_point(905, s).Y, bar_point(925, s).Z - 20)
                                                                              * Rot(0, 90, 0) * Cylinder(4.5, 3) for s in (-1, 1)]), S["levers"], 1.0)
    clear("Harness clear of the cradle", S["harness"], _fuse([S[k] for k in ("tray", "bands", "saddles", "stop", "receptacle", "gate", "latch")]), 2.0)
    clear("Harness clear of the wheels", S["harness"], S["wheels"], 10.0)
    clear("Harness clear of the cranks and chainring", S["harness"], S["drive"], 3.0)
    clear("Torque arms clear of the wheel", S["arms"] + S["arm_clamps"], S["wheels"], 10.0)
    touch("Panel on the stand rails", S["panel"], S["stand"])
    touch("Charger on the rear leg", S["charger"], S["stand"])
    clear("Charge cable clear of the bike", S["cable"], S["frame"] + S["drive"] + S["wheels"], 5.0)
    f = fit_checks(p)
    res.append(("Pack slides out with the gate down (overlap mm3)", "path", f["slide_overlap"], 0.5, f["slide_overlap"] < 0.5))
    res.append(("Pack lifts 45 mm and comes out to the left after the slide", "path", 1.0 if f["lift_ok"] else 0.0, 1.0, f["lift_ok"]))
    res.append((f"Free travel up the tube {f['travel']:.0f} mm, need {f['travel_needed']:.0f}", "path", f["travel"], f["travel_needed"],
                f["travel"] >= f["travel_needed"]))
    return res


DENS = {"al": 2.70e-6, "steel": 7.85e-6, "hdpe": 0.95e-6, "rubber": 1.2e-6, "timber": 0.55e-6}


def masses(p=PARAMS):
    """Masses of the made parts from the model volumes (kg)."""
    cp = cradle_parts(p)
    C = build_components(p)
    m = {"tray (aluminium 3 mm)": cp["tray"].volume * DENS["al"], "V-saddles (aluminium)": cp["saddles"].volume * DENS["al"],
         "liners": cp["liners"].volume * DENS["rubber"], "slide strips (HDPE)": cp["rails"].volume * DENS["hdpe"],
         "catch bar (steel)": cp["catch"].volume * DENS["steel"], "end stop (aluminium 3 mm)": cp["stop"].volume * DENS["al"],
         "gate (steel 3 mm)": cp["gate"].volume * DENS["steel"], "torque arms (steel)": C["arms"][0].volume * DENS["steel"],
         "panel stand (timber)": C["stand"][0].volume * DENS["timber"]}
    return m


KIT_ITEMS = {1, 2, 3, 4, 5, 7, 8, 9}


if __name__ == "__main__":
    if "--check" in sys.argv:
        bad = 0
        rows = constructability_checks()
        for name, kind, a, b, ok in rows:
            bad += not ok
            if kind == "touch":
                print(f"  {'PASS' if ok else 'FAIL'}  touch  {name}: gap {a:.2f} mm, overlap {b:.2f} mm3")
            elif kind == "clear":
                print(f"  {'PASS' if ok else 'FAIL'}  clear  {name}: gap {a:.1f} mm (need {b:.1f})")
            else:
                print(f"  {'PASS' if ok else 'FAIL'}  path   {name}")
        print(f"{len(rows) - bad} of {len(rows)} constructability checks pass")
        for k, v in masses().items():
            print(f"  mass {k:28s} {v:.3f} kg")
        sys.exit(1 if bad else 0)
    root = Path(__file__).resolve().parents[1]
    (root / "step").mkdir(exist_ok=True); (root / "stl").mkdir(exist_ok=True)
    parts = build_parts()
    kit = Compound([s for _, s, _, b, _ in parts if b in KIT_ITEMS])
    receiver = Compound([cradle_local(), receptacle_local(), pack_local(), cradle_parts()["adapter"]])
    asm = Compound([s for _, s, _, _, _ in parts])
    for name, shape in (("sunspoke-kit", kit), ("sunspoke-cradle-with-pack", receiver), ("sunspoke-assembly", asm)):
        export_step(shape, str(root / "step" / f"{name}.step"))
        export_stl(shape, str(root / "stl" / f"{name}.stl"), tolerance=0.2, angular_tolerance=0.3)
        bb = shape.bounding_box()
        print(f"{name:26s} {bb.size.X:7.1f} x {bb.size.Y:7.1f} x {bb.size.Z:7.1f} mm")
    f = fit_checks()
    print(f"down tube length {f['dt_len']:.0f} mm")
    print(f"pack clearance to top tube, seat tube and head tube {f['clearance']:.0f} mm")
    print(f"free travel along the down tube for removal {f['travel']:.0f} mm (needed {f['travel_needed']:.0f} mm)")
    print(f"slide-out overlap {f['slide_overlap']:.2f} mm3; lift-out clear: {f['lift_ok']}")
