# UPS monitoring with NUT

Hardware: a USB UPS (APC Back-UPS BX600C-IN / BX1100C-IN class). It powers
the HP ProDesk, router, internet modem and the Dongle Max USB adapter.

1. Connect the UPS USB cable to the HP ProDesk.
2. Settings → Apps → App Store → "Network UPS Tools" → Install.
3. Configuration tab:
   ```yaml
   users:
     - username: nutuser
       password: <long password>
       instcmds: [all]
       actions: [set]
   devices:
     - name: ups
       driver: usbhid-ups
       port: auto
   mode: netserver
   shutdown_host: false
   ```
   Start the add-on, "Start on boot" on. Log must show `Startup successful`.
4. Settings → Devices & services → Add integration → "Network UPS Tools":
   host `a0d7b954-nut`, port `3493`, username/password from step 3, then
   pick the `ups` device. Sensors appear as `sensor.ups_status`,
   `sensor.ups_battery_charge`, `sensor.ups_load`, `sensor.ups_input_voltage`.
5. Open the UPS device page → the "+N entities not shown" link → enable
   **Battery runtime** (it is disabled by default) so
   `sensor.ups_battery_runtime` exists for the dashboard.

Verification: pull the UPS mains plug; within 30 s `sensor.ups_status`
reads `On Battery`; replace it; reads `Online`.
