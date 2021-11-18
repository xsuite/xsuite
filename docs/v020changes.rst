===================================
Changes introduced in Xsuite v0.2.0
===================================

Significant changes are introduced with **Xsuite v0.2.0** and the corresponding subpackages **Xobjects v0.1.0**, **Xtrack v0.4.0**, **Xpart v0.2.0** and **Xfields v0.3.0** .

The main goals of these changes are to simplify the user interface bases on the (precious!) feedback from early users and developers and to ease the implementation of new features in the near future.

Most relevant changes to the interface are the following:

 - The xline package is removed
     - The class ``xline.Line`` is replaced by ``xtrack.Line`` for the creation and import of machine lattices (see :doc:`singlepart`).
     - Beam elements are created using directly the xtrack classes (``xtrack.Drift``, ``xtrack.Multipole``, ``xtrack.Cavity``, etc.) instead of of the xline ones (``xline.Drift``, ``xline.Multipole``, ``xtrack.Cavity``).
 - There is only one Particles class within Xsuite, which can be imported from xpart package. Therefore ``xline.Partices`` and ``xtrack.Particles`` should be replaced by ``xpart.Particles``.
 - The ``sequence`` argument of the tracker class was renamed ``line`` to be consistent with the naming used elsewhere.

**New feature**
 - Tracker class has new methods for closed-orbit search and one-turn-matrix calculation with finite differences
 - 

