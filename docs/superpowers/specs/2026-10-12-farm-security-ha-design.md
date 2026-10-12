# Farmhouse Security on Home Assistant — Design

**Date:** 2026-10-12
**Status:** Approved in conversation, pending written review
**Owner:** schowdhary

## 1. Purpose

Turn the existing Home Assistant OS install on the HP ProDesk into a security
system for a two-floor farmhouse in India, using Sonoff Zigbee hardware already
purchased, a 120 dB wired siren already owned, a 3-phase 7.5 hp submersible
irrigation pump, and cameras to be bought later.

Success means:

- Doors opened while armed sound the siren within 2 s, light every floodlight,
  and push a critical notification to every phone.
- A person approaching any side of the house after dark turns on that side's
  floodlight, and the event is logged.
- The pump can be started and stopped from a phone from anywhere, auto-stops
  on a timer, refuses to run on a lost phase, and reports whether it is
  actually running.
- Grid loss and restoration at the farm are reported to phones while the
  server is on battery.
- Everything degrades safely: wall switches keep working without Home
  Assistant, and the pump's manual starter still works.

Not in scope: comfort automations, voice assistants, Frigate NVR (deferred, see
§9), anything requiring cloud subscriptions.

## 2. Hardware

### 2.1 Owned

| Device | Qty | Zigbee role |
|---|---|---|
| Sonoff PoE Dongle Max (EFR32MG24 + ESP32) | 1 | Coordinator, Ethernet, USB-powered |
| MINI-ZB2GS (Mini One, 2-gang, 16 A) | 6 | Router |
| MINI-ZB1GS (Mini One, 1-gang, 16 A) | 3 | Router |
| ZBMINIR2 | 4 | Router |
| BASIC-ZB1GSP (DIN rail, energy metering) | 1 | Router |
| SNZB-03PR2 SenseGuard presence | 4 | End device, battery |
| SNZB-04PR1 door/window with tamper | 4 | End device, battery |
| 120 dB wired siren (GSM-alarm type) | 1 | Not Zigbee, assumed 12 V DC |
| HP ProDesk 600 G3 (i5-6500T, 8 GB, HAOS) | 1 | Server |

### 2.2 To buy

| Item | Purpose | Note |
|---|---|---|
| UPS with USB, ~600–1100 VA (APC BX600C-IN / BX1100C-IN class) | Keep server, router, modem, coordinator alive; source of grid-down signal via NUT | Required for Phase 1 |
| 12 V DC PSU, ≥ 2 A | Powers the siren, switched by a ZBMINIR2 | Confirm siren voltage on its label first |
| Zigbee 3-phase CT-clamp energy meter, Zigbee2MQTT-supported (Tuya PC321-Z-TY class) | Per-phase V/A/W on the pump feed | Required for Phase 3 |
| Auto/Manual selector switch, panel-mount | Pump starter integration | Electrician supplies |
| 4 weather hoods | SNZB-03PR2 are indoor units; mount under eaves in hoods | Phase 1 |
| 4 PoE cameras with on-camera person detection + PoE switch/NVR | Phase 4 | Brand decided at purchase; must expose a person-detected event to HA (Hikvision AcuSense via hikvision_next, or TP-Link VIGI) |
| 3 × MINI-ZB2GS | Five individually switched storage fans (§2.3) | Leaves one spare output |

### 2.3 Device budget

Every relay output and sensor is accounted for here; `docs/device-inventory.md`
is the living copy and is updated whenever a device is assigned, paired, or
bought. Fans switch through the relay in series with the existing wall
regulator, so HA gives on/off and the regulator keeps speed control.

Fans: five in the ground-floor storage, two on the first floor (living,
bedroom). Storage fans are switched individually (default). If group control
of the storage fans is acceptable, all five can share one 16 A output
(≈ 400 W total) and only 1 × ZB2GS needs buying instead of 3.

| Resource | Owned | Needed | Spare / (short) |
|---|---|---|---|
| Relay outputs (6×ZB2GS=12, 3×ZB1GS=3, 4×ZBMINIR2=4, 1×DIN=1) | 20 | 25 (8 exterior, 5 interior lights, 7 fans, storage lights, stairwell, roof, siren, pump) | (5) → buy 3×ZB2GS, then +1 spare |
| Presence sensors SNZB-03PR2 | 4 | 4 (one per side) | 0 |
| Door sensors SNZB-04PR1 | 4 | 4 | 0 |
| Energy-metered output BASIC-ZB1GSP | 1 | 1 (pump) | 0 |
| Coordinator | 1 | 1 | 0 |

Candidates for future extras, in priority order: door sensor on the pump room,
door sensor on the balcony door, presence sensor in the storage.

## 3. Software architecture

```
Phones (Companion app) ──Tailscale──▶ Home Assistant OS (HP ProDesk, on UPS)
                                        ├─ Mosquitto (MQTT broker)
                                        ├─ Zigbee2MQTT ──tcp://dongle:6638──▶ PoE Dongle Max ──Zigbee──▶ 22 devices
                                        ├─ NUT ──USB──▶ UPS
                                        ├─ Tailscale
                                        ├─ HACS → Mushroom cards
                                        └─ Phase 4: camera integration → person binary_sensors
```

- **Zigbee stack:** Zigbee2MQTT, chosen over ZHA because MINI-ZB1GS/ZB2GS,
  SNZB-03PR2 and BASIC-ZB1GSP are fully supported there today while ZHA still
  needs quirks.
- **Coordinator:** Dongle Max in Coordinator mode (its web console), Ethernet
  with DHCP reservation, USB power from the UPS. Z2M adapter `ember`, port
  `tcp://<dongle-ip>:6638`. Mounted at ceiling height between kitchen and
  living room.
- **Zigbee channel:** 15, 20 or 25 chosen at setup to avoid the farm's Wi-Fi
  channel. Network key generated, `permit_join: false` after pairing.
- **Remote access:** Tailscale add-on. HA internal URL set to the Tailscale
  MagicDNS name so notification links and snapshots open from anywhere.
- **Notifications:** Companion app push; a `notify.security_phones` group fans
  out to every phone. Alarm triggers use critical/high priority.
- **Config style:** HA packages, one file per phase (§7). Dashboard in YAML
  mode. Everything version-controlled in this repo and copied to `/config`
  over Samba.

## 4. Device placement and naming

Zigbee2MQTT friendly names are fixed here so YAML can reference entity ids
before pairing. Two-gang switches expose `switch.<name>_l1` and `_l2`.

| Friendly name | Device | Location | l1 / state | l2 |
|---|---|---|---|---|
| `ext_north` | ZB2GS | Exterior north | porch light | floodlight |
| `ext_east` | ZB2GS | Exterior east | porch light | floodlight |
| `ext_south` | ZB2GS | Exterior south / balcony | porch light | floodlight |
| `ext_west` | ZB2GS | Exterior west | porch light | floodlight |
| `living` | ZB2GS | Living room | light | fan |
| `bedroom` | ZB2GS | Bedroom | light | fan |
| `kitchen` | ZB1GS | Kitchen | light | |
| `storage_fans_a` | ZB2GS (to buy) | Storage | fan 1 | fan 2 |
| `storage_fans_b` | ZB2GS (to buy) | Storage | fan 3 | fan 4 |
| `storage_fans_c` | ZB2GS (to buy) | Storage | fan 5 | spare |
| `toilet_first` | ZB1GS | First-floor toilet | light | |
| `bathroom_ground` | ZB1GS | Ground bathroom | light | |
| `storage` | ZBMINIR2 | Storage | lights | |
| `stairwell` | ZBMINIR2 | External stairwell | light | |
| `roof` | ZBMINIR2 | Roof | light | |
| `siren` | ZBMINIR2 | Near siren | 12 V PSU → siren | |
| `pump` | BASIC-ZB1GSP | Pump panel | starter coil circuit | |
| `pump_meter` | 3-phase meter | Pump panel | per-phase V/A/W, kWh | |
| `presence_north` … `presence_west` | SNZB-03PR2 ×4 | Under eaves, each side | occupancy, illuminance | |
| `door_storage` | SNZB-04PR1 | Storage door (ground) | contact, tamper | |
| `door_main` | SNZB-04PR1 | Main first-floor door | contact, tamper | |
| `door_stairs` | SNZB-04PR1 | Stairwell ground door | contact, tamper | |
| `door_roof` | SNZB-04PR1 | Roof door | contact, tamper | |

Fans: five in the ground-floor storage (individually switched), two on the
first floor (living, bedroom). A `fan.storage_all` group lets the dashboard
and automations treat the five storage fans as one.

HA areas: Exterior North/East/South/West, Living Room, Bedroom, Kitchen,
Toilet, Ground Bathroom, Storage, Stairwell, Roof, Pump Room, Utility.

The siren ZBMINIR2 runs in detached-relay mode so its wall-switch input cannot
silence the siren; the input is left free for an optional wired panic button.

## 5. Security behaviour

### 5.1 Alarm panel

HA `manual` alarm_control_panel, entity `alarm_control_panel.farm`.

| Setting | Default | Adjustable from System view |
|---|---|---|
| Code | 4-digit, required to disarm only | changed in YAML |
| Arming (exit) delay, Armed Away | 30 s | yes |
| Entry (pending) delay | 30 s on `door_main` only; all other sensors instant | yes |
| Trigger (siren) time | 180 s, then panel returns to previous armed state | yes |
| Modes | disarmed, armed_home, armed_away | |

Helpers: `input_boolean.bypass_door_<name>` ×4, `input_boolean.siren_on_person`,
`input_number.entry_delay`, `input_number.siren_duration`,
`input_text.last_security_event`.

### 5.2 Response matrix

| Event | Disarmed | Armed Home | Armed Away |
|---|---|---|---|
| Door opens (not bypassed) | log | trigger panel | trigger panel |
| Tamper on any sensor | notify | notify + trigger | notify + trigger |
| Exterior presence after dark | floodlight that side 3 min, log | floodlight + notify | floodlight + notify; trigger if `siren_on_person` and camera person-confirmed within 30 s (Phase 4) |
| Panel → triggered | | siren on, all floodlights on, critical push, log | same |
| Panel leaves triggered | | siren off, floodlights resume normal rule | same |
| Disarm | siren off immediately | | |

### 5.3 Lighting

- Porch lights (all `ext_*_l1`): on at sun elevation < 0°, off at > 0°.
- Floodlights (`ext_*_l2`): on when that side's presence is detected and sun
  is below horizon; off 3 min after presence clears unless the panel is
  triggered. Timer per side.

### 5.4 Health and power

- Battery < 20 % on any device: one daily digest notification at 09:00.
- Any Zigbee device unavailable > 30 min: notify.
- UPS on battery ≥ 60 s: "Grid down at farm". UPS back online: "Grid
  restored after N min".
- UPS charge < 20 % while on battery: notify, then host shutdown at 10 %.

### 5.5 Logging

Every event in §5.2 and §5.4 calls `script.security_log` which writes a
`logbook.log` entry with name `Security` and updates
`input_text.last_security_event`. The dashboard shows the last 24 h filtered
to that name.

## 6. Pump control and protection

### 6.1 Wiring (electrician)

- BASIC-ZB1GSP output contact is placed in the DOL starter's **coil circuit**,
  selected by a 3-position **MANUAL–OFF–AUTO** selector, with a latching
  E-STOP and the overload relay in series with both paths.
  - Manual: original START/STOP/hold-in circuit, Zigbee contact out of
    circuit.
  - Off: local stop for Auto mode (a momentary STOP cannot hold a maintained
    contact off).
  - Auto: Zigbee contact (maintained) feeds the coil.
- Control circuit must be 230 V L-N; a 415 V coil needs an interposing
  relay.
- Because Auto bypasses the starter's no-volt release, the pump relay uses
  `power_on_behavior: off` so a grid return never restarts the motor.
- The overload relay and E-STOP remain in series in both modes. Zigbee can
  only request a run; it can never defeat thermal protection.
- Motor feed passes through the 3-phase meter's CT clamps; meter voltage taps
  on all three phases.
- `docs/wiring/pump-starter.md` carries the diagram and checklist.

### 6.2 Behaviour

| Rule | Detail |
|---|---|
| Start | Phone tap sets `switch.pump` on and starts `timer.pump_run` (default `input_number.pump_run_minutes`, 60) |
| Timer end | pump off, notify "Pump stopped after N min" |
| Start verification | If `sensor.pump_meter_power` < 1000 W 15 s after start: pump off, notify "Pump did not start" |
| Running state | `binary_sensor.pump_running` = power > 1000 W (7.5 hp ≈ 5.5 kW running) |
| Phase loss | Any phase < 180 V while another ≥ 180 V, for 3 s: pump off, notify, latch `input_boolean.pump_fault` until cleared from dashboard |
| Grid at pump panel | Meter unavailable AND UPS on battery → grid down (already notified by §5.4); meter back → log |
| Energy | Z2M energy sensor → utility_meter daily and monthly |

Dry-run detection (undercurrent) is intentionally deferred until a week of
real current readings exists to set a threshold.

## 7. Repository and configuration layout

```
homeassistant/
  README.md
  install-log.md
  docs/
    superpowers/specs/2026-10-12-farm-security-ha-design.md
    wiring/pump-starter.md
    wiring/siren.md
    shopping-list.md
    device-inventory.md          living owned / assigned / paired / spare table
  config/                        mirrors HA /config, copied via Samba
    configuration.yaml           packages: !include_dir_named packages, lovelace yaml dashboard
    packages/
      alarm.yaml
      perimeter_lights.yaml
      notifications.yaml
      power.yaml
      pump.yaml
      zigbee_health.yaml
      cameras.yaml               Phase 4 hooks
    dashboards/security.yaml
  addons/
    zigbee2mqtt/configuration.yaml
    mosquitto.md  nut.md  tailscale.md  hacs.md
```

Each package is self-contained (helpers, templates, automations, scripts for
that feature). A failing package disables only its feature.

## 8. Dashboard

YAML-mode dashboard `security`, Sections layout, Mushroom cards, phone-first,
five views as bottom tabs:

1. **Security** (default): Mushroom alarm card; chips for last event, UPS,
   offline count; four door cards (contact, tamper badge, battery); four
   perimeter cards (presence, porch, flood); siren card with hold-to-activate
   and a Silence button; filtered logbook, 24 h.
2. **Home**: lights by Ground, First, Stairs & Roof; a Storage fans section
   with the five fans as tap-to-toggle tiles plus "all storage fans on/off";
   living and bedroom fans sit with their room lights.
3. **Pump**: start/stop, run-timer slider, running/fault state, per-phase V
   and A, live W, today/month kWh, run history, grid status, fault reset.
4. **System**: UPS charge/load/runtime; Zigbee devices sorted offline first
   then battery ascending with LQI; backups and update status; alarm settings
   (entry delay, siren duration, bypass toggles, siren-on-person,
   pump run minutes).
5. **Cameras** (Phase 4): 2×2 live tiles with person badge.

## 9. Phases

| Phase | Delivers | Depends on |
|---|---|---|
| 1 Core | Mosquitto, Z2M over TCP, all 22 devices paired and named, areas, Tailscale, notify group, NUT + UPS, HACS + Mushroom, README | UPS purchased |
| 2 Security | alarm, perimeter_lights, notifications, zigbee_health, power packages; siren wiring; dashboard views Security/Home/System | Phase 1, 12 V PSU |
| 3 Pump | pump package, electrician wiring, 3-phase meter paired, Pump view | Phase 1, meter, electrician |
| 4 Cameras | camera integration, person sensors wired into §5.2, Cameras view, snapshot in notifications | Phases 1–2, cameras + PoE switch |

Frigate on the HP ProDesk is deliberately deferred: the HD 530 iGPU handles
one or two detect streams, not four, and on-camera detection removes the need.

## 10. Delivery and verification

- Files are authored here. The user copies `config/` to HA's config share,
  runs Developer Tools → Check Configuration, then restarts. Add-ons follow the
  step files in `addons/`. No tool in this repo ever contacts the HA instance.
- Before handover each phase's `config/` is validated locally with
  `hass --script check_config` in a Python venv on the Mac.
- Feedback loop: when state is needed, the user downloads a specific export
  (Z2M device list, `home-assistant.log`, dashboard raw YAML) into `exports/`
  in this repo.
- Each phase ends with a physical test list, for example:
  - Armed Away, open `door_storage`: siren ≤ 2 s, floodlights on, critical
    push on all phones, siren off at 180 s, panel back to Armed Away.
  - Armed Away, open `door_main`: 30 s pending with push, then as above.
  - Disarm with code: siren off ≤ 2 s.
  - Walk past `presence_east` after dark: east floodlight on, off 3 min later.
  - Pull UPS mains: "Grid down" push within 90 s; restore: "Grid restored".
  - Pump start from phone with meter reading > 1 kW; remove one phase fuse
    with electrician present: pump off ≤ 5 s, fault latched, push.

## 11. Risks and open items

- SNZB-04PR1 Zigbee2MQTT support is not confirmed on the device database;
  the predecessor SNZB-04P is. If unsupported at pairing time, an external
  converter is added to Z2M (small, Phase 1).
- SNZB-03PR2 is an indoor sensor; outdoor life under hoods is untested. If
  false triggers or weather failures occur, replace with outdoor mmWave units
  in Phase 4 alongside cameras.
- Siren voltage is assumed 12 V DC; confirm from the label before buying the
  PSU.
- Tailscale requires working internet at the farm; the modem must be on the
  UPS. Push notifications also require the server to reach the internet.
- Pump wiring must be done by a licensed electrician; this design describes
  intent, not a certified drawing.
