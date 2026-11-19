"""Generate the WIRELESS (Bluetooth / ESP-NOW) OPTION schematic + symbol library.

Reuses module symbols from the cable-version schematic (hardware/kicad/SnowHUD.kicad_sch) and adds
XIAO ESP32-S3, LiPo connector, power switch, battery divider and wire pads.
Run with KiCad's Python (or any Python 3):  python gen_sch.py
"""
import os, re, uuid, json

HERE = os.path.dirname(os.path.abspath(__file__))
PRJ = os.path.abspath(os.path.join(HERE, ".."))
CABLE = os.path.abspath(os.path.join(PRJ, "..", "..", "kicad"))
NAME = "SnowHUD_Wireless"
LIB = "SnowHUD_Wireless"
U = lambda: str(uuid.uuid4())
F = '(effects (font (size 1.27 1.27)))'
FH = '(effects (font (size 1.27 1.27)) hide)'

src = open(os.path.join(CABLE, "SnowHUD.kicad_sch"), encoding="utf-8").read()
libsec = src[src.index("(lib_symbols\n") + len("(lib_symbols\n"): src.index('\n)\n(text "GOGGLE SIDE')]
blocks = {}
for chunk in re.split(r'\n(?=\(symbol "SnowHUD:)', libsec):
    m = re.match(r'\(symbol "SnowHUD:([^"]+)"', chunk)
    if m: blocks[m.group(1)] = chunk.strip()

def rename(block, old, new):
    return block.replace(f'(symbol "SnowHUD:{old}"', f'(symbol "{LIB}:{new}"') \
                .replace(f'"{old}_0_1"', f'"{new}_0_1"').replace(f'"{old}_1_1"', f'"{new}_1_1"')

syms = {}
for n in ["ESP32-S3-DevKitC-1", "OLED_1.51_SPI", "NEO-6M", "GY-521_MPU6050", "BMP280_module"]:
    syms[n] = rename(blocks[n], n, n)

# XIAO ESP32-S3: same 14-pin layout and numbering as the XIAO RP2040 symbol, ESP32-S3 pin names
x = rename(blocks["XIAO_RP2040"], "XIAO_RP2040", "XIAO_ESP32S3")
for old, new in [("D0/A0/P26", "D0/A0/GPIO1"), ("D1/A1/P27", "D1/A1/GPIO2"), ("D2/A2/P28", "D2/A2/GPIO3"),
                 ("D3/A3/P29", "D3/A3/GPIO4"), ("D4/SDA/P6", "D4/SDA/GPIO5"), ("D5/SCL/P7", "D5/SCL/GPIO6"),
                 ("D6/TX/P0", "D6/TX/GPIO43"), ("D7/RX/P1", "D7/RX/GPIO44"), ("D8/SCK/P2", "D8/SCK/GPIO7"),
                 ("D9/MISO/P4", "D9/MISO/GPIO8"), ("D10/MOSI/P3", "D10/MOSI/GPIO9"),
                 ('(property "Value" "XIAO_RP2040"', '(property "Value" "XIAO_ESP32S3"')]:
    assert old in x, old
    x = x.replace(old, new)
syms["XIAO_ESP32S3"] = x

def mk(name, ref, fp, rect, pins, hide_names=False):
    pn = "(pin_names (offset 1.016) hide)" if hide_names else "(pin_names (offset 1.016))"
    s = (f'(symbol "{LIB}:{name}" {pn} (exclude_from_sim no) (in_bom yes) (on_board yes)\n'
         f'(property "Reference" "{ref}" (at 0 {rect[1] + 1.27} 0) {F})\n'
         f'(property "Value" "{name}" (at 0 {rect[3] - 1.27} 0) {F})\n'
         f'(property "Footprint" "{fp}" (at 0 0 0) {FH})\n'
         f'(property "Datasheet" "" (at 0 0 0) {FH})\n'
         f'(symbol "{name}_0_1" (rectangle (start {rect[0]} {rect[1]}) (end {rect[2]} {rect[3]}) (stroke (width 0.254) (type default)) (fill (type background))))\n'
         f'(symbol "{name}_1_1"\n')
    for (num, pname, px, py, ang) in pins:
        s += f'(pin passive line (at {px} {py} {ang}) (length 2.54) (name "{pname}" {F}) (number "{num}" {F}))\n'
    return s + "))"

FP = {
    "XIAO_ESP32S3": f"{LIB}:XIAO_ESP32S3_THT",
    "ESP32-S3-DevKitC-1": f"{LIB}:ESP32-S3-DevKitC-1_Socket",
    "OLED_1.51_SPI": "Connector_PinHeader_2.54mm:PinHeader_1x07_P2.54mm_Vertical",
    "NEO-6M": "Connector_PinSocket_2.54mm:PinSocket_1x04_P2.54mm_Vertical",
    "GY-521_MPU6050": "Connector_PinSocket_2.54mm:PinSocket_1x08_P2.54mm_Vertical",
    "BMP280_module": "Connector_PinSocket_2.54mm:PinSocket_1x06_P2.54mm_Vertical",
    "Conn_Battery_2": "Connector_JST:JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical",
    "SW_SPDT": "Button_Switch_THT:SW_Slide_SPDT_Straight_CK_OS102011MS2Q",
    "R": "Resistor_SMD:R_0603_1608Metric",
    "C": "Capacitor_SMD:C_0603_1608Metric",
    "WirePad": "TestPoint:TestPoint_THTPad_D2.0mm_Drill1.0mm",
}
syms["Conn_Battery_2"] = mk("Conn_Battery_2", "J", FP["Conn_Battery_2"], (-7.62, 3.81, 7.62, -3.81),
                            [("1", "BAT+", -10.16, 1.27, 0), ("2", "BAT-", -10.16, -1.27, 0)])
syms["SW_SPDT"] = mk("SW_SPDT", "SW", FP["SW_SPDT"], (-5.08, 3.81, 5.08, -3.81),
                     [("2", "COM", -7.62, 0, 0), ("1", "A", 7.62, 2.54, 180), ("3", "B", 7.62, -2.54, 180)])
syms["R"] = mk("R", "R", FP["R"], (-2.54, 1.016, 2.54, -1.016), [("1", "~", -5.08, 0, 0), ("2", "~", 5.08, 0, 180)], True)
syms["C"] = mk("C", "C", FP["C"], (-2.54, 1.016, 2.54, -1.016), [("1", "~", -5.08, 0, 0), ("2", "~", 5.08, 0, 180)], True)
syms["WirePad"] = mk("WirePad", "TP", FP["WirePad"], (-2.54, 1.27, 2.54, -1.27), [("1", "1", -5.08, 0, 0)], True)

def pins_of(name):
    return {m.group(4): (float(m.group(1)), float(m.group(2)), int(m.group(3)))
            for m in re.finditer(r'\(pin passive line \(at (\S+) (\S+) (\d+)\).*?\(number "([^"]+)"', syms[name])}

ROOT = U()
body = []

def place(sym, ref, value, desc, x, y, nets):
    """nets: pin number -> net name, or None for no-connect. Unlisted pins must not exist."""
    pins = pins_of(sym)
    assert set(nets) == set(pins), (ref, set(pins) ^ set(nets))
    ys = [p[1] for p in pins.values()]
    top, bot = max(ys) + 3.81, min(ys) - 3.81
    in_bom = "no" if sym == "WirePad" else "yes"   # bare pads, nothing to buy
    body.append(
        f'(symbol (lib_id "{LIB}:{sym}") (at {x} {y} 0) (unit 1) (exclude_from_sim no) (in_bom {in_bom}) (on_board yes) (dnp no) (uuid "{U()}")\n'
        f'(property "Reference" "{ref}" (at {x} {round(y - top, 2)} 0) {F})\n'
        f'(property "Value" "{value}" (at {x} {round(y - bot, 2)} 0) {F})\n'
        f'(property "Footprint" "{FP[sym]}" (at {x} {y} 0) {FH})\n'
        f'(property "Datasheet" "" (at {x} {y} 0) {FH})\n'
        f'(property "Description" "{desc}" (at {x} {y} 0) {FH})\n'
        + " ".join(f'(pin "{n}" (uuid "{U()}"))' for n in pins) + "\n"
        f'(instances (project "{NAME}" (path "/{ROOT}" (reference "{ref}") (unit 1)))))')
    for num, (px, py, ang) in pins.items():
        cx, cy = round(x + px, 2), round(y - py, 2)
        net = nets[num]
        if net is None:
            body.append(f'(no_connect (at {cx} {cy}) (uuid "{U()}"))'); continue
        dx = -5.08 if ang == 0 else 5.08
        x2 = round(cx + dx, 2)
        la, just = (180, "right") if dx < 0 else (0, "left")
        body.append(f'(wire (pts (xy {cx} {cy}) (xy {x2} {cy})) (stroke (width 0) (type default)) (uuid "{U()}"))')
        body.append(f'(label "{net}" (at {x2} {cy} {la}) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify {just} bottom)) (uuid "{U()}"))')

def text(t, x, y, size=1.27):
    t = t.replace("\n", "\\n").replace('"', "'")
    body.append(f'(text "{t}" (exclude_from_sim no) (at {x} {y} 0) (effects (font (size {size} {size})) (justify left top)) (uuid "{U()}"))')

OLED = lambda cs: {"1": "+3V3_XIAO", "2": "GND_HUD", "3": "SPI_MOSI", "4": "SPI_SCK", "5": cs, "6": "OLED_DC", "7": "OLED_RST"}

# ---------------- GOGGLE (wireless) ----------------
text("Snowboarding helmet goggles HUD - CONNECTION VIA BLUETOOTH / WIRELESS OPTION (no goggle-jacket cable)", 25.4, 15.24, 1.8)
text("GOGGLE SIDE - HUD renderer, XIAO ESP32-S3 + own LiPo battery", 25.4, 22.86, 2.54)
place("XIAO_ESP32S3", "U1", "Seeed XIAO ESP32S3", "Display controller + radio (BLE 5 / Wi-Fi / ESP-NOW). Built-in LiPo charger on underside BAT pads.",
      76.2, 66.04, {"1": "OLED_CS_L", "2": "OLED_CS_R", "3": "OLED_DC", "4": "OLED_RST", "5": None, "6": "VBAT_SENSE",
                    "7": None, "8": None, "9": "SPI_SCK", "10": None, "11": "SPI_MOSI", "12": "+3V3_XIAO", "13": "GND_HUD", "14": None})
place("OLED_1.51_SPI", "DS1", "Waveshare 1.51in OLED (LEFT)", "Left HUD display, 4-wire SPI mode", 160.02, 50.8, OLED("OLED_CS_L"))
place("OLED_1.51_SPI", "DS2", "Waveshare 1.51in OLED (RIGHT)", "Right HUD display, 4-wire SPI mode", 160.02, 86.36, OLED("OLED_CS_R"))
place("Conn_Battery_2", "J5", "LiPo 1S 3.7V", "Goggle battery, JST-PH 2-pin. CHECK battery lead polarity - not standardised!", 76.2, 101.6,
      {"1": "BAT_RAW", "2": "GND_HUD"})
place("SW_SPDT", "SW1", "Power ON/OFF", "Slide switch in battery + lead (battery cannot charge while OFF)", 119.38, 101.6,
      {"2": "BAT_RAW", "1": "VBAT", "3": None})
place("R", "R1", "220k", "Battery divider top", 99.06, 114.3, {"1": "VBAT", "2": "VBAT_SENSE"})
place("R", "R2", "220k", "Battery divider bottom", 160.02, 114.3, {"1": "VBAT_SENSE", "2": "GND_HUD"})
place("C", "C1", "100nF", "ADC filter", 99.06, 119.38, {"1": "VBAT_SENSE", "2": "GND_HUD"})
place("WirePad", "TP1", "BAT+ to XIAO", "Solder a short wire from here to the XIAO ESP32S3 underside BAT+ pad", 205.74, 104.14, {"1": "VBAT"})
place("WirePad", "TP2", "BAT- to XIAO", "Solder a short wire from here to the XIAO ESP32S3 underside BAT- pad", 205.74, 111.76, {"1": "GND_HUD"})

# ---------------- JACKET (wireless) ----------------
text("JACKET SIDE - sensor acquisition / telemetry (radio = ESP32-S3 built-in BLE / Wi-Fi)", 25.4, 124.46, 2.54)
place("ESP32-S3-DevKitC-1", "U2", "ESP32-S3 DevKit (subset of pins)", "Sensor acquisition + radio link to goggles", 76.2, 165.1,
      {"1": "+3V3_ESP", "2": "+5V_ESP", "3": "GND", "4": None, "5": None, "6": "I2C_SDA", "7": "I2C_SCL",
       "8": "MPU_INT", "9": "GPS_RX_IN", "10": "GPS_TX_OUT"})
place("NEO-6M", "U3", "NEO-6M GPS (GY-NEO6MV2)", "GPS, UART 9600 baud default", 160.02, 142.24,
      {"1": "+5V_ESP", "2": "GPS_RX_IN", "3": "GPS_TX_OUT", "4": "GND"})
place("GY-521_MPU6050", "U4", "MPU6050 (GY-521) addr 0x68", "6-axis IMU", 160.02, 172.72,
      {"1": "+3V3_ESP", "2": "GND", "3": "I2C_SCL", "4": "I2C_SDA", "5": None, "6": None, "7": "GND", "8": "MPU_INT"})
place("BMP280_module", "U5", "BMP280 addr 0x76", "Barometer, I2C mode (CSB high)", 160.02, 205.74,
      {"1": "+3V3_ESP", "2": "GND", "3": "I2C_SCL", "4": "I2C_SDA", "5": "+3V3_ESP", "6": "GND"})

text("NOTES - CONNECTION VIA BLUETOOTH / WIRELESS OPTION (rev W0.1). See ../README.md\n"
     "1. No wire between goggles and jacket. Link = ESP32-S3 radio on both ends: ESP-NOW (recommended, no pairing, low latency)\n"
     "   or Bluetooth LE. Jacket ESP32-S3-DevKitC-1 already has the radio; goggle XIAO RP2040 is replaced by a XIAO ESP32S3.\n"
     "2. XIAO ESP32S3 uses the same 14-pin XIAO layout. Same OLED pins as the cable version: D0 CS_L, D1 CS_R, D2 DC, D3 RST,\n"
     "   D8 SCK, D10 MOSI. D6/D7 (UART) no longer needed. Fit the included U.FL antenna and keep it clear of metal/carbon.\n"
     "3. Goggle power: 1S LiPo -> J5 -> SW1 -> VBAT -> TP1/TP2 -> short wires to the XIAO underside BAT+/BAT- pads.\n"
     "   The XIAO charges the LiPo from its USB-C. Battery cannot charge while SW1 is OFF.\n"
     "   CHECK LiPo connector polarity before plugging in - JST-PH battery leads are not standardised.\n"
     "4. Battery monitor: VBAT/2 via R1/R2 (220k/220k, ~9.5 uA) to D5 (GPIO6, ADC1). C1 100 nF filter.\n"
     "5. Jacket ESP32 GPIO4/5 (old cable UART) now unused. Jacket still USB powered (battery stage still open, see docs).\n"
     "6. Same unverified items as the cable version: header spacings and module pinouts must be measured before ordering.",
     228.6, 124.46)

lib_symbols = "(lib_symbols\n" + "\n".join(syms.values()) + "\n)"
sch = (f'(kicad_sch (version 20231120) (generator "eeschema") (generator_version "8.0") (uuid "{ROOT}") (paper "A3")\n'
       f'(title_block (title "Snowboarding Helmet Goggles HUD - WIRELESS / BLUETOOTH OPTION") (date "2026-11-19") (rev "W0.1")'
       f' (comment 1 "Connection via Bluetooth/ESP-NOW option - goggle XIAO ESP32S3 + LiPo, no tether") (comment 2 "Pins proposed, not yet verified on hardware"))\n'
       + lib_symbols + "\n" + "\n".join(body) + '\n(sheet_instances (path "/" (page "1")))\n)\n')
open(os.path.join(PRJ, NAME + ".kicad_sch"), "w", encoding="utf-8", newline="\n").write(sch)

lib = ('(kicad_symbol_lib (version 20231120) (generator "kicad_symbol_editor") (generator_version "8.0")\n'
       + "\n".join(s.replace(f'(symbol "{LIB}:', '(symbol "') for s in syms.values()) + "\n)\n")
open(os.path.join(PRJ, NAME + ".kicad_sym"), "w", encoding="utf-8", newline="\n").write(lib)
open(os.path.join(PRJ, "sym-lib-table"), "w", encoding="utf-8", newline="\n").write(
    f'(sym_lib_table (version 7)\n  (lib (name "{LIB}")(type "KiCad")(uri "${{KIPRJMOD}}/{NAME}.kicad_sym")(options "")(descr "Wireless option symbols"))\n)\n')

pro = json.load(open(os.path.join(CABLE, "SnowHUD.kicad_pro"), encoding="utf-8"))
pro.setdefault("meta", {})["filename"] = NAME + ".kicad_pro"
pro["sheets"] = [[ROOT, "Root"]]
pro.pop("boards", None)
json.dump(pro, open(os.path.join(PRJ, NAME + ".kicad_pro"), "w", encoding="utf-8", newline="\n"), indent=2)
print("wireless schematic generated:", len(body), "items")
