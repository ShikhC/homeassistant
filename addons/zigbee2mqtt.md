# Zigbee2MQTT — install, configure, pair

Prerequisite: Mosquitto running (addons/mosquitto.md), dongle in coordinator
mode (addons/dongle-max.md).

## Install

1. Zigbee2MQTT is not in the built-in store. Settings → Apps → App Store →
   three-dot menu (top right) → Repositories → add
   `https://github.com/zigbee2mqtt/hassio-zigbee2mqtt` → Close → refresh.
   A "Zigbee2MQTT" section appears; open **Zigbee2MQTT** (not Edge) →
   Install. Do not start yet.
2. `scripts/apply.sh` (addons/github-pull.md) has already placed the file
   at `/config/zigbee2mqtt/configuration.yaml`, with the dongle IP from the
   repo. The script installs it only while Z2M has never started; after
   first start it refuses to touch it, so a re-run can never create a new
   network. Change Z2M settings afterwards in the Z2M web UI only.
3. In the Terminal & SSH app create the MQTT secret (replace the password):
   ```sh
   echo "mqtt_password: <the z2m user password from addons/mosquitto.md>" > /config/zigbee2mqtt/secret.yaml
   ```
4. In the add-on's Configuration tab, set serial port to
   `tcp://192.168.31.186:6638` and adapter `ember` as well (the add-on merges
   its options into the file).
5. Start the add-on. Open its Log. Expect
   `Zigbee2MQTT started!` and `Coordinator firmware version`. If you see
   `Error while opening serialport`, re-check addons/dongle-max.md.
6. Open the Web UI (sidebar entry). Settings → Advanced: confirm channel 20,
   permit join off.
7. **Verify the network was created.** In the Terminal & SSH app:
   ```sh
   grep -c GENERATE /config/zigbee2mqtt/configuration.yaml
   ```
   must print `0`. If it prints anything else, Z2M has not started
   successfully; go back to step 5.
   Then in Home Assistant: Settings → System → Backups → Create backup
   named `z2m-network-created`. From this moment on, never copy the repo's
   `addons/zigbee2mqtt/configuration.yaml` to the box again. Tick the
   matching line in docs/phase1-checklist.md.

## Moving the system to the farmhouse (or any new network)

The only thing that changes is the dongle's address. Do NOT recopy the
configuration file.

1. On the farm router, give the Dongle Max a DHCP reservation and note the
   new IP.
2. Z2M Web UI → Settings → Settings → Serial → Port: change the address
   part of `tcp://<ip>:6638` to the new IP → Submit.
3. Z2M Web UI → Settings → Tools → Restart Zigbee2MQTT. The log should show
   `Zigbee2MQTT started!` again and every device keeps its name and
   history.

## Troubleshooting first start

- `zh:ember:uart:ash: Port Error: read ECONNRESET` repeating: something
  else holds the dongle's TCP port. The dongle serves one client. Check, in
  order: Settings → Devices & services for a configured **Zigbee Home
  Automation** (ZHA) entry or a Discovered card for the dongle (delete /
  ignore it); any other machine running Zigbee2MQTT or ZHA against the
  dongle; then reboot the dongle and restart the add-on. On Home Assistant
  OS nothing can run "underneath" HA, so a stray service there is not a
  possible cause (`docker ps` from Advanced SSH with protection mode off
  lists only `app_*`, `hassio_*` and `homeassistant`).
- A single ECONNRESET during startup followed by `Zigbee2MQTT started!` is
  the ember adapter resetting the radio and is normal.
- Add-on CLI from any terminal app: `ha apps restart 45df7312_zigbee2mqtt`,
  `ha apps logs 45df7312_zigbee2mqtt | tail -40`.

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

See addons/github-pull.md "Sending files back for review" for
`/config/zigbee2mqtt/devices.yaml`.
