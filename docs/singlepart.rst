===============
Getting started
===============

This page describes the basic usage of Xsuite to perform tracking simulations.
Instructions on how to install Xsuite are provided in the dedicated
:doc:`installation page <installation>`.

.. contents:: Table of Contents
    :depth: 4

A simple example
================

A simple tracking simulation can be configured and executed with the following
python code. More details on the different steps will be discussed in the following section.

.. code-block:: python

    import numpy as np

    import xobjects as xo
    import xtrack as xt

    ## Generate a simple line
    line = xt.Line(
        elements=[xt.Drift(length=2.),
                  xt.Multipole(knl=[0, 0.5], ksl=[0,0]),
                  xt.Drift(length=1.),
                  xt.Multipole(knl=[0, -0.5], ksl=[0,0])],
        element_names=['drift_0', 'quad_0', 'drift_1', 'quad_1'])

    ## Attach a reference particle to the line (optional)
    ## (defines the reference mass, charge and energy)
    line.particle_ref = xt.Particles(p0c=6500e9, #eV
                                     q0=1, mass0=xt.PROTON_MASS_EV)

    ## Choose a context
    context = xo.ContextCpu()         # For CPU
    # context = xo.ContextCupy()      # For CUDA GPUs
    # context = xo.ContextPyopencl()  # For OpenCL GPUs

    ## Transfer lattice on context and compile tracking code
    line.build_tracker(_context=context)

    ## Compute lattice functions
    tw = line.twiss(method='4d')
    tw.cols['s betx bety'].show()
    # prints:
    #
    # name       s    betx    bety
    # drift_0    0 3.02372 6.04743
    # quad_0     2 6.04743 3.02372
    # drift_1    2 6.04743 3.02372
    # quad_1     3 3.02372 6.04743
    # _end_point 3 3.02372 6.04743

    ## Build particle object on context
    n_part = 200
    particles = line.build_particles(
                            x=np.random.uniform(-1e-3, 1e-3, n_part),
                            px=np.random.uniform(-1e-5, 1e-5, n_part),
                            y=np.random.uniform(-2e-3, 2e-3, n_part),
                            py=np.random.uniform(-3e-5, 3e-5, n_part),
                            zeta=np.random.uniform(-1e-2, 1e-2, n_part),
                            delta=np.random.uniform(-1e-4, 1e-4, n_part))
    # Reference mass, charge, energy are taken from the reference particle.
    # Particles are allocated on the context chosen for the line.

    ## Track (saving turn-by-turn data)
    n_turns = 100
    line.track(particles, num_turns=n_turns,
                  turn_by_turn_monitor=True)

    ## Turn-by-turn data is available at:
    line.record_last_track.x
    line.record_last_track.px
    # etc...


Step-by-step description
========================

In this sections we will discuss in some more detail the different steps
outlined in the example above.

Getting the machine model
-------------------------

The first step to perform a tracking simulation consists in creating or importing
the lattice description of a ring or a beam line.

The lattice can be created from a list of elements:

.. code-block:: python

    import xtrack as xt

    # From a list of elements:
    line = xt.Line(
        elements=[xt.Drift(length=2.),
                  xt.Multipole(knl=[0, 1.], ksl=[0,0]),
                  xt.Drift(length=1.),
                  xt.Multipole(knl=[0, -1.], ksl=[0,0])],
        element_names=['drift_0', 'quad_0', 'drift_1', 'quad_1'])

The lattice can be manipulated in python after its creation. For example we can
change the strength of the first quadrupole as follows:

.. code-block:: python

    line['quad_0'].knl[1] = 2.

It is also possible to import a lattice from a MAD-X file, as discussed
:ref:`here <madximport>` or to define it as a sequence as discussed
:ref:`here <seqdef>`.

More information on how to import and manipulate lattices can be found in the
dedicated :doc:`Line section<line>`.


Define reference particle
-------------------------

A reference particle can be associated to the line and is used to define the
reference mass, charge and energy when generating other particle sets or when
performing other calculation (e.g. computing twiss parameters, compensating the
energy loss, etc.). The reference particle can be defined as follows:

.. code-block:: python

    line.particle_ref = xt.Particles(p0c=6500e9, #eV
                                     q0=1, mass0=xt.PROTON_MASS_EV)


Create a Context (CPU or GPU)
-----------------------------

To run tracking simulations with the created lattice, we need to choose the
hardware on which the simulation will run as xsuite can run on different kinds
of hardware (CPUs and GPUs). The user selects the hardware to be used by
creating a :doc:`context object <contexts>`, that is then passed to all other
Xsuite components.

To run on conventional CPUs you need the context is created with the following instructions:

.. code-block:: python

    import xobjects as xo
    context = xo.ContextCpu()

Similarly to run on GPUs using cupy or pyopenl you can use one of the following:

.. code-block:: python

    context = xo.ContextCupy()

.. code-block:: python

    context = xo.ContextPyopencl()


Build tracker
-------------

An Xtrack tracker object needs to be associated to the line in order to track
particles on the chosen computing platform (defined by the context):

.. code-block:: python

    line.build_tracker(_context=context)

This step transfers the machine model to the required platform and compiles
the required tracking code.

Twiss
-----

The Twiss parameters of the lattice can be through the ``twiss`` method of the
line object:

.. code-block:: python

    ## Compute lattice functions
    tw = line.twiss(method='4d')
    tw.cols['s betx bety'].show()
    # prints:
    #
    # name       s    betx    bety
    # drift_0    0 3.02372 6.04743
    # quad_0     2 6.04743 3.02372
    # drift_1    2 6.04743 3.02372
    # quad_1     3 3.02372 6.04743
    # _end_point 3 3.02372 6.04743

All capabilities and options of the twiss method are discussed in the
:doc:`Twiss section <twiss>`.

Generate particles to be tracked
--------------------------------

The particles to be tracked can be allocated on the chosen platform using
the ``build_particles`` method of the line

.. code-block:: python

    ## Build particle object on context
    n_part = 200
    particles = line.build_particles(
                            x=np.random.uniform(-1e-3, 1e-3, n_part),
                            px=np.random.uniform(-1e-5, 1e-5, n_part),
                            y=np.random.uniform(-2e-3, 2e-3, n_part),
                            py=np.random.uniform(-3e-5, 3e-5, n_part),
                            zeta=np.random.uniform(-1e-2, 1e-2, n_part),
                            delta=np.random.uniform(-1e-4, 1e-4, n_part))
    # Reference mass, charge, energy are taken from the reference particle.
    # Particles are allocated on the context chosen for the line.


The coordinates of the particle object are accessible with the conventional
python syntax. For example to access the *x* coordinate of the particle 20,
one can use the following instruction:

.. code-block:: python

    particles.x[20]

For more information on how to create and manipulate particle objects, please
refer to the :doc:`Particles section <particlesmanip>`.

Track particles
---------------

The line object can now be used to track the generated particles over
the specified lattice for an arbitrary number of turns:

.. code-block:: python

    num_turns = 100
    line.track(particles, num_turns=num_turns)

This returns the particles state after 100 revolutions over the lattice.

More information about Xsuite tracking capabilities can be found in the
:doc:`Track section <track>`.

Record turn-by-turn data
------------------------

Optionally the particles coordinates can be saved at each turn. This feature
can be activated when calling the tracking method:

.. code-block:: python

    n_turns = 100
    line.track(particles, num_turns=n_turns,
                  turn_by_turn_monitor=True)

The data can be retrieved as follows:

.. code-block:: python

    line.record_last_track.x # Shape is (n_part, n_turns)
    line.record_last_track.px
    # etc...

For more information about the Xsuite monitoring capabilities, please refer to
the :ref:`Monitors section <monitors>`.
