# Farmhouse Home Assistant

Security-first Home Assistant setup for a two-floor farmhouse. Design:
`docs/superpowers/specs/2026-10-12-farm-security-ha-design.md`.

## Layout

- `config/` mirrors Home Assistant's `/config`. Copy it over the Samba share.
- `addons/` holds add-on configuration files and step-by-step runbooks.
- `inventory/devices.yaml` is the source of truth for every Zigbee device:
  name, model, location, owned or to buy. `docs/device-inventory.md` is
  generated from it.
- `docs/wiring/` is for the electrician.
- `scripts/validate.sh` lints and checks everything locally.

## Working rule

Nothing here talks to the Home Assistant box. Files go in by Samba; state
comes back as exports placed in `exports/` (git-ignored).

## Phases

1. Core: MQTT, Zigbee2MQTT, pairing, Tailscale, UPS, HACS.
2. Security: alarm panel, siren, perimeter lights, notifications, dashboard.
3. Pump: remote control, phase-loss protection, energy.
4. Cameras.

## Developing

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
scripts/validate.sh
.venv/bin/python scripts/inventory.py --write
```
