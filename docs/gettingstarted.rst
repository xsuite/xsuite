Getting Started Guide
=====================

This page describes the basic usage of Xsuite (if you need to install Xfields, please follow the instructions in the dedicated :doc:`installation page <installation>`).

Create a Context
----------------

Xsuite can run on different kinds of hardware (CPUs and GPUs). The user selects the herdware to be used by
creating a :doc:`context object <contexts>`, that is then passed to all other Xfields components.

To run on conventional CPUs you need to create the corresponding context:

.. code-block:: python

    import xobjects as xo
    context = xo.ContextCpu()

Similarly to run on GPUs using cupy:

.. code-block:: python

    import xobjects as xo
    context = xo.ContextCupy()

And to run on GPUs and CPUs using PyOpenCL:

.. code-block:: python

    import xobjects as xo
    context = xo.ContextPyopencl()


Single-particle tracking with Xtrack
------------------------------------

Xtrack uses as input description of the beamline a ``sequence`` python object. Such a python object can be obtained, for example, from the MAD-X model of the machine or from a set of SixTrack input files, using the pysixtrack package.

The sequence can be used to create a tracker object to track particles on the chosen computing platform (defined by the context).

.. code-block:: python

    import xtrack as xt
    tracker = xt.Tracker(_contect=contect, sequence=sequence)

Xfields beam elements
---------------------

The context that has been created can be passed when constructing a beam element defining the hardware on which the calculation is performed.

Space charge element
~~~~~~~~~~~~~~~~~~~~

For example we can create a :class:`spacecharge<xfields.SpaceCharge3D>`  beam element (from Xfields) as follows:

.. code-block:: python

    from xfields import SpaceCharge3D

    spcharge = SpaceCharge3D(
        _context=context,   # defines the hardware
        length=5.,
        update_on_track=True,
        apply_z_kick=True,
        x_range=(-0.02, 0.02),
        y_range=(-0.015, 0.015),
        z_range=(-1.5, 1.5),
        nx=256, ny=256, nz=50,
        solver='FFTSolver2p5D',
        gamma0=27.64)



The beam element can be used to track a bunch stored on the same context:

.. code-block:: python

    spcharge.track(bunch)


A complete space-charge example, including also the generation of the bunch is available `here <https://github.com/xsuite/xfields/blob/master/examples/001_spacecharge/000_spacecharge_example.py>`_.

Beam-beam element
~~~~~~~~~~~~~~~~~

A :class:`beambeam<xfields.BeamBeamBiGaussian2D>` elements can be created by:

.. code-block:: python

    from xfields import BeamBeamBiGaussian2D

    bbeam_b1 = BeamBeamBiGaussian2D(
        _context=context, # defines the hardware
        n_particles=1e11,
        q0 = qe,
        beta0=1.,
        sigma_x=None, # needs to be specified only for weak-strong
        sigma_y=None, # needs to be specified only for weak-strong
        mean_x=None, # needs to be specified only for weak-strong
        mean_y=None, # needs to be specified only for weak-strong
        min_sigma_diff=1e-10)

The beam position and size can be measured from the set of macroparticles moodeling the other beam and used to update the element at each passage (soft-gaussian model):

.. code-block:: python

    from xfields import mean_and_std
    # Measure beam properties
    mean_x_meas, sigma_x_meas = mean_and_std(particles_b2.x)
    mean_y_meas, sigma_y_meas = mean_and_std(particles_b2.y)

    # Update bb lens
    bbeam_b1.update(sigma_x=sigma_x_meas, mean_x=mean_x_meas,
                    sigma_y=sigma_y_meas, mean_y=mean_y_meas)

Kicks to the particles can be applied with the track method:

.. code-block:: python

    bbeam_b1.track(particles_b1)

A complete beam-beam example, including also the generation of the bunch is available `here <https://github.com/xsuite/xfields/blob/master/examples/002_beambeam/000_beambeam.py>`_.