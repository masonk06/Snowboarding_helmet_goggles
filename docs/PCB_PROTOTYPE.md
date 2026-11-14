# PCB prototype — detachable goggle/body link

This is the first layout-ready electrical definition for the two-board wearable prototype. It is a **carrier-PCB design**: the purchased development boards and breakout modules plug into headers or cable connectors. It intentionally does not assume their final footprints or pin mappings.

## Board split

| Board | Location | Carries |
| --- | --- | --- |
| Goggle carrier | Goggle frame / side arm | XIAO RP2040, two OLED connectors, RS-485 receiver/transmitter, protected 5 V input |
| Body carrier | Jacket enclosure | ESP32-S3, NEO-6M, MPU6050, BMP280 connectors, battery power stage, RS-485 receiver/transmitter |

The only wire running from the goggles to the jacket is the detachable tether below. Sensor buses do not cross the tether.

## Tether and connector

Use two board-mounted **JST GH 6-pin** connectors (1.25 mm pitch) and a six-conductor flexible cable with matching crimp housings. This is a compact locking connector family, not a safety-rated breakaway. Add cable clamps/strain relief immediately behind both connectors.

| Pin | Net | Direction | Purpose |
| ---: | --- | --- | --- |
| 1 | GND | shared | Return, paired with 3. |
| 2 | GND | shared | Second return and shielding/low-impedance reference. |
| 3 | +5V_GOGGLE | body → goggles | Fused, protected 5 V power. |
| 4 | RS485_A | bidirectional | Differential telemetry pair. |
| 5 | RS485_B | bidirectional | Differential telemetry pair. |
| 6 | AUX_DETECT | reserved | Cable-presence detect or future button; leave unconnected on revision A. |

The initial link protocol is half-duplex UART-over-RS-485 at a conservative 115200 baud. Both boards use 3.3 V RS-485 transceivers. Place an optional 120 Ω termination resistor across A/B on **each** PCB, assembled only after cable testing; add one bias network on the body board only.

## Electrical blocks

```text
LiPo / protected pack
  → fuse → power switch → regulated 5 V
  → body carrier: ESP32-S3 + local sensors + RS-485
  → JST-GH tether (+5 V, GND, A, B)
  → goggle carrier: input protection + RS-485 + XIAO RP2040
  → local OLED connectors (short SPI wiring)
```

### Goggle carrier requirements

- Input connector: JST-GH 6-pin; add a resettable fuse, reverse-polarity protection, and a 5 V TVS footprint appropriate to the selected cable/rail.
- Data: a 3.3 V half-duplex RS-485 transceiver such as MAX3485-compatible part, with `RO` to RP2040 RX and `DI` to TX. Tie `DE` and `/RE` together to one GPIO.
- Display: two dedicated OLED connectors, using shared SPI `SCLK`/`MOSI` plus independent `CS`; reserve `DC` and `RESET` per the actual Waveshare module requirements.
- Keep the OLED connectors and RP2040 on the same PCB. Do not route unbuffered SPI through the tether.
- Provide test pads for `5V_GOGGLE`, `3V3`, `GND`, `A`, and `B`.

### Body carrier requirements

- Battery input and charging approach remain unselected. Do not connect a raw one-cell LiPo directly to a 5 V or 3.3 V board rail.
- Output the tether’s 5 V through a fuse/eFuse sized only after display and controller current measurements.
- Data: matching 3.3 V RS-485 circuit, plus ESD protection at the connector.
- Sensors connect locally: GPS over UART; IMU and barometer over short I²C runs.
- Keep the GPS antenna away from the ESP32-S3, boost converter and battery wiring; place the BMP280 behind a protected pressure vent.

## Carrier footprint placeholders

Use 2.54 mm female headers only after measuring each purchased board. Record every measured header spacing, board outline, mounting hole, and pin-1 orientation before laying out copper.

| Placeholder | What must be verified before routing |
| --- | --- |
| `J_XIAO_RP2040` | Standard vs Plus board, header count, pin labels, USB clearance and power input. |
| `J_ESP32_S3` | Exact development-board variant, header spacing, boot/reset button access and antenna keepout. |
| `J_OLED_L`, `J_OLED_R` | Transparent OLED revision, selected SPI/I²C jumper state, supply voltage and all control pins. |
| `J_GPS`, `J_IMU`, `J_BARO` | Module pin order, voltage tolerance and existing pull-ups/regulators. |

## Layout constraints for revision A

- Use a 2-layer board only if the RF/antenna keepouts and return paths remain clean; otherwise use four layers for the body board.
- Put the tether connector at a board edge with mechanical support, never relying on solder joints alone.
- Keep the RS-485 A/B traces paired and away from the OLED SPI lines. At the planned low link rate, controlled impedance is not required, but a continuous ground return is.
- Keep copper, tall components and cable strain relief clear of goggles, lens, vents and helmet impact structure.
- Make the goggle board as thin and low-profile as practical; use mounting slots/holes only in the housing or non-protective attachment system.

## Release gate before ordering PCBs

1. Photograph and measure every purchased module; update connector symbols and footprints from the actual pinouts.
2. Bench-test the OLEDs and both controllers independently from USB.
3. Build the RS-485 link on breadboard with the actual tether cable; confirm reconnect, power drop and packet-loss behavior.
4. Measure peak current with two OLEDs active. Select the fuse, regulator, wire gauge and battery only from those measurements.
5. Run ERC/DRC and print a 1:1 paper fit check before fabricating.

