Definition of the tracking function
===================================

Accessing beam-element data from C
----------------------------------

The class definition from previous section automatically generates a set of functions (API) to access and manipulate in C the data spcified in ``_xofields``.
The C API for the defined class can be inspected as follows:

.. code-block:: python

    source = SRotation._XoStruct._gen_c_api().source
    print(source)

By printing source we can see that C methods are available to set, get and get a pointer to the fields specified in ``_xofields``:

.. code-block:: c

    /*gpufun*/ double SRotationData_get_cos_z(const SRotationData/*restrict*/ obj);
    /*gpufun*/ void SRotationData_set_cos_z(SRotationData/*restrict*/ obj, double value);
    /*gpufun*/ /*gpuglmem*/double* SRotationData_getp_cos_z(SRotationData/*restrict*/ obj);

    /*gpufun*/ double SRotationData_get_sin_z(const SRotationData/*restrict*/ obj);
    /*gpufun*/ void SRotationData_set_sin_z(SRotationData/*restrict*/ obj, double value);
    /*gpufun*/ /*gpuglmem*/double* SRotationData_getp_sin_z(SRotationData/*restrict*/ obj);

The generated API source currently still uses legacy magic comments such as
``/*gpufun*/``, ``/*gpuglmem*/`` and ``/*restrict*/``. For new handwritten C
code, however, the preferred API is to include the Xobjects/Xtrack headers and
use macros such as ``GPUFUN``, ``GPUGLMEM`` and ``RESTRICT``. This lets the
compiler catch typos instead of silently ignoring misspelled magic comments.

These methods can be used to write a C header file containing the tracking code for the beam element.
The method takes two arguments, the element data in a data type called ``<ElementName>Data``, i.e. ``SRotationData`` in our example and a ``LocalParticle`` which is associated to methods to set and and get the particle coordinates.
The ``LocalParticle`` represents one particle of the particle set provided to the simulation.

Writing the tracking code
-------------------------

For our example beam elements the tracking code can be written as follows:

.. code-block:: c

    #ifndef XTRACK_SROTATION_H
    #define XTRACK_SROTATION_H

    #include "xtrack/headers/track.h"

    GPUFUN
    void SRotation_track_local_particle(SRotationData el, LocalParticle* part0){

        double const sin_z = SRotationData_get_sin_z(el);
        double const cos_z = SRotationData_get_cos_z(el);

        START_PER_PARTICLE_BLOCK(part0, part);

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

        END_PER_PARTICLE_BLOCK;

    }

    #endif

The ``GPUFUN`` macro specifies that the function is to be executed on the device for GPU contexts. It is defined in ``xobjects/headers/common.h``; for tracking code, including ``xtrack/headers/track.h`` is usually the most convenient choice because it includes ``xobjects/headers/common.h`` and also defines the particle-tracking block macros.

The ``START_PER_PARTICLE_BLOCK(part0, part)`` and ``END_PER_PARTICLE_BLOCK`` macros map ``part0`` to ``part`` and introduce a loop over the particles when needed (i.e. for the CPU contexts). Parallelization over CPU cores is also applied if this is set in the context.

Once ready the code needs to be associated to the class. This is done with the following instruction:

.. code-block:: python

    from pathlib import Path

    import xobjects as xo
    import xtrack as xt

    class SRotation(xt.BeamElement):

        _xofields={
            'cos_z': xo.Float64,
            'sin_z': xo.Float64,
            }

        _extra_c_sources = [Path('./srotation.h')]
