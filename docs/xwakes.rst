.. _xwakes_user_guide_section:

Xwakes: wakefields and impedances
=================================

``xwakes`` provides wakefield and impedance elements that plug into the
Xsuite tracking environment. It offers analytic resonator wakes, wakes read from
tables, multi-bunch/multi-turn support, transverse damping, monitoring, and
MPI pipeline wiring. The list of available wakefield elements is available in
:ref:`the API reference <xwakes_section>`.

Quick start: resonator wake on a single bunch
---------------------------------------------

.. code-block:: python

    import numpy as np
    import xtrack as xt
    import xwakes as xw

    # Build a wake as the sum of dipolar and quadrupolar resonators
    wf_dip_1 = xw.WakeResonator(kind='dipolar_x', r=1e8, q=1e5, f_r=1e3)
    wf_dip_2 = xw.WakeResonator(kind='dipolar_x', r=5e7, q=5e4, f_r=5e2)
    wf_quad_1 = xw.WakeResonator(kind='quadrupolar_x', r=2e7, q=8e4, f_r=2e3)
    wf_quad_2 = xw.WakeResonator(kind='quadrupolar_y', r=3e7, q=6e4, f_r=1.5e3)
    wf = wf_dip_1 + wf_dip_2 + wf_quad_1 + wf_quad_2

    # Configure for tracking: zeta range and number of slices
    wf.configure_for_tracking(
        zeta_range=(-0.1, 0.1),  # meters
        num_slices=100
    )

    # Simple accelerator lattice: one turn map plus wake
    one_turn = xt.LineSegmentMap(length=26000, betx=50., bety=40., qx=62.28, qy=62.31,
                                 longitudinal_mode='linear_fixed_qs', qs=1e-3, bets=100)
    line = xt.Line(elements=[one_turn, wf], element_names=['one_turn', 'wake'])
    line.set_particle_ref('proton', p0c=7e12)

    # One particle per slice, give it an offset, track once and inspect the kick
    particles = line.build_particles(
        x=0, px=0, y=0, py=0,
        zeta=wf.slicer.zeta_centers.flatten(),
    )
    particles.x += 1e-3  # mm-level offset

    # Track one turn
    line.track(particles, num_turns=1)

``configure_for_tracking`` prepares the internal slicer and wake tracker
(``zeta_range``, ``num_slices``) and must be called before tracking. Summing
wakes works naturally: ``wf_total = wf1 + wf2 + wf3``; the combined wake is
configured once and used like a single element.

.. include:: wakedefs.rst


Building wakes from tables
--------------------------

The class ``WakeFromTable`` builds wakefields from tabulated data in the time domain.
Columns must correspond to the wakefield kinds defined above. The function
``xw.read_headtail_file`` can be used to read HEADTAIL-format files, as illustrated
in the following examples.

.. code-block:: python

    import pathlib
    import xwakes as xw

    test_data = pathlib.Path(__file__).parent / 'test_data' / 'HLLHC_wake.dat'
    columns = ['time', 'longitudinal', 'dipolar_x', 'dipolar_y',
               'quadrupolar_x', 'quadrupolar_y']

    table = xw.read_headtail_file(test_data, columns)

    # use only dipolar terms
    wf = xw.WakeFromTable(table, columns=['dipolar_x', 'dipolar_y'])

    # Configure for tracking
    wf.configure_for_tracking(zeta_range=(-0.4, 0.4), num_slices=100)

    # Track as usual in a line
    # ...

Defining custom wakes
---------------------

For forms not covered by the built-in components, you can build a ``Component`` directly
from a wake callable in the time domain. Provide the plane of the kick, and the polynomial
exponents applied to the source/test offsets (``source_exponents`` for the source particle,
``test_exponents`` for the particle being kicked). The wake callable receives time ``t`` in
seconds; enforce causality by zeroing ``t <= 0``. Wrap one or more components in ``xw.Wake``
and configure it like any other wake.

.. code-block:: python

    import numpy as np
    import xwakes as xw

    a, b, c = 1.0e9, 0.1e9, 2.0  # frequency, damping rate, amplitude

    def wake_vs_t(t):
        t = np.atleast_1d(t)
        out = c * np.sin(a * t) * np.exp(-b * t)
        out[t <= 0] = 0.0  # causal wake
        return out

    custom_component = xw.Component(
        wake=wake_vs_t,
        plane='y',
        source_exponents=(2, 0),
        test_exponents=(1, 1),
        name="Example damped sine wake",
    )

    custom_wake = xw.Wake(components=[custom_component])

    # Inspect the zeta-domain wake or combine with other components
    zeta = np.linspace(-10, 10, 500)
    values = custom_component.function_vs_zeta(zeta, beta0=0.7)
    custom_wake.configure_for_tracking(zeta_range=(-0.1, 0.1), num_slices=200)

The snippet mirrors ``xwakes/examples/003_custom_wake.py``; you can mix these components with
resonators or tables via ``custom_wake + other_wake``.

Multi-bunch, multi-turn wakes
-----------------------------

``configure_for_tracking`` accepts multi-bunch/multi-turn options:

- ``filling_scheme``: array of 0/1 slots (length = number of RF buckets considered)
- ``bunch_spacing_zeta``: spacing between buckets in meters
- ``num_turns`` and ``circumference``: enable multi-turn wake memory

Example (two bunches, one-turn memory):

.. code-block:: python

    import numpy as np
    import xwakes as xw
    import xpart as xp
    import xtrack as xt

    filling_scheme = np.zeros(3564, dtype=int)
    filling_scheme[0] = filling_scheme[1] = 1

    wf = xw.WakeResonator(kind='dipolar_x', r=1e8, q=1e5, f_r=600e6)
    wf.configure_for_tracking(
        zeta_range=(-0.2, 0.2),
        num_slices=200,
        filling_scheme=filling_scheme,
        bunch_spacing_zeta=26658.8832 / 3564,
        num_turns=1,
        circumference=26658.8832,
    )

    # Simple one-turn map and line
    one_turn = xt.LineSegmentMap(
        length=26658.8832, betx=70., bety=80., qx=62.31, qy=60.32,
        longitudinal_mode='nonlinear', qs=2e-3, bets=731.27)
    line = xt.Line([one_turn, wf], element_names=['one_turn', 'wake'])
    line.particle_ref = xt.Particles(p0c=7e12)

    # Generate a matched two-bunch beam and track
    particles = xp.generate_matched_gaussian_multibunch_beam(
        line=line, filling_scheme=filling_scheme,
        bunch_num_particles=100_000, bunch_intensity_particles=2.3e11,
        nemitt_x=2e-6, nemitt_y=2e-6, sigma_z=0.08,
        bucket_length=26658.8832 / 35640, bunch_spacing_buckets=10,
    )
    line.track(particles, num_turns=10)

