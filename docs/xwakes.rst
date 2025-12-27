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
    import xpart as xp
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
    line.particle_ref = xt.Particles(p0c=7e12)
    line.build_tracker()

    # One particle per slice, give it an offset, track once and inspect the kick
    particles = xp.Particles(
        p0c=line.particle_ref.p0c[0],
        zeta=wf.slicer.zeta_centers.flatten(),
        x=np.zeros(wf.slicer.num_slices),
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
    line.build_tracker()

    # Generate a matched two-bunch beam and track
    particles = xp.generate_matched_gaussian_multibunch_beam(
        line=line, filling_scheme=filling_scheme,
        bunch_num_particles=100_000, bunch_intensity_particles=2.3e11,
        nemitt_x=2e-6, nemitt_y=2e-6, sigma_z=0.08,
        bucket_length=26658.8832 / 35640, bunch_spacing_buckets=10,
        bunch_selection=[0, 1],
    )
    line.track(particles, num_turns=10)

Transverse damper and collective monitor
----------------------------------------

``xwakes`` ships with simple bunch-by-bunch tools that share the same slicer
interface as the wakes:

.. code-block:: python

    import xwakes as xw

    # Damper with 100-turn equivalent gains, using the same slicing as the wake
    damper = xw.TransverseDamper(
        gain_x=2/100, gain_y=2/100,
        zeta_range=wf.slicer.zeta_range,
        num_slices=wf.slicer.num_slices,
        bunch_spacing_zeta=wf.slicer.bunch_spacing_zeta,
        filling_scheme=filling_scheme,
        circumference=26658.8832,
    )

    # Monitor to record bunch statistics to HDF5 every 100 turns
    monitor = xw.CollectiveMonitor(
        base_file_name='sps_tune_shift',
        monitor_bunches=True, monitor_slices=False, monitor_particles=False,
        flush_data_every=100,
        stats_to_store=['mean_x', 'mean_y'],
        zeta_range=wf.slicer.zeta_range,
        num_slices=wf.slicer.num_slices,
        bunch_spacing_zeta=wf.slicer.bunch_spacing_zeta,
        filling_scheme=filling_scheme,
    )

    line = xt.Line([one_turn, wf, damper, monitor],
                   element_names=['one_turn', 'wake', 'damper', 'monitor'])
    line.particle_ref = xt.Particles(p0c=26e9)
    line.build_tracker()
    line.track(particles, num_turns=200)

Pipeline/MPI integration
------------------------

For MPI runs with ``xt.pipeline``, use ``xw.config_pipeline_for_wakes`` to wire
particles, wakes, dampers, and monitors. It reconfigures slicers per rank and
sets partner names automatically:

.. code-block:: python

    import xtrack as xt
    from mpi4py import MPI
    import xwakes as xw

    comm = MPI.COMM_WORLD
    pipeline_manager = xw.config_pipeline_for_wakes(
        particles=particles, line=line, communicator=comm)

    multitracker = xt.PipelineMultiTracker(
        branches=[xt.PipelineBranch(line=line, particles=particles)])
    multitracker.track(num_turns=10)

Pointers to worked scripts
--------------------------

- SPS tune shift (single and multi-bunch): ``xwakes/examples/000a_sps_tune_shift.py`` and ``000b_sps_tune_shift_multibunch.py``
- HLLHC instability against wake tables: ``xwakes/examples/001a_hllhc_instability_wake_table.py`` (single bunch) and ``001b_hllhc_instability_wake_table_multibunch.py``
- Wake construction and summation demos: ``xwakes/examples/001_many_resonators.py`` and ``002_wake_sum.py``
- Multibunch convolution/pipeline checks: ``xwakes/examples/convolution_multibunch/*``

These mirror the automated tests in ``xwakes/tests`` and are good starting
points to adapt to your machine and impedance model.

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
