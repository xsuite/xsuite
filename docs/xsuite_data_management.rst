
=========================
Data management in Xsuite
=========================

Done through the Xobjects package

Beam elements and Particles objects are xobjects Hybrid classes.

They contain data that is made accessible from C along with standard
python attributes and methods.

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

The data accessible from C is stored in a the _xobject attribute present in all
Particles and beam element objects.


