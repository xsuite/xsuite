=====
Twiss
=====

Xtrack provides a twiss method associated to the tracker that can be used to
obtain the twiss parameters and other quantities like tunes, chromaticities,
slip factor, etc. This is illustrated in the following example. For a complete
description of all available options and output quantities, please refer to the
:meth:`xtrack.Line.twiss` method documentation.

.. literalinclude:: generated_code_snippets/twiss.py
   :language: python

.. figure:: figures/twiss.png
    :width: 75%
    :align: center

    Twiss functions and accelerator parameters as obtained by Xtrack twiss.
    `See the full code generating the image. <https://github.com/xsuite/xtrack/
    blob/main/examples/twiss/000_twiss.py>`_


