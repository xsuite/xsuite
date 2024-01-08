Multisetters
------------

When the number of beam elements to be changed is very large, this can introduce
a significant overhead on the simulation time. For these cases it is possible to use
the :class:`xtrack.MultiSetter` class, to perform the changes in a more efficient way,
bypassing the expressions and acting directly on the element properties.
Furthermore, the ``MultiSetter`` stores the
memory addresses of the quantities to be changed and performs the changes with a single
compiled kernel, using multithreading when allowed by the context.

The following example shows how to use the ``MultiSetter`` to apply a sinusoidal
ripple to the strength of several quadropoles of a synchrotron.

See also: :class:`xtrack.MultiSetter`

.. literalinclude:: generated_code_snippets/ripple.py
   :language: python