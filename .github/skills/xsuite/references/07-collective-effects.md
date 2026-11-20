# Xsuite: Collective Effects

## Overview
Collective effects in Xsuite are handled by the xfields package (space charge, beam-beam, electron cloud) and xwakes (wakefields and impedances).

## Space Charge

### Space Charge Setup
```python
import xfields as xf
import xtrack as xt

# Install frozen/quasi-frozen space charge
xf.install_spacecharge_frozen(
    line=line,
    particle_ref=line.particle_ref,
    longitudinal_profile=xf.LongitudinalProfileQGaussian(
        number_of_particles=1e11,
        sigma_z=0.22,
        z_kick_num_integ_per_sigma=5),
    nemitt_x=2e-6, nemitt_y=2e-6,
    sigma_z=0.22,
    num_spacecharge_interactions=120)
```

### PIC (Particle-In-Cell) Space Charge
```python
xf.replace_spacecharge_with_PIC(
    line=line,
    n_sigmas_range_pic_x=8,
    n_sigmas_range_pic_y=8,
    nx_grid=128, ny_grid=128, nz_grid=64,
    n_lims_x=7, n_lims_y=7,
    z_range=(-0.5, 0.5))
```

### Quasi-Frozen Space Charge
```python
xf.replace_spacecharge_with_quasi_frozen(
    line=line,
    _buffer=line._buffer,
    update_mean_x_on_track=True,
    update_mean_y_on_track=True)
```

## Beam-Beam Interactions

### Weak-Strong Beam-Beam
```python
# 2D beam-beam (round beam approximation)
bb_lens = xf.BeamBeamBiGaussian2D(
    n_particles=1.15e11,
    sigma_x=15e-6,
    sigma_y=15e-6,
    other_beam_q0=1)

# Insert into line
line.insert_element(element=bb_lens, name='bb_ip1', at_s=s_ip1)
```

### 6D Strong-Strong Beam-Beam with Pipeline
For strong-strong beam-beam simulations, use the MPI pipeline:
```python
# Requires MPI: mpirun -n 2 python script.py
from xfields import BeamBeamBiGaussian3D
# Configure using pipeline manager and branches
```

### Beam-Beam in Collider (via xmask)
```python
# Install beam-beam elements
# (see xmask documentation for full workflow)
# Typically:
# 1. Build collider from MAD-X model
# 2. Install beam-beam elements with xmask
# 3. Configure beam-beam interactions
```

## Wakefields and Impedances (xwakes)

### Resonator Wake
```python
import xwakes as xw

# Create individual wake components
wf_dip = xw.WakeResonator(kind='dipolar_x', r=1e8, q=1e5, f_r=1e3)
wf_quad = xw.WakeResonator(kind='quadrupolar_x', r=2e7, q=8e4, f_r=2e3)

# Sum wakes
wf = wf_dip + wf_quad

# Configure for tracking
wf.configure_for_tracking(zeta_range=(-0.1, 0.1), num_slices=100)

# Add to line
one_turn = xt.LineSegmentMap(length=26000, betx=50., bety=40., qx=62.28, qy=62.31,
                              longitudinal_mode='linear_fixed_qs', qs=1e-3, bets=100)
line = xt.Line(elements=[one_turn, wf], element_names=['one_turn', 'wake'])
line.set_particle_ref('proton', p0c=7e12)
line.track(particles, num_turns=100)
```

### Wake kinds
Available `kind` values for WakeResonator and WakeFromTable:
- `'dipolar_x'`, `'dipolar_y'` - dipolar (kick proportional to source offset)
- `'quadrupolar_x'`, `'quadrupolar_y'` - quadrupolar (kick proportional to test offset)
- `'constant_x'`, `'constant_y'` - constant (offset-independent)
- `'longitudinal'` - longitudinal energy kick
- `'dipolar_xy'`, `'dipolar_yx'` - coupled dipolar
- `'quadrupolar_xy'`, `'quadrupolar_yx'` - coupled quadrupolar

### Wake from Table
```python
table = xw.read_headtail_file('wake_file.dat',
    columns=['time', 'longitudinal', 'dipolar_x', 'dipolar_y',
             'quadrupolar_x', 'quadrupolar_y'])
wf = xw.WakeFromTable(table, columns=['dipolar_x', 'dipolar_y'])
wf.configure_for_tracking(zeta_range=(-0.4, 0.4), num_slices=100)
```

### Custom Wake
```python
def wake_vs_t(t):
    t = np.atleast_1d(t)
    out = 2.0 * np.sin(1e9 * t) * np.exp(-0.1e9 * t)
    out[t <= 0] = 0.0  # causal
    return out

component = xw.Component(
    wake=wake_vs_t,
    plane='y',
    source_exponents=(2, 0),
    test_exponents=(1, 1),
    name="custom_wake")
wf = xw.Wake(components=[component])
wf.configure_for_tracking(zeta_range=(-0.1, 0.1), num_slices=200)
```

### Multi-Bunch, Multi-Turn Wakes
```python
filling_scheme = np.zeros(3564, dtype=int)
filling_scheme[0] = filling_scheme[1] = 1

wf.configure_for_tracking(
    zeta_range=(-0.2, 0.2),
    num_slices=200,
    filling_scheme=filling_scheme,
    bunch_spacing_zeta=26658.8832 / 3564,
    num_turns=1,
    circumference=26658.8832)
```

## Intrabeam Scattering (IBS)

### IBS Growth Rates
```python
import xfields as xf

# Analytical growth rates
tw = line.twiss()
ibs = xf.IBSAnalyticalKick(
    formalism='nagaitsev',  # or 'bjorken-mtingwa'
    line=line,
    num_slices=50)

# Get growth rates
rates = ibs.get_growth_rates(
    nemitt_x=2.5e-6, nemitt_y=2.5e-6,
    sigma_z=0.08, num_particles=1e11)
# rates contains Tx, Ty, Tz growth rates
```

### IBS Tracking with Kicks
```python
ibs_kick = xf.IBSAnalyticalKick(
    formalism='nagaitsev',
    line=line,
    num_slices=50)
# Install in line and track
line.insert_element(element=ibs_kick, name='ibs', at_s=0)
line.track(particles, num_turns=1000)
```

### IBS Kinetic Model
```python
ibs_kick = xf.IBSKineticKick(line=line, num_slices=50)
```

### Steady-State Emittances with IBS
Compute equilibrium emittances balancing IBS growth with radiation damping:
```python
# For electron/positron machines with synchrotron radiation
ibs.get_steady_state_emittances(
    nemitt_x=..., nemitt_y=..., sigma_z=...,
    num_particles=..., coupling=0.0)
```

## Exciter Element
```python
# For tune measurement, RFKO extraction, etc.
samples = np.sin(2 * np.pi * f_excite * np.arange(0, total_time, 1/sampling_freq))

exciter = xt.Exciter(
    samples=samples,
    sampling_frequency=sampling_freq,
    frev=f_rev,
    start_turn=0,
    knl=[0, 1e-6],  # thin dipole + quad
    ksl=[0, 0])

line.insert_element(element=exciter, name='exciter', index=42)
```

## Electron Cloud

Set up electron cloud elements from pre-computed field maps:

```python
import xfields as xf

# Full electron cloud setup from HDF5 field maps
xf.full_electroncloud_setup(
    line=line,
    ecloud_info=ecloud_info_dict,
    filenames=fieldmap_filenames,
    context=context)

# Or step-by-step:
# 1. Load field map
fieldmap = xf.get_electroncloud_fieldmap_from_h5(filename='ecloud_map.h5')

# 2. Configuration
xf.config_electronclouds(line, twiss=tw, ecloud_info=ecloud_info,
                          shift_to_closed_orbit=True)

# 3. Insert
xf.insert_electronclouds(eclouds=ecloud_elements, fieldmap=fieldmap, line=line)
```

## AC Dipole

For optics measurements and forced oscillations:
```python
acd = xt.ACDipole(...)
line.insert_element(element=acd, name='acdipole', at_s=s_pos)
```
