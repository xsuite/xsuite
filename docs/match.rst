=====
Match
=====

The Xtrack Line class provides a match method that allows using a numerical optimizer
to adjust knobs attached to the line in order to obtain desired values
in the twiss results (or as a result of other user-defined actions).

.. contents:: Table of Contents
    :depth: 3

Basic usage
-----------

The numerical optimizer can be used calling the method :meth:`xtrack.Line.match`.
The optimization is define by a set of :ref:`Vary and Target objects  <vary_target_label>` defining the
knobs to be varied and the targets to be matched. The following example shows
how to match the tunes and chromaticities of a ring.


.. literalinclude:: generated_code_snippets/match_basic.py
   :language: python

Interactive matching
--------------------

The match method can also be used in an interactive way passing `solve=False`
to the :method:`xtrack.Line.match`. In this case an :class:`xdeps.Optimize` object
is returned that can be used to interactively drive the optimization process,
by enabling/disabling knobs and targets, changing target values and tolerances,
controlling the number of optimization steps. This is illustrated in the
following example.

.. literalinclude:: generated_code_snippets/match_interactive.py
   :language: python

Match an orbit bump
-------------------

See also :meth:`xtrack.Line.match`

The match method can also be used with targets at specific locations in the line.

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