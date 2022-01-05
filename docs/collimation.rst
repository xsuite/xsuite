===========
Collimation
===========

Loss location refinement
========================

In Xtrack simulations particles are lost at defined aperture elements (e.g.
:class:`xtrack.LimitRect`, :class:`xtrack.LimitEllipse`, :class:`xtrack.LimitRectEllipse`,
:class:`xtrack.LimitPolygon`). A more accurate estimate of the loss locations can be
obtained using the :class:`xtrack.LossLocationRefinement` tool. The tool builds
an interpolated aperture model between the aperture elements and backtracks the
particles in order to find the impact point. The following example illustrates how
to use this feature.

.. literalinclude:: generated_code_snippets/loss_location_refinement.py
   :language: python

.. figure:: figures/loss_location_refinement.png
    :width: 85%
    :align: center

    Generated transition between the defined apertures. Red dots represent the
    location of the particle-loss events.

Beam interaction (generation of secondary particles)
====================================================

Xtrack includes an interface to ease the modeling of beam-matter interaction,
including the loss of the impacting particles and the production of secondary
particles, which need to be tracked together with the surviving beam.

.. literalinclude:: generated_code_snippets/beam_interaction.py
   :language: python