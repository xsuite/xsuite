==============
Tune footprint
==============

The Line class provides a method to compute and optionally plot the tune footprint
as illustrated in the following example.

Basic usage
===========

See also: :meth:`xtrack.Line.get_footprint`

.. literalinclude:: generated_code_snippets/footprint.py
   :language: python

.. figure:: figures/footprint_polar.png
    :width: 80%
    :align: center

    Footprints produced with a polar grid.

.. figure:: figures/footprint_unif_action.png
    :width: 80%
    :align: center

    Footprints produced with a uniform grid in action space.

Linear rescale on knobs
=======================

In some cases the effects introducing the detuning also introduce other effects
(e.g. coupling, or non-linear resonances) that disturb the particles tune
measurement. In this case it is possible to rescale quantify the detuning for
smaller values of the knobs associate to the detuning effects and rescale to
the actual value of the knob. This can be done by the `linear_rescale_on_knobs`
option as illustrated in the following example for a case where the detuning
with amplitude is introduced by beam-beam interactions.

See also: :meth:`xtrack.Line.get_footprint`

.. literalinclude:: generated_code_snippets/footprint_with_bb.py
   :language: python

.. figure:: figures/footprint_bb_no_rescale.png
    :width: 80%
    :align: center

    Footprints produced without rescaling beam-beam knob.

.. figure:: figures/footprint_bb_with_rescale.png
    :width: 80%
    :align: center

    Footprints produced with rescaling beam-beam knob.

