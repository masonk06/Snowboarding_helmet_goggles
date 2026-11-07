# Phased implementation

All phases below are planned. Hardware ownership and documentation are the only confirmed milestones in this snapshot.

| Phase | Work | Acceptance evidence |
| --- | --- | --- |
| 0 — Identify hardware | Photograph labels; record exact board revisions, schematics, voltage limits, display interface and pin budget | Reviewed inventory and wiring table with no unresolved rail conflicts |
| 1 — Display bench tests | USB-power XIAO; run vendor-compatible example on one OLED, then two with independent CS | Each screen shows different stable test content; record refresh behavior, current and reset behavior |
| 2 — Sensor bench tests | ESP32-S3 reads GPS over UART and both sensors over local I2C | Timestamped raw logs; valid outdoor GPS fixes; stationary IMU bias and pressure plausibility; unplug/fault handling |
| 3 — End-to-end telemetry | Define packet format; short UART link; minimal speed/altitude/status HUD | Verified units and CRC/framing; corrupted, missing and stale data handled without frozen valid-looking values |
| 4 — Optical feasibility | Adjustable one-eye jig before two-eye alignment; test indoors and bright outdoor conditions while stationary | Readable focus, eye relief, contrast and clear primary view; documented comfort; redesign or stop if unusable |
| 5 — Wearable power/cable | Measure loads; select protected battery and regulated power; test longer link and RS-485 if needed | Peak-load rail stability, measured runtime, voltage drop, reconnect recovery and accessible off control |
| 6 — Packaging | Enclosures, ventilation, strain relief and breakaway routing; preserve protective equipment | Stationary fit, condensation checks and cable release tests; no obstruction or structural compromise |
| 7 — Controlled validation | Log telemetry against reference measurements; evaluate cold behavior within component limits | Recorded errors, dropouts and limitations; progression to wearable trials only after bench/fit gates pass |

## First implementation session

1. Identify both OLED driver boards and the exact XIAO/ESP32-S3 revisions.
2. Produce a verified pin/rail table from their schematics.
3. Run one OLED on USB power, then demonstrate independent content on both.
4. Commit actual source, toolchain/library versions, wiring, and reproducible build instructions when working code exists.

Keep a test log containing setup, date, firmware revision, conditions, measurements and failures. Calibrated altitude, smoothing, sensor fusion, logging storage, wireless features and custom PCBs are subsequent decisions, not completed features.
