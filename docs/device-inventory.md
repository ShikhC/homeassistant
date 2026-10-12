# Device inventory

Generated from `inventory/devices.yaml` by `scripts/inventory.py --write`. Do not edit by hand.

## Budget

| Model | Owned | Assigned (owned) | To buy | Spare |
|---|---:|---:|---:|---:|
| MINI-ZB2GS | 6 | 6 | 3 | 0 |
| MINI-ZB1GS | 3 | 3 | 0 | 0 |
| ZBMINIR2 | 4 | 4 | 0 | 0 |
| BASIC-ZB1GSP | 1 | 1 | 0 | 0 |
| SNZB-03PR2 | 4 | 4 | 0 | 0 |
| SNZB-04PR1 | 4 | 4 | 0 | 0 |
| PoE-Dongle-Max | 1 | 1 | 0 | 0 |
| 3PH-METER | 0 | 0 | 1 | 0 |

Relay outputs assigned: 26. Spare outputs: `storage_fans_c.l2`.

## Devices

| Name | Model | Status | Location | Outputs |
|---|---|---|---|---|
| `coordinator` | PoE-Dongle-Max | owned | First floor ceiling |  |
| `ext_north` | MINI-ZB2GS | owned | Exterior North | l1: porch light, l2: floodlight |
| `ext_east` | MINI-ZB2GS | owned | Exterior East | l1: porch light, l2: floodlight |
| `ext_south` | MINI-ZB2GS | owned | Exterior South | l1: porch light, l2: floodlight |
| `ext_west` | MINI-ZB2GS | owned | Exterior West | l1: porch light, l2: floodlight |
| `living` | MINI-ZB2GS | owned | Living room | l1: light, l2: fan |
| `bedroom` | MINI-ZB2GS | owned | Bedroom | l1: light, l2: fan |
| `kitchen` | MINI-ZB1GS | owned | Kitchen | l1: light |
| `toilet_first` | MINI-ZB1GS | owned | First-floor toilet | l1: light |
| `bathroom_ground` | MINI-ZB1GS | owned | Ground bathroom | l1: light |
| `storage` | ZBMINIR2 | owned | Storage | l1: lights |
| `stairwell` | ZBMINIR2 | owned | External stairwell | l1: light |
| `roof` | ZBMINIR2 | owned | Roof | l1: light |
| `siren` | ZBMINIR2 | owned | Utility | l1: 12 V PSU to siren |
| `pump` | BASIC-ZB1GSP | owned | Pump panel | l1: starter coil circuit |
| `storage_fans_a` | MINI-ZB2GS | to_buy | Storage | l1: fan 1, l2: fan 2 |
| `storage_fans_b` | MINI-ZB2GS | to_buy | Storage | l1: fan 3, l2: fan 4 |
| `storage_fans_c` | MINI-ZB2GS | to_buy | Storage | l1: fan 5, l2: spare |
| `presence_north` | SNZB-03PR2 | owned | Exterior North |  |
| `presence_east` | SNZB-03PR2 | owned | Exterior East |  |
| `presence_south` | SNZB-03PR2 | owned | Exterior South |  |
| `presence_west` | SNZB-03PR2 | owned | Exterior West |  |
| `door_storage` | SNZB-04PR1 | owned | Storage door |  |
| `door_main` | SNZB-04PR1 | owned | Main first-floor door |  |
| `door_stairs` | SNZB-04PR1 | owned | Stairwell ground door |  |
| `door_roof` | SNZB-04PR1 | owned | Roof door |  |
| `pump_meter` | 3PH-METER | to_buy | Pump panel |  |

## Wishlist (priority order)

- SNZB-04PR1 — Pump room door
- SNZB-04PR1 — Balcony door
- SNZB-03PR2 — Storage interior
