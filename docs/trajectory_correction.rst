======================================
Closed orbit and trajectory correction
======================================

Xsuite offers the possibility to correct the beam closed orbit for circular
accelerators and the beam trajectory in transfer lines. The correction is
performed using a linearized response matrix, which is built from a twiss table.
The correction is computed using the singular value decomposition (SVD) of the
response matrix or the MICADO algorithm.

For the case of rings, in order to proceed with the correction, is in necessary
to successfully measure the closed orbit to correct. In certain cases, when
strong lattice perturbations are present (e.g. field errors or large element
misalignments), the closed orbit search might fail. In such cases, the user can
use a threading capability to perform a first correction of the trajectory,
after which the closed orbit search can be performed.

The following sections illustrate different usages of the trajectory correction
module.

.. contents:: Table of Contents
    :depth: 3


Basic usage
===========

See also: :meth:`xtrack.Line.correct_trajectory`

.. literalinclude:: generated_code_snippets/closed_orbit_correction_basic.py
    :language: python

.. figure:: figures/orbit_correction_basic.png
    :width: 80%
    :align: center

    Bla bla bla



MICADO correction
=================

See also: :meth:`xtrack.Line.correct_trajectory`

.. literalinclude:: generated_code_snippets/closed_orbit_correction_micado.py
    :language: python

.. figure:: figures/orbit_correction_micado.png
    :width: 80%
    :align: center

    Bla bla bla


Customized correction
=====================

See also: :meth:`xtrack.Line.correct_trajectory`

.. literalinclude:: generated_code_snippets/closed_orbit_correction_customize.py
   :language: python

.. figure:: figures/orbit_correction_svalues.png
    :width: 80%
    :align: center

    Bla bla bla

.. figure:: figures/orbit_correction_custom.png
    :width: 80%
    :align: center

    Bla bla bla


Threading
=========

See also: :meth:`xtrack.Line.correct_trajectory`

.. literalinclude:: generated_code_snippets/closed_orbit_correction_thread.py
   :language: python

.. figure:: figures/orbit_correction_thread.png
    :width: 80%
    :align: center

    Bla bla bla

Trajectory correction for transfer lines
========================================

See also: :meth:`xtrack.Line.correct_trajectory`

.. literalinclude:: generated_code_snippets/transfer_line_correction.py
    :language: python

.. figure:: figures/orbit_correction_ti2.png
    :width: 80%
    :align: center

    Bla bla bla

