# Xsuite: Collimation (Xcoll)

## Overview
Xcoll provides collimation simulation capabilities including:
- Black absorber collimators (perfect absorbers)
- Everest scattering engine (built-in)
- FLUKA interface for detailed material interaction
- Geant4 interface for detailed material interaction
- Crystal collimators (channeling)
- Loss map generation

## Collimator Types

### Black Absorber (perfect absorption)
```python
import xcoll as xc
import xtrack as xt

# Simple black absorber
collimator = xc.BlackAbsorber(
    length=1.0,
    jaw_L=-0.003,     # left jaw position [m]
    jaw_R=0.003,      # right jaw position [m]
    side='both',      # 'both', 'left', 'right'
    angle=0)          # collimator angle [rad]
```

### Everest Collimator (scattering)
```python
collimator = xc.EverestCollimator(
    length=1.0,
    jaw_L=-0.003,
    jaw_R=0.003,
    side='both',
    angle=0,
    material=xc.materials.Carbon)
```

### Crystal Collimator
```python
crystal = xc.EverestCrystal(
    length=0.002,
    jaw_L=-0.003,
    jaw_R=0.003,
    material=xc.materials.Silicon,
    bending_angle=50e-6,   # crystal bending angle [rad]
    width=0.002,
    height=0.05,
    side='left')
```

### FLUKA and Geant4 Collimators
```python
# FLUKA (requires FLUKA installation)
collimator = xc.FlukaCollimator(length=1.0, jaw_L=-0.003, jaw_R=0.003)

# Geant4 (requires Geant4 installation)
collimator = xc.Geant4Collimator(length=1.0, jaw_L=-0.003, jaw_R=0.003)
```

## Collimator Database

Load collimator settings from a database:
```python
colldb = xc.CollimatorDatabase.from_yaml('colldb.yaml')
# or
colldb = xc.CollimatorDatabase.from_json('colldb.json')

# Install collimators into line
colldb.install_everest_collimators(line=line)
# or
colldb.install_black_absorbers(line=line)
```

## Loss Maps

Generate loss maps from tracking:
```python
# After tracking particles through a line with collimators
lossmap = xc.LossMap(line=line, part=particles)

# Access loss map data
lossmap.summary   # summary table
lossmap.lossmap   # detailed loss map

# Plot
lossmap.plot()

# Save
lossmap.to_json('lossmap.json')
```

### Multi-run Loss Maps
```python
lossmaps = []
for seed in range(10):
    particles = generate_particles(seed)
    line.track(particles, num_turns=200)
    lossmaps.append(xc.LossMap(line=line, part=particles))

combined = xc.MultiLossMap(lossmaps)
combined.plot()
```

## Materials

Built-in materials available:
```python
xc.materials.Carbon
xc.materials.Copper
xc.materials.Tungsten
xc.materials.Silicon
xc.materials.Beryllium
xc.materials.Molybdenum
xc.materials.MolGraphite    # Molybdenum-graphite composite
xc.materials.CopperDiamond
# ... and more
```

Custom materials:
```python
my_material = xc.Material(
    Z=29,           # atomic number
    A=63.546,       # atomic mass
    density=8.96,   # g/cm^3
    radiation_length=1.436,  # cm
    nuclear_length=15.32)    # cm
```

## Interaction Record

Record particle-matter interactions:
```python
# Enable interaction recording
record = xc.InteractionRecord()
line.track(particles, num_turns=200, io_buffer=record)

# Access interaction data
record.interactions  # interaction types
record.at_element    # where interactions occurred
record.at_turn       # when they occurred
```

## Particle States

After collimation tracking, particles have specific states:
- `state > 0`: alive
- `state == 0`: lost on aperture
- `state == -333`: absorbed in collimator
- Various negative codes for different loss mechanisms

```python
alive = particles.filter(particles.state > 0)
absorbed = particles.filter(particles.state == -333)
```

## Loss Location Refinement

Refine loss locations with sub-element precision:
```python
# Built into xtrack
aper_interp = xt.LossLocationRefinement(line, n_theta=360, r_max=0.01)
aper_interp.refine_loss_location(particles)

# After refinement, particles.s_last_turn gives precise loss location
```

## Full Collimation Workflow Example

```python
import xcoll as xc
import xtrack as xt
import xpart as xp
import numpy as np

# 1. Load lattice
line = xt.load('lattice.json')
line.set_particle_ref('proton', p0c=7e12)

# 2. Install collimators
colldb = xc.CollimatorDatabase.from_yaml('colldb.yaml')
colldb.install_everest_collimators(line=line)

# 3. Generate halo particles
particles = xp.generate_matched_gaussian_bunch(
    line=line, num_particles=100000,
    nemitt_x=3.5e-6, nemitt_y=3.5e-6, sigma_z=0.08)

# 4. Track
line.track(particles, num_turns=200)

# 5. Generate loss map
lossmap = xc.LossMap(line=line, part=particles)
lossmap.plot()
```

## Emittance Monitor
```python
em = xc.EmittanceMonitor(num_particles=n_part, start_at_turn=0, stop_at_turn=1000)
# Records emittance evolution during tracking
```

## BlowUp Element
```python
blowup = xc.BlowUp(plane='y', amplitude=1e-6)
# Artificially grows beam emittance
```
