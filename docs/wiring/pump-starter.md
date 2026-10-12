# Pump starter integration — for the electrician

Motor: 7.5 hp, 3-phase submersible, existing manual DOL starter (contactor
K1, overload relay OL, START and STOP push buttons, hold-in contact K1-aux).

Devices: SONOFF BASIC-ZB1GSP DIN-rail switch (friendly name `pump`), a
2-position AUTO/MANUAL selector S-AM, a Zigbee 3-phase CT energy meter.

## Control circuit intent

```
 Control L ──► OL (NC) ──► STOP (NC) ──┬─► S-AM:MANUAL ─► START (NO) ─┬─► K1 coil ─► Control N
                                       │                 └─ K1-aux ────┘
                                       └─► S-AM:AUTO  ─► BASIC-ZB1GSP contact (NO) ─► K1 coil
```

- In MANUAL the original START/STOP/hold-in circuit operates unchanged.
- In AUTO the Zigbee contact is a maintained contact feeding the coil.
  STOP and the overload relay remain in series: pressing STOP or an
  overload trip de-energises the coil regardless of Zigbee state.
- The BASIC-ZB1GSP switches only the coil circuit (< 1 A). It must never be
  in the motor power path.
- BASIC-ZB1GSP power: L and N from the control supply; it needs permanent
  power to stay on the Zigbee network.

## Energy meter

- Three CT clamps on L1, L2, L3 of the motor feed after the contactor.
- Voltage sense taps on L1, L2, L3 and N (or per the meter's manual).
- Meter power from the control supply.

## Acceptance test (electrician present)

1. S-AM = MANUAL: START runs the motor, STOP stops it. Zigbee switch state
   has no effect.
2. S-AM = AUTO: `switch.pump` on from Home Assistant runs the motor; meter
   shows ≈ 5.5 kW; `switch.pump` off stops it.
3. S-AM = AUTO, motor running: press STOP → motor stops although Zigbee is
   still on. Turn Zigbee off then on to restart.
4. Overload test per the starter manual: trip must stop the motor in AUTO.
