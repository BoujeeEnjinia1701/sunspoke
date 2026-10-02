"""SunSpoke sizing calculations for SSP-CAL-001 (TRL 3).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number quoted in docs/04-calcs/01-sizing.md and writes
docs/04-calcs/results.csv with the requirement status table.

First-principles estimates on paper. Every input is an assumption stated below;
nothing here is measured. SwapCell values follow SwapCell interface v0.3 and
SWC-CAL-001 (swapcell repo).
"""
import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
G = 9.81
RHO_AIR = 1.2

# ---------------------------------------------------------------- assumptions
# Design load case (SSP-REQ-001)
RIDER, CARGO, BIKE = 75.0, 25.0, 22.0          # kg

# Kit mass (kg), estimates; pack from SWC-CAL-001
KIT_MASS = {
    "Motor wheel, increase over the donor front wheel": 1.20,
    "Torque arms (pair) and band clamps": 0.28,
    "Controller, rubber pad and two band clamps": 0.55,
    "SwapCell receiver cradle, three band clamps, gate and draw latch": 1.10,
    "Host adapter and charge port": 0.15,
    "Pedal-assist sensor": 0.10,
    "Handlebar control and brake sensors": 0.15,
    "Wiring harness and fuse": 0.40,
}
PACK_MASS = 2.85                                # kg, SWC-CAL-001

# SwapCell pack (SWC-CAL-001, interface v0.3)
PACK_WH_NOM = 466.0          # Wh at 0.2C, nominal cells
PACK_WH_MIN = 452.0          # Wh at 0.2C, cells at datasheet minimum
PACK_V = 46.8
PACK_R = 0.110               # ohm
USABLE = 0.90                # usable window (10 to 100 %)
LEGACY_A = 15.0              # A, legacy discharge-only limit (no heartbeat)
PACK_CHG_LIMIT_A = 5.0       # A, standard allowed charge current

# Road and rider
CRR = 0.020                  # dry dirt road
CDA = 0.60                   # m^2
V_CRUISE = 18.0              # km/h
ALLOW = 1.30                 # hills, rough surface, stop-start
P_RIDER_CRUISE = 70.0        # W
P_RIDER_CLIMB = 80.0         # W
ETA_DRIVE = 0.75             # motor plus controller, cruise
WHEEL_R = 0.355              # m, 28 in (ETRTO 635) tyre outer radius
ASSIST_LIMIT = 20.0          # km/h, decided default (SSP-DDR-001)

CASES = {  # name: (cargo kg, Crr, allowance, speed km/h)
    "Design (25 kg cargo, dirt)": (25.0, 0.020, 1.30, 18.0),
    "Light (no cargo, graded murram)": (0.0, 0.015, 1.20, 18.0),
    "Heavy (80 kg cargo, rough dirt)": (80.0, 0.025, 1.30, 15.0),
}

# Hill (R3)
GRADE = 0.08
V_CLIMB = 8.0                # km/h
CLIMB_LEN = 500.0            # m
T_AMB_HOT = 35.0             # C
# Motor model: 250 W geared hub, 48 V, slow winding (about 200 rpm no-load at 48 V)
NOLOAD_RPM = 200.0
GEAR_EFF = 0.90
R_WIND = 0.45                # ohm, line to line, warm
P_IRON = 15.0                # W, iron, gear and bearing losses (assumption)
C_TH = 600.0                 # J/K, stator and winding heat capacity
R_TH = 1.2                   # K/W, winding to ambient while riding
T_WIND_LIMIT = 120.0         # C, practical limit for small geared hubs with nylon gears
MOTOR_PEAK_NM = 40.0         # N m at the wheel, typical 250 W geared hub
# Thermal derate on the motor thermistor (SSP-DDR-002, decided 2026-09-25)
T_DERATE_START = 110.0       # C, controller starts reducing current

# Solar (R8)
PANEL_W, SUN_H, SUN_H_LOW, DERATE = 100.0, 4.5, 4.0, 0.80
ETA_MPPT, ETA_CELL_CHG, ETA_PACK_OUT = 0.92, 0.95, 0.97
CHARGE_V = 50.0              # V, mid-charge pack voltage
LOAD_ON_W = 4.0              # W, display and lights while charging in mode 4

# Fork and torque arms (R10)
FLAT_LEVER = 0.005           # m, effective lever of the axle flats on each dropout
ARM_LEVER = 0.130            # m, axle to torque arm clamp
ARM_W, ARM_T = 20.0, 5.0     # mm plate width and thickness
STEEL_YIELD = 250.0          # MPa, mild steel
MOTOR_FLATS = 10.0           # mm across flats
DROPOUT_SLOT = 9.53          # mm, 3/8 in roadster slot (assumption, to survey)

# Cradle retention (interface v0.3 item V, class V1), constructable design (SSP-DDR-003):
# three band clamps, each through two slots in the tray, round a 120 degree V-saddle and the tube
CRADLE_MASS = 1.10           # kg, from the model volumes plus bought parts (SSP-DDR-003)
N_BANDS = 3
V_HALF = math.radians(60.0)  # half angle of the V-saddle, from the vertical
LINER = 1.5                  # mm, rubber liner in the V
SADDLE_HALF_W, SADDLE_H, SADDLE_LAND = 17.5, 12.0, 4.0   # mm
RECEIVER_DESIGN_PACK = 3.5   # kg, SwapCell receiver design mass
VIB_G, SHOCK_G = 8.0, 25.0
BAND_T = 1500.0              # N, worm-drive band tension at 3 to 4 N m screw torque
MU_LINER = 0.40              # rubber liner on painted steel
TUBE_R = 0.0143              # m, 28.6 mm down tube
CG_OFFSET = 0.077            # m, pack plus cradle centroid above the down tube axis (70 mm, plus 7 mm for the V-saddles)
HAND_F = 50.0                # N
PRELOAD = 330.0              # N, SwapCell V1 receiver preload

# Braking (R11)
V_BRAKE = 20.0               # km/h
T_APPLY = 0.5                # s, lever travel and linkage delay
STOP_TARGET = 9.0            # m
PAD_N = 250.0                # N clamp per pad from a 100 N hand force on rod levers
MU_DRY, MU_WET = 0.40, 0.12  # block on steel rim
R_RIM = 0.310                # m, braking surface radius

# INTERLOCK wake (item W)
V_SLEEP, R_PULLUP, R_CODE = 3.3, 100e3, 10e3

OUT = {}


def put(key, value, fmt="{:.2f}"):
    OUT[key] = value
    print(f"  {key:58s} {fmt.format(value)}")


def section(t):
    print(f"\n== {t}")


def road_force(m, crr, v_kmh, grade=0.0):
    v = v_kmh / 3.6
    th = math.atan(grade)
    return (m * G * math.sin(th), crr * m * G * math.cos(th), 0.5 * RHO_AIR * CDA * v * v)


# ---------------------------------------------------------------- mass
section("Mass (R6)")
kit = sum(KIT_MASS.values())
added = kit + PACK_MASS
m_design = RIDER + CARGO + BIKE + added
put("Kit mass without pack, kg", kit)
put("Added mass with pack, kg", added)
put("Design load case total, kg", m_design)
put("R6 margin to 7 kg, kg", 7.0 - added)

# ---------------------------------------------------------------- energy and range
section("Energy per km and range (R2)")
usable_nom = PACK_WH_NOM * USABLE
usable_min = PACK_WH_MIN * USABLE
put("Usable pack energy, nominal cells, Wh", usable_nom, "{:.0f}")
put("Usable pack energy, minimum cells, Wh", usable_min, "{:.0f}")
ranges = {}
for name, (cargo, crr, allow, v) in CASES.items():
    m = RIDER + cargo + BIKE + added
    _, fr, fd = road_force(m, crr, v)
    road = (fr + fd) * 1000 / 3600 * allow           # Wh/km at the wheel
    rider = P_RIDER_CRUISE / v                        # Wh/km
    pack = max(road - rider, 0) / ETA_DRIVE
    rng = usable_nom / pack
    ranges[name] = (pack, rng)
    print(f"  {name}: mass {m:.1f} kg, rolling {fr:.1f} N, drag {fd:.1f} N, wheel {road:.2f} Wh/km, "
          f"rider {rider:.2f} Wh/km, pack {pack:.2f} Wh/km, range {rng:.0f} km")
e_design = ranges["Design (25 kg cargo, dirt)"][0]
put("Pack energy, design case, Wh/km", e_design)
put("Range, design case, nominal cells, km", usable_nom / e_design, "{:.1f}")
put("Range, design case, minimum cells, km", usable_min / e_design, "{:.1f}")
put("Range, light case, km", ranges["Light (no cargo, graded murram)"][1], "{:.0f}")
put("Range, heavy case, km", ranges["Heavy (80 kg cargo, rough dirt)"][1], "{:.0f}")
p_cruise = e_design * V_CRUISE
i_cruise = p_cruise / PACK_V
put("Mean pack power, design cruise, W", p_cruise, "{:.0f}")
put("Mean pack current, design cruise, A", i_cruise, "{:.1f}")
put("Pack heat at cruise current, W", i_cruise ** 2 * PACK_R, "{:.1f}")
put("Controller limit as pack current, A (legacy limit 15 A)", LEGACY_A, "{:.0f}")
put("Pack heat at 15 A, W", LEGACY_A ** 2 * PACK_R, "{:.1f}")

# ---------------------------------------------------------------- hill and motor heating
section("Hill climb and motor heating (R3)")
fg, fr, fd = road_force(m_design, CRR, V_CLIMB, GRADE)
f_hill = fg + fr + fd
v = V_CLIMB / 3.6
p_wheel = f_hill * v
p_motor = p_wheel - P_RIDER_CLIMB
omega = v / WHEEL_R
t_wheel = f_hill * WHEEL_R
t_motor = p_motor / omega
ke = 48.0 / (NOLOAD_RPM * 2 * math.pi / 60)       # V s/rad at the wheel
i_ph = t_motor / (ke * GEAR_EFF)
p_cu = i_ph ** 2 * R_WIND
p_loss = p_cu + P_IRON
eta_hill = p_motor / (p_motor + p_loss)
put("Grade force, N", fg, "{:.1f}")
put("Rolling force, N", fr, "{:.1f}")
put("Drag force at 8 km/h, N", fd, "{:.1f}")
put("Total force on 8 % grade, N", f_hill, "{:.1f}")
put("Power at the wheel, W", p_wheel, "{:.0f}")
put("Motor mechanical power (rider 80 W), W", p_motor, "{:.0f}")
put("Wheel torque, N m", t_wheel, "{:.1f}")
put("Motor torque, N m", t_motor, "{:.1f}")
put("Motor torque as share of assumed 40 N m peak, %", 100 * t_motor / MOTOR_PEAK_NM, "{:.0f}")
put("Motor current, A", i_ph, "{:.1f}")
put("Motor losses on the climb, W", p_loss, "{:.0f}")
put("Motor efficiency on the climb, %", 100 * eta_hill, "{:.0f}")
put("Pack current on the climb, A", (p_motor + p_loss) / 0.95 / PACK_V, "{:.1f}")
# Cruise winding temperature, then adiabatic climb
v_c = V_CRUISE / 3.6
p_mech_c = (e_design * ETA_DRIVE) * V_CRUISE      # W at the wheel from the motor
i_c = p_mech_c / (v_c / WHEEL_R) / (ke * GEAR_EFF)
p_loss_c = i_c ** 2 * R_WIND + P_IRON
t_start = T_AMB_HOT + p_loss_c * R_TH
t_climb = CLIMB_LEN / v
tau = C_TH * R_TH
t_ss = T_AMB_HOT + p_loss * R_TH
t_end = t_ss - (t_ss - t_start) * math.exp(-t_climb / tau)
t_allow = -tau * math.log((t_ss - T_WIND_LIMIT) / (t_ss - t_start)) if t_ss > T_WIND_LIMIT else float("inf")
put("Motor losses at cruise, W", p_loss_c, "{:.0f}")
put("Winding temperature at cruise, 35 C ambient, C", t_start, "{:.0f}")
put("Climb duration, s", t_climb, "{:.0f}")
put("Winding temperature at the top of 500 m, C", t_end, "{:.0f}")
put("Margin to 120 C, K", T_WIND_LIMIT - t_end, "{:.0f}")
put("Climb length to reach 120 C at 8 km/h, m", t_allow * v, "{:.0f}")
# Sensitivity: winding resistance 0.60 ohm, heat capacity 450 J/K, 1.5 K/W (smaller, hotter hub)
r2, c2, th2 = 0.60, 450.0, 1.5
pl2 = i_ph ** 2 * r2 + P_IRON
ts2 = T_AMB_HOT + (i_c ** 2 * r2 + P_IRON) * th2
tss2 = T_AMB_HOT + pl2 * th2
te2 = tss2 - (tss2 - ts2) * math.exp(-t_climb / (c2 * th2))
put("Sensitivity: winding at top of 500 m (0.60 ohm, 450 J/K, 1.5 K/W), C", te2, "{:.0f}")
# Thermal derate (SSP-DDR-002): distance to the derate threshold, and the
# sustained speed on an unending 8 % climb with the winding held at 120 C.
def derate(r_w, c_th, r_th, t0):
    t_ss_ = T_AMB_HOT + (i_ph ** 2 * r_w + P_IRON) * r_th
    t_on = (-c_th * r_th * math.log((t_ss_ - T_DERATE_START) / (t_ss_ - t0))
            if t_ss_ > T_DERATE_START else float("inf"))
    p_cu_ok = (T_WIND_LIMIT - T_AMB_HOT) / r_th - P_IRON
    i_ok = math.sqrt(max(p_cu_ok, 0.0) / r_w)
    f_motor = min(i_ok, i_ph) * ke * GEAR_EFF / WHEEL_R
    lo_, hi_ = 0.5, 30.0
    for _ in range(60):
        mid_ = (lo_ + hi_) / 2
        need = sum(road_force(m_design, CRR, mid_, GRADE))
        lo_, hi_ = (mid_, hi_) if f_motor + P_RIDER_CLIMB / (mid_ / 3.6) > need else (lo_, mid_)
    return t_on * v, i_ok, lo_
d_base, i_base, v_base = derate(R_WIND, C_TH, R_TH, t_start)
d_hot, i_hot, v_hot = derate(r2, c2, th2, ts2)
put("Derate: climb length to 110 C, base case, m", min(d_base, 99999), "{:.0f}")
put("Derate: climb length to 110 C, hot case, m", d_hot, "{:.0f}")
put("Derate: sustained motor current at 120 C, base case, A", i_base, "{:.1f}")
put("Derate: sustained motor current at 120 C, hot case, A", i_hot, "{:.1f}")
put("Derate: sustained speed on 8 % at 120 C, base case, km/h", v_base, "{:.1f}")
put("Derate: sustained speed on 8 % at 120 C, hot case, km/h", v_hot, "{:.1f}")
# Speed on a 10 % grade with 250 W motor plus 80 W rider
lo, hi = 1.0, 30.0
for _ in range(60):
    mid = (lo + hi) / 2
    f = sum(road_force(m_design, CRR, mid, 0.10))
    lo, hi = (mid, hi) if f * mid / 3.6 < 330.0 else (lo, mid)
put("Speed on a 10 % grade at 330 W, km/h", lo, "{:.1f}")

# ---------------------------------------------------------------- solar
section("Solar charging (R8) and charge-discharge mode (item C)")
for label, h in (("mid", SUN_H), ("low", SUN_H_LOW)):
    panel = PANEL_W * h * DERATE
    chg = panel * ETA_MPPT
    stored = chg * ETA_CELL_CHG
    out = stored * ETA_PACK_OUT
    put(f"Panel output, {label} ({h} h), Wh/day", panel, "{:.0f}")
    put(f"Charger output, {label}, Wh/day", chg, "{:.0f}")
    put(f"Stored in pack, {label}, Wh/day", stored, "{:.0f}")
    put(f"Pack output, {label}, Wh/day", out, "{:.0f}")
    put(f"Daily loaded range, {label}, km", out / e_design, "{:.1f}")
    put(f"Days to recharge 10 to 100 %, {label}", 0.9 * 468.0 / stored, "{:.2f}")
p_chg_peak = PANEL_W * DERATE * ETA_MPPT
i_chg = p_chg_peak / CHARGE_V
i_net = i_chg - LOAD_ON_W / PACK_V
put("Peak charge power into pack, W", p_chg_peak, "{:.0f}")
put("Peak charge current, A", i_chg, "{:.2f}")
put("Peak charge rate, C", i_chg / 10.0, "{:.2f}")
put("Net charge current in mode 4 with 4 W load, A", i_net, "{:.2f}")
put("Share of 5 A standard charge limit, %", 100 * i_net / PACK_CHG_LIMIT_A, "{:.0f}")
# Figure 2 flow diagram values (mid case)
flow = [PANEL_W * SUN_H, PANEL_W * SUN_H * DERATE]
flow += [flow[-1] * ETA_MPPT, flow[-1] * ETA_MPPT * ETA_CELL_CHG]
flow += [flow[-1] * ETA_PACK_OUT, flow[-1] * ETA_PACK_OUT * ETA_DRIVE]
print("  Flow stages, Wh/day:", ", ".join(f"{x:.0f}" for x in flow))

# ---------------------------------------------------------------- INTERLOCK wake
section("INTERLOCK wake (item W)")
node = V_SLEEP * R_CODE / (R_CODE + R_PULLUP)
put("INTERLOCK node with 10 kOhm coding resistor, V", node)
put("Loop current, uA", V_SLEEP / (R_CODE + R_PULLUP) * 1e6, "{:.0f}")

# ---------------------------------------------------------------- fork and torque arms
section("Fork dropouts and torque arms (R4, R10)")
t_peak = MOTOR_PEAK_NM
f_dropout = (t_peak / 2) / FLAT_LEVER
f_arm_total = t_peak / ARM_LEVER
m_arm = (t_peak / 2) / ARM_LEVER * ARM_LEVER      # N m at the axle end of one arm
z = ARM_T * ARM_W ** 2 / 6
sig = m_arm * 1000 / z
put("Peak motor reaction torque, N m", t_peak, "{:.0f}")
put("Climb reaction torque, N m", t_motor, "{:.1f}")
put("Force on each dropout face without arms, N", f_dropout, "{:.0f}")
put("Force at the arm clamps, total, N", f_arm_total, "{:.0f}")
put("Force per arm clamp, N", f_arm_total / 2, "{:.0f}")
put("Arm bending stress at the axle, MPa", sig, "{:.0f}")
put("Arm safety factor on yield", STEEL_YIELD / sig, "{:.1f}")
put("Slot filing needed per side, mm", (MOTOR_FLATS - DROPOUT_SLOT) / 2, "{:.2f}")

# ---------------------------------------------------------------- cradle retention
section("Cradle retention, latch class V1 (item V)")
m_ret = RECEIVER_DESIGN_PACK + CRADLE_MASS
f_vib = m_ret * VIB_G * G
f_shock = m_ret * SHOCK_G * G
# Normal force each band puts on the tube: its own wrap on the underside of the tube, plus the
# V-saddle pressed down by the band's two legs (a 120 degree V gives 1/cos(30 deg) of that load).
r_mm = TUBE_R * 1000
apex = (r_mm + LINER) / math.sin(V_HALF)
sad_bot = apex + SADDLE_LAND - SADDLE_H
px, pz = SADDLE_HALF_W, sad_bot                  # the saddle's lower corner, where the band leaves it
d = math.hypot(px, pz)
th_t = math.atan2(pz, px) - math.acos(r_mm / d)  # where the band leaves the tube (from horizontal)
wrap = math.pi + 2 * th_t
tx, tz = r_mm * math.cos(th_t), r_mm * math.sin(th_t)
leg = math.hypot(px - tx, pz - tz)
w_saddle = 2 * (pz - tz) / leg                   # downward pull on the saddle, per unit band tension
n_factor = wrap + w_saddle / math.cos(math.pi / 2 - V_HALF)
f_band = MU_LINER * n_factor * BAND_T
cap_axial = N_BANDS * f_band
cap_rot = N_BANDS * f_band * TUBE_R
put("Band wrap on the tube (each band), degrees", math.degrees(wrap), "{:.0f}")
put("Normal force on the tube per unit band tension", n_factor)
put("Retained mass (3.5 kg pack plus cradle), kg", m_ret)
put("Load at 8 g, N", f_vib, "{:.0f}")
put("Load at 25 g, N", f_shock, "{:.0f}")
put("Axial slip capacity of three band clamps, N", cap_axial, "{:.0f}")
put("Axial margin at 25 g", cap_axial / f_shock, "{:.1f}")
put("Rotation moment at 25 g lateral, N m", f_shock * CG_OFFSET, "{:.0f}")
put("Rotation capacity of three band clamps, N m", cap_rot, "{:.0f}")
put("Rotation margin at 25 g lateral", cap_rot / (f_shock * CG_OFFSET), "{:.2f}")
put("Over-centre lever ratio for 330 N at 50 N", PRELOAD / HAND_F, "{:.1f}")
# Drop-down gate: hinged 2.5 mm above the tray, pad centre 19.5 mm above the hinge, latch 20.5 mm above
put("Draw latch pull for 330 N preload, N", PRELOAD * 19.5 / 20.5, "{:.0f}")
# End stop at 25 g: the pack bears on the wall round the plug notch; the 16 mm columns beside the
# notch are held along the side flanges and the 25 mm strip below it along the foot (cantilevers)
STOP_T, AL_YIELD = 3.0, 193.0                    # mm; MPa, 5052-H32
area = 92 * 72 - 60 * 47                         # wall less the open-topped notch, mm2
q = f_shock / area
sig_col = 6 * (q * 16 ** 2 / 2) / STOP_T ** 2
sig_low = 6 * (q * 25 ** 2 / 2) / STOP_T ** 2
put("End stop bearing pressure at 25 g, MPa", q, "{:.3f}")
put("End stop bending stress at 25 g, worst strip, MPa", max(sig_col, sig_low), "{:.0f}")
put("End stop safety factor on yield at 25 g", AL_YIELD / max(sig_col, sig_low), "{:.1f}")

# ---------------------------------------------------------------- braking
section("Braking (R11)")
vb = V_BRAKE / 3.6
d_react = vb * T_APPLY
a_need = vb ** 2 / (2 * (STOP_TARGET - d_react))
res = {}
for label, mu in (("dry", MU_DRY), ("wet", MU_WET)):
    f = 2 * (2 * mu * PAD_N * R_RIM / WHEEL_R)       # two wheels, two pads each
    a = f / m_design
    d = d_react + vb ** 2 / (2 * a)
    res[label] = (a, d)
    put(f"Deceleration, both rod brakes, {label}, m/s2", a)
    put(f"Stopping distance from 20 km/h, {label}, m", d, "{:.1f}")
put("Distance during 0.5 s application, m", d_react)
put("Deceleration needed for 9 m, m/s2", a_need)
put("Dry margin on deceleration, %", 100 * (res["dry"][0] / a_need - 1), "{:.0f}")
ke20 = 0.5 * m_design * vb ** 2
ke13 = 0.5 * (RIDER + CARGO + BIKE) * (13 / 3.6) ** 2
put("Kinetic energy at 20 km/h, J", ke20, "{:.0f}")
put("Kinetic energy, unconverted bike at 13 km/h, J", ke13, "{:.0f}")
put("Ratio", ke20 / ke13, "{:.1f}")
v25 = 25 / 3.6
put("Dry stopping distance from 25 km/h, m", v25 * T_APPLY + v25 ** 2 / (2 * res["dry"][0]), "{:.1f}")

# ---------------------------------------------------------------- cost
section("Cost (R12) from bom/bom.csv")
rows = list(csv.DictReader((ROOT / "bom/bom.csv").open()))
num = lambda r: int(r["item"].split()[0])
BIKE_KIT = {1, 2, 3, 4, 5, 7, 8, 9, 14}
SOLAR = {10, 11, 12, 13}
cost = {num(r): float(r["qty"]) * float(r["unit_cost_usd"]) for r in rows}
bike_kit = sum(v for k, v in cost.items() if k in BIKE_KIT)
solar = sum(v for k, v in cost.items() if k in SOLAR)
generic = sum(cost[num(r)] for r in rows if num(r) in BIKE_KIT | SOLAR and "generic" in r["notes"].lower())
put("Bike conversion kit (1-5, 7-9, 14), USD", bike_kit, "{:.0f}")
put("Solar charging set (10-13), USD", solar, "{:.0f}")
put("Kit plus solar set, pack excluded, USD", bike_kit + solar, "{:.0f}")
put("SwapCell pack, priced in SwapCell, USD", cost[6], "{:.0f}")
put("Full system for one rider, USD", bike_kit + solar + cost[6], "{:.0f}")
put("Bike kit under the USD 250 value-engineering target by, USD", 250 - bike_kit, "{:.0f}")
put("Generic share of kit plus solar cost, %", 100 * generic / (bike_kit + solar), "{:.0f}")

# ---------------------------------------------------------------- results table
R = OUT
results = [
    ("R3", f"{R['Winding temperature at the top of 500 m, C']:.0f} °C winding at the top of 500 m from 35 °C "
           f"({R['Sensitivity: winding at top of 500 m (0.60 ohm, 450 J/K, 1.5 K/W), C']:.0f} °C in the hot case); "
           f"{R['Motor torque, N m']:.1f} N·m motor torque; {R['Motor mechanical power (rider 80 W), W']:.0f} W motor; "
           f"hot case derates after {R['Derate: climb length to 110 C, hot case, m']:.0f} m",
     "8 % for 500 m at 8 km/h at 35 °C; thermistor derate from 110 °C, no cutout", "At risk"),
    ("R4", f"Slot filing about {R['Slot filing needed per side, mm']:.2f} mm per side on a 9.53 mm slot; fitting time not calculable",
     "No fabrication; 90 min or less", "At risk"),
    ("R11", f"{R['Stopping distance from 20 km/h, dry, m']:.1f} m dry ({R['Dry margin on deceleration, %']:.0f} % margin); "
            f"{R['Stopping distance from 20 km/h, wet, m']:.1f} m wet",
     "9 m or less from 20 km/h, dry dirt", "At risk"),
    ("R7", "IP ratings by part selection only", "IP65 electronics, IP54 motor, 150 mm water, 0 to 45 °C", "Not verifiable at TRL 3"),
    ("R9", f"Generic parts {R['Generic share of kit plus solar cost, %']:.0f} % of kit cost; swap time not calculable",
     "Pluggable joints, 20 min swap, 70 % generic", "Not verifiable at TRL 3"),
    ("R10", f"Arm clamp {R['Force per arm clamp, N']:.0f} N each, arm safety factor {R['Arm safety factor on yield']:.1f}; 0.5 s cut-off needs a bench test",
     "Brake cut-off, 0.5 s stop, fuse, torque arms", "Not verifiable at TRL 3"),
    ("R13", f"Coding node {R['INTERLOCK node with 10 kOhm coding resistor, V']:.2f} V; mode 4 net {R['Net charge current in mode 4 with 4 W load, A']:.2f} A; "
            f"clamp rotation margin {R['Rotation margin at 25 g lateral']:.2f} at 25 g",
     "SwapCell interface v0.3 items W, C and V1", "Not verifiable at TRL 3"),
    ("R1", "250 W rated motor, 20 km/h cut-off, pedal assist and 6 km/h walk assist", "250 W; 25 km/h or lower; assist only when pedaling", "Met (by specification)"),
    ("R2", f"{R['Range, design case, nominal cells, km']:.0f} km ({R['Range, design case, minimum cells, km']:.0f} km with minimum cells)",
     "30 km or more", "Met"),
    ("R5", "Cradle for 28 to 32 mm tubes; motor for 100 mm spacing and 635 rim; pack fits the main triangle in the model",
     "Common roadster", "Met (on paper)"),
    ("R6", f"{R['Added mass with pack, kg']:.2f} kg", "7 kg or less", "Met"),
    ("R8", f"{R['Daily loaded range, mid, km']:.0f} km/day; recharge {R['Days to recharge 10 to 100 %, mid']:.1f} days "
           f"({R['Days to recharge 10 to 100 %, low']:.1f} at 4 h)", "20 km/day; 2 days or less", "Met"),
    ("R12", f"Bike kit ${R['Bike conversion kit (1-5, 7-9, 14), USD']:.0f} (${R['Bike kit under the USD 250 value-engineering target by, USD']:.0f} under the target); solar set ${R['Solar charging set (10-13), USD']:.0f} costed separately",
     "Bike kit $250 or less (value-engineering target)", "Met"),
]
with (Path(__file__).parent / "results.csv").open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "value", "target", "status"])
    w.writerows(results)
section("Requirement status (written to docs/04-calcs/results.csv)")
for r in results:
    print(f"  {r[0]:4s} {r[3]:24s} {r[1]}")
