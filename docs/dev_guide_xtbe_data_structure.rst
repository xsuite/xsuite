Introduction
============

In this page we illustrate how to introduce a new beam element compatible with Xtrack.
We will use for illustration the "SRotation" element which performs the following transformation of the particle coordinates:

 - x  =  cos(theta) * x + sin(theta) * y
 - y  = -sin(theta) * x + cos(theta) * y
 - px  =  cos(theta) * px + sin(theta) * py
 - py  = -sin(theta) * px + cos(theta) * py

The element is fully described by the rotation angle theta.


Definition of the data structure
================================

New beam elements are defined as python classes inheriting from the class ``BeamElement`` of xtrack.
In each element class we define a dictionary called ``_xofields``, which specifies names and types of the data to be made accessible to the C tracking code.

Although our beam element is defined by the single parameter (theta), it is convenient to store the quantities sin(theta) and cos(theta) to avoid recalculating them multiple times:

.. code-block:: python

    import xobjects as xo
    import xtrack as xt

    class SRotation(xt.BeamElement):

        _xofields={
            'cos_z': xo.Float64,
            'sin_z': xo.Float64,
            }

Allocation of beam elements on CPU or GPU
-----------------------------------------

Objects of the defined class can be allocated as follows:

.. code-block:: python

    srot = SRotation(sin_z=1., cos_z=0)

By default the objects are allocated in the CPU memory. They can be allocated in the memory of a GPU by providing an xobject context or buffer. For example:

.. code-block:: python

    ctx = xo.ContextCupy()

    # Object allocated on the GPU
    srot = SRotation(sin_z=1., cos_z=0, _context=ctx)

Python access to beam-element data
----------------------------------

The fields specified in ``_xofields`` are automatically exposed as attributes of the objects that can be read and set with the standard python syntax, also if the object is allocated on the GPU:

.. code-block:: python

    print(srot.sin_z)
    # returns 1.0

    srot.sin_z = 0.9

    print(srot.sin_z)
    # returns 0.9


Additional attributes and methods can be added to the class. If the ``__init__`` method is defined, the ``__init__`` of the parent class needs to be called to initialize the ``xobject``, i.e. the data structure accessible from the C code.

Custom ``__init__`` method
--------------------------

In our example we want to initialize the object providing the rotation angle and not its sine and cosine and we introduce a property called ``angle`` that allows setting or getting the angle from the stored sine and cosine. This can be done as follows:

.. code-block:: python

    import numpy as np

    import xobjects as xo
    import xtrack as xt

    class SRotation(BeamElement):

        def __init__(self, angle=0, **kwargs):
            anglerad = angle / 180 * np.pi
            kwargs['cos_z']=np.cos(anglerad)
            kwargs['sin_z']=np.sin(anglerad)
            super().__init__(**kwargs)

        @property
        def angle(self):
            return np.arctan2(self.sin_z, self.cos_z) * (180.0 / np.pi)

        @angle.setter
        def angle(self, value):
            anglerad = value / 180 * np.pi
            self.cos_z = np.cos(anglerad)
            self.sin_z = np.sin(anglerad)

