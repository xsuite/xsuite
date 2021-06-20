=========================
Define a new beam element
=========================

.. code-block:: python

    import xobjects as xo

    class SRotationData(xo.Struct):
        cos_z = xo.Float64
        sin_z = xo.Float64


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
