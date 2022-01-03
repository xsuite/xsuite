========================
Space-charge simulations
========================

Xsuite can be used to perform simulations including space-charge effects. Three
modes can  be used to simulate the space-charge forces:
 - **Forzen:**  A fixed Gaussian bunch distribution is used to compute the space-charge forces.
 - **Quasi-frozen:** Forces are computed assuming a Gaussian distribution. The properties of the distribution (transverse r.m.s. sizes,transverse positions) are updated at each interaction based on the particle distribution.
 - **PIC:** The Particle In Cell method is used to compute the forces acting among particles. No assumption is made on the bunch shape.

The last two options constitute collective interactions. As discussed 
in the :doc:`dedicated section <collective>`, the Xtrack Tracker works such that particles are tracked asynchronously by separate threads in the non-collective sections of the sequence and are regrouped at each collective element (in PIC or quasi-forzen space-charge lenses).


Xfields provides tools to configure qausi-frozen and Particle-In-Cell space-charge simulations by automatically replacing in an Xline sequence the frozen space-charge lenses with the corresponding collective beam elements. This is illustrated in the following example.

Example
=======

Import modules
~~~~~~~~~~~~~~

We import all the required modules

.. code-block:: python

    import json
    import numpy as np

    import xobjects as xo
    import xpart as xp
    import xtrack as xt
    import xfields as xf

Machine model
~~~~~~~~~~~~~

For this example we load from the `SPS Xtrack test_data folder <https://github.com/xsuite/xtrack/tree/main/test_data/sps_w_spacecharge>`_ a sequence with frozen space-charge lenses together with the corresponding particle on the closed orbit and linearized one-turn matrix. The same folder contains also example code to generate these files from the MAD-X model of the accelerator.

.. code-block:: python

    fname_line = ('xtrack/test_data/sps_w_spacecharge/'
                    'line_with_spacecharge_and_particle.json')

    fname_optics = ('xtrack/test_data/sps_w_spacecharge/'
                    'optics_and_co_at_start_ring.json')

    with open(fname_line, 'r') as fid:
        line_dict = json.load(fid)
    with open(fname_optics, 'r') as fid:
        co_opt_dict = json.load(fid)

    line = xt.Line.from_dict(line_dict['line'])
    part_on_co = xp.Particles.from_dict(co_opt_dict['particle_on_madx_co'])
    RR = np.array(co_opt_dict['RR_madx']) # Linear one-turn matrix


Choice of the context
~~~~~~~~~~~~~~~~~~~~~

We choose the hardware on which we want to run by buildind an Xobjects context:

.. code-block:: python

    context = xo.ContextCupy()
    #context = xo.ContextPyopencl('0.0')
    #context = xo.ContextCpu()


Configuration quasi-frozen or PIC space-charge elements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We use the Xfields functions ``replace_spacecharge_with_quasi_frozen`` or ``replace_spacecharge_with_PIC`` to replace the frozen space-charge lenses with PIC or quasi-frozen collective elements:

.. code-block:: python

    mode = 'pic' # Can be 'pic', 'quasi-frozen' or 'forzen'

    if mode == 'frozen':
        pass # Already configured in line
    elif mode == 'quasi-frozen':
        xf.replace_spacecharge_with_quasi_frozen(
                    line, _buffer=context.new_buffer(),
                    update_mean_x_on_track=True,
                    update_mean_y_on_track=True)
    elif mode == 'pic':
        pic_collection, all_pics = xf.replace_spacecharge_with_PIC(
                    _context=context, line=line,
                    n_sigmas_range_pic_x=8,
                    n_sigmas_range_pic_y=8,
                    nx_grid=256, ny_grid=256, nz_grid=100,
                    n_lims_x=7, n_lims_y=3,
                    z_range=(-0.7, 0.7))
    else:
        raise ValueError(f'Invalid mode: {mode}')



Build Xtrack tracker
~~~~~~~~~~~~~~~~~~~~

We build an Xtrack tracker:

.. code-block:: python

    tracker = xt.Tracker(_context=context,
                        line=line)

As discussed :doc:`here <collective>`, the tracker is built in such a way that particles are tracked asynchronously by separate threads in the non-collective sections of the sequence and are regrouped at each collective element (in our case the PIC or quasi-forzen space-charge lenses).


Generation of matched particle set
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We use Xpart to generate a matched particle distribution and we transfer it to the context:

.. code-block:: python

    part = xp.generate_matched_gaussian_bunch(
            num_particles=int(1e6), total_intensity_particles=1e11,
            nemitt_x=2.5e-6, nemitt_y=2.5e-6, sigma_z=22.5e-2,
            particle_on_co=part_on_co, R_matrix=RR,
            circumference=6911., alpha_momentum_compaction=0.0030777,
            rf_harmonic=4620, rf_voltage=3e6, rf_phase=0)

    # Transfer particles to context
    xtparticles = xt.Particles(_context=context, **part.to_dict())

Simulate
~~~~~~~~

The simulation can be started by calling the ``track`` method of the tracker:

.. code-block:: python

    tracker.track(xtparticles, num_turns=3)

A :class:`ParticlesMonitor <xtrack.ParticlesMonitor>` object can be passed to the track method to record all or a fraction of the particles coordinated.


