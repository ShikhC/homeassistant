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
   host `a0d7b954-nut`, port `3493`, username/password from step 3. Select
   at least: Status, Battery charge, Load, Battery runtime, Input voltage.
5. Rename the device to `UPS` so entity ids become `sensor.ups_status`,
   `sensor.ups_battery_charge`, `sensor.ups_load`,
   `sensor.ups_battery_runtime`, `sensor.ups_input_voltage`.

Verification: pull the UPS mains plug; within 30 s `sensor.ups_status`
reads `On Battery`; replace it; reads `Online`.
