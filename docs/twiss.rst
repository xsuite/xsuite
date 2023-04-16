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

Basic usage
===========

.. literalinclude:: generated_code_snippets/twiss.py
   :language: python

.. figure:: figures/twiss.png
    :width: 75%
    :align: center

    Twiss functions and accelerator parameters as obtained by Xtrack twiss.
    `See the full code generating the image. <https://github.com/xsuite/xtrack/
    blob/main/examples/twiss/000_twiss.py>`_

Access option of twiss table
============================

The twiss table has several access options as illustrated in the following
example. 

.. literalinclude:: generated_code_snippets/table_slicing.py
   :language: python

