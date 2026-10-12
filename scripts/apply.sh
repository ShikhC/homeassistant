#!/bin/sh
# Run ON the Home Assistant box, inside the Terminal & SSH app, from the
# cloned repo:   sh /config/farm/scripts/apply.sh
# Copies this repo's config into /config. Safe to re-run at any time:
#  - configuration.yaml, packages/ and dashboards/ are always refreshed
#  - automations.yaml / scripts.yaml / scenes.yaml are created only if missing
#  - the Zigbee2MQTT file is installed only until Z2M has started once
set -eu
REPO=$(cd "$(dirname "$0")/.." && pwd)
CFG=${HA_CONFIG:-/config}

mkdir -p "$CFG/packages" "$CFG/dashboards"
cp "$REPO/config/configuration.yaml" "$CFG/configuration.yaml"
cp "$REPO"/config/packages/*.yaml "$CFG/packages/"
cp "$REPO"/config/dashboards/*.yaml "$CFG/dashboards/"
for f in automations.yaml scripts.yaml scenes.yaml; do
  [ -f "$CFG/$f" ] || cp "$REPO/config/$f" "$CFG/$f"
done
[ -f "$CFG/secrets.yaml" ] || echo "note: create $CFG/secrets.yaml from config/secrets.yaml.example"
echo "HA config refreshed in $CFG"

Z="$CFG/zigbee2mqtt/configuration.yaml"
if [ -f "$Z" ] && ! grep -q GENERATE "$Z"; then
  echo "Zigbee2MQTT already initialised (network key present); not touching $Z"
else
  mkdir -p "$CFG/zigbee2mqtt"
  cp "$REPO/addons/zigbee2mqtt/configuration.yaml" "$Z"
  echo "Zigbee2MQTT config installed at $Z (first start pending)"
fi
