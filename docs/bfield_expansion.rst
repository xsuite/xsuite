.. _bfield_expansion:

====================================
Magnetic fields with BFieldExpansion
====================================

The :class:`xtrack.BFieldExpansion` element represents a static magnetic field
with a polynomial dependence on the longitudinal coordinate, in a straight or
curved reference frame. Normal and skew transverse-field profiles and an
on-axis longitudinal field define a scalar-potential expansion. This provides
the off-axis field, including longitudinal components associated with fringe
fields. It can be used for dipoles, combined-function magnets, quadrupole
fringes, and solenoids.

.. contents:: On this page
   :local:
   :depth: 2

Specifying the field
--------------------

All input fields are normalized by the signed reference magnetic rigidity
:math:`B\rho`, available as ``particles.rigidity0`` in T m. The coefficients
therefore describe :math:`\mathbf{B}/(B\rho)`, rather than a field in tesla.

The arrays ``knc`` and ``ksc`` specify transverse derivatives on the reference
axis. At :math:`y=0`, their convention is

.. math::

   \frac{B_y(x,0,s)}{B\rho}
       &= \sum_{i=0}^{n_b-1}\frac{x^i}{i!}
          \sum_{j=0}^{d} \mathrm{knc}_{ij}\,s^j, \\
   \frac{B_x(x,0,s)}{B\rho}
       &= \sum_{i=0}^{n_a-1}\frac{x^i}{i!}
          \sum_{j=0}^{d} \mathrm{ksc}_{ij}\,s^j, \\
   \frac{B_s(0,0,s)}{B\rho}
       &= \sum_{j=0}^{d-1} \mathrm{ksol}_j\,s^j.

Row zero of ``knc`` is the normal dipole profile, row one is its quadrupole
gradient, and row two is its sextupole second derivative. The factorial in
the transverse expansion is applied internally. Columns contain ascending
powers of ``s`` in metres, with no longitudinal factorial and no rescaling by
the element length. Thus ``knc[i, j]`` and ``ksc[i, j]`` have units
:math:`\mathrm{m}^{-(i+j+1)}`, and ``ksol[j]`` has units
:math:`\mathrm{m}^{-(j+1)}`.

Both coefficient matrices must have the same number of columns as the length
of ``ksol``; their numbers of rows may differ. Pad unused coefficients with
zeros. In particular, **the last coefficient of ``ksol`` must be zero**: the
scalar potential stores its integral using the same polynomial degree. For
example, a constant longitudinal field needs ``ksol=[ks, 0]`` and at least two
columns in both transverse matrices.

The required parameter ``ny`` controls the truncation of the expansion in
the vertical coordinate. It is independent of the longitudinal polynomial
degree, which is inferred from the coefficient arrays. Check convergence in
``ny`` over the transverse aperture of interest.

For example, a straight element with a varying dipole, a quadrupole gradient,
and a longitudinal field can be constructed and tracked as follows:

.. code-block:: python

   import numpy as np
   import xtrack as xt

   magnet = xt.BFieldExpansion(
       length=0.8,
       h=0.0,
       knc=[[0.05, 0.04, 0.07],     # Normal dipole: 0.05 + 0.04*s + 0.07*s**2
            [0.40, -0.10, 0.0]],   # Normal quadrupole: 0.40 - 0.10*s
       ksc=[[0.0, 0.0, 0.0]],
       ksol=[0.10, 0.02, 0.0],     # On-axis longitudinal field: 0.10 + 0.02*s
       ny=5,
       nstep=40,
       pkin_const=True,
   )
   particles = xt.Particles(p0c=1e9, x=0.003, y=0.002, px=0.001)
   magnet.track(particles)
   print(particles.x, particles.kin_px, particles.y, particles.kin_py)

Longitudinal coordinate and geometry
------------------------------------

``length`` is the path length along the reference trajectory, in metres.
Tracking evaluates the polynomial from ``sstart`` to ``sstart + length``;
``sstart`` defaults to zero. This polynomial coordinate is independent of
the particle's accumulated ``s`` in a line. When fitting separate polynomial
segments, either use a common coordinate and set ``sstart`` accordingly, or
express each polynomial in its own local coordinate and use ``sstart=0``.
For SciPy piecewise polynomials, coefficients are usually in descending
powers of the coordinate relative to each interval's left endpoint; reverse
their order before passing them to ``BFieldExpansion``.

``h=0`` selects straight geometry. Curved geometry currently requires
``h > 1e-4`` in :math:`\mathrm{m}^{-1}`. The mode is fixed at construction:
changing between straight and curved geometry requires a new element.
Within curved geometry, ``h`` can be updated while respecting this bound.
The read-only attributes ``straight`` and ``angle`` report the mode and
``length * h``, respectively. Survey uses this reference bend angle.

Curvature describes the reference frame; the magnetic field must still be
specified independently. For example, the following element has a constant
normal dipole field equal to the reference curvature:

.. code-block:: python

   bend = xt.BFieldExpansion(
       length=1.0, h=0.2, knc=[[0.2]], ksc=[[0.0]], ksol=[0.0],
       ny=5, nstep=40,
   )
   print(bend.angle)  # 0.2 rad

Evaluating fields and potentials
--------------------------------

:meth:`~xtrack.BFieldExpansion.get_field` accepts scalars or broadcastable
arrays, with all three coordinates in metres. For a parent
``BFieldExpansion``, ``s`` is the polynomial coordinate: the entrance is at
``sstart``. The method evaluates the polynomial at the requested points
without clipping to the tracked
interval. In curved geometry, the coordinate axis ``1 + h*x = 0`` is singular
and is rejected.

The result is a structured NumPy array with the broadcast input shape
(including a zero-dimensional array for scalar inputs). Its fields are
``phi``, ``Bx``, ``By``, ``Bs``, ``Ax``, ``Ay``, ``As``, ``dAx_dx``,
``dAx_dy``, ``dAx_ds``, ``dAs_dx``, ``dAs_dy``, and ``dAs_ds``. Magnetic
fields are normalized by :math:`B\rho`; the scalar and vector potentials
use the same rigidity normalization, and ``Ay`` is zero in the chosen gauge.
The result is returned on the CPU even when the element uses a GPU context.

.. code-block:: python

   s = np.linspace(magnet.sstart, magnet.sstart + magnet.length, 101)
   field = magnet.get_field(x=0.003, y=0.002, s=s)
   by_tesla = field['By'] * particles.rigidity0[0]
   bs_tesla = field['Bs'] * particles.rigidity0[0]

   # Broadcasting: evaluate two horizontal offsets along the same interval.
   grid = magnet.get_field(x=np.array([[0.0], [0.01]]), y=0.002, s=s)
   print(grid.shape)  # (2, 101)

Integration and boundary momenta
--------------------------------

Both geometry modes integrate Hamilton's equations with classical
fourth-order Runge--Kutta (RK4). ``nstep`` is a positive integer, defaults
to 10, and sets the step size ``ds = length / nstep``. Updating ``length``
or ``nstep`` updates ``ds``. For a fixed, sufficiently smooth field model,
the global integration error is expected to decrease as ``nstep**-4`` until
other errors dominate. RK4 is not an exactly symplectic integrator.

``pkin_const`` controls the handling of the vector potential at element
boundaries; it does not change the integration method:

* ``pkin_const=False`` (the default) keeps canonical momenta across
  interfaces. Tracking leaves ``px`` and ``py`` in the element's gauge and
  stores the exit vector potential in ``particles.ax`` and ``particles.ay``.
  A discontinuous transverse vector potential at a join can therefore
  change the kinetic momentum. This is the canonical boundary convention,
  but the finite-step RK4 map is still not exactly symplectic.
* ``pkin_const=True`` preserves kinetic momentum when changing the vector
  potential at entrance and exit. It converts to the element's canonical
  momenta internally and returns to zero transverse vector potential at
  exit. Consequently, the outgoing ``px`` and ``py`` are kinetic momenta.

Use ``particles.kin_px`` and ``particles.kin_py`` when comparing physical
trajectories between these modes. To start the default mode from prescribed
kinetic momenta inside a nonzero field, initialize the canonical momenta
using the entrance potential:

.. code-block:: python

   canonical_magnet = magnet.copy()
   canonical_magnet.pkin_const = False
   canonical_particles = xt.Particles(p0c=1e9, x=0.003, y=0.002, px=0.001)
   entrance = canonical_magnet.get_field(
       canonical_particles.x, canonical_particles.y,
       s=canonical_magnet.sstart,
   )
   canonical_particles.px += entrance['Ax']
   canonical_particles.py += entrance['Ay']
   canonical_particles.ax = entrance['Ax']
   canonical_particles.ay = entrance['Ay']
   canonical_magnet.track(canonical_particles)

For a piecewise field model, convergence of the on-axis profile alone does
not establish convergence of the off-axis field. Its higher longitudinal
derivatives contribute to the expansion, and discontinuities of the vector
potential make the boundary convention relevant. Refine the field model
and ``ny`` separately from ``nstep``. In particular, increasing ``nstep``
cannot recover high-order fringe terms omitted by a low-degree polynomial fit.

Updating coefficients and using an Environment
----------------------------------------------

Coefficient arrays have fixed shapes. Update their entries or slices to
rebuild the cached expansion and integrated strengths automatically:

.. code-block:: python

   magnet.knc[1, 0] = 0.45
   magnet.ksol[:] = [0.12, 0.02, 0.0]
   magnet.knc *= 1.1

   # NumPy conversions are detached copies; write back to apply an edit.
   coefficients = np.asarray(magnet.knc)
   coefficients[0, 0] = 0.06
   magnet.knc[...] = coefficients

Direct reassignment such as ``magnet.knc = coefficients`` is prohibited.
Construct a new element to change the coefficient shapes or expansion order.

The read-only arrays ``knl`` and ``ksl`` contain the normal and skew profiles
integrated over ``[sstart, sstart + length]``, with one entry per transverse
derivative order. ``ksoll`` is a one-entry array containing the integrated
longitudinal profile. They also update when ``sstart`` or ``length`` changes.

:ref:`xtrack.Environment <environment-api-reference>` accepts coefficient
matrices containing numbers and deferred expressions through ``new`` and ``set``:

.. code-block:: python

   env = xt.Environment()
   env['k1'] = 0.4
   env.new('q', 'BFieldExpansion', length=0.3, ny=5, nstep=40,
           knc=[[0.0, 0.0], ['k1', 0.0]],
           ksc=[[0.0, 0.0]], ksol=[0.0, 0.0])
   env['k1'] = 0.45
   env.set('q', knc=[[0.0, 0.0], ['2*k1', 0.0]])
   line = env.new_line(components=['q'])
   line.get_table(attr=True).cols['element_type length angle k1l'].show()

Thick slicing
-------------

Use a slicing scheme with ``mode='thick'``. Each
``ThickSliceBFieldExpansion`` shares its parent's coefficients and cached
expansion, and tracks its own longitudinal interval. Slicing does not refit
the field polynomial. Parent coefficient updates are therefore visible to
all slices; slice lengths and offsets follow changes in the parent length.

.. code-block:: python

   sliced_line = xt.Line(elements={'magnet': magnet})
   sliced_line.slice_thick_elements([
       xt.Strategy(xt.Uniform(4, mode='thick'),
                   element_type=xt.BFieldExpansion),
   ])
   sliced_particles = xt.Particles(p0c=1e9, x=0.003, y=0.002, px=0.001)
   sliced_line.track(sliced_particles)

A slice with weight ``w`` uses ``max(1, ceil(parent.nstep * w))`` RK4 steps.
Rounding can increase the total number of steps. Uniform slicing with a
parent step count divisible by the number of slices retains the original
integration grid. Each slice's integrated strengths are computed over its
own interval, rather than by scaling the parent's integral. Unlike the
parent method, a slice's ``get_field(x, y, s)`` takes ``s`` relative to the
slice entrance and adds the slice's ``sstart`` internally.

Thin slicing, element rotations and shifts, radiation tracking, and spin
tracking are currently unsupported. Tracking and field evaluation support
CPU, CuPy, and PyOpenCL contexts.

Comparing convergence and speed with SplineBoris
------------------------------------------------

For straight geometry, :class:`xtrack.SplineBoris` provides another way to
represent longitudinally varying fields (see
:doc:`s_dependent_magnetic_fields`). It takes ``Spline4`` data in SI units
and uses a second-order spatial Boris integrator. ``BFieldExpansion`` takes
rigidity-normalized polynomial coefficients and uses RK4. Equal step counts
therefore do not imply equal tracking accuracy.

The Xtrack example ``examples/bfieldexpansion/compare_splineboris_speed.py``
compares the two methods at a common exit-error tolerance. Run it from the
Xtrack repository root:

.. code-block:: console

   python -m examples.bfieldexpansion.compare_splineboris_speed --no-plot --tolerance 1e-8 --particles 10000

The example first checks agreement of all three field components off axis.
It then calibrates each integrator's step count against the same refined
DOP853 Lorentz-force reference. The error criterion is the maximum absolute
difference over the particle ensemble and the six dimensionless coordinates
``(x/length, kin_px, y/length, kin_py, zeta/length, delta)``. This is an
absolute exit-error criterion, rather than a relative error in each
coordinate or a long-term symplecticity test.

Only warmed-up, single-pass tracking on a serial CPU is timed. Construction,
compilation, particle copies, and reference integration are excluded. Omit
``--no-plot`` to display error versus step count and tracking time, including
the points selected at the common tolerance. The measured speed ratio
depends on the field, accuracy target, particle ensemble, and hardware.

The examples ``convergence_pkin_const.py``,
``convergence_pkin_const_straight_solenoid.py``,
``convergence_pkin_const_curved_solenoid.py``, and
``convergence_pkin_const_curved_dipole.py`` in the same directory examine
integration error, polynomial segmentation, and boundary conventions.
``survey_and_slicing.py`` compares surveyed geometry and laboratory-frame
trajectories before and after thick slicing.
