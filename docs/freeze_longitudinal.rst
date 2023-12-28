Freeze longitudinal coordinates
===============================

In certain studies, it is convenient to track particles updating only the
transverse coordinates, while keeping the longitudinal coordinates fixed (frozen).
Xsuite offers the possibility to freeze the longitudinal coordinates within a
single method or changing the state of the Line, as illustrated in the following
sections.

Freezing longitudinal when calling methods
------------------------------------------

The ``Line.twiss`` and ``Line.track`` can work with frozen longitudinal
coordinates. This is done by setting the ``freeze_longitudinal`` argument to
``True``, as shown in the following example:

.. literalinclude:: generated_code_snippets/freeze_individual_methods.py
   :language: python

Freezing longitudinal coordinates within a ``with`` block
---------------------------------------------------------

A context manager is also available to freeze the longitudinal coordinates within
a ``with`` block. The normal tracking mode, updating the longitudinal
coordinates, is automatically restored when exiting the ``with`` block, as it is
illustrated in the following example:

.. literalinclude:: generated_code_snippets/freeze_freeze_context_manager.py
   :language: python

Freezing longitudinal coordinates with Line method
---------------------------------------------------

The ``xtrack.Line`` class provides a method called ``freeze_longitudinal()``
to explicitly freeze the longitudinal coordinates. The normal tracking mode,
updating the longitudinal coordinates, can be restored by calling
``freeze_longitudinal(False)``. This is illustrated in the following example:

.. literalinclude:: generated_code_snippets/freeze_unfreeze_explicit.py
   :language: python



