Fast lattice changes
====================

Changes to beam line parameters can be applied using the python interface. For
example to change the strength of a quadrupole one can use the following.

.. code-block:: python

    line['myquad'].knl[1] = 0.5

This approach works well when the change is applied to a small number of elements,
but can introduce a significant overhead on the simulation time when the number of
changes is very large. For these cases it is possible to use an :class:`xtrack.MultiSetter`
to perform the changes in a more efficient way. The ``MultiSetter`` stores the
memory addresses of the quantities to be changed and performs the changes with a single
compiled kernel, using multithreading when allowed by the context.

The following example shows how to use the ``MultiSetter`` to apply a sinusoidal
ripple to the strength of several quadropoles of a synchrotron.

See also: :class:`xtrack.MultiSetter`

.. literalinclude:: generated_code_snippets/ripple.py
   :language: python