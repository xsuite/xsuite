# Xsuite: Matching and Optimization

## Basic Usage

The `line.match()` method uses a numerical optimizer to adjust knobs to achieve desired values from twiss or other actions.

```python
import xtrack as xt

line = xt.load('lattice.json')

# Match tunes and chromaticities
opt = line.match(
    method='4d',
    vary=[
        xt.VaryList(['kqtf.b1', 'kqtd.b1'], step=1e-8, tag='quad'),
        xt.VaryList(['ksf.b1', 'ksd.b1'], step=1e-4, limits=[-0.1, 0.1], tag='sext'),
    ],
    targets=[
        xt.TargetSet(qx=62.315, qy=60.325, tol=1e-6, tag='tune'),
        xt.TargetSet(dqx=10.0, dqy=12.0, tol=0.01, tag='chrom'),
    ])

# Inspect results
opt.log()
opt.target_status()
opt.vary_status()
opt.get_knob_values()
opt.get_knob_values(iteration=0)  # values before optimization
```

## Vary Objects

```python
# Single vary
xt.Vary('knob_name', step=1e-8)
xt.Vary('knob_name', step=1e-8, limits=[-0.5, 0.5])

# List of varies
xt.VaryList(['knob1', 'knob2'], step=1e-8, tag='group_name')
```

## Target Objects

```python
# Set targets (from twiss results)
xt.Target('qx', value=62.31, tol=1e-6)
xt.Target('betx', value=100.0, at='ip1', tol=0.1)

# Target set (multiple in one)
xt.TargetSet(qx=62.31, qy=60.32, tol=1e-6)
xt.TargetSet(betx=0.15, bety=0.15, at='ip1', tol=0.001)

# Targets at specific locations
xt.Target('x', value=0.001, at='corrector_1')
xt.Target('x', value=0, at=xt.END)        # at end of range
xt.Target('x', value=0, at=xt.START)      # at start of range

# Inequalities
xt.Target('betx', xt.GreaterThan(50), at='ip1')
xt.Target('betx', xt.LessThan(200), at='ip1')

# Target from callable
xt.Target(lambda tw: tw['betx', 'ip1'] - tw['bety', 'ip1'], value=0)
```

## Match at Specific Locations (Orbit Bumps)

```python
opt = line.match(
    start='corrector_0', end='corrector_5',
    init_at=xt.START,    # boundary conditions at start
    betx=tw_ref['betx', 'corrector_0'],  # boundary from reference table
    bety=tw_ref['bety', 'corrector_0'],
    vary=[
        xt.Vary('acbh_corr1', step=1e-10),
        xt.Vary('acbh_corr2', step=1e-10),
        xt.Vary('acbh_corr3', step=1e-10),
    ],
    targets=[
        xt.Target('x', value=0.003, at='ip'),
        xt.Target('x', value=0, at=xt.END),
        xt.Target('px', value=0, at=xt.END),
    ])
```

## Match Involving Multiple Lines

```python
opt = line_b1.match(
    lines=['lhcb1', 'lhcb2'],  # collider line names
    vary=[
        xt.VaryList(['acbx_ir1_b1', 'acbx_ir1_b2'], step=1e-10),
    ],
    targets=[
        xt.Target('px', value=250e-6, at='ip1', line='lhcb1'),
        xt.Target('px', value=-250e-6, at='ip1', line='lhcb2'),
    ])
```

## Matching on Custom Actions

```python
class MyAction(xt.Action):
    def run(self):
        # Perform custom computation
        line.track(particles, num_turns=100)
        qx = ... # compute from tracking
        return {'qx_track': qx}

opt = line.match(
    vary=[xt.Vary('kqf', step=1e-8)],
    targets=[xt.Target(action=MyAction(), tar='qx_track', value=62.31)])
```

## Interactive Match

```python
opt = line.match(
    solve=False,    # don't solve immediately
    vary=[...],
    targets=[...])

opt.step(10)        # run 10 iterations
opt.target_status() # check progress
opt.tag('step1')    # save current state
opt.step(20)        # more iterations
opt.reload('step1') # go back to saved state
opt.disable(target='tune')  # disable targets by tag
opt.enable(target='tune')   # re-enable
opt.solve()         # solve to convergence
```

## Create New Knobs by Matching (match_knob)

```python
line.match_knob(
    knob_name='dqx_knob',
    knob_value_start=0,
    knob_value_end=1,
    vary=[xt.VaryList(['ksf.b1', 'ksd.b1'], step=1e-4)],
    targets=[
        xt.TargetSet(dqx=15., dqy=tw.dqy, tol=0.05),
    ])

# Now use the knob
line.vars['dqx_knob'] = 0.5  # sets intermediate value (linear interpolation)
```

## Targets from Variables and Line Elements

```python
targets = [
    xt.Target(line='lhcb1', tar='kqtf.b1', value=0.01),  # target on variable
    xt.TargetSet(at='mq.12.l5.b1', betx=100, line='lhcb1'),  # target on element
]
```

## Specialized Targets

```python
# Phase advance target between two elements
xt.TargetRelPhaseAdvance(mux=0.25, start='elem_a', end='elem_b')

# R-matrix element target
xt.TargetRmatrixTerm(r_term='r11', value=0.5, start='a', end='b')

# Full R-matrix target
xt.TargetRmatrix(r_matrix=R_desired, start='a', end='b')

# Luminosity target (for colliders)
xt.TargetLuminosity(...)

# Separation target (for colliders)
xt.TargetSeparation(...)
xt.TargetSeparationOrthogonalToCrossing(...)
```

## Amplitude Detuning and Non-Linear Chromaticity

Computed from tracking, useful in matching workflows:

```python
# Amplitude detuning coefficients
adc = line.get_amplitude_detuning_coefficients(
    nemitt_x=2.5e-6, nemitt_y=2.5e-6)
# Returns dqx/dJx, dqx/dJy, dqy/dJy coefficients

# Non-linear chromaticity
nlc = line.get_non_linear_chromaticity()
```
