# Bill of materials: connection via Bluetooth / wireless option (rev W0.1)

Separate from the cable version. Machine-readable export: [`kicad/fab/SnowHUD_Wireless_bom.csv`](kicad/fab/SnowHUD_Wireless_bom.csv).

## New parts to buy for this option

| Ref | Part | Qty | Package / footprint | Notes |
| --- | --- | ---: | --- | --- |
| U1 | **Seeed Studio XIAO ESP32S3** | 1 | XIAO 14-pin, THT on 2.54 mm headers (`SnowHUD_Wireless:XIAO_ESP32S3_THT`) | Radio (BLE 5 + Wi-Fi + ESP-NOW) and built-in LiPo charger. Not the "Sense" variant. Includes the U.FL antenna. |
| — | 1S 3.7 V LiPo pouch cell, JST-PH 2.0 mm 2-pin lead | 1 | ~300–500 mAh, e.g. 502535 | Must have built-in protection (PCM). **Check lead polarity.** Size it after measuring current. |
| J5 | JST PH B2B-PH-K-S (2-pin vertical header) | 1 | `Connector_JST:JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical` | Battery socket |
| SW1 | C&K OS102011MS2Q slide switch, SPDT | 1 | `Button_Switch_THT:SW_Slide_SPDT_Straight_CK_OS102011MS2Q` | Battery on/off |
| R1, R2 | 220 kΩ, 1 %, 0603 | 2 | `Resistor_SMD:R_0603_1608Metric` | VBAT/2 divider to D5 |
| C1 | 100 nF, 0603, X7R | 1 | `Capacitor_SMD:C_0603_1608Metric` | ADC filter |
| — | 2.54 mm male pin headers, 1×7 | 2 | for the XIAO ESP32S3 | Usually included with the XIAO |
| — | Thin wire (~28–30 AWG), ~5 cm | 1 | — | TP1/TP2 → XIAO underside BAT+/BAT− pads |

## Already owned, reused unchanged

| Ref | Part | Board |
| --- | --- | --- |
| DS1, DS2 | Waveshare 1.51-inch OLED (×2) + 1×7 pin headers | Goggle |
| U2 | ESP32-S3-DevKitC-1 + 2× 1×22 female sockets | Jacket |
| U3 | NEO-6M GPS (GY-NEO6MV2) + 1×4 socket | Jacket |
| U4 | MPU6050 (GY-521) + 1×8 socket | Jacket |
| U5 | BMP280 module + 1×6 socket | Jacket |

## Not needed in this option

| Part | Why |
| --- | --- |
| XIAO RP2040 | Replaced by XIAO ESP32S3 (no radio). Keep it for the cable version or bench tests. |
| JST-PH 4-pin connectors J3/J4 and the 4-wire tether cable | No cable between goggles and jacket |
| JP1 solder jumper | No cable 5 V |
| RS-485 transceivers (rev-A plan) | No long wired link |
