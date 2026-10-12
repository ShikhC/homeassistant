# Sonoff PoE Dongle Max — coordinator setup

Goal: the dongle runs as a Zigbee coordinator reachable at a fixed IP over
Ethernet, powered by USB from the UPS.

1. Mount the dongle at ceiling height between kitchen and living room, both
   antennas attached. Connect Ethernet to the router and USB to a 5 V USB
   adapter plugged into the UPS.
2. On the router, create a DHCP reservation for the dongle's MAC and note
   the IP. This plan assumes `192.168.1.50`; edit
   `addons/zigbee2mqtt/configuration.yaml` if different.
3. Open the dongle's web console at `http://<ip>` (or `http://Dongle-M.local`).
4. Set EFR32MG24 operation mode to **Coordinator Mode**.
5. Set integration target to **Zigbee2MQTT**. Leave the serial-over-TCP port
   at `6638`, baud `115200`.
6. Reboot the dongle from the console. Confirm `nc -vz <ip> 6638` from the
   Mac reports open (only the dongle is contacted, never Home Assistant).

Verification: Zigbee2MQTT starts without "Error while opening serialport"
in its log (addons/zigbee2mqtt.md step 5).
