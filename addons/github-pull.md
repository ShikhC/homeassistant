# Getting the repo onto the box via GitHub

The Mac never connects to Home Assistant. The repo is pushed to GitHub and
the box pulls it with its own Terminal app.

## One-time setup

1. Push this repo to GitHub (public is simplest; nothing secret is tracked,
   `secrets.yaml` is git-ignored). For a private repo you will paste a
   read-only token into the clone URL in step 4.
2. Home Assistant → Settings → Apps → App Store → **Terminal & SSH** →
   Install → Start → "Start on boot" on → **Open Web UI**. A black terminal
   appears; you are now typing on the HP ProDesk.
3. Type the following and press Enter after each line (replace the URL):
   ```sh
   cd /config
   git clone https://github.com/<you>/homeassistant farm
   ```
   For a private repo: `git clone https://<token>@github.com/<you>/homeassistant farm`
4. Apply the files:
   ```sh
   sh /config/farm/scripts/apply.sh
   ```
   Expected output ends with `HA config refreshed in /config` and
   `Zigbee2MQTT config installed ... (first start pending)`.
5. Create the secrets file once:
   ```sh
   cp /config/farm/config/secrets.yaml.example /config/secrets.yaml
   ```
6. Settings → Developer tools → YAML → **Check configuration** →
   "Configuration valid" → **Restart**.

## Every later update

In the Terminal app:
```sh
cd /config/farm && git pull && sh scripts/apply.sh
```
then Check configuration → Restart. The script never overwrites the
Zigbee2MQTT file once Z2M has started (it prints "not touching"), and never
overwrites automations you created in the UI.

## Sending files back for review

Still in the Terminal app, for example the Zigbee2MQTT device list:
```sh
mkdir -p /config/farm/exports && cp /config/zigbee2mqtt/devices.yaml /config/farm/exports/
cd /config/farm && git add exports && git commit -m "Export Z2M devices" && git push
```
(`exports/` is git-ignored by default; remove that line from `.gitignore`
first if you want exports tracked, or paste the file contents into the
chat instead.)
