Contexts
=========

Xsuite supports different platforms allowing the exploitation of different kinds of hardware (CPUs and GPUs).
A context is initialized by instantiating objects from one of the context classes available in Xobjects, which is then passed to the other Xsuite components (see example in :doc:`Getting Started Guide <gettingstarted>`).
Contexts are interchangeable as they expose the same API.
Custom kernel functions can be added to the contexts. General source code with annotations can be provided to define the kernels, which is then automatically specialized for the chosen platform (see :doc:`dedicated section <autogeneration>`).

Three contexts are presently available:

 - The :ref:`Cupy context<cupy_context>`, based on `cupy`_-`cuda`_ to run on NVIDIA GPUs
 - The :ref:`Pyopencl context<pyopencl_context>`, based on `PyOpenCL`_, to run on CPUs or GPUs through the PyOpenCL library.
 - The :ref:`CPU context<cpu_context>`, to use conventional CPUs

The corresponding API is described in the following subsections.

.. _cupy: https://cupy.dev
.. _cuda: https://developer.nvidia.com/cuda-zone
.. _PyOpenCL: https://documen.tician.de/pyopencl/


.. _cupy_context:

Cupy context
-------------

.. autoclass:: xobjects.ContextCupy
    :members:
    :undoc-members:
    :member-order: bysource
    :inherited-members:

.. _pyopencl_context:

PyOpenCL context
-----------------
.. autoclass:: xobjects.ContextPyopencl
    :members:
    :undoc-members:
    :member-order: bysource
    :inherited-members:


.. _cpu_context:

CPU context
------------

.. autoclass:: xobjects.ContextCpu
    :members:
    :undoc-members:
    :member-order: bysource
    :inherited-members:
