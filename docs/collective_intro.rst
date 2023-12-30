Tracking with collective elements
=================================

A collective beam element is an element that needs access to the entire particle set (in read and/or write mode). The following example shows how to handle such elements in Xsuite.

Example
-------

A typical example of collective element is a space-charge interaction. We can create a space-charge beam element as follows:

.. code-block:: python

    import xobjects as xo
    import xfields as xf

    context = xo.ContextCpu()

    spcharge = xf.SpaceChargeBiGaussian(_context=context,
        update_on_track = ['sigma_x', 'sigma_y'], length=2,
        longitudinal_profile=xf.LongitudinalProfileQGaussian(
            _context=context, number_of_particles=1e11, sigma_z=0.2))

This creates a space-charge element where the transverse beam sizes are updated based on the particle set at each interaction. Such an element can be included in an :doc:`xtrack tracker <singlepart>` similarly to single-particle elements.

.. code-block:: python

    import xtrack as xt

    ## Generate a simple beam line including the spacecharge element
    myqf = xt.Multipole(knl=[0, 1.])
    myqd = xt.Multipole(knl=[0, -1.])
    mydrift = xt.Drift(length=1.)
    line = xt.Line(
        elements = [myqf, mydrift, myqd, mydrift,
                    spcharge,
                    myqf, mydrift, myqd, mydrift,],
        element_names = ['qf1', 'drift1', 'qd1', 'drift2',
                            'spcharge'
                            'qf2', 'drift3', 'qd2', 'drift4'])

    ## Transfer lattice on context and compile tracking code
    line.build_tracker(_context=context)

    ## Build particle object on context
    n_part = 200
    particles = xt.Particles(_context=context,
                            p0c=6500e9,
                            x=np.random.uniform(-1e-3, 1e-3, n_part),
                            px=np.random.uniform(-1e-5, 1e-5, n_part),
                            y=np.random.uniform(-2e-3, 2e-3, n_part),
                            py=np.random.uniform(-3e-5, 3e-5, n_part),
                            zeta=np.random.uniform(-1e-2, 1e-2, n_part),
                            delta=np.random.uniform(-1e-4, 1e-4, n_part),
                            )

    ## Track (saving turn-by-turn data)
    n_turns = 100
    line.track(particles, num_turns=n_turns,
                turn_by_turn_monitor=True)

How does it work?
-----------------

To decide whether or not an element needs to be treated as collective, the
tracker inspects its ``iscollective`` attribute. In our example:

.. code-block:: python

    print(qf.iscollective)
    # Gives "False"

    print(spcharge.iscollective)
    # Gives "True"

Based in this information the line is divided in parts that are either collective
elements or xtrack trackers simulating groups of consecutive non-collective elements.

We can visualize this in our example:

.. code-block:: python

    print(line.tracker._parts)
    # Gives:
    # [<xtrack.tracker.Tracker object at 0x7f5ba8ce7760>,
    #  <xfields.beam_elements.spacecharge.SpaceChargeBiGaussian object at 0x7f5ba8e1bd30>,
    #  <xtrack.tracker.Tracker object at 0x7f5ba8ce7610>]

where the first part tracks the particles through to the first potion of the
machine up to the space-charge element, the second part simulates the space-charge
interaction, the third part tracks the particles from the space-charge element to the end of the line.

As all xsuite and xsuite-compatible beam elements need to expose a ``.track``
method the instruction:

.. code-block:: python

    line.track(particles)

is equivalent to the loop:

.. code-block:: python

    for pp in line.tracker._parts:
        pp.track(particles)

Any python object exposing a '.track' method can be used as beam_element. If the
attribute ``iscollective`` is not present the element is handled as collective.
