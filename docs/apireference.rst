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

List of methods
...............

.. autoautosummary:: xtrack.Line
    :methods:

Detailed description of methods
...............................

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

    .. rubric:: Methods

    .. autoautosummary:: xpart.ParticlesBase
        :methods:

Beam elements (xtrack)
======================

Marker
------

.. autoclass:: xtrack.Marker
    :members:
    :member-order: bysource

Drift
-----

.. autoclass:: xtrack.Drift
    :members:
    :member-order: bysource

Multipole
---------

.. autoclass:: xtrack.Multipole
    :members:
    :member-order: bysource

Cavity
------

.. autoclass:: xtrack.Cavity
    :members:
    :member-order: bysource

RFMultipole
-----------

.. autoclass:: xtrack.RFMultipole
    :members:
    :member-order: bysource

DipoleEdge
----------

.. autoclass:: xtrack.DipoleEdge
    :members:
    :member-order: bysource

ReferenceEnergyIncrease
-----------------------

.. autoclass:: xtrack.ReferenceEnergyIncrease
    :members:
    :member-order: bysource

Elens
-----

.. autoclass:: xtrack.Elens
    :members:
    :member-order: bysource

Exciter
-------

.. autoclass:: xtrack.Exciter
    :members:
    :member-order: bysource

Wire
----

.. autoclass:: xtrack.Wire
    :members:
    :member-order: bysource

FirstOrderTaylorMap
-------------------

.. autoclass:: xtrack.FirstOrderTaylorMap
    :members:
    :member-order: bysource


LinearTransferMatrix
--------------------

.. autoclass:: xtrack.LinearTransferMatrix
    :members:
    :member-order: bysource

LongitudinalLimitRect
---------------------

.. autoclass:: xtrack.LongitudinalLimitRect
    :members:
    :member-order: bysource

XYShift
-------

.. autoclass:: xtrack.XYShift
    :members:
    :member-order: bysource

SRotation
----------

.. autoclass:: xtrack.SRotation
    :members:
    :member-order: bysource

XRotation
---------

.. autoclass:: xtrack.XRotation
    :members:
    :member-order: bysource

YRotation
---------

.. autoclass:: xtrack.YRotation
    :members:
    :member-order: bysource

ZetaShift
---------

.. autoclass:: xtrack.ZetaShift
    :members:
    :member-order: bysource


LimitEllipse
------------

.. autoclass:: xtrack.LimitEllipse
    :members:
    :member-order: bysource

LimitRect
---------

.. autoclass:: xtrack.LimitRect
    :members:
    :member-order: bysource

LimitRectEllipse
----------------

.. autoclass:: xtrack.LimitRectEllipse
    :members:
    :member-order: bysource

LimitRacetrack
--------------

.. autoclass:: xtrack.LimitRacetrack
    :members:
    :member-order: bysource

LimitPolygon
------------

.. autoclass:: xtrack.LimitPolygon
    :members:
    :member-order: bysource


ParticlesMonitor
----------------

.. autoclass:: xtrack.ParticlesMonitor
    :members:
    :member-order: bysource

LastTurnsMonitor
----------------

.. autoclass:: xtrack.LastTurnsMonitor
    :members:
    :member-order: bysource

Beam elements (xfields)
======================


Beam-beam Bi-Gaussian 2D
------------------------

.. autoclass:: xfields.BeamBeamBiGaussian2D
    :members:
    :member-order: bysource

Beam-beam Bi-Gaussian 3D
------------------------

.. autoclass:: xfields.BeamBeamBiGaussian3D
    :members:
    :member-order: bysource

Space Charge Bi-Gaussian
------------------------

.. autoclass:: xfields.SpaceChargeBiGaussian
    :members:
    :member-order: bysource

Space Charge 3D
---------------

.. autoclass:: xfields.SpaceCharge3D
    :members:
    :member-order: bysource


CPU and GPU contexts
====================
