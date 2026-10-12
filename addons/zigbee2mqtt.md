# Zigbee2MQTT — install, configure, pair

Prerequisite: Mosquitto running (addons/mosquitto.md), dongle in coordinator
mode (addons/dongle-max.md).

## Install

1. Settings → Apps → App Store → Zigbee2MQTT → Install. Do not start yet.
2. Copy `addons/zigbee2mqtt/configuration.yaml` from this repo to
   `/config/zigbee2mqtt/configuration.yaml` over the Samba share (create the
   folder if needed). Fix the IP if yours is not `192.168.1.50`.
   **Copy it exactly once, before the first start.** Z2M fills in the real
   network key on first start; copying the file again later creates a new
   network and orphans every paired device. Change settings afterwards in
   the Z2M web UI only.
3. Create `/config/zigbee2mqtt/secret.yaml`:
   ```yaml
   mqtt_password: <the z2m user password from addons/mosquitto.md>
   ```
4. In the add-on's Configuration tab, set serial port to
   `tcp://192.168.1.50:6638` and adapter `ember` as well (the add-on merges
   its options into the file).
5. Start the add-on. Open its Log. Expect
   `Zigbee2MQTT started!` and `Coordinator firmware version`. If you see
   `Error while opening serialport`, re-check addons/dongle-max.md.
6. Open the Web UI (sidebar entry). Settings → Advanced: confirm channel 20,
   permit join off.

## Pair and name

Pair devices one at a time, nearest the coordinator first, mains switches
before battery sensors (switches become routers that extend range).

1. Web UI → Permit join (All) → it auto-disables after 254 s.
2. Put the device in pairing mode:
   - MINI-ZB1GS / MINI-ZB2GS / ZBMINIR2 / BASIC-ZB1GSP: power on, hold the
     button 5 s until the LED blinks.
   - SNZB-03PR2 / SNZB-04PR1: pull the battery tab, hold the button 5 s.
3. If the device page says **Unsupported** (possible for SNZB-04PR1, see
   spec §11): note the `model` and `zigbeeModel` shown, stop pairing that
   model, and report them so an external converter can be added. Do not
   rename or rely on its entities yet.
4. When it appears, click the device → Rename → enter the friendly name from
   `docs/device-inventory.md` exactly, tick "Update Home Assistant entity
   ID". Set the `status` for that device to `paired` in
   `inventory/devices.yaml` and run `scripts/inventory.py --write`.
5. For two-gang switches confirm two entities appear in HA:
   `switch.<name>_l1` and `switch.<name>_l2`.
6. For the `siren` ZBMINIR2: device page → Settings (specific) →
   `detach_relay_mode` = ON so the wall switch input no longer drives the
   relay.
7. Power-on behaviour (device page → Settings (specific)):
   - `pump`: `power_on_behavior` = **off**. When the grid returns the relay
     must stay open; otherwise a 7.5 hp motor restarts unattended.
   - `siren`: `power_on_behavior` = **off**.
   - every other switch: `power_on_behavior` = `previous` (both gangs on
     two-gang models: `power_on_behavior_l1` and `_l2`).
8. After the last device: Permit join off (it should already be), then
   verify the Web UI map shows every battery device linked to a router.

## Export for the repo

Web UI → Settings → Tools → "Download state" and copy
`/config/zigbee2mqtt/database.db` and `devices.yaml` into `exports/z2m/` on
the Mac when asked. These are git-ignored.
