======================
Match twiss parameters
======================

The Xtrack Line class provides a match method that allows to match the twiss parameters of a
to adjust knobs attached to the line in order to obtain desired values
in the twiss results (see also :meth:`xtrack.Line.match`).
This feature is illustrated in the following examples.

.. contents:: Table of Contents
    :depth: 3

Match tunes and chromaticities
------------------------------

.. literalinclude:: generated_code_snippets/match_tune_chroma.py
   :language: python

Match an orbit bump
-------------------

The match mathod can also be used with targets at specific locations in the line.

.. literalinclude:: generated_code_snippets/match_4c_bump.py
   :language: python

.. figure:: figures/orbit_bump.png
    :width: 99%
    :align: center

    The matched orbit bump. The green vertical lines mark the range used For
    the matching. The red line is the point where the position and angle are
    imposed. The grey lines mark the location of the used orbit correctors.
    `See the full code generating the image. <https://github.com/xsuite/xtrack/
    blob/main/examples/twiss/003b_match_4c_bump.py>`_