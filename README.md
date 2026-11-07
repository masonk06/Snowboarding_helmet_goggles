# Snowboarding_helmet_goggles

SnowLens-inspired experimental heads-up display for snowboarding. Two small OLEDs are intended to show concise ride telemetry, with an ESP32-S3 collecting sensor data and a XIAO RP2040 driving the displays.

## Current progress — November 6, 2026

The main electronics are owned. Architecture, remaining parts, and implementation phases are documented below. No working firmware, assembled wiring, validated optics, runtime measurements, or on-snow results have been supplied or verified. This snapshot records design progress; it does not claim a working AR product or affiliation with SnowLens.

| Confirmed owned part | Qty | Intended role |
| --- | ---: | --- |
| Waveshare 1.51-inch OLED | 2 | Left/right HUD displays; prior discussion identifies the transparent model, exact revision to verify |
| Seeed Studio XIAO RP2040 | 1 | Display controller |
| ESP32-S3 development board | 1 | Sensor acquisition and telemetry; exact board variant to record |
| NEO-6M GPS module | 1 | Position and ground speed |
| MPU6050 module | 1 | Acceleration and angular velocity |
| BMP280 module | 1 | Pressure, sensor temperature, relative altitude estimate |

## Project documents

- [Architecture and technical caveats](docs/ARCHITECTURE.md)
- [Owned inventory and remaining BOM](docs/BOM.md)
- [Phased implementation and acceptance checks](docs/ROADMAP.md)

Start with USB-powered bench tests, one OLED and one sensor at a time. Record board revisions and verify module pinouts and voltage requirements before wiring. Final pin assignments and battery selection remain open.

## Prototype boundaries

Transparent OLEDs alone do not form a focused near-eye image. Optical feasibility, daylight contrast, field of view, eye relief, and binocular comfort must be demonstrated before committing to mounts. GPS outages cannot be bridged accurately by simply integrating the MPU6050. Keep invalid or stale measurements visibly distinct from valid telemetry.

The prototype must preserve vision and the protective function of goggles and helmet. Begin with stationary fit checks and controlled tests; it is not navigation or safety equipment.

## Primary hardware references

- [Waveshare 1.51-inch transparent OLED wiki](https://www.waveshare.com/wiki/1.51inch_Transparent_OLED) — candidate model, SPI/I2C configuration and vendor examples.
- [Seeed XIAO RP2040 documentation](https://wiki.seeedstudio.com/XIAO-RP2040/) — identify the actual board revision, pinout and power arrangement; standard and Plus variants differ.

Use the documentation and schematic for each exact purchased breakout before selecting wiring or power hardware. No firmware build or automated test suite exists in this documentation snapshot.
