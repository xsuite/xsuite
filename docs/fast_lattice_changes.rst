====================
Fast lattice changes
====================

Changes to beam line parameters can be applied using the python interface. For
example to change the strenght of a quadrupole one can use the following.

.. code-block:: python

    line['myquad'].knl[1] = 0.5

This approach is fine when the change is applied to a small number of elements,
but can introduce a significant overhead on the simulation time when the number of
changes is very large. For these cases it is possible to use an ``xtrack.CustomSetter``
to perform the changes in a more efficient way. The ``CustomSetter`` stores the
memory addresses of the quantities to be changed and performs the changes with a single
compiled kernel, using multithreading when allowed by the context.

The following examples show how to use the ``CustomSetter`` to apply a sinusoidal
ripple to the strength of several quadropoles of a synchrotron.

.. literalinclude:: generated_code_snippets/ripple.py
   :language: python