# Xsuite: Particles

## Introduction
Particle ensembles are generated using xpart and stored as `xpart.Particles` (aliased as `xt.Particles`) objects.

## Creating Particles Directly
```python
import xtrack as xt
import numpy as np

particles = xt.Particles(
    mass0=xt.PROTON_MASS_EV,    # reference mass [eV]
    q0=1,                        # reference charge [e]
    p0c=7e12,                    # reference momentum [eV/c]
    x=[1e-3, 2e-3, 3e-3],
    px=[0, 0, 0],
    y=[0, 0, 0],
    py=[0, 0, 0],
    zeta=[0, 0, 0],
    delta=[0, 0, 0])
```

## The `build_particles` Function

Three modes available:

### "set" mode (default)
Reference quantities from reference particle; coordinates set from input:
```python
particles = line.build_particles(
    x=[1e-3, 2e-3],
    px=[0, 0],
    y=[0, 0],
    py=[0, 0],
    zeta=[0, 0],
    delta=[0, 0])
```

### "shift" mode
Coordinates are shifted relative to the reference particle:
```python
particles = line.build_particles(
    mode='shift',
    x=[1e-3, 0],     # offset from closed orbit
    px=[0, 0],
    delta=[1e-3, 0])
```

### "normalized_transverse" mode
Transverse coordinates given in normalized phase space:
```python
particles = line.build_particles(
    x_norm=[1, 0, -1],
    px_norm=[0, 1, 0],
    y_norm=[0.5, 0, 0],
    py_norm=[0, 0.5, 0],
    zeta=[0, 0, 0],
    delta=[0, 0, 0],
    nemitt_x=2.5e-6,
    nemitt_y=2.5e-6)
```

## Particle Distributions

### Gaussian bunch (matched to RF bucket)
```python
import xpart as xp

particles = xp.generate_matched_gaussian_bunch(
    line=line,
    num_particles=10000,
    nemitt_x=2.5e-6,
    nemitt_y=2.5e-6,
    sigma_z=0.08)    # bunch length in meters
```

### Matched Gaussian at a custom location
```python
particles = line.generate_matched_gaussian_bunch(
    num_particles=10000,
    nemitt_x=2.5e-6,
    nemitt_y=2.5e-6,
    sigma_z=0.08,
    at_element='ip1')
```

### Multi-bunch beam
```python
filling_scheme = np.zeros(3564, dtype=int)
filling_scheme[0] = 1
filling_scheme[10] = 1  # two bunches

particles = xp.generate_matched_gaussian_multibunch_beam(
    line=line,
    filling_scheme=filling_scheme,
    bunch_num_particles=100_000,
    bunch_intensity_particles=2.3e11,
    nemitt_x=2e-6,
    nemitt_y=2e-6,
    sigma_z=0.08,
    bucket_length=26658.8832 / 35640,
    bunch_spacing_buckets=10)
```

### Pencil beam
```python
x_norm, px_norm = xp.generate_2D_gaussian(num_particles=10000)
y_norm, py_norm = xp.generate_2D_pencil(
    num_particles=10000,
    pos_cut_sigmas=6, dr_sigmas=0.1,
    side='+')
zeta, delta = xp.generate_longitudinal_coordinates(
    line=line,
    num_particles=10000,
    distribution='gaussian',
    sigma_z=0.08)

particles = xp.build_particles(
    line=line,
    x_norm=x_norm, px_norm=px_norm,
    y_norm=y_norm, py_norm=py_norm,
    zeta=zeta, delta=delta,
    nemitt_x=2.5e-6, nemitt_y=2.5e-6)
```

### Halo beam
```python
x_norm, px_norm = xp.generate_2D_uniform_circular_sector(
    num_particles=10000,
    r_range=(4, 8),        # 4 to 8 sigma
    theta_range=(0, np.pi/4))  # azimuthal cut

particles = xp.build_particles(
    line=line,
    x_norm=x_norm, px_norm=px_norm,
    y_norm=0, py_norm=0,
    zeta=0, delta=0,
    nemitt_x=2.5e-6, nemitt_y=2.5e-6)
```

## Particles Coordinates

Key attributes of the `Particles` object:
- `x`, `px` - horizontal position [m] and angle [rad]
- `y`, `py` - vertical position [m] and angle [rad]
- `zeta` - longitudinal coordinate (s - beta0*c*t) [m]
- `delta` - relative momentum deviation (p - p0) / p0
- `pzeta` - conjugate of zeta
- `ptau` - energy deviation
- `mass0` - reference mass [eV/c^2]
- `q0` - reference charge [e]
- `p0c` - reference momentum [eV/c]
- `energy0` - reference energy [eV]
- `gamma0` - reference Lorentz gamma
- `beta0` - reference velocity ratio v/c
- `state` - particle state (> 0 = alive, 0 = lost, < 0 = lost with code)
- `at_turn` - current turn (or turn of loss)
- `at_element` - current element index (or element of loss)
- `weight` - statistical weight
- `particle_id` - unique identifier

## Copying Particles (Including Across Contexts)
```python
particles_copy = particles.copy()
particles_cpu = particles.copy(_context=xo.ContextCpu())  # GPU to CPU
particles_gpu = particles.copy(_context=xo.ContextCupy())  # CPU to GPU
```

## Saving and Loading
```python
# To/from dictionary
d = particles.to_dict()
particles = xt.Particles.from_dict(d)

# To/from JSON
particles.to_json('particles.json')
particles = xt.Particles.from_json('particles.json')

# To/from pandas
df = particles.to_pandas()
particles = xt.Particles.from_pandas(df)
```

## Merging and Filtering
```python
# Merge
merged = xt.Particles.merge([particles1, particles2])

# Filter
alive = particles.filter(particles.state > 0)
selected = particles.filter(particles.x > 0)
```

## GPU Access
```python
# On GPU contexts, arrays are CuPy/PyOpenCL arrays
# To get numpy arrays:
x_cpu = context.nparray_from_context_array(particles.x)
```

## Mass Constants
```python
xt.PROTON_MASS_EV     # 938272088.16 eV
xt.ELECTRON_MASS_EV   # 510998.95 eV
xt.MUON_MASS_EV       # muon mass
xt.Pb208_MASS_EV      # lead-208 mass
```

## Additional Distribution Generators

### Polar grid
```python
x_norm, px_norm = xp.generate_2D_polar_grid(
    num_particles=1000,
    r_range=(0.1, 6),
    n_r=10, n_theta=20)
```

### Hypersphere distributions
```python
# 2D hypersphere (circle)
x_norm, px_norm = xp.generate_hypersphere_2D(num_particles=1000, r=3)

# 4D hypersphere
x_norm, px_norm, y_norm, py_norm = xp.generate_hypersphere_4D(
    num_particles=1000, rx=3, ry=3)

# 6D hypersphere
x_norm, px_norm, y_norm, py_norm, zeta_norm, pzeta_norm = \
    xp.generate_hypersphere_6D(num_particles=1000, rx=3, ry=3, rzeta=1)
```

### Longitudinal distribution types
```python
# Gaussian (default)
zeta, delta = xp.generate_longitudinal_coordinates(
    line=line, num_particles=10000,
    distribution='gaussian', sigma_z=0.08)

# Q-Gaussian
zeta, delta = xp.generate_qgaussian_longitudinal_coordinates(
    line=line, num_particles=10000, q=1.2, sigma_z=0.08)

# Binomial
zeta, delta = xp.generate_binomial_longitudinal_coordinates(
    line=line, num_particles=10000, m=2.5, sigma_z=0.08)

# Parabolic
zeta, delta = xp.generate_parabolic_longitudinal_coordinates(
    line=line, num_particles=10000, sigma_z=0.08)
```

### Pencil with absolute cut
```python
y_norm, py_norm = xp.generate_2D_pencil_with_absolute_cut(
    num_particles=10000, abs_cut=6.0, dr_sigmas=0.1, side='+')
```
