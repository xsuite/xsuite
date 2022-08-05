========================================
Definition a new beam element for Xtrack
========================================

.. contents:: Table of Contents
    :depth: 4

In this page we illustrate how to introduce a new beam element in Xtrack.
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



Definition of the tracking function
===================================

Accessing beam-element data from C
----------------------------------

The class definition from previous section automatically generates a set of functions (API) to access and manipulate in C the data spcified in ``_xofields``.
The C API for the defined class can be inspected as follows:

.. code-block:: python

    source, kernels, cdefs = SRotation.XoStruct._gen_c_api()
    print(source)

By printing source we can see that C methods are available to set, get and get a pointer to the fields specified in ``_xofields``:

.. code-block:: c

    /*gpufun*/ double SRotationData_get_cos_z(const SRotationData/*restrict*/ obj);
    /*gpufun*/ void SRotationData_set_cos_z(SRotationData/*restrict*/ obj, double value);
    /*gpufun*/ /*gpuglmem*/double* SRotationData_getp_cos_z(SRotationData/*restrict*/ obj);

    /*gpufun*/ double SRotationData_get_sin_z(const SRotationData/*restrict*/ obj);
    /*gpufun*/ void SRotationData_set_sin_z(SRotationData/*restrict*/ obj, double value);
    /*gpufun*/ /*gpuglmem*/double* SRotationData_getp_sin_z(SRotationData/*restrict*/ obj);

Note the annotations ``/*gpufun*/`` that indicates that these are device functions on GPU and ``/*gpuglmem*/`` that indicates that the annotated pointer refers to the GPU global memory space.

These methods can be used to write a C header file containing the tracking code for the beam element.
The method takes two arguments, the element data in a data type called ``<ElementName>Data``, i.e. ``SRotationData`` in our example and a ``LocalParticle`` which is associated to methods to set and and get the particle coordinates.
The ``LocalParticle`` represents one particle of the particle set provided to the simulation. On CPU it is possible to change the particle pointed by the local particle by changing the index ``ipart``.

Writing the tracking code
-------------------------

For our example beam elements the tracking code can be writte as follows:

.. code-block:: c

    #ifndef XTRACK_SROTATION_H
    #define XTRACK_SROTATION_H

    /*gpufun*/
    void SRotation_track_local_particle(SRotationData el, LocalParticle* part0){


        double const sin_z = SRotationData_get_sin_z(el);
        double const cos_z = SRotationData_get_cos_z(el);

        //start_per_particle_block (part0->part)

            double const x  = LocalParticle_get_x(part);
            double const y  = LocalParticle_get_y(part);
            double const px = LocalParticle_get_px(part);
            double const py = LocalParticle_get_py(part);

            double const x_hat  =  cos_z * x  + sin_z * y;
            double const y_hat  = -sin_z * x  + cos_z * y;

            double const px_hat =  cos_z * px + sin_z * py;
            double const py_hat = -sin_z * px + cos_z * py;


            LocalParticle_set_x(part, x_hat);
            LocalParticle_set_y(part, y_hat);

            LocalParticle_set_px(part, px_hat);
            LocalParticle_set_py(part, py_hat);

        //end_per_particle_block

    }

    #endif

You can note in the code above the ``/*gpufun*/`` annotation specifying that the function is to be executed on the device for the GPU contexts.

The annotations ```//start_per_particle_block``` and ```//end_per_particle_block``` map part0 to part and introduce a loop over the particle when needed (i.e. for the CPU contexts). Parallelization over CPU cores is also applied if this is set in  the context.

Once ready the code needs to be associated to the class. This is done with the following instruction:

.. code-block:: python

    from pathlib import Path

    SRotation.XoStruct.extra_sources = [Path('./srotation.h')]

Data recording in beam elements
===============================

.. contents:: Table of Contents
    :depth: 3

Introduction
------------

Xsuite beam elements can store data in dedicated data structures allocated in a
specific io_buffer handled by the tracker. This feature is illustrated in the
following three examples, which cover the storage of data into one or multiple
data tables for a given element type and the usage of data recording for elements
used within a tracker and in standalone mode.

Recording of an individual table
--------------------------------

.. literalinclude:: generated_code_snippets/internal_record.py
   :language: python

Recording of multiple tables
----------------------------

.. literalinclude:: generated_code_snippets/internal_multirecord.py
   :language: python

Internal record for elements used in standalone mode
----------------------------------------------------

.. literalinclude:: generated_code_snippets/internal_record_standalone.py
   :language: python
