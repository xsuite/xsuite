Getting Started Guide
=====================

This page describes the basic usage of Xsuite to perform tracking simulations.
Instructions on how to install Xsuite are provided in the dedicated :doc:`installation page <installation>`.

.. contents:: Table of Contents
    :depth: 3

A simple example
----------------

A simple tracking simulation can be configured and executed with the following python code:

.. code-block:: python

    import numpy as np

    import xobjects as xo
    import xline as xl
    import xtrack as xt

    ## Generate a simple sequence
    sequence = xl.Line(
        elements=[xl.Drift(length=2.),
                  xl.Multipole(knl=[0, 1.], ksl=[0,0]),
                  xl.Drift(length=1.),
                  xl.Multipole(knl=[0, -1.], ksl=[0,0])], 
        element_names=['drift_0', 'quad_0', 'drift_1', 'quad_1'])

    ## Chose a context
    xo.ContextCpu()         # For CPU
    # xo.ContectCupy()      # For CUDA GPUs
    # xo.ContectPyopencl()  # For OpenCL GPUs    

    ## Transfer lattice on context and compile tracking code
    tracker = xt.Tracker(_contect=context, sequence=sequence)

    ## Build particle object on context 
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
    tracker.track(particles, num_turns=n_turns
                  turn_by_turn_monitor=True)

    ## Turn-by-turn data is available at:
    tracker.record_last_track.x
    tracker.record_last_track.px 
    # etc...

    
Getting the Xline machine model
-------------------------------

The first step to perform a tracking simulation consists in creating or importing the lattice description of a ring or a beam line. 

This is done with the Xline package, which allows:

 - creating a lattice directly in python script
 - importing the lattice from a MAD-X model 
 - importing the lattice from a set of Sixtrack input files (fort.2, fort.3, etc.)

These three options will be briefly described in the following.

We can create a simple lattice in python as follows:

.. code-block:: python

    import xline as xl

    sequence = xl.Line(
        elements=[xl.Drift(length=2.),
                  xl.Multipole(knl=[0, 1.], ksl=[0,0]),
                  xl.Drift(length=1.),
                  xl.Multipole(knl=[0, -1.], ksl=[0,0])], 
        element_names=['drift_0', 'quad_0', 'drift_1', 'quad_1'])

The lattice can be manipulated in python after its creation. For example we can change the strength of the first quadrupole as follows:

.. code-block:: python

    q1 = sequence.elements[1]
    q1.knl = 2.

Importing a MAD-X lattice 
~~~~~~~~~~~~~~~~~~~~~~~~~

Xline can import a MAD-X lattice using the `cpymad`_ interface of MAD-X.

.. _cpymad: http://hibtc.github.io/cpymad/

Assuming that we have a MAD-X script called ``myscript.madx`` that creates and manipulates (e.g. matches) a thin sequence called "lhcb1", we can execute the script using cpymad and import transform the sequence into and Xline object using the following instructions:

.. code-block:: python

    import xline as xl
    from cpymad.madx import Madx
    
    mad = Madx()    
    mad.call("mad/lhcwbb.seq")
    
    line = xl.Line.from_madx_sequence(mad.sequence['lhcb1'])

Importing lattice from sixtrack input
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Xline can import a lattice from a set of sixtrack input files using the sixtracktools package.
    
Assuming that we have a sixtrack input files (fort.2, fort.3, etc.) in a folder called ``sixtrackfiles`` we can import the lattice using the following instructions:

.. code-block:: python

    import xline as xl
    import sixtracktools as st

    sequence = xl.Line.from_sixinput(st.sixinput('./sixtrackfiles'))


Tracking particles
------------------

Once a Xline lattice is available, it can be used to track particles CPU or GPU.

Create a Context (CPU or GPU)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The first step consists in choosing the hardware on which the simulation will run as xsuite can run on different kinds of hardware (CPUs and GPUs). The user selects the hardware to be used by
creating a :doc:`context object <contexts>`, that is then passed to all other Xsuite components.

To run on conventional CPUs you need the context is created with the following instructions:

.. code-block:: python

    import xobjects as xo
    context = xo.ContextCpu()

Similarly to run on GPUs using cupy or pyopenl you can use one of the following:

.. code-block:: python

    context = xo.ContextCupy()

.. code-block:: python

    context = xo.ContextPyopencl()


Create an Xtrack tracker object
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An Xtrack tracker object needs to be created to track particles on the chosen computing platform (defined by the context) using the Xline sequence created or imported as described above:

.. code-block:: python

    import xtrack as xt
    tracker = xt.Tracker(_contect=context, sequence=sequence)

This step transfers the machine model to the required platform and compiles the required tracking code.

Generate particles to be tracked
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The particles to be tracked can be allocated on the chosen platform using the following instruction (in this example particle coordinates are randomly generated):

.. code-block:: python

    import numpy as np
    n_part = 100
    particles = xt.Particles(_context=context,
                            p0c=6500e9,
                            x=np.random.uniform(-1e-3, 1e-3, n_part),
                            px=np.random.uniform(-1e-5, 1e-5, n_part),
                            y=np.random.uniform(-2e-3, 2e-3, n_part),
                            py=np.random.uniform(-3e-5, 3e-5, n_part),
                            zeta=np.random.uniform(-1e-2, 1e-2, n_part),
                            delta=np.random.uniform(-1e-4, 1e-4, n_part),
                            )

The coordinates of the particle object are accessible with the conventional python syntax. For example to access the *x* coordinate of the particle 20, one can use the following instruction:

.. code-block:: python

    particles.x[20]

Track particles
~~~~~~~~~~~~~~~

The tracker object can now be used to track the generated particles over the specified lattice for an arbitrary number of turns:

.. code-block:: python

    num_turns = 100
    tracker.track(particles, num_turns=num_turns)

This returns the particles state after 100 revolutions over the lattice.

Recording turn-by-turn data
~~~~~~~~~~~~~~~~~~~~~~~~~~~





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