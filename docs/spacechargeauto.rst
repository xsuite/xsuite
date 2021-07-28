==============================================
Quasi-frozen and PIC space-charge simulations
==============================================

Xfields provides tools to configure qausi-frozen and Particle-In-Cell space-charge simulations by automatically replacing in an Xline sequence the frozen space-charge lenses with the corresponding collective beam elements. This is illustrated in the following example.

Import modules
~~~~~~~~~~~~~~

We import all the required modules

.. code-block:: python

    import json
    import numpy as np

    import xobjects as xo
    import xline as xl
    import xpart as xp
    import xtrack as xt
    import xfields as xf

Machine model
~~~~~~~~~~~~~

For this example we load from the `SPS Xtrack test_data folder <https://github.com/xsuite/xtrack/tree/main/test_data/sps_w_spacecharge>`_ a sequence with frozen space-charge lenses together with the corresponding particle on the closed orbit and linearized one-turn matrix. The same folder contains also example code to generate these files from the MAD-X model of the accelerator.

.. code-block:: python

    fname_sequence = ('xtrack/test_data/sps_w_spacecharge/'
                    'line_with_spacecharge_and_particle.json')

    fname_optics = ('xtrack/test_data/sps_w_spacecharge/'
                    'optics_and_co_at_start_ring.json')

    with open(fname_sequence, 'r') as fid:
        seq_dict = json.load(fid)
    with open(fname_optics, 'r') as fid:
        co_opt_dict = json.load(fid)

    sequence = xl.Line.from_dict(seq_dict['line'])
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

We use the Xfields functions ``replace_spaceharge_with_quasi_frozen`` or ``replace_spaceharge_with_PIC`` to replace the frozen space-charge lenses with PIC or quasi-frozen collective elements:

.. code-block:: python

    mode = 'PIC' # Can be 'PIC', 'quasi-frozen' or 'forzen'

    if mode == 'frozen':
        pass # Already configured in line
    elif mode == 'quasi-frozen':
        xf.replace_spaceharge_with_quasi_frozen(
                                        sequence, _buffer=context.new_buffer(),
                                        update_mean_x_on_track=True,
                                        update_mean_y_on_track=True)
    elif mode == 'pic':
        pic_collection, all_pics = xf.replace_spaceharge_with_PIC(
            _context=context, sequence=sequence,
            n_sigmas_range_pic_x=8,
            n_sigmas_range_pic_y=8,
            nx_grid=256, ny_grid=256, nz_grid=100,
            n_lims_x=7, n_lims_y=3,
            z_range=(-3*sigma_z, 3*sigma_z))
    else:
        raise ValueError(f'Invalid mode: {mode}')



Build Xtrack tracker
~~~~~~~~~~~~~~~~~~~~

We build an Xtrack tracker:

.. code-block:: python

    tracker = xt.Tracker(_context=context,
                        sequence=sequence)

As discussed in the :ref:`dedicated section <collective>`, 




    part = xp.generate_matched_gaussian_bunch(
            num_particles=n_part, total_intensity_particles=bunch_intensity,
            nemitt_x=neps_x, nemitt_y=neps_y, sigma_z=sigma_z,
            particle_on_co=part_on_co, R_matrix=RR,
            circumference=6911., alpha_momentum_compaction=0.0030777,
            rf_harmonic=4620, rf_voltage=rf_voltage, rf_phase=0)

    # Transfer particles to context
    xtparticles = xt.Particles(_context=context, **part.to_dict())

    #########
    # Track #
    #########
    tracker.track(xtparticles, num_turns=3)




Additional settings
~~~~~~~~~~~~~~~~~~~

We set some additional beam and machine parameters

.. code-block:: python

    bunch_intensity = 1e11
    sigma_z = 22.5e-2
    neps_x=2.5e-6
    neps_y=2.5e-6
    n_part=int(1e6)
    rf_voltage=3e6
