# Xsuite: API Reference

## xtrack (xt)

### Core Classes

#### Environment
```python
env = xt.Environment()
env['var_name'] = value              # set variable
env['var_name']                      # get variable value
env.ref['var_name']                  # get reference (for deferred expressions)
env.ref['var_name']._info()          # inspect dependencies
env.new('name', ElementType, **kwargs)  # create element
env.new('child', 'parent', **kwargs)    # create element inheriting from parent
env.new_line(name='...', components=[...])  # create line
env.new_line(name='...', length=L, compose=True)  # compose mode
env.new_particle(name='...', mass0=..., q0=..., p0c=...)  # reference particle
env.to_json('file.json')             # save
env.lines                            # dict of lines
env.particles                        # particle references
```

#### Line
```python
line = xt.Line(elements=[...], element_names=[...])
line = xt.load('file.json')          # load from JSON
line = xt.load(['file.seq', 'file.str'])  # load MAD-X files
line = xt.load(string='...', format='madx')  # from MAD-X string

# Reference particle
line.set_particle_ref('proton', p0c=7e12)
line.set_particle_ref('proton', energy0=7e12)
line.set_particle_ref('electron', energy0=45.6e9)
line.set_particle_ref(mass0=..., charge0=..., p0c=...)
line.particle_ref                    # access reference particle

# Optics
line.twiss()                         # full 6D twiss
line.twiss4d()                       # 4D twiss (no RF)
line.twiss(method='4d', delta0=1e-3) # off-momentum
line.twiss(start='a', end='b', init=tw_init)  # with initial conditions
line.twiss(start='a', end='b', init='periodic')  # periodic section
line.twiss(reverse=True)             # counter-rotating beam
line.twiss(eneloss_and_damping=True) # with radiation
line.twiss_defaults = {}             # default twiss kwargs

# Matching
line.match(vary=[...], targets=[...])
line.match(vary=[...], targets=[...], solve=False)  # interactive
line.match_knob(knob_name='...', knob_value_start=0, knob_value_end=1,
                vary=[...], targets=[...])

# Tracking
line.track(particles, num_turns=N)
line.track(particles, num_turns=N, turn_by_turn_monitor=True)
line.track(particles, ele_start='a', ele_stop='b')
line.track(particles, num_turns=N, backtrack=True)

# Lattice manipulation
line.get_table()                     # element table
line.insert([...], at_s=[...])       # insert elements
line.remove('element_name')          # remove element
line.replace('old', new_element)     # replace element
line.slice_thick_elements(slicing_strategies=[...])
line.cut_at_s(s_values)              # cut at s positions
line.optimize_for_tracking()         # optimize for speed

# Trajectory correction
line.correct_trajectory(twiss_table=tw)
line.correct_trajectory(twiss_table=tw, correction_method='micado', n_micado=5)

# Other
line.build_particles(**kwargs)       # create particles
line.generate_matched_gaussian_bunch(**kwargs)
line.get_footprint(**kwargs)         # tune footprint
line.configure_radiation(model='mean')  # radiation
line.compensate_radiation_energy_loss()  # tapering
line.freeze_longitudinal()           # freeze zeta/delta
line.unfreeze_longitudinal()
line.to_json('file.json')            # save
line.env                             # parent environment
line.vars                            # variable access
line.vv                              # shorthand for vars.val
line.element_names                   # list of element names
line.elements                        # list of element objects
line.element_refs                    # element references (for deferred expressions)
line.attr                            # element attributes as table
line.enable_time_dependent_vars      # enable/disable time-dependent variables

# Survey
line.survey()                        # geometric layout
line.survey(X0=0, Y0=0, Z0=0, theta0=0)

# Additional analysis
line.find_closed_orbit()             # closed orbit search
line.compute_T_matrix(start='a', end='b')  # transfer matrix
line.get_amplitude_detuning_coefficients(nemitt_x=..., nemitt_y=...)
line.get_non_linear_chromaticity()
line.get_elements_of_type(xt.Quadrupole)
line.get_s_position(at_elements=[...])
line.get_length()                    # total line length
line.get_strengths()                 # element strengths table
line.get_aperture_table()            # aperture table
line.cycle(name_first_element='ip1') # cycle start element

# Export
line.to_madx_sequence(sequence_name='ring')
line.to_madng(sequence_name='seq')
```

### Beam Elements
```python
xt.Drift(length=L)
xt.Quadrupole(length=L, k1=K1)
xt.Sextupole(length=L, k2=K2)
xt.Octupole(length=L, k3=K3)
xt.Bend(length=L, angle=A, k0=K0, h=H, k1=K1)
xt.Multipole(knl=[...], ksl=[...], length=L)
xt.Cavity(voltage=V, frequency=F, lag=LAG)  # lag in degrees
xt.CrabCavity(...)
xt.Solenoid(length=L, ks=KS)
xt.Marker()
xt.XYShift(dx=DX, dy=DY)
xt.SRotation(angle=A)  # radians
xt.ReferenceEnergyIncrease(Delta_p0c=DP)
xt.Exciter(samples=S, sampling_frequency=FS, frev=FR, knl=KNL, ksl=KSL)
xt.LimitEllipse(a=A, b=B)
xt.LimitRect(min_x=..., max_x=..., min_y=..., max_y=...)
xt.LimitRacetrack(...)
xt.LimitPolygon(x_vertices=..., y_vertices=...)
xt.LineSegmentMap(length=L, betx=BX, bety=BY, qx=QX, qy=QY, ...)
xt.NonLinearLens(...)
xt.Elens(...)
xt.Wire(...)
```

### Match/Optimize Objects
```python
xt.Vary('knob_name', step=1e-8, limits=[lo, hi], weight=1.0, tag='...')
xt.VaryList(['k1', 'k2'], step=1e-8, tag='...')
xt.Target('quantity', value=V, tol=T, at='element', tag='...')
xt.TargetSet(qx=62.31, qy=60.32, tol=1e-6, tag='...')
xt.TargetSet(betx=0.15, at='ip1')
xt.GreaterThan(value)
xt.LessThan(value)
xt.START    # constant for start of range
xt.END      # constant for end of range
xt.Action   # base class for custom actions

class MyAction(xt.Action):
    def run(self): return {'key': computed_value}

# Specialized targets
xt.TargetRelPhaseAdvance(mux=0.25, start='a', end='b')
xt.TargetRmatrixTerm(r_term='r11', value=0.5, start='a', end='b')
xt.TargetRmatrix(r_matrix=R, start='a', end='b')
xt.TargetLuminosity(...)
xt.TargetSeparation(...)
xt.TargetSeparationOrthogonalToCrossing(...)
```

### TwissInit
```python
xt.TwissInit(betx=..., bety=..., alfx=..., alfy=...,
             dx=..., dpx=..., dy=..., dpy=...,
             x=..., px=..., y=..., py=...,
             mux=..., muy=...)
```

### Monitors
```python
xt.ParticlesMonitor(num_particles=N, start_at_turn=0, stop_at_turn=T)
xt.BeamPositionMonitor(num_particles=N, start_at_turn=0, stop_at_turn=T)
xt.BeamSizeMonitor(num_particles=N, start_at_turn=0, stop_at_turn=T)
xt.BeamProfileMonitor(...)
xt.LastTurnsMonitor(num_particles=N, n_last_turns=20)
xt.MultiElementMonitor(element_names=[...], ...)
```

### Slicing
```python
xt.Strategy(slicing=scheme, element_type=Type, name='...')
xt.Teapot(n_slices)    # Teapot slicing scheme
xt.Uniform(n_slices)   # Uniform slicing scheme
xt.Custom(at_s=[...])  # Custom slicing positions
```

### Survey
```python
sv = line.survey(X0=0, Y0=0, Z0=0, theta0=0, phi0=0, psi0=0)
# Returns table with: X, Y, Z, theta, phi, psi, s
```

### Resonance Driving Terms
```python
from xtrack import rdt_first_order_perturbation
rdt = rdt_first_order_perturbation('f3000', twiss=tw, strengths=strengths,
                                     feed_down=True)
# Available: f1001, f1010, f3000, f2100, f1020, f1002, etc.
```

### Luminosity
```python
from xtrack.lumi import luminosity
lumi = luminosity(num_colliding_bunches=..., num_particles_per_bunch=...,
                   sigma_x=..., sigma_y=..., f_rev=...)
```

### TwissTable Methods
```python
tw.get_twiss_init(at_element='ip1')
tw.get_betatron_sigmas(nemitt_x=..., nemitt_y=...)
tw.get_beam_covariance(nemitt_x=..., nemitt_y=..., nemitt_zeta=...)
tw.get_R_matrix(start='a', end='b')
tw.get_normalized_coordinates(particles, nemitt_x=..., nemitt_y=...)
tw.get_ibs_growth_rates(formalism='nagaitsev', total_beam_intensity=...,
    nemitt_x=..., nemitt_y=..., sigma_delta=..., bunch_length=...)
tw.plot()
tw.to_pandas()
tw.to_json('file.json')
tw.to_hdf5('file.h5')
tw.to_csv('file.csv')
tw.to_tfs('file.tfs')
```

### Energy Program
```python
xt.EnergyProgram(t_s=[...], kinetic_energy0=[...])
```

### Additional Elements
```python
xt.ACDipole(...)                     # AC dipole
xt.RBend(...)                        # rectangular bend
xt.DipoleEdge(...)                   # dipole edge focusing
xt.LongitudinalLimitRect(...)        # longitudinal aperture
xt.LimitRectEllipse(...)             # combined rect+ellipse aperture
```

### Constants
```python
xt.PROTON_MASS_EV      # 938272088.16
xt.ELECTRON_MASS_EV    # 510998.95
xt.MUON_MASS_EV
xt.Pb208_MASS_EV
```

## xpart (xp)

```python
# Particle creation
xp.build_particles(line=line, x=..., px=..., mode='set')
xp.build_particles(line=line, x_norm=..., mode='normalized_transverse',
                    nemitt_x=..., nemitt_y=...)

# Distributions
xp.generate_matched_gaussian_bunch(line=line, num_particles=N,
    nemitt_x=..., nemitt_y=..., sigma_z=...)
xp.generate_matched_gaussian_multibunch_beam(line=line,
    filling_scheme=..., bunch_num_particles=N, ...)
xp.generate_2D_gaussian(num_particles=N)
xp.generate_2D_pencil(num_particles=N, pos_cut_sigmas=6, dr_sigmas=0.1)
xp.generate_2D_uniform_circular_sector(num_particles=N, r_range=(...), theta_range=(...))
xp.generate_longitudinal_coordinates(line=line, num_particles=N,
    distribution='gaussian', sigma_z=...)

# Additional distributions
xp.generate_2D_polar_grid(num_particles=N, r_range=(...), n_r=..., n_theta=...)
xp.generate_2D_pencil_with_absolute_cut(num_particles=N, abs_cut=..., dr_sigmas=...)
xp.generate_hypersphere_2D(num_particles=N, r=...)
xp.generate_hypersphere_4D(num_particles=N, rx=..., ry=...)
xp.generate_hypersphere_6D(num_particles=N, rx=..., ry=..., rzeta=...)
xp.generate_qgaussian_longitudinal_coordinates(line=line, num_particles=N, q=..., sigma_z=...)
xp.generate_binomial_longitudinal_coordinates(line=line, num_particles=N, m=..., sigma_z=...)
xp.generate_parabolic_longitudinal_coordinates(line=line, num_particles=N, sigma_z=...)

# Interface
xp.enable_pyheadtail_interface()
xp.disable_pyheadtail_interface()
```

## xfields (xf)

```python
# Space charge
xf.install_spacecharge_frozen(line=..., ...)
xf.replace_spacecharge_with_PIC(line=..., ...)
xf.replace_spacecharge_with_quasi_frozen(line=..., ...)

# Beam-beam
xf.BeamBeamBiGaussian2D(...)
xf.BeamBeamBiGaussian3D(...)
xf.install_beambeam_elements_in_lines(...)
xf.configure_beam_beam_elements(...)

# IBS
xf.IBSAnalyticalKick(formalism='nagaitsev', line=..., num_slices=50)
xf.IBSKineticKick(line=..., num_slices=50)

# Electron cloud
xf.full_electroncloud_setup(line=..., ecloud_info=..., filenames=..., context=...)
xf.config_electronclouds(line, twiss=tw, ecloud_info=..., shift_to_closed_orbit=True)
xf.insert_electronclouds(eclouds=..., fieldmap=..., line=...)
xf.get_electroncloud_fieldmap_from_h5(filename='...')

# Field maps
xf.TriLinearInterpolatedFieldMap(...)
xf.TriCubicInterpolatedFieldMap(...)
xf.BiGaussianFieldMap(...)

# Profiles
xf.LongitudinalProfileQGaussian(number_of_particles=N, sigma_z=..., z_kick_num_integ_per_sigma=5)
xf.LongitudinalProfileCoasting(...)
```

## xobjects (xo)

```python
# Contexts
xo.ContextCpu(omp_num_threads=N)
xo.ContextCupy()
xo.ContextPyopencl()

# Types
xo.Float64, xo.Float32
xo.Int64, xo.Int32, xo.Int16, xo.Int8
xo.UInt64, xo.UInt32

# Data structures
xo.Struct    # base for C-compatible structs
xo.Float64[:]   # dynamic array type
xo.HybridClass  # Python+C hybrid

# Kernels
xo.Kernel(args=[...], n_threads='...')
xo.Arg(Type, name='...')
```

## xcoll (xc)

```python
# Collimators
xc.BlackAbsorber(length=..., jaw_L=..., jaw_R=..., side='both')
xc.EverestCollimator(length=..., jaw_L=..., jaw_R=..., material=..., side='both')
xc.EverestCrystal(length=..., jaw_L=..., jaw_R=..., material=..., bending_angle=...)
xc.FlukaCollimator(...)
xc.Geant4Collimator(...)

# Loss maps
xc.LossMap(line=..., part=...)
xc.MultiLossMap(lossmaps_list)

# Database
xc.CollimatorDatabase.from_yaml('file.yaml')
xc.CollimatorDatabase.from_json('file.json')
```

## xwakes (xw)

```python
# Wakes
xw.WakeResonator(kind='dipolar_x', r=R, q=Q, f_r=FR)
xw.WakeFromTable(table, columns=[...])
xw.Wake(components=[...])
xw.Component(wake=callable, plane='x', source_exponents=(...), test_exponents=(...))

# Configure
wake.configure_for_tracking(zeta_range=(...), num_slices=N)
wake.configure_for_tracking(..., filling_scheme=..., bunch_spacing_zeta=...,
                            num_turns=..., circumference=...)

# IO
xw.read_headtail_file('file.dat', columns=[...])
```

## xdeps

```python
xd.FunctionPieceWiseLinear(x=[...], y=[...])
xd.FunctionPieceWiseLinear.sin(arg)
xd.FunctionPieceWiseLinear.cos(arg)
```
