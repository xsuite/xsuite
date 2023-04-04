=============
API reference
=============

.. contents:: Table of Contents
    :depth: 6

Core classes
============

This secion documents two core classes of Xsuite: :class:`xtrack.Line` and
:class:`xpart.ParticlesBase`, which are the two main building blocks of Xsuite
simulations.

xtrack.Line class
-----------------

The Xsuite Line class is the main class to build beam lines. Its interface is
described in the following (more info on how to build and use beam lines for
different purposes can be found in the :doc:`Xsuite user's guide <usersguide>`).

.. autoclass:: xtrack.Line
    :members:
    :member-order: bysource

xpart.Particles class
---------------------

Xsuite Particles classes, including the default xpart.Particles class, expose
the API described in the following (for more info on how to manipulate Particles
objects, see the :doc:`Working with Particles objects <particlesmanip>`).

.. autoclass:: xpart.ParticlesBase
    :members:
    :inherited-members:
    :member-order: bysource

Beam elements
=============

CPU and GPU contexts
====================








