===========
Xfields API
===========

.. contents:: Table of Contents
    :depth: 4


Beam elements
=============

Space Charge element
--------------------

The spacecharge computation in this class uses an :doc:`Xfields fieldmap <fieldmaps>` instance.

.. autoclass:: xfields.SpaceCharge3D
    :members:
    :undoc-members:
    :member-order: bysource

Beam-beam element
-----------------

.. autoclass:: xfields.BeamBeamBiGaussian2D
    :members:
    :undoc-members:
    :member-order: bysource


Field maps
==========

Interpolated field maps
-----------------------

.. autoclass:: xfields.fieldmaps.TriLinearInterpolatedFieldMap
    :members:
    :undoc-members:
    :member-order: bysource

Solvers
=======

FFT solvers
-----------

.. autoclass:: xfields.solvers.FFTSolver3D
    :members:
    :undoc-members:
    :member-order: bysource

.. autoclass:: xfields.solvers.FFTSolver2p5D
    :members:
    :undoc-members:
    :member-order: bysource
    :inherited-members:


BiGaussian field maps
---------------------

.. autoclass:: xfields.fieldmaps.BiGaussianFieldMap
    :members:
    :undoc-members:
    :member-order: bysource