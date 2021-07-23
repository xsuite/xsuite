========================
Collective beam elements
========================

A collective beam element is an element that needs access to the entire particle set (in read and/or write mode). The following example shows how to handle such elements in Xsuite.

Trackers with collective elements
=================================

A typical example of collective element is a space-charge interaction. We can create a space-charge beam element as follows:

.. code-block:: python

    import xobjects as xo
    import xfields as xf

    context = xo.ContextCpu

    spcharge = xf.SpaceChargeBiGaussian(_context=context,
        update_on_track = ['sigma_x', 'sigma_y'], length=2,
        longitudinal_profile=xf.LongitudinalProfileQGaussian(
            _context=context, number_of_particles=1e11, sigma_z=0.2))

This creates a space-charge element where the transverse beam sizes are updated based on the particle set at each interaction. Such an element can be included in an :doc:`xtrack tracker <singlepart>` similarly to single-particle elements.

.. code-block:: python

    import xline as xl
    import xtrack as xt

    myqf = xl.Multipole(knl=[0, 1.])
    myqd = xl.Multipole(knl=[0, -1.])
    mydrift = xl.Drift(length=1.)

    sequence = xl.Line(
        elements = [myqf, mydrift, myqd, mydrift,
                    spcharge,
                    myqf, mydrift, myqd, mydrift,],
        element_names = ['qf1', 'drift1', 'qd1', 'drift2',
                            'spcharge'
                            'qf2', 'drift3', 'qd2', 'drift4'])

    tracker = xt.Tracker(_context=context, sequence=sequence)

