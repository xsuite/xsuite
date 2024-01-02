=====
Twiss
=====

Xtrack provides a twiss method associated to the line that can be used to
obtain the twiss parameters and other quantities like tunes, chromaticities,
slip factor, etc. This is illustrated in the following example. For a complete
description of all available options and output quantities, please refer to the
:meth:`xtrack.Line.twiss` method documentation.

.. contents:: Table of Contents
    :depth: 3

Basic usage (ring)
==================

.. literalinclude:: generated_code_snippets/twiss.py
   :language: python

.. figure:: figures/twiss.png
    :width: 75%
    :align: center

    Twiss functions and accelerator parameters as obtained by Xtrack twiss.

Inspecting twiss output
=======================

The twiss table has several access options as illustrated in the following
example.

.. literalinclude:: generated_code_snippets/table_slicing.py
   :language: python

4d method
=========

When the RF cavities are disabled or not included in the lattice or when the
longitudinal motion is artificially frozen, the one-turn matrix of the line is
singular, and it is no possible to use the standard method for the twiss
calculation and to generate particles distributions matched to the lattice.
In these cases, the "4d" method can be used, as illustrated in the following
examples:

.. literalinclude:: generated_code_snippets/method_4d.py
   :language: python

Off-momentum twiss
==================

The 4d mode of the twiss can be used providing in input the initial momentum.
Such a feature can be used to measure the non linear momentum detuning of the
accelerator as shown in the following example:

.. literalinclude:: generated_code_snippets/tune_vs_delta.py
   :language: python

.. figure:: figures/twiss_vs_delta.png
    :width: 80%
    :align: center

Twiss with "initial" conditions
===============================

The twiss calculation can be performed with initial conditions provided by the
users or extracted from an existing twiss table, as illustrated in the
following example:

.. literalinclude:: generated_code_snippets/twiss_range.py
   :language: python

.. figure:: figures/twiss_range.png
    :width: 75%
    :align: center

    Result of all twiss calculations with initial conditions shown in the
    example above.


Periodic twiss on a portion of a line
=====================================

The twiss method can also be used to find the periodic solution for a portion of
a beam line, as illustrated in the following example:

.. literalinclude:: generated_code_snippets/twiss_range_periodic.py
   :language: python

.. figure:: figures/twiss_periodic.png
    :width: 75%
    :align: center

    Result of the twiss with periodic boundary conditions.

Twiss with synchrotron radiation
================================

Bla


Beam sizes from twiss table
===========================

Bla

Particles normalized coordinates
====================================

The twiss table holds the information to convert particle physical coordinates
into normalized coordinates. This can be done with the method
``get_normalized_coordinates`` as illustrated in the following example:

.. literalinclude:: generated_code_snippets/compute_norm_coordinates.py
   :language: python

Output in the reverse reference frame
=====================================

Bla

Twiss defaults
==============

Bla