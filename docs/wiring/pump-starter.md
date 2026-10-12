# Pump starter integration — for the electrician

Motor: 7.5 hp, 3-phase submersible, existing manual DOL starter (contactor
K1, overload relay OL, START and STOP push buttons, hold-in contact K1-aux).

Devices: SONOFF BASIC-ZB1GSP DIN-rail switch (friendly name `pump`), a
3-position selector MANUAL–OFF–AUTO (S-AM), a latching mushroom-head
emergency stop (E-STOP), a Zigbee 3-phase CT energy meter.

## Control voltage — read first

The BASIC-ZB1GSP is a 250 V AC device. The control circuit it switches
**must be 230 V line-to-neutral**. If the existing starter coil is 415 V
line-to-line, add an interposing 230 V relay: the Sonoff drives the
interposing relay's coil, and the interposing relay's contact replaces the
Sonoff contact in the diagram below. Never connect 415 V across the Sonoff.

## Control circuit intent

```
 Control L ─► E-STOP (NC, latching) ─► OL (NC) ─► STOP (NC) ─┬─► S-AM:MANUAL ─► START (NO) ─┬─► K1 coil ─► N
                                                             │                 └─ K1-aux ────┘
                                                             ├─► S-AM:OFF    (open)
                                                             └─► S-AM:AUTO   ─► BASIC-ZB1GSP contact (NO) ─► K1 coil ─► N
```

- **MANUAL**: the original START/STOP/hold-in circuit operates unchanged.
  Zigbee state has no effect.
- **OFF**: the coil cannot be energised from either path. This is the local
  stop for AUTO mode.
- **AUTO**: the Zigbee contact is a maintained contact feeding the coil.
  Remote start = Zigbee on; remote stop = Zigbee off. Because the contact is
  maintained, the momentary STOP button only stops the motor while it is
  held; local stop in AUTO is **turn S-AM to OFF** or hit the E-STOP.
- The E-STOP and the overload relay are in series with both paths: either
  one de-energises the coil regardless of mode or Zigbee state, and the
  E-STOP stays latched until twisted to release.
- **No no-volt release in AUTO.** A DOL starter normally will not restart
  after a power cut because the hold-in contact drops. The AUTO path
  bypasses that. The Zigbee relay is therefore configured
  `power_on_behavior: off` (addons/zigbee2mqtt.md) so it comes back open
  after a grid cut, and Home Assistant only re-closes it on a deliberate
  command.
- The BASIC-ZB1GSP switches only the coil circuit (< 1 A). It must never be
  in the motor power path.
- BASIC-ZB1GSP power: L and N from the 230 V control supply; it needs
  permanent power to stay on the Zigbee network.

## Energy meter

- Three CT clamps on L1, L2, L3 of the motor feed after the contactor.
- Voltage sense taps on L1, L2, L3 and N (or per the meter's manual).
- Meter power from the control supply.

## Acceptance test (electrician present)

1. S-AM = MANUAL: START runs the motor, STOP stops it and it stays stopped.
   Zigbee switch on/off has no effect.
2. S-AM = AUTO: `switch.pump` on from Home Assistant runs the motor; meter
   shows ≈ 5.5 kW; `switch.pump` off stops it.
3. S-AM = AUTO, motor running: turn S-AM to OFF → motor stops and stays
   stopped. Return to AUTO with Zigbee still on → motor restarts (expected;
   turn Zigbee off first if that is not wanted).
4. S-AM = AUTO, motor running: press E-STOP → motor stops and stays stopped
   until the E-STOP is released and Zigbee is cycled off/on.
5. S-AM = AUTO, motor running: cut the control supply for 10 s and restore
   → motor must NOT restart (Zigbee relay comes back off).
6. Overload test per the starter manual: trip must stop the motor in AUTO.
