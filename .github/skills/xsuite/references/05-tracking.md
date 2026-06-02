# Xsuite: Tracking

## Basic Tracking

```python
import numpy as np
import xtrack as xt

line = xt.Line(
    elements=[xt.Drift(length=2.),
              xt.Multipole(knl=[0, 0.5], ksl=[0,0]),
              xt.Drift(length=1.),
              xt.Multipole(knl=[0, -0.5], ksl=[0,0])],
    element_names=['drift_0', 'quad_0', 'drift_1', 'quad_1'])
line.set_particle_ref('proton', p0c=6.5e12)

# Build particles
particles = line.build_particles(
    x=np.random.uniform(-1e-3, 1e-3, 200),
    px=np.random.uniform(-1e-5, 1e-5, 200),
    y=np.random.uniform(-2e-3, 2e-3, 200),
    py=np.random.uniform(-3e-5, 3e-5, 200),
    zeta=np.random.uniform(-1e-2, 1e-2, 200),
    delta=np.random.uniform(-1e-4, 1e-4, 200))

# Track without saving turn-by-turn data
line.track(particles, num_turns=100)

# Access results
particles.state  # > 0 for alive particles
particles.at_turn  # turn number (or turn of loss for lost particles)
particles.x  # final x position

# Track with turn-by-turn monitoring
particles2 = line.build_particles(x=[1e-3, 2e-3])
line.track(particles2, num_turns=100, turn_by_turn_monitor=True)

# Access turn-by-turn data
line.record_last_track.x   # shape: (n_particles, n_turns)
line.record_last_track.px
```

## Tracking Range (Start/Stop Elements)

```python
# Track through a portion of the line
line.track(particles, ele_start='element_a', ele_stop='element_b')

# Track from element to end, then from start to element
line.track(particles, ele_start='mid_ring', num_turns=1)
```

## Backtracking

```python
line.track(particles, num_turns=10, backtrack=True)
```

## Freeze Longitudinal Motion

When you want to track with frozen longitudinal dynamics (e.g., for studies at fixed delta):

```python
# Using context manager
with xt.freeze_longitudinal(line):
    line.track(particles, num_turns=100)

# Explicit freeze/unfreeze
line.freeze_longitudinal()
line.track(particles, num_turns=100)
line.unfreeze_longitudinal()

# Or on individual twiss/track calls
tw = line.twiss(freeze_longitudinal=True)
```

## Monitors

### Quick Monitor (turn-by-turn at start)
```python
line.track(particles, num_turns=1000, turn_by_turn_monitor=True)
mon = line.record_last_track  # access monitor data
mon.x   # shape (n_particles, n_turns)
mon.px
mon.y
# etc.
```

### Custom Monitor (configure buffer size, start/stop turns)
```python
monitor = xt.ParticlesMonitor(
    start_at_turn=0,
    stop_at_turn=500,
    num_particles=n_part)
line.track(particles, num_turns=500, turn_by_turn_monitor=monitor)
# monitor.x, monitor.px, etc.
```

### Multiframe Monitor
```python
monitor = xt.ParticlesMonitor(
    start_at_turn=0,
    stop_at_turn=100,
    n_repetitions=5,    # record 5 frames
    repetition_period=200,  # every 200 turns
    num_particles=n_part)
```

### Monitors as Beam Elements
Monitors can be inserted into the line as beam elements to record at specific locations:
```python
monitor = xt.ParticlesMonitor(num_particles=n_part,
                               start_at_turn=0, stop_at_turn=100)
line.insert_element(element=monitor, name='my_monitor', index=42)
line.track(particles, num_turns=100)
```

### Beam Position Monitor (BPM)
```python
bpm = xt.BeamPositionMonitor(num_particles=n_part, start_at_turn=0, stop_at_turn=1000)
# Records mean x, y for each turn
```

### Beam Size Monitor
```python
bsm = xt.BeamSizeMonitor(num_particles=n_part, start_at_turn=0, stop_at_turn=1000)
# Records sigma_x, sigma_y for each turn
```

### Last Turns Monitor
```python
ltm = xt.LastTurnsMonitor(num_particles=n_part, n_last_turns=20)
# Always keeps the last 20 turns for each particle
```

### Multi-Element Monitor
Records turn-by-turn data at multiple elements simultaneously:
```python
monitor = xt.MultiElementMonitor(
    element_names=['bpm1', 'bpm2', 'bpm3'],
    start_at_turn=0, stop_at_turn=100, num_particles=n_part)
line.insert_element(element=monitor, name='mem')
```

## Acceleration (Energy Ramp)

For energy ramps, use `ReferenceEnergyIncrease` elements and time-dependent expressions:
```python
# Simple acceleration
line.insert_element(
    element=xt.ReferenceEnergyIncrease(Delta_p0c=1e6),  # 1 MeV/turn
    name='accel', index=0)

# Energy ramp with time-dependent functions
env['Delta_E'] = 0
env.ref['accel_elem'].Delta_p0c = env.ref['Delta_E']
# Link Delta_E to a function of t_turn_s
```

## Time-Dependent Knobs

The variable `t_turn_s` provides time in seconds and is updated each turn:
```python
# Sinusoidal excitation
import xdeps as xd
env.ref['corr_knob'] = 0.001 * xd.FunctionPieceWiseLinear.sin(
    2 * np.pi * 100 * env.ref['t_turn_s'])  # 100 Hz modulation

# Piece-wise linear function
f_pwl = xd.FunctionPieceWiseLinear(x=[0, 0.001, 0.002, 0.003],
                                     y=[0, 1, 1, 0])
env.ref['bump_knob'] = 0.005 * f_pwl(env.ref['t_turn_s'])
```

## Optimize for Multi-Turn Tracking

```python
line.optimize_for_tracking()  # merges consecutive drifts, etc.
```

## Radial Steering (for slow-cycling machines)
For machines where the energy changes during a cycle, radial steering adjusts RF frequency to move the beam radially:
```python
line.enable_radial_steering()
```
