========================
Single-particle tracking
========================

This page describes the basic usage of Xsuite to perform tracking simulations.
Instructions on how to install Xsuite are provided in the dedicated :doc:`installation page <installation>`.

.. contents:: Table of Contents
    :depth: 4

A simple example
================

A simple tracking simulation can be configured and executed with the following python code. More details on the different steps will be discussed in the following section.

.. code-block:: python

    import numpy as np

    import xobjects as xo
    import xtrack as xt
    import xpart as xp

    ## Generate a simple sequence
    line = xt.Line(
        elements=[xt.Drift(length=2.),
                  xt.Multipole(knl=[0, 1.], ksl=[0,0]),
                  xt.Drift(length=1.),
                  xt.Multipole(knl=[0, -1.], ksl=[0,0])],
        element_names=['drift_0', 'quad_0', 'drift_1', 'quad_1'])

    ## Choose a context
    context = xo.ContextCpu()         # For CPU
    # context = xo.ContextCupy()      # For CUDA GPUs
    # context = xo.ContextPyopencl()  # For OpenCL GPUs

    ## Transfer lattice on context and compile tracking code
    tracker = xt.Tracker(_context=context, line=line)

    ## Build particle object on context
    n_part = 200
    particles = xp.Particles(_context=context,
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
    tracker.track(particles, num_turns=n_turns,
                  turn_by_turn_monitor=True)

    ## Turn-by-turn data is available at:
    tracker.record_last_track.x
    tracker.record_last_track.px
    # etc...



Step-by-step description
========================

In this sections we will discussed in some more detail the difference steps outlined in the example above.

Getting the Xline machine model
-------------------------------

The first step to perform a tracking simulation consists in creating or importing the lattice description of a ring or a beam line. 

This is done with the Line class, which allows:

 - creating a lattice directly in python script
 - importing the lattice from a MAD-X model
 - importing the lattice from a set of Sixtrack input files (fort.2, fort.3, etc.)

These three options will be briefly described in the following.

We can create a simple lattice in python as follows:

.. code-block:: python

    import xtrack as xt

    line = xt.Line(
        elements=[xt.Drift(length=2.),
                  xt.Multipole(knl=[0, 1.], ksl=[0,0]),
                  xt.Drift(length=1.),
                  xt.Multipole(knl=[0, -1.], ksl=[0,0])], 
        element_names=['drift_0', 'quad_0', 'drift_1', 'quad_1'])

The lattice can be manipulated in python after its creation. For example we can change the strength of the first quadrupole as follows:

.. code-block:: python

    q1 = line.elements[1]
    q1.knl = 2.

Importing a MAD-X lattice
~~~~~~~~~~~~~~~~~~~~~~~~~

Xtrack can import a MAD-X lattice using the `cpymad`_ interface of MAD-X.

.. _cpymad: http://hibtc.github.io/cpymad/

Assuming that we have a MAD-X script called ``myscript.madx`` that creates and manipulates (e.g. matches) a thin sequence called "lhcb1", we can execute the script using cpymad and import transform the sequence into and Xtrack Line object using the following instructions:

.. code-block:: python

    import xtrack as xt
    from cpymad.madx import Madx

    mad = Madx()
    mad.call("mad/lhcwbb.seq")

    line = xt.Line.from_madx_sequence(mad.sequence['lhcb1'])

Importing lattice from sixtrack input
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Xtrack can import a lattice from a set of sixtrack input files using the sixtracktools package.

Assuming that we have a sixtrack input files (fort.2, fort.3, etc.) in a folder called ``sixtrackfiles`` we can import the lattice using the following instructions:

.. code-block:: python

    import xtrack as xt
    import sixtracktools as st

    sequence = xt.Line.from_sixinput(st.sixinput('./sixtrackfiles'))


Once a Xtrack lattice is available, it can be used to track particles CPU or GPU.

Create a Context (CPU or GPU)
-----------------------------

To run tracking simulations with the created lattice, we need to choose the hardware on which the simulation will run as xsuite can run on different kinds of hardware (CPUs and GPUs). The user selects the hardware to be used by
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
-------------------------------

An Xtrack tracker object needs to be created to track particles on the chosen computing platform (defined by the context) using the Xtrack line created or imported as described above:

.. code-block:: python

    import xtrack as xt
    tracker = xt.Tracker(_context=context, line=line)

This step transfers the machine model to the required platform and compiles the required tracking code.

Generate particles to be tracked
--------------------------------

The particles to be tracked can be allocated on the chosen platform using the following instruction (in this example particle coordinates are randomly generated):

.. code-block:: python

    import xpart as xp

    import numpy as np
    n_part = 100
    particles = xp.Particles(_context=context,
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
---------------

The tracker object can now be used to track the generated particles over the specified lattice for an arbitrary number of turns:

.. code-block:: python

    num_turns = 100
    tracker.track(particles, num_turns=num_turns)

This returns the particles state after 100 revolutions over the lattice.

Record turn-by-turn data
------------------------

Optionally the particles coordinates can be saved at each turn. This feature can be activated when calling the tracking method:

.. code-block:: python

    n_turns = 100
    tracker.track(particles, num_turns=n_turns,
                  turn_by_turn_monitor=True)

The data can be retrieved as follows:

.. code-block:: python

    tracker.record_last_track.x # Shape is (n_part, n_turns)
    tracker.record_last_track.px
    # etc...







