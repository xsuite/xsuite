Interface to PyHEADTAIL
=======================

PyHEADTAIL elements cannot be natively used by an Xsuite line due to different
naming conventions for the particles coordinates. A specific interface has been
introduced in Xsuite which indtroduces additional properties in the Particles
objects in order to make them compatible with PyHEADTAIL beam elements.
The interface can be enabled by calling the function
``enable_pyheadtail_interface`` right after importing xtrack, as illustrated
in the following example.

.. code-block:: python

    import pathlib
    import json
    import numpy as np

    import xobjects as xo
    import xtrack as xt
    xt.enable_pyheadtail_interface()

    fname_line = '../../test_data/lhc_no_bb/line_and_particle.json'
    num_turns = int(100)
    n_part = 200

    ####################
    # Choose a context #
    ####################

    context = xo.ContextCpu()

    ##############
    # Get a line #
    ##############

    with open(fname_line, 'r') as fid:
        input_data = json.load(fid)
    line = xt.Line.from_dict(input_data['line'])

    #########################
    # Add PyHEADTAIL damper #
    #########################

    from PyHEADTAIL.feedback.transverse_damper import TransverseDamper
    damper = TransverseDamper(dampingrate_x=10., dampingrate_y=15.)
    line.append_element(damper, 'Damper')

    ##################
    # Build TrackJob #
    ##################

    line.build_tracker(_context=context)

    ######################
    # Get some particles #
    ######################

    particles = xt.Particles(_context=context,
                            p0c=6500e9,
                            x=np.random.uniform(-1e-3, 1e-3, n_part)+1e-3,
                            px=np.random.uniform(-1e-7, 1e-7, n_part),
                            y=np.random.uniform(-0.5e-3, 0.5e-3, n_part)-1.2e-3,
                            py=np.random.uniform(-1e-7, 1e-7, n_part),
                            zeta=0*np.random.uniform(-1e-2, 1e-2, n_part),
                            delta=0.*np.random.uniform(-1e-5, 1e-5, n_part))

    #########
    # Track #
    #########

    line.track(particles, num_turns=num_turns, turn_by_turn_monitor=True)

    ########
    # Plot #
    ########

    res = line.record_last_track

    import matplotlib.pyplot as plt
    plt.close('all')
    fig1 = plt.figure(1)
    sp1 = fig1.add_subplot(2,1,1)
    sp2 = fig1.add_subplot(2,1,2)
    sp1.plot(np.mean(res.x, axis=0))
    sp2.plot(np.mean(res.y, axis=0))
    plt.show()