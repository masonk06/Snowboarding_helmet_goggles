"""WIRELESS OPTION footprints: XIAO ESP32S3 (THT, same XIAO layout) and ESP32-S3-DevKitC-1 (2x22 sockets)."""
import os
PRJ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LIB = os.path.join(PRJ, "SnowHUD_Wireless.pretty")
os.makedirs(LIB, exist_ok=True)

def txt(kind, val, x, y, layer, size=1.0, hide=False):
    h = " hide" if hide else ""
    return (f'  (property "{kind}" "{val}" (at {x} {y} 0) (layer "{layer}"){h}\n'
            f'    (effects (font (size {size} {size}) (thickness 0.15))))\n')

def rect(x0, y0, x1, y1, layer, w):
    return f'  (fp_rect (start {x0} {y0}) (end {x1} {y1}) (stroke (width {w}) (type solid)) (fill no) (layer "{layer}"))\n'

def user(t, x, y, layer, size=0.8, rot=0):
    return (f'  (fp_text user "{t}" (at {x} {y} {rot}) (layer "{layer}")\n'
            f'    (effects (font (size {size} {size}) (thickness 0.12))))\n')

def pad(num, x, y, first=False):
    shape = "rect" if first else "circle"
    return (f'  (pad "{num}" thru_hole {shape} (at {round(x,3)} {round(y,3)}) (size 1.7 1.7) (drill 1.0)'
            f' (layers "*.Cu" "*.Mask"))\n')

def write(name, descr, body):
    s = (f'(footprint "{name}"\n  (version 20240108)\n  (generator "pcbnew")\n  (layer "F.Cu")\n'
         f'  (descr "{descr}")\n  (attr through_hole)\n' + body + ')\n')
    open(os.path.join(LIB, name + ".kicad_mod"), "w", encoding="utf-8", newline="\n").write(s)

# ---------------- XIAO ESP32S3 ----------------
# symbol pins 1..7 = D0..D6 (left, top->bottom), 8 = D7 (right bottom) ... 14 = 5V (right top). USB at -Y.
b = txt("Reference", "REF**", 0, -11.6, "F.SilkS") + txt("Value", "XIAO_ESP32S3_THT", 0, 11.6, "F.Fab")
for (xa, ya, xb, yb) in [(-8.75, -9.6, -8.75, 10.5), (8.75, -9.6, 8.75, 10.5), (-8.75, 10.5, 8.75, 10.5)]:
    b += f'  (fp_line (start {xa} {ya}) (end {xb} {yb}) (stroke (width 0.12) (type solid)) (layer "F.SilkS"))\n'
b += rect(-8.75, -10.5, 8.75, 10.5, "F.Fab", 0.1)
b += rect(-9.0, -10.75, 9.0, 10.75, "F.CrtYd", 0.05)
b += user("USB", 0, -9.2, "F.SilkS")
b += user("XIAO ESP32S3", 0, 0, "F.Fab", 1.0) + user("U.FL antenna on module - keep clear", 0, 12.8, "F.Fab", 0.8)
for n in range(1, 8):
    b += pad(n, -7.62, -7.62 + 2.54 * (n - 1), first=(n == 1))
for n in range(8, 15):
    b += pad(n, 7.62, 7.62 - 2.54 * (n - 8))
write("XIAO_ESP32S3_THT", "Seeed XIAO ESP32S3 (same 14-pin XIAO layout), 2x7 THT 2.54mm, rows 15.24mm apart, USB-C toward -Y (board edge). "
      "Solder with pin headers, or castellations directly onto the pads.", b)

# ---------------- ESP32-S3-DevKitC-1 ----------------
# J1 (left, x=-11.43) pin k at y=-26.67+2.54(k-1); J3 right. Pin 1 (3V3) at antenna end, USB at +Y.
# Pads are numbered by the SnowHUD symbol pin they carry; unused header pins are unnumbered (no net).
J1 = {1: "1", 2: "1", 4: "4", 5: "5", 7: "8", 10: "9", 11: "10", 12: "6", 15: "7", 21: "2", 22: "3"}
J3 = {1: "3", 21: "3", 22: "3"}
b = txt("Reference", "REF**", 0, -30.2, "F.SilkS") + txt("Value", "ESP32-S3-DevKitC-1_Socket", 0, 0, "F.Fab")
b += rect(-12.7, -29.0, 12.7, 33.74, "F.Fab", 0.1)
b += rect(-12.95, -29.25, 12.95, 34.0, "F.CrtYd", 0.05)
# silk: outline of the two socket strips only (module itself overhangs at the USB end)
for x in (-11.43, 11.43):
    b += rect(round(x - 1.33, 2), -28.0, round(x + 1.33, 2), 28.0, "F.SilkS", 0.12)
b += user("J1", -11.43, -29.0, "F.SilkS")
b += user("J3", 11.43, -29.0, "F.SilkS")
b += user("ANT", 0, -26.5, "F.SilkS", 1.0)
b += user("USB", 0, 31.5, "F.Fab", 1.0)
b += user("3V3", -8.4, -26.67, "F.SilkS", 0.8)
b += user("5V", -8.8, 24.13, "F.SilkS", 0.8)
b += user("GND", -8.4, 26.67, "F.SilkS", 0.8)
b += user("ESP32-S3-DevKitC-1", 0, -2.0, "F.SilkS", 1.0, 90)
for k in range(1, 23):
    y = -26.67 + 2.54 * (k - 1)
    b += pad(J1.get(k, ""), -11.43, y, first=(k == 1))
    b += pad(J3.get(k, ""), 11.43, y)
write("ESP32-S3-DevKitC-1_Socket", "Espressif ESP32-S3-DevKitC-1 on 2x 1x22 female sockets, rows 22.86mm apart. "
      "Pads numbered per SnowHUD symbol; unused header pins unnumbered. VERIFY row spacing against your board.", b)

open(os.path.join(PRJ, "fp-lib-table"), "w", encoding="utf-8", newline="\n").write(
    '(fp_lib_table\n  (version 7)\n  (lib (name "SnowHUD_Wireless")(type "KiCad")(uri "${KIPRJMOD}/SnowHUD_Wireless.pretty")'
    '(options "")(descr "SnowHUD wireless option footprints"))\n)\n')
print("footprints written")
