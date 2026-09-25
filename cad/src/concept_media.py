"""SunSpoke concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Coordinates in mm. The bicycle lies in the XZ plane (X forward, Z up, Y across the bike),
rear axle at X = 0, ground at Z = 0. The donor bicycle is grey; kit parts are colored.
"""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Torus, Pos, Rot, Solid, Plane, Vector
from concept import Part, render_all

# Donor bicycle: 28 in (ETRTO 635) steel roadster, about 1,150 mm wheelbase
WHEEL_R = 355.0            # tyre outer radius
WB = 1150.0                # wheelbase
REAR = (0.0, WHEEL_R)      # rear axle (x, z)
FRONT = (WB, WHEEL_R)      # front axle
BB = (430.0, 290.0)        # bottom bracket
SEAT_TOP = (225.0, 815.0)  # seat cluster
HEAD_BOT = (1030.0, 690.0)
HEAD_TOP = (975.0, 840.0)
TUBE_R = 14.0              # frame tube radius (28.6 mm tubes)

FRAME = "#6B7280"
TYRE = "#1F2937"
KIT_ACCENT = "#0F766E"


def tube(p1, p2, r, y=0.0):
    """Round tube between two (x, z) points at lateral offset y."""
    a = Vector(p1[0], y, p1[1]); b = Vector(p2[0], y, p2[1])
    d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def tube3(a, b, r):
    """Round tube between two 3D points."""
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def wheel(cx, cz):
    tyre = Pos(cx, 0, cz) * Rot(90, 0, 0) * Torus(WHEEL_R - 20, 20)
    rim = Pos(cx, 0, cz) * Rot(90, 0, 0) * (Cylinder(WHEEL_R - 38, 20) - Cylinder(WHEEL_R - 52, 22))
    spokes = None
    for k in range(12):
        t = math.radians(k * 30)
        s = tube3((cx, 0, cz), (cx + (WHEEL_R - 50) * math.cos(t), 0, cz + (WHEEL_R - 50) * math.sin(t)), 2.0)
        spokes = s if spokes is None else spokes + s
    return tyre + rim + spokes


def along(p1, p2, t):
    return (p1[0] + (p2[0] - p1[0]) * t, p1[1] + (p2[1] - p1[1]) * t)


# ---------------- donor bicycle (grey, no BOM number) ----------------
frame = (tube(BB, SEAT_TOP, TUBE_R) + tube(SEAT_TOP, HEAD_TOP, TUBE_R) + tube(BB, HEAD_BOT, TUBE_R + 2)
         + tube(HEAD_BOT, HEAD_TOP, 18)
         + tube(BB, REAR, 9, 45) + tube(BB, REAR, 9, -45)
         + tube(SEAT_TOP, REAR, 8, 45) + tube(SEAT_TOP, REAR, 8, -45)
         + tube((210, 850), (205, 900), 13))                              # seat post
fork = (tube(HEAD_BOT, FRONT, 11, 50) + tube(HEAD_BOT, FRONT, 11, -50)
        + tube((HEAD_BOT[0], HEAD_BOT[1]), (HEAD_BOT[0] + 5, HEAD_BOT[1] + 5), 20))
fork = fork + Pos(HEAD_BOT[0], 0, HEAD_BOT[1]) * Box(40, 110, 20)       # fork crown
stem = tube(HEAD_TOP, (950, 960), 12)
bars = (tube3((950, -300, 960), (950, 300, 960), 11)
        + tube3((950, 300, 960), (820, 330, 945), 11) + tube3((950, -300, 960), (820, -330, 945), 11))
saddle = Pos(200, 0, 925) * Box(260, 150, 55)
carrier = (Pos(-60, 0, 800) * Box(420, 170, 12)
           + tube3((-230, 60, 795), (0, 60, WHEEL_R), 6) + tube3((-230, -60, 795), (0, -60, WHEEL_R), 6))
cranks = (tube3((BB[0], -75, BB[1]), (BB[0] + 60, -75, BB[1] - 160), 9)
          + tube3((BB[0], 75, BB[1]), (BB[0] - 60, 75, BB[1] + 160), 9)
          + Pos(BB[0], 45, BB[1]) * Rot(90, 0, 0) * Cylinder(100, 5))
bike = frame + fork + stem + bars + saddle + carrier + cranks
wheels = wheel(*REAR) + wheel(*FRONT)

# ---------------- kit parts ----------------
# 1 Front hub motor (geared, 250 W), laced into the donor-size 28 in rim
motor = Pos(FRONT[0], 0, FRONT[1]) * Rot(90, 0, 0) * Cylinder(80, 72)

# 2 Torque arms, one each side, clamped to the fork blades
fork_dir = (HEAD_BOT[0] - FRONT[0], HEAD_BOT[1] - FRONT[1])
fl = math.hypot(*fork_dir)
arm_end = (FRONT[0] + fork_dir[0] / fl * 130, FRONT[1] + fork_dir[1] / fl * 130)
torque_arms = (tube(FRONT, arm_end, 9, 64) + tube(FRONT, arm_end, 9, -64)
               + tube3((arm_end[0], 72, arm_end[1]), (arm_end[0], 40, arm_end[1]), 12)
               + tube3((arm_end[0], -72, arm_end[1]), (arm_end[0], -40, arm_end[1]), 12))

# Down tube geometry for the pack cradle
dt_ang = math.degrees(math.atan2(HEAD_BOT[1] - BB[1], HEAD_BOT[0] - BB[0]))
ux, uz = math.cos(math.radians(dt_ang)), math.sin(math.radians(dt_ang))
nx, nz = -uz, ux                       # normal pointing up and back, into the main triangle
mid = along(BB, HEAD_BOT, 0.52)


def on_downtube(offset_n, offset_u=0.0):
    return (mid[0] + nx * offset_n + ux * offset_u, mid[1] + nz * offset_n + uz * offset_u)


# 4 SwapCell receiver cradle with two hose-clamp style band mounts (no welding)
c = on_downtube(TUBE_R + 2 + 12)
cradle = Pos(c[0], 0, c[1]) * Rot(0, -dt_ang, 0) * (Box(380, 104, 16)
                                                     + Pos(-186, 0, 30) * Box(12, 104, 60))  # lower end stop
bands = None
for du in (-110, 110):
    b = on_downtube(0, du)
    band = Pos(b[0], 0, b[1]) * Rot(0, -dt_ang, 0) * Rot(0, 90, 0) * (Cylinder(TUBE_R + 8, 22) - Cylinder(TUBE_R + 3, 24))
    bands = band if bands is None else bands + band
cradle = cradle + bands

# 5 Host adapter (CAN heartbeat and interlock), sealed box at the cradle's upper end
h = on_downtube(TUBE_R + 2 + 30, 215)
adapter = Pos(h[0], 0, h[1]) * Rot(0, -dt_ang, 0) * Box(50, 70, 35)

# 6 SwapCell pack, 340 x 90 x 80 mm, on the cradle inside the main triangle
p = on_downtube(TUBE_R + 2 + 20 + 40)
pack = Pos(p[0], 0, p[1]) * Rot(0, -dt_ang, 0) * Box(340, 90, 80)

# 3 Controller, sealed box on the seat tube
st = along(BB, SEAT_TOP, 0.38)
st_ang = math.degrees(math.atan2(SEAT_TOP[1] - BB[1], SEAT_TOP[0] - BB[0]))
controller = Pos(st[0] + 42, 0, st[1]) * Rot(0, -st_ang, 0) * Box(150, 62, 42)

# 7 Pedal-assist sensor ring on the left crank axle
pas = Pos(BB[0], -58, BB[1]) * Rot(90, 0, 0) * (Cylinder(38, 8) - Cylinder(18, 10))

# 8 Handlebar control unit and brake cut-off sensors
hbar = (Pos(950, -120, 975) * Box(55, 45, 30)
        + Pos(860, -318, 950) * Box(35, 22, 22) + Pos(860, 318, 950) * Box(35, 22, 22))

# 9 Wiring harness: controller to motor along the down tube and fork, plus a branch to the bars
w_lo = (st[0] + 80, -30, st[1] - 60)
w_bb = (BB[0] + 60, -30, BB[1] + 60)
w_hd = (HEAD_BOT[0] - 20, -30, HEAD_BOT[1] - 10)
w_ax = (FRONT[0] - 10, -60, FRONT[1] + 40)
harness = (tube3(w_lo, w_bb, 5) + tube3(w_bb, w_hd, 5) + tube3(w_hd, w_ax, 5)
           + tube3(w_hd, (HEAD_TOP[0] - 10, -30, HEAD_TOP[1] + 60), 5)
           + tube3((HEAD_TOP[0] - 10, -30, HEAD_TOP[1] + 60), (950, -120, 960), 5))

# 10 to 12 Solar charging set, standing ahead of the bike (100 W panel about 1,000 x 670 mm)
PX, PY, TILT = 2250.0, 0.0, 15.0
panel = Pos(PX, PY, 620) * Rot(0, TILT, 0) * Box(670, 1000, 35)
stand = None
for dx, zt in ((-300, 700), (300, 540)):
    for dy in (-440, 440):
        leg = tube3((PX + dx, PY + dy, 0), (PX + dx * 0.95, PY + dy, zt), 14)
        stand = leg if stand is None else stand + leg
stand = stand + tube3((PX - 300, PY - 440, 150), (PX + 300, PY - 440, 150), 10) \
              + tube3((PX - 300, PY + 440, 150), (PX + 300, PY + 440, 150), 10)
charger = Pos(PX + 20, PY - 440 - 60, 360) * Box(120, 70, 45)
charge_cable = (tube3((PX + 20, PY - 520, 340), (PX - 300, -200, 40), 4)
                + tube3((PX - 300, -200, 40), (c[0] + 60, -200, 40), 4)
                + tube3((c[0] + 60, -200, 40), (c[0], -40, c[1] - 40), 4))

parts = [
    Part("Donor roadster frame, fork and bars", bike, FRAME, None),
    Part("Donor wheels", wheels, TYRE, None),
    Part("Front hub motor, 250 W geared", motor, KIT_ACCENT, 1, (260, -300, 0)),
    Part("Torque arms (pair)", torque_arms, "#D4A017", 2, (380, -520, 200)),
    Part("Controller, sealed", controller, "#115E59", 3, (-120, -480, -40)),
    Part("SwapCell receiver cradle and clamps", cradle, "#94A3B8", 4, (0, -300, 170)),
    Part("Host adapter (CAN, interlock)", adapter, "#7C3AED", 5, (140, -560, 360)),
    Part("SwapCell pack (not in kit cost)", pack, "#C2410C", 6, (-140, -120, 420)),
    Part("Pedal-assist sensor", pas, "#0EA5E9", 7, (0, -360, -60)),
    Part("Handlebar control and brake cut-off", hbar, "#2563EB", 8, (160, -120, 300)),
    Part("Wiring harness with fuse", harness, "#111827", 9, (0, -300, -260)),
    Part("Solar panel, 100 W", panel, "#1E3A8A", 10, (-600, -2600, -300)),
    Part("Boost MPPT charger", charger, "#16A34A", 11, (-600, -2900, -700)),
    Part("Panel stand (local make)", stand, "#A16207", 12, (-600, -2600, -700)),
    Part("Charge cable", charge_cable, "#374151", 13, (500, -900, -450)),
]

render_all(
    parts, project="SunSpoke", title="Roadster conversion kit concept", dwg_no="SSP-DWG-010",
    key_figures=["250 W geared front hub motor, 48 V class (proposed)",
                 "SwapCell pack about 468 Wh; about 35 km loaded (estimate)",
                 "100 W panel: about 315 Wh/day stored at 4.5 sun hours (estimate)",
                 "Torque arms both sides; no welding or frame drilling",
                 "Kit about $260 with solar set, pack excluded (indicative)"],
    cut=False,
    flow={"title": "daily solar energy flow, Wh per day (estimates, 4.5 peak sun hours)", "unit": "Wh",
          "stages": [("Sun on 100 W panel", 450), ("Panel output", 360), ("Charger output", 331),
                     ("Stored in pack", 315), ("Pack output", 305), ("At the wheel", 229)],
          "losses": [(0, "Heat, dust, wiring (20 %)", 90), (1, "Boost MPPT (8 %)", 29),
                     (2, "Cell charging (5 %)", 17), (3, "Pack resistance (3 %)", 9),
                     (4, "Controller and motor (25 %)", 76)]},
)
