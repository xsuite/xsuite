===========
Collimation
===========

Loss location refinement
========================

In Xtrack simulations particles are lost at defined aperture elements (e.g.
:class:`xtrack.LimitRect`, :class:`xtrack.LimitEllipse`, :class:`xtrack.LimitRectEllipse`,
:class:`xtrack.LimitPolygon`). A more accurate estimate of the loss locations can be
obtained after the tracking is finished using the
:class:`xtrack.LossLocationRefinement` tool . The tool builds
an interpolated aperture model between the aperture elements and backtracks the
particles in order to identify the impact point. The following example illustrates
how to use this feature.

See also: :class:`xtrack.LossLocationRefinement`

.. literalinclude:: generated_code_snippets/loss_location_refinement.py
   :language: python

.. figure:: figures/loss_location_refinement.png
    :width: 85%
    :align: center

    Generated transition between the defined apertures. Red dots represent the
    location of the particle-loss events. `See the code generating the image.
    <https://github.com/xsuite/xtrack/blob/main/examples/collimation/
    001_loss_location_refinement.py>`_

Beam interaction (generation of secondary particles)
====================================================

Xtrack includes an interface to ease the modeling of beam-matter interaction
(collimators, beam-gas, collisions with another beam),
including the loss of the impacting particles and the production of secondary
particles, which need to be tracked together with the surviving beam.
Such interface can be used to create a link with other programs for the modeling
of these effects,  e.g. GEANT, FLUKA, K2, GuineaPig.

The interaction is defined as an object that provides a ``.interact(particles)``
method, which sets to zero or negative the ``state`` flag for the particles that are lost and
returns a dictionary with the coordinates of the secondary particles that are
emitted. The interaction process is embedded in one or multiple
:class:`xtrack.BeamInteraction` beam elements that can be included in Xtrack line.

This is illustrated by the following example:

.. literalinclude:: generated_code_snippets/beam_interaction.py
   :language: python