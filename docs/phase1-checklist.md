# Phase 1 checklist

Tick in order. Each step names its runbook.

## Before going to the farm
- [ ] Buy UPS, 3 × MINI-ZB2GS, 5 V USB adapter, weather hoods (docs/shopping-list.md).
- [ ] Install the Companion app and Tailscale on every phone.
- [ ] `scripts/validate.sh` passes on the Mac.

## On the farm
- [ ] UPS installed; server, router, modem on it (addons/nut.md hardware).
- [ ] Copy `config/` from the repo to the Samba `config` share
      (overwrite `configuration.yaml`; keep existing `.storage`). Create
      `secrets.yaml` from `secrets.yaml.example`.
- [ ] Developer Tools → YAML → Check configuration → "Configuration valid".
- [ ] Settings → System → Restart.
- [ ] Mosquitto (addons/mosquitto.md).
- [ ] Dongle Max coordinator mode and IP (addons/dongle-max.md).
- [ ] Zigbee2MQTT installed and started (addons/zigbee2mqtt.md "Install").
- [ ] HACS + Mushroom (addons/hacs.md). Sidebar "Farm" opens.
- [ ] Tailscale (addons/tailscale.md). Phone loads HA on mobile data.
- [ ] NUT (addons/nut.md). `sensor.ups_status` = Online.
- [ ] Edit `config/packages/notifications.yaml`: replace `mobile_app_phone_1`
      with each real `mobile_app_<device>` action; recopy; restart.

## Pair devices (addons/zigbee2mqtt.md "Pair and name")
Order: `living`, `bedroom`, `kitchen`, `toilet_first`, `ext_north`,
`ext_east`, `ext_south`, `ext_west`, `bathroom_ground`, `storage`,
`storage_fans_a`, `storage_fans_b`, `storage_fans_c`, `stairwell`, `roof`,
`siren`, `pump`, then `door_main`, `door_storage`, `door_stairs`,
`door_roof`, `presence_north`, `presence_east`, `presence_south`,
`presence_west`.
- [ ] Each device renamed in Z2M, `status: paired` in `inventory/devices.yaml`.
- [ ] Settings → Areas: create Exterior North/East/South/West, Living Room,
      Bedroom, Kitchen, Toilet, Ground Bathroom, Storage, Stairwell, Roof,
      Pump Room, Utility; assign each Z2M device to its area.
- [ ] Z2M map: every battery device has a router neighbour.

## Acceptance (spec §10)
- [ ] Tap "Living light" on the Farm dashboard: light toggles within 1 s.
- [ ] Open `door_main`: `binary_sensor.door_main_contact` goes `on` in HA.
- [ ] Walk past `presence_east`: `binary_sensor.presence_east_occupancy` goes `on`.
- [ ] Pull UPS mains: `sensor.ups_status` = On Battery within 30 s; restore.
- [ ] Developer Tools → Actions → `notify.security_phones` with message
      "test": every phone receives it on mobile data.
- [ ] Settings → System → Backups → create a full backup named "phase1".

## Export back to the repo
- [ ] Copy `/config/zigbee2mqtt/devices.yaml` to `exports/z2m/devices.yaml`.
- [ ] Download diagnostics for the MQTT integration into `exports/`.
- [ ] Commit `inventory/devices.yaml` and regenerated `docs/device-inventory.md`.
