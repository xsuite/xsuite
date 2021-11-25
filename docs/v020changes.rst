===================================
Changes introduced in Xsuite v0.2.0
===================================

Significant changes are introduced with **Xsuite v0.2.0** and the corresponding subpackages **Xobjects v0.1.0**, **Xtrack v0.4.0**, **Xpart v0.2.0** and **Xfields v0.3.0** .

The main goals of these changes are to simplify the user interface bases on the (precious!) feedback from early users and developers and to ease the implementation of new features in the near future.

We are trying to adapt and improve the user interface as much as possible at this early stage of development to minimize future changes, which would affect a larger number of users and a larger amount of user's code.

Changes to the interface
========================

Most relevant changes to the interface are the following:

 - The xline package is removed
     - The class ``xline.Line`` is replaced by ``xtrack.Line`` for the creation and import of machine lattices (see :doc:`singlepart`).
     - Beam elements are created using directly the xtrack classes (``xtrack.Drift``, ``xtrack.Multipole``, ``xtrack.Cavity``, etc.) instead of of the xline ones (``xline.Drift``, ``xline.Multipole``, ``xtrack.Cavity``).
 - There is only one Particles class within Xsuite, which can be imported from xpart package. Therefore ``xline.Particles`` and ``xtrack.Particles`` should be replaced by ``xpart.Particles``.
 - The ``sequence`` argument of the tracker class was renamed ``line`` to be consistent with the naming used elsewhere.
 - The PyHEADTAIL interface is moved from xtrack to xpart (see :doc:`pyhtinterface`)
 - The random number generators are moved from xtrack to xpart.
 - The method ``xtrack.Line.from_json`` has been removed. A line can be loaded from a json file by:

.. code-block:: python

    import json
    with open(''line.json", "r") as fid:
        line = xtrack.Line.from_dict(json.load(fid))

New features
============

 - The ``xtrack.Tracker`` class has new methods for closed-orbit search and one-turn-matrix calculation with finite differences.
 - Added ``xpart.build_particles`` function allowing to build a particles object from a reference particles plus arrays with geometric or normalized coordinates.

