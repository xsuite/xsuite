Getting Started Guide
=====================

This page describes the basic usage of Xfields (if you need to install Xfields, please follow the instructions in the dedicated :doc:`installation page <installation>`).

Create a Context
--------------------------

Xfield can run on different kinds of hardware (CPUs and GPUs). The user selects the herdware to be used by
creating a :doc:`context object<contexts>`, that is then passed to all other Xfields components.

To run on conventional CPUs you need to create the corresponding context:

.. code-block:: python

    from xfields.contexts import XfCpuContext
    context = XfCpuContext()

Similarly to run on GPUs using cupy:

.. code-block:: python

    from xfields.contexts import XfCupyContext
    context = XfCupyContext()

And to run on GPUs and CPUs using PyOpenCL:

.. code-block:: python

    from xfields.contexts import XfPyopenclContext
    context = XfPyopenclContext()


Create a Beam Element
---------------------

The context that has been created can be passed when constructing a beam element defining the hardware on which the calculation is performed. For example we can create a spacecharge beam element as follows:

.. code-block:: python

    from xfields import SpaceCharge3D

    spcharge = SpaceCharge3D(
        context=context,   # defines the hardware
        length=5.,
        update_on_track=True,
        apply_z_kick=True,
        x_range=(-0.02, 0.02),
        y_range=(-0.015, 0.015),
        z_range=(-1.5, 1.5),
        nx=256, ny=256, nz=50,
        solver='FFTSolver2p5D',
        gamma0=27.64)

Track
-----

The beam element can be used to track a bunch stored on the same context:

.. code-block:: python

    spcharge.track(bunch)

Full example
------------

A complete example, including also the generation of the bunch is available `here <exgit>`_.

.. _exgit: https://github.com/xsuite/xfields/blob/master/examples/001_spacecharge/000_spacecharge_example.py
