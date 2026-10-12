# HACS and Mushroom

1. Settings → Apps → App Store → Terminal & SSH → Install → Start → open.
2. Run: `wget -O - https://get.hacs.xyz | bash -`
3. Settings → System → Restart Home Assistant.
4. Settings → Devices & services → Add integration → HACS → follow the
   GitHub device-code login.
5. HACS → search "Mushroom" → Download. HACS registers the card resource
   globally, so the YAML dashboard needs nothing extra.
6. Hard-refresh the browser. Open the sidebar entry "Farm" → the Home view
   renders Mushroom tiles (they show "Entity not found" until pairing).

Verification: a Mushroom tile toggles `switch.living_l1` after pairing.
