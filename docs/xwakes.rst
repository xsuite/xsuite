Xwakes: wakefields and impedances
=================================

``xwakes`` provides wakefield and impedance elements that plug into the
Xsuite tracking stack. It offers analytic resonator wakes, wakes read from
tables, multi-bunch/multi-turn support, transverse damping, monitoring, and
MPI pipeline wiring. The examples below mirror the test-suite patterns and the
``xwakes/examples`` directory.

Quick start: resonator wake on a single bunch
---------------------------------------------

.. code-block:: python

    import numpy as np
    import xtrack as xt
    import xwakes as xw

    # Build a wake (here: transverse dipolar resonator) and configure slicing
    wf = xw.WakeResonator(kind='dipolar_x', r=1e8, q=1e5, f_r=1e3)
    wf.configure_for_tracking(
        zeta_range=(-0.1, 0.1),  # meters
        num_slices=100
    )

    # Simple lattice: one turn map plus wake
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
    line.track(particles, num_turns=1)

``configure_for_tracking`` prepares the internal slicer and wake tracker
(``zeta_range``, ``num_slices``) and must be called before tracking. Summing
wakes works naturally: ``wf_total = wf1 + wf2 + wf3``; the combined wake is
configured once and used like a single element.

Building wakes from tables
--------------------------

Use ``xw.read_headtail_file`` to parse HEADTAIL-format files, then wrap with
``WakeFromTable``. Columns must match the entries in ``xwakes.wit.component.KIND_DEFINITIONS``
(``longitudinal``, ``dipolar_x``, ``quadrupolar_y``, ``constant_x``, etc.).

.. code-block:: python

    import pathlib
    import xwakes as xw

    test_data = pathlib.Path(__file__).parent / 'test_data' / 'HLLHC_wake.dat'
    columns = ['time', 'longitudinal', 'dipolar_x', 'dipolar_y',
               'quadrupolar_x', 'quadrupolar_y']

    table = xw.read_headtail_file(test_data, columns)
    wf = xw.WakeFromTable(table, columns=['dipolar_x', 'dipolar_y'])
    wf.configure_for_tracking(zeta_range=(-0.4, 0.4), num_slices=100)

Multi-bunch, multi-turn wakes
-----------------------------

``configure_for_tracking`` accepts multi-bunch/multi-turn options:

- ``filling_scheme``: array of 0/1 slots (length = number of RF buckets considered)
- ``bunch_spacing_zeta``: spacing between buckets in meters
- ``bunch_selection``: subset of slots for this process (used in MPI)
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
        bunch_selection=[0, 1],
    )
    line.track(particles, num_turns=10)


Resonator API
-------------

``xwakes.WakeResonator`` builds one or more analytic resonator components.

Constructor
~~~~~~~~~~~

.. code-block:: python

    xw.WakeResonator(
        kind=None,                 # str | list/tuple[str] | dict[str,float] | xw.Yokoya
        plane=None,                # 'x' | 'y' | 'z' (used only when kind is None)
        source_exponents=None,     # (int, int) for custom source term (kind is None)
        test_exponents=None,       # (int, int) for custom test term (kind is None)
        r=None, q=None, f_r=None,  # shunt impedance [Ohm/m^n], quality factor, resonant freq [Hz]
        f_roi_level=0.5            # fractional cutoff to define ROI for sampling
    )

- ``kind``:
  - string: e.g. ``'dipolar_x'``, ``'longitudinal'``
  - list/tuple: several kinds with unit weight
  - dict: mapping ``kind -> scale`` (scale multiplies the wake/impedance)
  - ``xw.Yokoya``: expand yokoya factors into the appropriate kinds
  - ``None``: supply ``plane``, ``source_exponents``, ``test_exponents`` directly for a custom polynomial term.
- ``r``, ``q``, ``f_r`` define the resonator; all kinds in the same instance share them.
- ``f_roi_level`` tunes how ROIs are generated for impedance/wake sampling.

After construction, call ``configure_for_tracking(...)`` with slicing options
as shown above. You can also combine resonators via ``+``; the resulting
``CombinedWake`` is configured and tracked like a single wake.

Examples of resonator initialization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Single component
    .. code-block:: python

        # Horizontal dipolar resonator
        w1 = xw.WakeResonator(kind='dipolar_x', r=1e8, q=1e5, f_r=1e9)

Multiple components (list/tuple)
    .. code-block:: python

        # Horizontal + vertical dipolar with same r/q/f_r
        w2 = xw.WakeResonator(kind=['dipolar_x', 'dipolar_y'],
                              r=1e8, q=1e5, f_r=1e9)

Weighted components (dict)
    .. code-block:: python

        # Scale horizontal twice as strong as vertical
        w3 = xw.WakeResonator(kind={'dipolar_x': 2.0, 'dipolar_y': 1.0},
                              r=1e8, q=1e5, f_r=1e9)

Using Yokoya factors
    .. code-block:: python

        # Flat chamber (horizontal) yokoya factors expanded into the right components
        w4 = xw.WakeResonator(kind=xw.Yokoya('flat_horizontal'),
                              r=1e8, q=1e5, f_r=1e9)

Custom polynomial term
    .. code-block:: python

        # Custom plane/exponents without a predefined kind entry
        w5 = xw.WakeResonator(
            plane='y',
            source_exponents=(1, 0),  # x_source^1 y_source^0
            test_exponents=(0, 2),    # x_test^0 y_test^2
            r=1e8, q=1e5, f_r=1e9)

Combine and configure
    .. code-block:: python

        w = w1 + w2 + w3.components[0]  # mix whole wakes and single components
        w.configure_for_tracking(zeta_range=(-0.1, 0.1), num_slices=200)
