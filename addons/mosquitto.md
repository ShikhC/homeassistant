# Mosquitto broker

1. Settings → Apps → App Store → Mosquitto broker → Install → Start.
   Enable "Start on boot" and "Watchdog".
2. Settings → People → Users → Add user: username `z2m`, a long password.
   Leave the other options at their defaults. Save the password for
   `secret.yaml` (addons/zigbee2mqtt.md).
3. Settings → Devices & services: the MQTT integration is discovered.
   Configure → accept the broker defaults. The "MQTT" card shows Connected.

Verification: Settings → Devices & services → MQTT → Configure → Listen to
`zigbee2mqtt/bridge/state` shows `online` once Z2M runs.
