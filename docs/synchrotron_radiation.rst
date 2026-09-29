=====================
Synchrotron radiation
=====================

.. contents:: Table of Contents
    :depth: 3

Twiss and track with radiation
==============================

The following example illustrates the use of synchrotron radiation in Xsuite.
Explanations can be found in the comments interleaved in the code. For the
considered case, the lattice is loaded from a MAD-X thick sequence and converted
using the ``MAKETHIN`` command of MAD-X to obtain a thin sequence compatible
with Xsuite.

See also: :meth:`xtrack.Line.configure_radiation`

.. literalinclude:: generated_code_snippets/radiation.py
   :language: python

.. include:: tapering.rst

