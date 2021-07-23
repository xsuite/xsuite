========================
Collective beam elements
========================

A collective beam element is an element that needs access to the entire particle set (in read and/or write mode). The following example shows how to handle such elements in Xsuite.

A typical example of collective element is a space-charge interaction. We can creat a space-charge beam element as follows:

.. code-block:: python

    import xobjects as xo
    import xfields as xf

    context = xo.ContextCpu

    spcharge = xf.SpaceChargeBiGaussian(_context=context,
        length=2, sigma_x=1e-3, sigma_y=1.5e-3,
        longitudinal_profile=xf.LongitudinalProfileQGaussian(
            _context=context, number_of_particles=1e11, sigma_z=0.2)
        )
