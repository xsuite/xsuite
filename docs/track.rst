=====
Track
=====

.. contents:: Table of Contents
    :depth: 3

Tracking particles with Xsuite
==============================

The tracking of particles through a beam line can be simulated using the
:meth:`xtrack.Line.track` method of the :class:`xtrack.Line` class. This is
illustrated in the following example:

.. literalinclude:: generated_code_snippets/track.py
    :language: python

.. include:: dynamic_aperture.rst

.. include:: particles_monitor.rst

.. include:: optimize_for_tracking.rst

.. include:: freeze_longitudinal.rst

.. include:: time_dependent_knobs.rst

.. include:: fast_lattice_changes.rst

.. include:: exciter.rst

