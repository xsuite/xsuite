# Xsuite: Synchrotron Radiation and Spin Polarization

## Synchrotron Radiation

### Enabling Radiation
```python
import xtrack as xt

line = xt.load('lattice.json')
line.set_particle_ref('electron', energy0=45.6e9)

# Configure radiation
line.configure_radiation(model='mean')      # mean energy loss only
# or
line.configure_radiation(model='quantum')   # quantum excitation included

# Track with radiation
particles = line.build_particles(x=1e-3)
line.track(particles, num_turns=1000)
```

### Radiation Models
- `model='mean'` - deterministic energy loss, no quantum fluctuations
- `model='quantum'` - includes quantum excitation (stochastic photon emission)

### Twiss with Radiation
```python
# Twiss with radiation gives equilibrium emittances
tw = line.twiss(eneloss_and_damping=True)

tw.eq_nemitt_x    # equilibrium normalized emittance x
tw.eq_nemitt_y    # equilibrium normalized emittance y
tw.eq_nemitt_zeta # equilibrium normalized emittance zeta
tw.damping_constants_s  # damping times [s] for x, y, zeta
tw.partition_numbers    # damping partition numbers
tw.eq_beam_covariance_matrix  # equilibrium beam matrix
```

### Tapering (Compensate Radiation Energy Loss)

Adjust RF phase and magnet strengths to compensate for energy loss:
```python
line.compensate_radiation_energy_loss()
# This:
# 1. Adjusts RF cavity phases to compensate mean energy loss
# 2. Adapts magnet strengths to local particle momentum on closed orbit
```

After tapering, the closed orbit can be found even with strong radiation.

### Synchrotron Radiation Integrals
From twiss output:
```python
tw = line.twiss(eneloss_and_damping=True)
# Radiation integrals I1-I5 available in twiss output
```

## Spin and Polarization

### Spin Tracking
Xsuite supports spin tracking for leptons (electrons, positrons).

```python
line = xt.load('lattice.json')
line.set_particle_ref('electron', energy0=45.6e9)
line.configure_radiation(model='quantum')

# Enable spin tracking
# Particles carry spin vector (sx, sy, sz) in the spin reference frame
```

### Equilibrium Polarization (Sokolov-Ternov)

```python
tw = line.twiss(eneloss_and_damping=True)

# n0 axis (stable spin direction)
tw.spin_n0_x   # x-component of n0 at each element
tw.spin_n0_y   # y-component
tw.spin_n0_z   # z-component

# Equilibrium polarization (Derbenev-Kondratenko)
tw.eq_polarization   # equilibrium polarization level (0 to 1)
tw.spin_tune         # spin tune (a * gamma)
```

### Monte Carlo Polarization Build-up

Track particles with spin to simulate polarization build-up:
```python
particles = line.build_particles(num_particles=1000,
    nemitt_x=1e-9, nemitt_y=1e-9, sigma_z=0.001)

# Initialize spin (all along +y = vertical)
particles.spin_x[:] = 0
particles.spin_y[:] = 1
particles.spin_z[:] = 0

# Track with radiation and spin
line.track(particles, num_turns=100000)

# Compute average polarization
polarization = np.mean(particles.spin_y[particles.state > 0])
```

## Intrabeam Scattering with Radiation (Equilibrium)

For lepton machines, IBS competes with radiation damping to set equilibrium emittances:
```python
import xfields as xf

ibs = xf.IBSAnalyticalKick(formalism='nagaitsev', line=line, num_slices=50)

# Compute steady-state emittances balancing IBS and radiation
eq = ibs.get_steady_state_emittances(
    nemitt_x=tw.eq_nemitt_x,
    nemitt_y=tw.eq_nemitt_y,
    sigma_z=tw.eq_sigma_z,
    num_particles=1e10,
    damping_constants_s=tw.damping_constants_s,
    partition_numbers=tw.partition_numbers)
```
