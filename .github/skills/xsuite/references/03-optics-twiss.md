# Xsuite: Optics and Twiss Calculations

## Basic Twiss Usage (Ring)

```python
import xtrack as xt

line = xt.load('lattice.json')
line.set_particle_ref('proton', energy0=7e12)
line['vrf400'] = 16  # set RF voltage

tw = line.twiss()

# Global quantities
tw.qx    # Horizontal tune
tw.qy    # Vertical tune
tw.dqx   # Horizontal chromaticity
tw.dqy   # Vertical chromaticity
tw.slip_factor              # slip factor
tw.momentum_compaction_factor  # momentum compaction

# Per-element quantities (arrays indexed by element)
tw.s      # longitudinal position
tw.betx   # horizontal beta function
tw.bety   # vertical beta function
tw.alfx   # horizontal alpha function
tw.alfy   # vertical alpha function
tw.dx     # horizontal dispersion
tw.dy     # vertical dispersion
tw.dpx    # horizontal dispersion derivative
tw.dpy    # vertical dispersion derivative
tw.x      # horizontal closed orbit
tw.y      # vertical closed orbit
tw.px     # horizontal orbit angle
tw.py     # vertical orbit angle
tw.mux    # horizontal phase advance
tw.muy    # vertical phase advance
```

## Inspecting Twiss Output

```python
# Table access
tw['betx']                        # array of betx at all elements
tw['betx', 'ip1']                 # betx at element named 'ip1'
tw.rows['ip1':'ip5']              # slice between elements
tw.rows['ip1':'ip5', 'betx bety'] # specific columns for slice
tw.cols['betx bety']              # only specific columns

# As pandas DataFrame
df = tw.to_pandas()
```

## 4D Method (RF off)

When RF cavities are disabled or not in the lattice, use the 4D method:
```python
tw = line.twiss4d()
# or equivalently:
tw = line.twiss(method='4d')
```

## Off-Momentum Twiss

Measure tune vs momentum offset:
```python
delta_values = np.linspace(-1e-3, 1e-3, 50)
qx_values = []
for dd in delta_values:
    tw = line.twiss(method='4d', delta0=dd)
    qx_values.append(tw.qx)
```

## Twiss with Initial Conditions

```python
# From explicit values
tw_init = xt.TwissInit(
    betx=10., bety=20., alfx=0., alfy=0.,
    dx=0., dpx=0., x=0., px=0., y=0., py=0.,
    mux=0., muy=0.)
tw = line.twiss(start='element_a', end='element_b', init=tw_init)

# From an existing twiss table at a specific element
tw_full = line.twiss()
tw = line.twiss(start='element_a', end='element_b',
                init_at='element_a', init=tw_full)
```

## Periodic Twiss on a Portion of a Line

```python
tw = line.twiss(start='cell_start', end='cell_end',
                init='periodic')
```

## Beam Sizes from Twiss

```python
tw = line.twiss()
sigma_x = tw.get_beam_covariance(nemitt_x=2.5e-6, nemitt_y=2.5e-6,
                                   sigma_z=0.08).sigma_x
sigma_y = tw.get_beam_covariance(nemitt_x=2.5e-6, nemitt_y=2.5e-6,
                                   sigma_z=0.08).sigma_y
```

## Normalized Coordinates

```python
# Convert physical to normalized coordinates
norm_coord = tw.get_normalized_coordinates(particles,
                                            nemitt_x=2.5e-6,
                                            nemitt_y=2.5e-6)
norm_coord.x_norm    # normalized x
norm_coord.px_norm   # normalized px
```

## Reverse Twiss (Counter-Rotating Beam)

For two-beam machines (e.g., LHC beam 2):
```python
tw_b2 = line_b2.twiss(reverse=True)
```

## Twiss Defaults

Set default twiss arguments for a line:
```python
line.twiss_defaults['method'] = '4d'
line.twiss_defaults['delta0'] = 1e-4
tw = line.twiss()  # uses the defaults
```

## Survey (Geometric Layout)

Compute the geometrical layout of the beam line in global Cartesian coordinates:

```python
sv = line.survey()
# or with custom initial conditions:
sv = line.survey(X0=0, Y0=0, Z0=0, theta0=0, phi0=0, psi0=0)

sv.X    # global X coordinate [m]
sv.Y    # global Y coordinate [m]
sv.Z    # global Z coordinate [m]
sv.theta  # horizontal bending angle
sv.phi    # vertical bending angle
sv.psi    # roll angle
sv.s      # s position along beam line
```

## Resonance Driving Terms (RDTs)

Compute first-order RDTs from a twiss table and strengths:

```python
from xtrack import rdt_first_order_perturbation

tw = line.twiss()
strengths = line.get_strengths()

# Compute specific RDT (e.g., f3000 for third-order horizontal)
rdt = rdt_first_order_perturbation('f3000', twiss=tw, strengths=strengths)
# Returns complex array along the line

# Available RDTs: f1001, f1010, f3000, f2100, f1020, f1002, etc.
# feed_down: include feed-down from orbit (default True)
rdt = rdt_first_order_perturbation('f1001', twiss=tw, strengths=strengths,
                                     feed_down=True)
```

## Coupling

```python
# Closest tune approach (linear coupling)
tw = line.twiss()
tw.c_minus   # closest tune approach parameter

# R-matrix between two elements
R = tw.get_R_matrix(start='element_a', end='element_b')
# Returns 6x6 transfer matrix
```

## TwissTable Methods

```python
tw = line.twiss()

# Get twiss initial conditions at an element (for use in partial twiss)
tw_init = tw.get_twiss_init(at_element='ip1')

# Get betatron beam sizes
sigmas = tw.get_betatron_sigmas(nemitt_x=2.5e-6, nemitt_y=2.5e-6)
sigmas.sigma_x   # horizontal beam size
sigmas.sigma_y   # vertical beam size

# Get beam covariance matrix (full details)
cov = tw.get_beam_covariance(nemitt_x=2.5e-6, nemitt_y=2.5e-6,
                              nemitt_zeta=1e-3)
cov.sigma_x      # sigma_x at each element
cov.sigma_y      # sigma_y at each element
cov.sigma_zeta   # sigma_zeta
cov.sigma_px     # sigma_px

# Get R-matrix (transfer matrix) between elements
R = tw.get_R_matrix(start='elem_a', end='elem_b')

# Get normalized coordinates for particles
norm = tw.get_normalized_coordinates(particles,
                                      nemitt_x=2.5e-6, nemitt_y=2.5e-6)
norm.x_norm   # normalized horizontal coordinate
norm.px_norm  # normalized horizontal angle
norm.y_norm   # normalized vertical coordinate
norm.py_norm  # normalized vertical angle

# Compute IBS growth rates directly from twiss
rates = tw.get_ibs_growth_rates(
    formalism='nagaitsev',
    total_beam_intensity=1e11,
    nemitt_x=2.5e-6, nemitt_y=2.5e-6,
    sigma_delta=1e-4, bunch_length=0.08)

# Plot twiss parameters
tw.plot()

# Export twiss table
tw.to_pandas()        # pandas DataFrame
tw.to_json('tw.json') # JSON
tw.to_hdf5('tw.h5')   # HDF5
tw.to_csv('tw.csv')   # CSV
tw.to_tfs('tw.tfs')   # MAD-X TFS format
```

## Key Twiss Table Attributes

### Global quantities:
- `qx`, `qy` - tunes
- `dqx`, `dqy` - chromaticities
- `slip_factor`, `momentum_compaction_factor`
- `circumference` - ring circumference
- `T_rev0` - revolution period
- `betz0` - longitudinal beta at fixed point
- `qs` - synchrotron tune
- `c_minus` - closest tune approach (coupling)

### Per-element quantities:
- `s` - longitudinal position [m]
- `betx`, `bety` - beta functions [m]
- `alfx`, `alfy` - alpha functions
- `gamx`, `gamy` - gamma functions [1/m]
- `dx`, `dy`, `dpx`, `dpy` - dispersion and derivatives
- `x`, `y`, `px`, `py` - closed orbit
- `mux`, `muy` - phase advances [2pi]
- `muzeta` - longitudinal phase advance
- `W_matrix` - 6x6 W matrix at each element
- `name` - element name
