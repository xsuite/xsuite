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

The scalar and vector potentials, curved-coordinate expansion, and tracking
equations are derived in the ``Modeling s-dependent magnetic fields`` chapter
of the :doc:`Physics Guide <physicsguide>`.

.. contents:: On this page
   :local:
   :depth: 2

Specifying the field
--------------------

All input fields are normalized by the signed reference magnetic rigidity
:math:`B\rho`, available as ``particles.rigidity0`` in T m. The coefficients
therefore describe :math:`\mathbf{B}/(B\rho)`, rather than a field in tesla.

The arrays ``knc`` and ``ksc`` specify transverse derivatives on the reference
axis. With the additional scalar and integrated strengths set to zero and
``kscale=1``, their convention at :math:`y=0` is

.. math::

   \frac{B_y(x,0,s)}{B\rho}
       &= \sum_{i=0}^{n_b-1}\frac{x^i}{i!}
          \sum_{j=0}^{d_n} \mathrm{knc}_{ij}\,s^j, \\
   \frac{B_x(x,0,s)}{B\rho}
       &= \sum_{i=0}^{n_a-1}\frac{x^i}{i!}
          \sum_{j=0}^{d_s} \mathrm{ksc}_{ij}\,s^j, \\
   \frac{B_s(0,0,s)}{B\rho}
       &= \sum_{j=0}^{d_\ell} \mathrm{ksolc}_j\,s^j.

The suffix ``c`` denotes coefficients. The three profiles may have independent
longitudinal degrees :math:`d_n`, :math:`d_s`, and :math:`d_\ell`.

Row zero of ``knc`` is the normal dipole profile, row one is its quadrupole
gradient, and row two is its sextupole second derivative. The factorial in
the transverse expansion is applied internally: ``knc[i, 0]`` has the same
normalization as Xtrack's ``k0``, ``k1``, ``k2``, and higher-order strengths.
Use :meth:`~xtrack.BFieldExpansion.get_total_knl_ksl` for the longitudinal
integrals, including the additional strengths and scale described below.
Columns contain ascending powers of ``s`` in metres, with no longitudinal
factorial and no rescaling by the element length. Thus ``knc[i, j]`` and
``ksc[i, j]`` have units
:math:`\mathrm{m}^{-(i+j+1)}`, and ``ksolc[j]`` has units
:math:`\mathrm{m}^{-(j+1)}`.

Coefficient arrays are optional: omitted, ``None``, or empty arrays remain
empty and contribute no field. ``knc`` and ``ksc`` can have different row
counts and widths, and ``ksolc`` can have an independent length. Ragged
transverse rows are padded with zeros within their own matrix at construction;
rectangular inputs retain their shapes. The integrated inputs ``knl`` and
``ksl`` also have independent lengths and default to empty arrays.

No manual padding is needed. Every coefficient in ``ksolc`` is retained,
including its highest power: the scalar potential reserves the extra degree
needed for the integral internally. A constant longitudinal field therefore
only needs ``ksolc=[ks]``. Explicitly supplied zero coefficients retain storage
for later updates or deferred expressions. To add coefficients later, supply
the desired array shape at construction.

The optional ``num_phi`` parameter controls the vertical truncation order
of the scalar-potential reconstruction. Its default, ``'auto'``, uses the
coefficient array shapes and longitudinal polynomial degree to retain the
complete straight-field polynomial expansion, including the vector potential.
It accounts for the allocated integrated-strength arrays and initially zero
coefficients that may be changed later, including through deferred expressions.
It also reserves capacity for all eight scalar strengths, ``k0`` through
``k3`` and ``k0s`` through ``k3s``, even when the profiles have fewer rows.
The automatic order is at least 5 in straight geometry. The transverse row
count alone is insufficient to choose the order, since longitudinal
derivatives also generate higher powers of the vertical coordinate.

For curved geometry, ``'auto'`` adds two orders to retain every term through
first order in ``h``. A curved expansion generally does not terminate, and
terms of higher order in ``h`` are not generally complete. When these terms
matter, construct elements with successively larger explicit nonnegative
integer values of ``num_phi`` and check convergence over the transverse
aperture of interest.

The resolved integer is stored in ``element.num_phi`` and is fixed at
construction. Fields are evaluated through ``y**num_phi``; an additional
scalar-potential coefficient is stored internally for the derivative giving
``By``. Evaluation skips unused orders and degrees; the populated bounds are
recomputed when coefficients or strengths change.

For example, a straight element with a varying dipole, a quadrupole gradient,
and a longitudinal field can be constructed and tracked as follows:

.. code-block:: python

   import numpy as np
   import xtrack as xt

   magnet = xt.BFieldExpansion(
       length=0.8,
       h=0.0,
       s_start=0.15,               # Track the polynomial over s in [0.15, 0.95] m
       knc=[[0.05, 0.04, 0.07],     # Normal dipole: 0.05 + 0.04*s + 0.07*s**2
            [0.40, -0.10]],        # Normal quadrupole: 0.40 - 0.10*s
       ksolc=[0.10, 0.02],         # On-axis longitudinal field: 0.10 + 0.02*s
       num_phi='auto',
       num_integration_steps=40,
       pkin_const=True,
   )
   particles = xt.Particles(p0c=1e9, x=0.003, y=0.002, px=0.001)
   magnet.track(particles)
   print(particles.x, particles.kin_px, particles.y, particles.kin_py)

Additional strengths and scaling
--------------------------------

``k0``, ``k1``, ``k2``, and ``k3`` add uniform normal dipole through octupole
strengths; ``k0s``, ``k1s``, ``k2s``, and ``k3s`` add the corresponding skew
strengths. All default to zero and use the usual Xtrack normalization.
They are independent of the polynomial profiles and of the reference
curvature ``h``.

The writable arrays ``knl`` and ``ksl`` add integrated hard-edge strengths.
Their contributions to the local field are ``knl[i] / length`` and
``ksl[i] / length``. These contributions leave the polynomial input arrays
unchanged and add no extra fringe at the element boundaries. The arrays may
contain higher multipole orders than the profiles. Nonzero ``knl`` or ``ksl``
requires nonzero ``length``; changing the length preserves these integrated
inputs and recomputes their field densities.

For normal order :math:`i`, the combined local strength is

.. math::

   K_i(s) = \mathrm{kscale}\left(
       k_i + \sum_j \mathrm{knc}_{ij}s^j
       + \frac{\mathrm{knl}_i}{L}\right).

The skew convention is analogous. Missing array entries and scalar orders
above octupole contribute zero. ``kscale`` defaults to 1 and multiplies all
field components, including the longitudinal field, reconstructed potentials,
derivatives, and integrated strengths. It leaves the input strengths and
reference geometry unchanged: zero switches off the field, and a negative
value reverses it.

.. code-block:: python

   combined = xt.BFieldExpansion(
       length=0.8, knc=[[0.05, 0.02], [0.40, 0.0]],
       k1=0.10, knl=[0.004, 0.008], kscale=0.5,
       num_integration_steps=40,
   )  # Omitted skew and longitudinal profiles are empty and contribute zero.
   normal, skew = combined.get_total_knl_ksl()
   print(normal[1])  # 0.5 * ((0.40 + 0.10) * 0.8 + 0.008) = 0.204 1/m

Longitudinal coordinate and geometry
------------------------------------

``length`` is the path length along the reference trajectory, in metres.
Tracking evaluates the polynomial from ``s_start`` to ``s_start + length``;
``s_start`` defaults to zero. This polynomial coordinate is independent of
the particle's accumulated ``s`` in a line. When fitting separate polynomial
segments, either use a common coordinate and set ``s_start`` accordingly, or
express each polynomial in its own local coordinate and use ``s_start=0``.
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
       length=1.0, h=0.2, k0=0.2, num_integration_steps=40,
   )
   print(bend.angle)  # 0.2 rad

Evaluating fields and potentials
--------------------------------

:meth:`~xtrack.BFieldExpansion.get_field` takes ``x``, ``y``, and ``s_local``
as scalars or broadcastable arrays, with all three coordinates in metres.
``s_local`` is measured from the element's entrance: zero is the entrance
and ``length`` is the exit, even when ``s_start`` is nonzero. The polynomial
is evaluated at ``s = s_start + s_local``, as in tracking, without clipping
to the tracked interval. In curved geometry, the coordinate axis
``1 + h*x = 0`` is singular: ``get_field`` raises ``ValueError`` there.
Tracking marks a particle that reaches this axis as lost with state ``-43``
without partially committing its coordinates for the element or slice.

The result is a structured NumPy array with the broadcast input shape
(including a zero-dimensional array for scalar inputs). Its fields are
``phi``, ``Bx``, ``By``, ``Bs``, ``Ax``, ``Ay``, ``As``, ``dAx_dx``,
``dAx_dy``, ``dAx_ds``, ``dAs_dx``, ``dAs_dy``, and ``dAs_ds``. Magnetic
fields are normalized by :math:`B\rho`; the scalar and vector potentials
use the same rigidity normalization, and ``Ay`` is zero in the chosen gauge.
All returned quantities include ``kscale``. Coordinates and field components
refer to the element's local frame; shifts and rotations do not change the
result of ``get_field`` at the same local coordinates.
The result is returned on the CPU even when the element uses a GPU context.

.. code-block:: python

   s_local = np.linspace(0.0, magnet.length, 101)
   field = magnet.get_field(x=0.003, y=0.002, s_local=s_local)
   by_tesla = field['By'] * particles.rigidity0[0]
   bs_tesla = field['Bs'] * particles.rigidity0[0]

   # Broadcasting: evaluate two horizontal offsets along the same interval.
   grid = magnet.get_field(x=np.array([[0.0], [0.01]]), y=0.002,
                           s_local=s_local)
   print(grid.shape)  # (2, 101)

Integration and boundary momenta
--------------------------------

Both geometry modes integrate Hamilton's equations with classical
fourth-order Runge--Kutta (RK4). ``integrator='rk4'`` is the default and the
only supported scheme; ``get_available_integrators()`` returns ``['rk4']``.
``num_integration_steps`` is a positive integer, defaults to 10, and sets the
read-only step size ``ds = length / num_integration_steps``. Changing the
length or step count changes ``ds``. For a fixed, sufficiently smooth field
model, the global integration error is expected to decrease as
``num_integration_steps**-4`` until other errors dominate. RK4 is not an
exactly symplectic integrator.

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
       s_local=0.0,
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
and ``num_phi`` separately from ``num_integration_steps``. Increasing the
step count cannot recover high-order fringe terms omitted by a low-degree
polynomial fit.

Updating coefficients and using an Environment
----------------------------------------------

Coefficient arrays have fixed shapes. Update their entries or slices to
rebuild the cached expansion and integrated strengths automatically:

.. code-block:: python

   magnet.knc[1, 0] = 0.45
   magnet.ksolc[:] = [0.12, 0.02]
   magnet.knc *= 1.1

   # NumPy conversions are detached copies; write back to apply an edit.
   coefficients = np.asarray(magnet.knc)
   coefficients[0, 0] = 0.06
   magnet.knc[...] = coefficients

Direct reassignment such as ``magnet.knc = coefficients`` is prohibited.
``knl`` and ``ksl`` also support in-place updates, and accept whole-array
assignment when the shape is unchanged. Updating a scalar strength or
``kscale`` rebuilds the shared expansion from the unscaled inputs.
Construct a new element to change the coefficient shapes or ``num_phi``.
The read-only ``order`` is ``max(knc.shape[0], ksc.shape[0]) - 1`` and reports
the allocated polynomial multipole order, regardless of which coefficients
are nonzero. Independent scalar or integrated strengths may have higher
orders. ``na`` and ``nb`` are the read-only skew and normal row counts.
``deg`` is the largest input polynomial degree across the three profiles
(zero when all are empty). The independent scalar strengths remain writable
even when all coefficient arrays were omitted.

The coefficient argument and attribute are named ``ksolc``, replacing
``ksol``. Update constructor keywords, coefficient accesses, expression
references, and the coefficient key in saved element dictionaries to the
new name. The integrated quantity keeps its name ``ksoll``.

``get_total_knl_ksl()`` sums the profile integrals over
``[s_start, s_start + length]``, the scalar strengths times ``length``, and
the additional ``knl``/``ksl`` inputs, then multiplies the sum by ``kscale``.
The result is a pair of detached
NumPy arrays padded to the same length, with at least four entries.
``line.get_table(attr=True)`` and Twiss strength columns report these totals.
The read-only one-entry array ``ksoll`` contains the integral of ``ksolc``
over the same interval, including ``kscale``. These computed quantities
reflect changes to the strengths, scale, polynomial origin, and length.

:ref:`xtrack.Environment <environment-api-reference>` accepts coefficient
matrices containing numbers and deferred expressions through ``new`` and ``set``:

.. code-block:: python

   env = xt.Environment()
   env['k1'] = 0.4
   env['field_scale'] = 0.8
   env.new('q', 'BFieldExpansion', length=0.3, num_phi='auto',
           num_integration_steps=40, integrator='rk4',
           k1='0.1*k1', kscale='field_scale', knl=[0.0, 0.01],
           knc=[[0.0], ['k1']])
   env['k1'] = 0.45
   env.set('q', knc=[[0.0], ['2*k1']])
   line = env.new_line(components=['q'])
   line.get_table(attr=True).cols['element_type length angle k1l'].show()

``num_phi`` is fixed when the expansion cache is allocated. Neither
``num_phi`` nor ``integrator`` can be a deferred expression. Updating
coefficients within their allocated shapes does not change the resolved
expansion order.
