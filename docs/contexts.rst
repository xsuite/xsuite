Contexts
=========

Xfields supports different plaforms allowing the exploitation of different kinds of hardware (CPUs and GPUs).
A context is initialized by instanciating objects from one of the context classes, which is then passed to the other Xfields components.
Contexts are interchangeable as they expose the same API.

Three contexts are presently available:

 - The :ref:`Cupy context<cupy_context>`, based on `cupy`_-`cuda`_ to run on NVidia GPUs
 - The :ref:`Pyopencl context<pyopencl_context>`, bases on `PyOpenCL`_, to run on CPUs or GPUs throught PyOPENCL library.
 - The :ref:`CPU context<cpu_context>`, to use conventional CPUs

The corresponfig API is described in the following subsections.

.. _cupy: https://cupy.dev
.. _cuda: https://developer.nvidia.com/cuda-zone
.. _PyOpenCL: https://documen.tician.de/pyopencl/


.. _cupy_context:

Cupy context
-------------

.. autoclass:: xobjects.context.ContextCupy
    :members:
    :undoc-members:
    :member-order: bysource
    :inherited-members:

.. _pyopencl_context:

PyOpenCL context
-----------------
.. autoclass:: xobjects.context.ContextPyopencl
    :members:
    :undoc-members:
    :member-order: bysource
    :inherited-members:


.. _cpu_context:

CPU context
------------

.. autoclass:: xobjects.context.ContextCpu
    :members:
    :undoc-members:
    :member-order: bysource
    :inherited-members:
