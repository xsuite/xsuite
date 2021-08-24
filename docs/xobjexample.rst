=========================================
 Multiplatform programming with xobjects
=========================================

Definition of a simple data structure class
===========================================

.. code-block:: python

    import xobjects as xo

    class DataStructure(xo.Struct):
        a = xo.Float64[:]
        b = xo.Float64[:]
        c = xo.Float64[:]
        s = xo.Float64


Allocation of a data object on the GPU
======================================

.. code-block:: python

    ctx = xo.ContextCpu()
    # ctx = xo.ContextCupy() # for NVIDIA GPUs

    obj = DataStructure(_context=ctx,
                        a=[1,2,3], b=[4,5,6], c=[0,0,0],
                        d=0)

The object is accessible in read/write directly from python:

.. code-block:: python

    print(obj.a[2]) # gives: 3
    a[2] = 10
    print(obj.a[2]) # gives: 10

Array


