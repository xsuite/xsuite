# Xsuite: Environment and Lattice Model

## Environment

The `xt.Environment` is the central container for lattice design. It holds variables, elements, and lines.

```python
import xtrack as xt
import numpy as np

env = xt.Environment()

# Define variables (can use deferred expressions)
env['k1'] = 0.1
env['l_quad'] = 1.0
env['angle'] = 'pi / n_bends'  # deferred expression

# Create elements (parent/child pattern for element families)
env.new('mq', xt.Quadrupole, length='l_quad')           # parent element
env.new('mqf', 'mq', k1='k1')                           # child inherits from 'mq'
env.new('mqd', 'mq', k1='-k1')                          # child with negated k1

# Create a line from components
line = env.new_line(name='ring', components=['mqf', 'drift1', 'mqd', 'drift2'])
```

## Variable System (Deferred Expressions)

Variables support deferred expressions using strings that reference other variables. When a source variable changes, all dependent variables update automatically.

```python
env['kq'] = 0.12
env['kq_f'] = 'kq'       # tracks kq
env['kq_d'] = '-kq'      # tracks -kq
env['kq'] = 0.15          # kq_f and kq_d update automatically
```

Inspect expressions:

```python
env.ref['kq_f']._info()   # shows dependency chain
env.ref['kq_f']._expr     # shows the expression
```

Key points about the variable system:

- String values are interpreted as deferred expressions referencing other variables.
- Numeric values are stored directly without creating an expression.
- Expressions can use arithmetic operators (`+`, `-`, `*`, `/`, `**`) and standard math functions (`sin`, `cos`, `sqrt`, `pi`, etc.).
- Circular dependencies are not allowed and will raise an error.
- Variables can be used to parameterise element attributes (e.g., `k1='kq'`), keeping the lattice description symbolic throughout.

## Creating Lines

### Direct element list

Build a line by listing element names in the order they appear along the beamline:

```python
line = env.new_line(name='fodo', components=['qf', 'drift', 'qd', 'drift2'])
```

### Compose mode (placing elements at specific s positions)

Compose mode lets you place elements at absolute or relative longitudinal positions within a line of a given length. Drifts are inserted automatically to fill the gaps.

```python
myline = env.new_line(name='myline', length=12.0, compose=True)
myline.place('q1', anchor='center', at=3.0)
myline.place('q2', anchor='start', at=5.0)
myline.place('q3', anchor='start', at='q2@end')     # relative positioning
myline.place('q4', anchor='center', at='ds.q4', from_='q3@start')
myline.place('s4')   # right after previous
myline.end_compose()
```

Placement parameters:

| Parameter  | Description                                                                 |
|------------|-----------------------------------------------------------------------------|
| `anchor`   | Which point of the element is placed at the target: `'start'`, `'center'`, or `'end'`. |
| `at`       | Absolute s-position (number) or a deferred expression / reference position string. |
| `from_`    | Reference point for relative placement (e.g., `'q3@start'`, `'q3@end'`).  |

### Inline element creation in compose mode

Elements can be created and placed in a single call inside compose mode:

```python
myline = env.new_line(name='myline', length=12.0, compose=True)
myline.new('q1', xt.Quadrupole, length=1.0, k1=0.1, at=3.0)
myline.new('q2', xt.Quadrupole, length=1.0, k1=-0.1, anchor='start', at=5.0)
myline.end_compose()
```

## Line Mirroring and Composition

Lines can be mirrored and concatenated using Python operators. This is especially useful for building symmetric lattice cells from a half-cell definition.

```python
mirror_half_cell = -half_cell           # mirror the line
full_cell = -half_cell + half_cell      # mirror then concatenate
arc = 2 * full_cell                     # two cells
```

- The unary `-` operator creates a mirrored copy (reverses element order and accounts for element polarity).
- The `+` operator concatenates two lines.
- Multiplication by an integer (`n * line`) repeats the line n times.

## Beam Elements

### Magnetic elements

| Element | Constructor | Key Parameters | Description |
|---------|-------------|----------------|-------------|
| `xt.Drift` | `length` | `length` in metres | Free-space drift. |
| `xt.Quadrupole` | `length`, `k1` | `k1` in 1/m^2 (positive = horizontal focusing) | Normal quadrupole. |
| `xt.Sextupole` | `length`, `k2` | `k2` in 1/m^3 | Normal sextupole. |
| `xt.Octupole` | `length`, `k3` | `k3` in 1/m^4 | Normal octupole. |
| `xt.Bend` | `length`, `angle`, `k0`, `h`, `k1` | `angle` in rad, `h` = 1/rho | Combined-function dipole bend. |
| `xt.Multipole` | `knl`, `ksl` | `knl` = normal strengths, `ksl` = skew strengths (integrated, list) | Thin multipole kick. |
| `xt.Solenoid` | `length`, `ks` | `ks` = solenoid strength | Solenoid magnet. |
| `xt.Cavity` | `voltage`, `frequency`, `lag` | `voltage` in V, `frequency` in Hz, `lag` in degrees | RF cavity. |
| `xt.CrabCavity` | various | | Crab cavity for crossing-angle compensation. |

### Geometric transformations

These elements change the reference frame without introducing any physical aperture or field:

- `xt.XYShift(dx=..., dy=...)` -- lateral displacement of the reference frame [m].
- `xt.SRotation(angle=...)` -- rotation around the beam axis (s-axis) [rad].
- `xt.XRotation(angle=...)` -- rotation around the x-axis [rad].
- `xt.YRotation(angle=...)` -- rotation around the y-axis [rad].

### Apertures

Aperture elements define the physical boundary. Particles outside the boundary are flagged as lost during tracking.

- `xt.LimitEllipse(a=..., b=...)` -- elliptical aperture (semi-axes a, b in metres).
- `xt.LimitRect(min_x=..., max_x=..., min_y=..., max_y=...)` -- rectangular aperture.
- `xt.LimitRectEllipse(...)` -- intersection of a rectangle and an ellipse.
- `xt.LimitRacetrack(...)` -- racetrack-shaped aperture.
- `xt.LimitPolygon(x_vertices=..., y_vertices=...)` -- arbitrary polygon aperture.

### Specialized elements

- `xt.Marker()` -- zero-length position marker (used for observation points, injection/extraction locations, etc.).
- `xt.Exciter(samples=..., sampling_frequency=..., frev=..., knl=..., ksl=...)` -- transverse exciter driven by a waveform.
- `xt.NonLinearLens(...)` -- integrable-optics non-linear lens element.
- `xt.Elens(...)` -- hollow or Gaussian electron lens.
- `xt.Wire(...)` -- wire compensator for long-range beam-beam effects.
- `xt.ReferenceEnergyIncrease(Delta_p0c=...)` -- changes the reference momentum of the beam (used for energy ramps or linac sections).

### Monitors

Monitor elements record particle data during tracking:

- `xt.BeamPositionMonitor(...)` -- records turn-by-turn centroid position.
- `xt.BeamProfileMonitor(...)` -- records transverse beam profile (histogram).
- `xt.BeamSizeMonitor(...)` -- records beam sizes (RMS and statistical moments).
- `xt.ParticlesMonitor(...)` -- records the full phase-space coordinates of every particle at every turn.
- `xt.LastTurnsMonitor(...)` -- circular buffer that keeps the last N turns for each particle (memory-efficient for long simulations).

## Element Transformations

### Multipolar field errors (knl / ksl)

Thick magnetic elements (quadrupoles, sextupoles, bends, etc.) carry integrated multipolar error arrays `knl` (normal) and `ksl` (skew). These are indexed by multipole order: 0 = dipole, 1 = quadrupole, 2 = sextupole, 3 = octupole, and so on.

```python
env.new('my_quad', xt.Quadrupole, length=1.0, k1=0.1)
env['my_quad'].knl[3] = 1e-4  # add octupole error (normal)
env['my_quad'].ksl[2] = 5e-5  # add sextupole error (skew)
```

### Element misalignment and tilts

Misalignments are applied as a compound transformation: shift and rotation before the element, then the inverse after the element.

```python
# Applied as compound element (shift + rotation + element + inverse)
env['my_quad'].shift_x = 1e-3    # horizontal misalignment [m]
env['my_quad'].shift_y = -0.5e-3 # vertical misalignment [m]
env['my_quad'].rot_s_rad = 0.001 # tilt around s-axis [rad]
```

These transformations are transparent to tracking: the user sets misalignment attributes, and xtrack internally builds the appropriate sandwich of geometric transforms around the element.

## Clones and Replicas

Xsuite distinguishes two mechanisms for sharing element definitions:

- **Clone**: shares the parent's data. Changes to the parent propagate automatically to all clones. Clones are lightweight references suitable for identical copies of the same physical magnet.
- **Replica**: an independent copy that shares the parent's element type but can hold different parameter values. Replicas are suitable when magnets of the same family need individual tuning.

## Insert, Remove, Replace Elements

After a line has been constructed, its element sequence can be modified:

```python
# Insert element(s) at specified s-position(s)
line.insert([
    env.new('corr1', xt.Multipole, knl=[1e-4]),
], at_s=[5.0])

# Remove an element by name
line.remove('old_element')

# Replace an element with a new one
line.replace('old_name', env.new('new_name', xt.Quadrupole, length=1.0, k1=0.2))
```

## Slicing

Thick elements can be sliced into thinner sub-elements for higher-accuracy symplectic tracking. Xsuite supports Teapot-style and uniform slicing schemes, applied through a strategy pattern:

```python
line.slice_thick_elements(
    slicing_strategies=[
        xt.Strategy(slicing=xt.Teapot(3)),                           # default: 3 slices
        xt.Strategy(slicing=xt.Teapot(5), element_type=xt.Bend),    # 5 slices for bends
        xt.Strategy(slicing=xt.Uniform(10), name='special_quad'),   # 10 uniform slices
    ])
```

Slicing strategies are evaluated in order. More specific strategies (by element name) override more general ones (by element type or default). The `xt.Teapot` scheme distributes slices following the Yoshida integration pattern, while `xt.Uniform` places slices at equal intervals.

## Reference Particles

The reference particle defines the species, charge, and design momentum (or energy) of the beam. It is required for optics calculations and tracking.

```python
# Set built-in species
line.set_particle_ref('proton', energy0=7e12)         # total energy in eV
line.set_particle_ref('proton', p0c=7e12)             # momentum in eV/c
line.set_particle_ref('proton', kinetic_energy0=6e12) # kinetic energy in eV
line.set_particle_ref('proton', gamma0=7460.5)        # relativistic gamma

# Alternatively, set mass0 and charge0 directly (for exotic ions, etc.)
line.set_particle_ref(mass0=xt.PROTON_MASS_EV, charge0=1, p0c=7e12)

# Reusable reference particles in environment with deferred expressions
env.new_particle('myref', mass0=xt.PROTON_MASS_EV, q0=1, energy0='E_gev * 1e9')
line.particle_ref = 'myref'
```

Exactly one of `energy0`, `p0c`, `kinetic_energy0`, or `gamma0` must be provided. The remaining quantities are derived from the mass and the given parameter.

## Saving and Loading

Xsuite uses JSON as its native serialisation format. Both full environments and individual lines can be saved and restored.

```python
# Save/load environment (includes all variables, elements, and lines)
env.to_json('env.json')
env2 = xt.load('env.json')

# Save/load individual line
line.to_json('line.json')
line_loaded = xt.load('line.json')
```

## Loading MAD-X Lattices

### Native parser (recommended)

Xsuite includes a built-in MAD-X parser that reads `.seq` and `.str` files directly, preserving deferred expressions:

```python
env = xt.load(['ps.seq', 'ps_strengths.str'])
line = env.lines['ring']

# From a MAD-X source string
env = xt.load(string=madx_source_code, format='madx')
```

### Via cpymad (legacy)

For compatibility with existing workflows, lattices can also be imported through the cpymad interface:

```python
from cpymad.madx import Madx
mad = Madx()
mad.call('lattice.seq')
mad.use(sequence='ring')
line = xt.Line.from_madx_sequence(mad.sequence.ring, deferred_expressions=True)
```

The native parser is preferred because it runs without a MAD-X installation and preserves the full deferred-expression graph inside the xsuite environment.

## Line Inspection

The line table provides a tabular view of all elements, their types, positions, and key parameters:

```python
tt = line.get_table()
tt.show()
tt.show(cols=['s_start', 's_center', 's_end'])
tt.rows['element_name']    # specific element
tt.rows[10:20]             # row range
```

The table object supports column selection, row slicing, filtering, and export, making it convenient for both interactive exploration and programmatic analysis.

## Line Utility Methods

```python
# Get total length
line.get_length()

# Cycle line to start from a different element
line.cycle(name_first_element='ip1')

# Get s-positions of specific elements
line.get_s_position(at_elements=['ip1', 'ip5'], mode='upstream')

# Get elements of a specific type
quads, quad_names = line.get_elements_of_type(xt.Quadrupole)

# Get element strengths as table
strengths = line.get_strengths()

# Get aperture table
aper = line.get_aperture_table()

# Cut line at specific s-positions
line.cut_at_s(s_values=[100.0, 200.0, 300.0])

# Build/discard tracker (freeze/unfreeze the line)
line.build_tracker(_context=context)  # compile and freeze
line.discard_tracker()                 # unfreeze for editing

# Variable access
line.vars['knob_name'] = 0.5
line.vv['knob_name']   # shorthand for value access

# Element references (for deferred expressions)
line.element_refs['quad1'].k1 = line.vars['kq']
```

## Exporting Lines

```python
# To JSON
line.to_json('line.json')

# To MAD-X sequence
line.to_madx_sequence(sequence_name='myring')

# To MAD-NG
line.to_madng(sequence_name='seq')
```
