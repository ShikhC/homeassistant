# Shopping list

Quantities derive from `docs/device-inventory.md`; regenerate that first.

| Item | Qty | Needed by | Notes |
|---|---:|---|---|
| UPS with USB data port, 600–1100 VA (APC BX600C-IN / BX1100C-IN) | 1 | Phase 1 | Must run server + router + modem + dongle ≥ 20 min |
| SONOFF MINI-ZB2GS | 3 | Phase 1 (pair) / Phase 2 (fans) | Storage fans |
| 5 V USB adapter for Dongle Max | 1 | Phase 1 | Plugged into UPS |
| Weather hood for PIR-size sensor | 4 | Phase 1 | For SNZB-03PR2 under eaves |
| 12 V DC power supply, ≥ 2 A, enclosed | 1 | Phase 2 | Confirm siren label voltage first |
| Spare coin cells (check each sensor manual for CR2477 / CR2450) | 8 | Phase 2 | One spare per sensor |
| Zigbee 3-phase CT-clamp energy meter, Zigbee2MQTT-supported (Tuya PC321-Z-TY class) | 1 | Phase 3 | Order online; check zigbee2mqtt.io/supported-devices before buying |
| Panel-mount Auto/Manual selector switch, 2-position | 1 | Phase 3 | Electrician may supply |
| PoE cameras with on-camera person detection + PoE switch/NVR | 4 + 1 | Phase 4 | Hikvision AcuSense or TP-Link VIGI; must expose person events to HA |
