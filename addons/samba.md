# Samba share — see the Home Assistant config folder in Finder

1. Settings → Apps → App Store → search `Samba share` → Install.
2. Configuration tab: set a `username` and a `password` (anything you will
   remember). Leave the rest. Save.
3. Start the app, turn on "Start on boot".
4. On the Mac: Finder → Go → Connect to Server (⌘K) → type
   `smb://homeassistant.local` → Connect → choose "Registered User" and
   enter the username/password from step 2 → select the `config` share.
5. A Finder window opens showing files like `configuration.yaml`. That
   folder is Home Assistant's `/config`. Everything in this repo's `config/`
   folder is copied into it.

Verification: you can open `configuration.yaml` from the share in TextEdit.
