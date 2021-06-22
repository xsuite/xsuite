=============================
Definition a new beam element
=============================

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

Although our beam element is defined by the single parameter (theta), it is convenient to store the quantities sin(theta) and cos(theta) to avoid recalculating them multiple times.

.. code-block:: python

    import xobjects as xo
    import xtrack as xt

    class SRotation(BeamElement):

        _xofields={
            'cos_z': xo.Float64,
            'sin_z': xo.Float64,
            }

Objects of the defined class can be allocated as follows:

.. code-block:: python

    srot = SRotation(sin_z=1., cos_z=0)

By default the objects are allocated in the CPU memory. They can be allocated in the memory of a GPU by providing an xobject context or buffer:

.. code-block:: python

    ctx = xo.ContextCupy()

    # Object allocated on the GPU
    srot = SRotation(sin_z=1., cos_z=0, _context=ctx)

The fields specified in ``_xofields`` are automatically exposed as attributes of the objects that can be accessed with the standard python syntax, also if the object is allocated on the GPU:

.. code-block:: python

    print(srot.sin_z)
    # returns 1.0

    srot.sin_z = 0.9

    print(srot.sin_z)
    # returns 0.9




        def __init__(self, angle=0, **nargs):
            anglerad = angle / 180 * np.pi
            nargs['cos_z']=np.cos(anglerad)
            nargs['sin_z']=np.sin(anglerad)
            super().__init__(**nargs)

        @property
        def angle(self):
            return np.arctan2(self.sin_z, self.cos_z) * (180.0 / np.pi)

        @angle.setter
        def angle(self, value):
            anglerad = value / 180 * np.pi
            self.cos_z = np.cos(anglerad)
            self.sin_z = np.sin(anglerad)



Old stuff
=========

The first step consists in defining the data structure associated to the new beam element. Such data structure will be accessible to the C code implementing the beam elements.
Although our beam element is defined by the single parameter (theta), it is convenient to store the quantities sint(theta) and cos(theta) to avoid recalculating them multiple times.
The data structure is defined as an ``xobjects`` structure as follows:

.. code-block:: python

    import xobjects as xo

    class SRotationData(xo.Struct):
        cos_z = xo.Float64
        sin_z = xo.Float64


Definition of the high-level python class
=========================================

A high-level python class can be defined on top of the data structure exposed to the C code. This is done with the ``dress_element`` functionality.

If the field names to build the high-level python object are the same 

.. code-block:: python

    import numpy as np
    from xtrack import dress_element

    class SRotation(dress_element(SRotationData)):

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


.. code-block:: c

    #ifndef XOBJ_TYPEDEF_SRotationData
    typedef /*gpuglmem*/ struct SRotationData_s * SRotationData;
    #define XOBJ_TYPEDEF_SRotationData
    #endif

    /*gpufun*/ double SRotationData_get_cos_z(const SRotationData/*restrict*/ obj);
    /*gpufun*/ void SRotationData_set_cos_z(SRotationData/*restrict*/ obj, double value);
    /*gpufun*/ /*gpuglmem*/double* SRotationData_getp_cos_z(SRotationData/*restrict*/ obj);

    /*gpufun*/ double SRotationData_get_sin_z(const SRotationData/*restrict*/ obj);
    /*gpufun*/ void SRotationData_set_sin_z(SRotationData/*restrict*/ obj, double value);
    /*gpufun*/ /*gpuglmem*/double* SRotationData_getp_sin_z(SRotationData/*restrict*/ obj);


.. code-block:: c

    #ifndef XTRACK_SROTATION_H
    #define XTRACK_SROTATION_H

    /*gpufun*/
    void SRotation_track_local_particle(SRotationData el, LocalParticle* part){

        int64_t const n_part = LocalParticle_get_num_particles(part); 
        for (int ii=0; ii<n_part; ii++){ //only_for_context cpu_serial cpu_openmp
        part->ipart = ii;            //only_for_context cpu_serial cpu_openmp

            double const sin_z = SRotationData_get_sin_z(el);
            double const cos_z = SRotationData_get_cos_z(el);

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
        } //only_for_context cpu_serial cpu_openmp

    }

    #endif

.. code-block:: python

    SRotationData.extra_sources = [
            _pkg_root.joinpath('beam_elements/elements_src/srotation.h')]