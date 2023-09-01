============
Beam-beam interactions
============

Weak-strong 2D
==============

The example below shows how to introduce a 2D beam-beam element and perform few studies based on tracking. The 2D beam-beam element gives a kick based on the Basseti-Erskine formula neglecting any longitudinal varitations of the beam-beam force.

.. literalinclude:: generated_code_snippets/beambeamws.py
   :language: python


Weak-strong 3D
==============

The 3D beam-beam element can be used similarly, replacing the instanciation of the beam-beam element as in the example below. This element takes into account longitudinal variations of the beam-beam force (hourglass, crossing angle) based on a longitudinal slicing of the beam (Hirata's method).

.. code-block:: python

   n_slices = 21
   slicer = xf.TempSlicer(n_slices=n_slices, sigma_z=sigma_z, mode="shatilov")
   bbeam = xf.BeamBeamBiGaussian3D(
               _context=context,
               other_beam_q0 = particles.q0,
               phi = 500.0E-2,
               alpha = 0.0)

Strong-strong 2D (soft-Gaussian)
================================

.. code-block:: python

    beam-beam

Strong-strong 3D (soft-Gaussian)
================================

.. code-block:: python

    beam-beam

Poisson Solver
==============
