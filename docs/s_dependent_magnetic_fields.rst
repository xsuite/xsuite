====================================
Modeling s-dependent magnetic fields
====================================

Xsuite provides two elements for modeling magnetic fields that vary along the
longitudinal coordinate: :class:`xtrack.SplineBoris` and
:class:`xtrack.BFieldExpansion`. They reconstruct the off-axis magnetic field
from longitudinal profiles of the field and its transverse derivatives on the
reference axis. These models can describe devices such as undulators,
wigglers, magnets with fringe fields, and solenoids, for which a constant
multipolar description is not sufficient.

* :class:`xtrack.SplineBoris` uses fourth-order polynomial profiles specified
  through :class:`xtrack.Spline4` objects, with field data in SI units. It
  tracks particles in a straight reference frame using a second-order spatial
  Boris integrator. The examples in :doc:`spline_boris` show how to build an
  undulator from a field map and install it in a ring.
* :class:`xtrack.BFieldExpansion` accepts polynomial coefficients normalized
  by the signed reference magnetic rigidity and supports straight and curved
  reference frames. It tracks particles using fourth-order Runge--Kutta
  integration. See :doc:`bfield_expansion` for field specification, geometry,
  field evaluation, and integration settings.

The reconstruction of the three-dimensional field is described in the
``Field expansion for s-dependent magnetic field`` chapter of the
:doc:`Physics Guide <physicsguide>`.

.. toctree::
   :maxdepth: 2

   spline_boris
   bfield_expansion
