# Xsuite: Advanced Topics

## Dynamic Aperture Studies

Track particles for many turns to determine dynamic aperture:
```python
import xtrack as xt
import numpy as np

line = xt.load('lattice.json')
line.set_particle_ref('proton', p0c=7e12)

# Generate particles on a grid of normalized amplitudes
r_values = np.linspace(0, 10, 20)    # amplitudes in sigma
theta_values = np.linspace(0, np.pi/2, 7)  # angles

x_norm = []
y_norm = []
for r in r_values:
    for theta in theta_values:
        x_norm.append(r * np.cos(theta))
        y_norm.append(r * np.sin(theta))

particles = line.build_particles(
    x_norm=x_norm, y_norm=y_norm,
    nemitt_x=2.5e-6, nemitt_y=2.5e-6)

# Long tracking
line.optimize_for_tracking()
line.track(particles, num_turns=100000, turn_by_turn_monitor=True)

# Analyze survival
alive = particles.state > 0
# DA = minimum amplitude where particles are lost
```

## Tune Footprint

Compute amplitude-dependent tune shift (footprint):
```python
fp = line.get_footprint(
    nemitt_x=2.5e-6, nemitt_y=2.5e-6,
    n_turns=256,    # turns for FFT
    n_r=10,         # number of radial points
    n_theta=7,      # number of angular points
    r_range=(0.1, 6))  # amplitude range in sigma

# Plot
fp.plot()

# Access data
fp.qx   # horizontal tunes for each amplitude
fp.qy   # vertical tunes for each amplitude
```

### Custom Footprint with LinearRescale
```python
fp = line.get_footprint(
    nemitt_x=2.5e-6, nemitt_y=2.5e-6,
    linear_rescale_on_knobs=[
        xt.LinearRescale(knob_name='beambeam_scale', v0=0, dv=0.1)
    ])
```

## Stability Diagram

```python
sd = line.get_stability_diagram(
    nemitt_x=2.5e-6, nemitt_y=2.5e-6,
    n_turns=256,
    n_r=50, r_range=(0.1, 8))

# Access stability diagram data
sd.re_x, sd.im_x  # real and imaginary parts for horizontal
sd.re_y, sd.im_y  # real and imaginary parts for vertical
sd.plot()
```

## Closed Orbit and Trajectory Correction

### Basic Orbit Correction (SVD)
```python
# Correct closed orbit using all available correctors and monitors
correction = line.correct_trajectory(twiss_table=tw)

# Inspect correction
correction.x_correction   # applied corrections
correction.y_correction
```

### MICADO Correction
Use a limited number of correctors for best correction:
```python
correction = line.correct_trajectory(
    twiss_table=tw,
    correction_method='micado',
    n_micado=5)   # use only 5 correctors per plane
```

### Customized Correction
```python
correction = line.correct_trajectory(
    twiss_table=tw,
    run=False)     # don't apply yet

# Inspect singular values
correction.singular_values_x
correction.singular_values_y

# Apply with custom number of singular values
correction.correct(n_singular_values=20)
```

### Threading (for perturbed lattices)
When closed orbit search fails due to strong perturbations:
```python
correction = line.correct_trajectory(
    twiss_table=tw,
    thread=True)   # thread first, then correct
```

### Transfer Line Correction
```python
# Also works for transfer lines (not rings)
correction = line.correct_trajectory(
    twiss_table=tw)
```

## Taylor Maps and Segment Maps

### LineSegmentMap (simple transfer map)
Use for simplified tracking models:
```python
one_turn = xt.LineSegmentMap(
    length=26658.8832,
    betx=70., bety=80.,
    alfx=0., alfy=0.,
    qx=62.31, qy=60.32,
    longitudinal_mode='nonlinear',  # 'linear_fixed_qs', 'nonlinear'
    qs=2e-3,
    bets=731.27,
    dqx=2.0, dqy=2.0)  # chromaticity (optional)
```

### SecondOrderTaylorMap
Construct a second-order map from tracking:
```python
map = xt.SecondOrderTaylorMap.from_line(
    line=line, start='ip1', end='ip5')
# or from a full ring:
map = xt.SecondOrderTaylorMap.from_line(line=line)
```

## Numerical Reproducibility
For reproducible results across platforms:
```python
line.config.XTRACK_GLOBAL_XY_LIMIT = 1.0  # meters, default
line.config.XSUITE_GLOBAL_TURNS_LIMIT = 1e9
# Reproducibility is maintained within same platform and compilation
```

## PyHEADTAIL Interface
For combining PyHEADTAIL elements with Xsuite:
```python
# Enable PyHEADTAIL compatibility
import xpart as xp
xp.enable_pyheadtail_interface()
# Now particles can be used with PyHEADTAIL elements

# For GPU tracking with CPU PyHEADTAIL elements:
element.needs_cpu = True
element.needs_hidden_lost_particles = True
```

## Magnet Models and Integrators
```python
# Set model for bend/quadrupole elements
# Available models: 'full', 'bend-kick-bend', 'rot-kick-rot', 'expanded', 'adaptive'
line.configure_bend_model(core='full')
line.configure_bend_model(edge='full')
```

## Luminosity Calculations

```python
from xtrack.lumi import luminosity

lumi = luminosity(
    num_colliding_bunches=2808,
    num_particles_per_bunch=1.15e11,
    sigma_x=16.7e-6,
    sigma_y=16.7e-6,
    f_rev=11245,
    # ... additional parameters for crossing, separation, etc.
)
```

## Energy Program (Time-Dependent Energy)

For slow-cycling machines, define a time-dependent energy program:

```python
energy_prog = xt.EnergyProgram(
    t_s=[0, 0.5, 1.0, 1.5],
    kinetic_energy0=[0.16e9, 0.16e9, 25e9, 25e9])  # eV
line.energy_program = energy_prog
```

## Line Utility Methods

```python
# Cycle line to start from different element
line.cycle(name_first_element='ip1')

# Get line length
length = line.get_length()

# Get s-positions of elements
s_vals = line.get_s_position(at_elements=['ip1', 'ip5'], mode='upstream')

# Get elements by type
quads, quad_names = line.get_elements_of_type(xt.Quadrupole)

# Get element strengths
strengths = line.get_strengths()   # returns Table

# Get aperture table
aper = line.get_aperture_table()

# Build/discard tracker (freeze/unfreeze line)
line.build_tracker(_context=context)  # freeze and compile
line.discard_tracker()                 # unfreeze for editing

# Access line variables
line.vars['knob_name'] = 0.5          # set
val = line.vars['knob_name']           # get
line.vv['knob_name']                   # shorthand for value access

# Element references (for deferred expressions)
line.element_refs['quad1'].k1 = line.vars['kq']

# Compute transfer matrix
T = line.compute_T_matrix(start='elem_a', end='elem_b')

# Find closed orbit
co = line.find_closed_orbit()
```

## Export Formats

```python
# To MAD-X sequence
line.to_madx_sequence(sequence_name='myring')

# To MAD-NG
line.to_madng(sequence_name='seq')

# Table exports (works for twiss, survey, element tables)
table.to_json('file.json')
table.to_hdf5('file.h5')
table.to_csv('file.csv')
table.to_tfs('file.tfs')   # MAD-X TFS format
table.to_pandas()            # pandas DataFrame
```
