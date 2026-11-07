# Bill of materials

Inventory confirmed by the project owner on November 6, 2026. Ownership does not imply bench validation. No prices, vendors, or remaining purchases are committed.

## Owned

| Part | Qty | Verification still needed |
| --- | ---: | --- |
| Waveshare 1.51-inch OLED | 2 | Transparent model/revision, driver board, interface configuration, supplied cables |
| XIAO RP2040 | 1 | Standard/Plus revision, pinout and power circuitry |
| ESP32-S3 development board | 1 | Manufacturer/variant, usable GPIOs and regulators |
| NEO-6M GPS module | 1 | Breakout input voltage vs UART logic, antenna, fix and update rate |
| MPU6050 module | 1 | Breakout voltage, I2C address/pull-ups, calibration |
| BMP280 module | 1 | Part identity, voltage, I2C address/pull-ups and pressure response |

## Planned or ownership unconfirmed

| Item | Planning quantity | Selection gate |
| --- | ---: | --- |
| Breadboard, jumper wires, headers | 1 set | Check existing supplies; short bench wiring |
| USB data cables | 2 | Match both controller connectors; confirm data capability |
| Multimeter / current measurement equipment | Access to 1 set | Verify rails, peak current and energy use |
| 3.3 V RS-485 transceivers | 2, conditional | Longer cable testing; logic compatibility, duplex/direction control |
| Termination/bias components | As designed | Bus impedance and module onboard resistors |
| Flexible wearable cable | About 1 m initially | Actual routing, power loss, twisted data pair, conductor count |
| Breakaway connector pair, strain relief | 1 set | Reliable electrical contact and suitable release behavior |
| Protected 1S LiPo | 1, capacity TBD | Measured load, runtime target, enclosure and cold limits; ~2000 mAh is only an initial candidate |
| Compatible charger/protection and power-path solution | 1 system | Match cell; confirm protection and USB isolation |
| Voltage regulation | As designed | Verified controller/display input requirements; 5 V boost only if needed |
| Switch, fuse, battery connector | 1 set | Current ratings, wire protection and accessible power-off |
| Near-eye optical test lenses | Up to 2 after one-eye test | Focal length, eye relief, image size/contrast; avoid buying on magnification alone |
| Adjustable goggle mounts and enclosure | 1 set | Optical results, comfort, clear view, moisture protection |
| Perfboard/PCB, locking connectors, fasteners | As designed | Proven wiring and pin allocation; custom PCB comes later |

Record exact part numbers and schematics before ordering the power, cable, and optics system. Obtain current quotations after the design gates; prior conversation cost ranges were rough estimates rather than a validated shopping list.
