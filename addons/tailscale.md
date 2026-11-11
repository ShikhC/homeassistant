# Tailscale remote access

1. Create a Tailscale account (tailscale.com) and install the app on every
   phone that will receive alerts; sign in on each.
2. Settings → Apps → App Store → Tailscale → Install → Start, "Start on
   boot" on.
3. Open the add-on Web UI → follow the login link → approve the machine.
4. In the Tailscale admin console → Machines → the HA node → Disable key
   expiry (otherwise access silently stops after 180 days).
5. Note the MagicDNS name, this install: `homeassistant.tail0b5409.ts.net`.
6. Settings → System → Network → Home Assistant URL:
   - Internet (external): `http://homeassistant.tail0b5409.ts.net:8123`
   - Local network: `http://homeassistant.local:8123`
7. On each phone: Companion app → Settings → Companion app → Servers →
   edit → External URL = the Tailscale URL. Enter the farm Wi-Fi SSID under
   "Internal connection" so the app uses the local URL at home.

Verification: with mobile data only and Tailscale connected, the app loads
the dashboard; a test notification from Developer Tools → Actions →
`notify.mobile_app_<phone>` arrives.
