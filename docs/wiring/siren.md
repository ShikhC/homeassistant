# Siren wiring

Parts: ZBMINIR2 (friendly name `siren`), 12 V DC PSU ≥ 2 A, the 120 dB
wired siren.

```
 Mains L ──► ZBMINIR2 L_in          ZBMINIR2 L_out ──► PSU AC L
 Mains N ──► ZBMINIR2 N        and  Mains N        ──► PSU AC N
                                    PSU +12 V      ──► Siren +
                                    PSU 0 V        ──► Siren −
```

- ZBMINIR2 S1/S2 input: leave disconnected; `detach_relay_mode` is ON in
  Zigbee2MQTT so a wall switch can never silence the siren. Optional: a
  momentary push button on S1 becomes a panic button in Phase 2.
- Mount the siren high on the exterior wall facing away from the house,
  the PSU and ZBMINIR2 indoors in a junction box.
- Confirm the siren's rated voltage on its label before buying the PSU.
  If it is 24 V, buy a 24 V PSU; the wiring is identical.

Test: Developer Tools → Actions → `switch.turn_on` on `switch.siren`
sounds the siren; `switch.turn_off` silences it.
