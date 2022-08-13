
=========================
Data management in Xsuite
=========================

Done through the Xobjects package

Beam elements and Particles objects are xobjects Hybrid classes.

They contain along with standard python attributes and methods also an "xobject"
that can be optionally stored on GPU and made accessible to the C code used
in the implementation.

The set of attibutes accessible in C and the corresponding types can be found in
```_xofields``` dictionary attached to the class for example:

.. code-block:: python

    xtrack.Multipole._xofields

    # contains:
    # {'order': Int64,
    #  'inv_factorial_order': Float64,
    #  'length': Float64,
    #  'hxl': Float64,
    #  'hyl': Float64,
    #  'radiation_flag': Int64,
    #  'knl': <array ArrNFloat64>,
    #  'ksl': <array ArrNFloat64>,
    #  '_internal_record_id': <struct RecordIdentifier>}

Each instance of the class contains an xobject storint the corresponding data.

For example:

.. code-block:: python

    m = xtrack.Multipole(knl=[1,2,3])

    m._xobject.knl # contains [1,2,3]

All attributes of the xobject are automatically exposed as attributes of the beam element.
For example, ``m._xobject.length`` is the same as ``m.length``.

Arrays are exposed as native Xobjects arrays in the ``_xobject`` attribute, and
as numpy or numpy-like arrays as attributes of the beam element. For example:

.. code-block:: python

    m = xtrack.Multipole(knl=[1,2,3])

    mp._xobject.knl
    # is an xobjects.Array

    mp.knl
    # is a numpy array

It should be noted that the two are different views of the same memory area,
hence any modification can be made indifferently on any of them.

The numpy view (or np-like on GPU contexts) gives the possibility of using
numpy comptible functions and features on the array (e.g. ``np.sum``, ``np.mean``, 
slicing, masking, etc.).


