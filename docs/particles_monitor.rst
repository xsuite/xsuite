.. _monitors:

Monitors
========

See also: :class:`xtrack.ParticlesMonitor`, :class:`xtrack.LastTurnsMonitor`, :class:`xtrack.BeamPositionMonitor`, :class:`xtrack.BeamProfileMonitor`, :class:`xtrack.BeamSizeMonitor`.

The easy way
------------

When starting a tracking simulation with the Xtrack Line object, the easiest
way of logging the coordinates of all particles for all turns is to enable the
default turn-by-turn monitor, as illustrated by the following example.
Note: this mode requires that ``particles.at_turn`` is ``0`` for all particles
at the beginning of the simulation.

.. literalinclude:: generated_code_snippets/quick_monitor.py
   :language: python


Custom monitors
---------------

In order to customize the monitor's behaviour,
a custom monitor object can be built and passed to the ``Line.track``
function.

Particles coordinates can be recorded only in a selected range of turns
by specifying ``start_at_turn`` and ``stop_at_turn``.
The monitoring can also be limited to a selected range of particles IDs,
by using the argument ``particle_id_range`` of the ``ParticlesMonitor`` class
to provide a tuple defining the range to be recorded. In that case the
``num_particles`` input of the monitor is omitted.

The example above is changed as follows:

.. code-block:: python

    ...

    monitor = xt.ParticlesMonitor(_context=context,
        particle_id_range=(5, 42),
        start_at_turn=5, # <-- first turn to monitor (including)
        stop_at_turn=15, # <-- last turn to monitor (excluding)
    )

    line.track(particles, num_turns=num_turns,
               turn_by_turn_monitor=monitor, # <-- pass the monitor here
    )

Now, ``line.record_last_track.x[3, 5]`` gives the x coordinates for the
particle 3 (which has the id 8) and the
recorded turn 5 (which is turn number 10)
The particle ids that are recorded can be inspected in ``line.record_last_track.particle_id``
and the turn indeces in ``line.record_last_track.at_turn``.


**Multi-frame particles monitor**

The particles monitor can also record periodically spaced intervals of turns (frames)
This feature can be activated by providing the arguments ``n_repetitions`` and
``repetition_period`` when creating the monitor.
In the following example, we record turns in range 5 to 10 (first frame),
range 25 to 30 (second frame) and range 45 to 50 (third frame).
Note that each frame consists of 5 turns since ``stop_at_turn`` is excluding.

.. code-block:: python

    monitor = xt.ParticlesMonitor(_context=context,
        num_particles=num_particles,
        start_at_turn=5,
        stop_at_turn=10,
        n_repetitions=3,      # <--
        repetition_period=20, # <--
    )

Now, the measured data are 3D array with the first index being the frame number.
For example, ``line.record_last_track.x[0, :, :]`` contains the recorded
x position for the first frame (turns 5, 6, 7, 8 and 9) and
``line.record_last_track.x[-1, :, 0]`` refers to the last frame and the first turn within,
which is turn number turn 25.
As before, the turn numbers recorded can be inspected with ``line.record_last_track.at_turn``.



Particles monitor as beam elements
----------------------------------

Particles monitors can be used as regular beam element to record the particle
coordinates at specific locations in the beam line. For this purpose they can be
inserted in the line, as illustrated in the following example.

.. literalinclude:: generated_code_snippets/monitors_as_beam_elements.py
   :language: python


As all Xtrack elements, the Particles Monitor has a track method and can be used
in stand-alone mode as illustrated in the following example.

.. code-block:: python

    # line.track(particles, num_turns=num_turns)
    for iturn in range(num_turns):
        monitor.track(particles)
        line.track(particles)



Last turns monitor
------------------

The :class:`xtrack.LastTurnsMonitor` records particle data in the last turns before respective particle loss
(or the end of tracking).

The idea is to use a rolling buffer instead of saving all the turns. This saves a lot of memory resources
when the interest lies only in the last few turns.
For each particle, the recorded data will cover up to ``n_last_turns*every_n_turns`` turns before it is lost (or the tracking ends).

.. code-block:: python

    monitor = LastTurnsMonitor(
        particle_id_range=(0, 5),  
        n_last_turns=5,            # amount of turns to store
        every_n_turns=3,           # only consider turns which are a multiples of this
    )

    ... # track

    monitor.at_turn[:,-1]  # turn number of each particle before it is lost (last turn alive)
    monitor.x[3,-2]        # x coordinate of particle 3 in one but last turn (-2)

The monitor provides the following data as 2D array of shape ``(num_particles, n_last_turns)``,
where the first index corresponds to the particle in ``particle_id_range``
and the second index corresponds to the turn (or every_n_turns) before the respective particle is lost:
``particle_id``, ``at_turn``, ``x``, ``px``, ``y``, ``py``, ``delta``, ``zeta``


.. _MonitorBPM:

Beam position monitor
---------------------

The :class:`xtrack.BeamPositionMonitor` records transverse beam positions,
i.e. it stores the x and y centroid positions of particles.
This can be useful for tune or beam-transfer-function diagnostics
as well as transverse schottky spectra.

The monitor allows for arbitrary sampling frequencies and can thus not only be used for
bunch positions, but also coasting beam positions. Higher sampling frequencies give
access to transverse beam oscillations at higher harmonics, which is especially useful
for schottky diagnostics.
Internally, the particle arrival time is used when determining the record index.
For coasting beams this ensures, that the centroid is computed considering all particles
which arrive at the monitor at the same time (as in a real-world measurement device), even
if some particles might have made more or less turns than the synchronous particle due to
a non-negligible momentum deviation.

.. math:: 
    i = f_{samp} \times \left(\frac{n-n_0}{f_{rev}} - \frac{\zeta}{\beta_0  c_0}\right)

where
:math:`f_{samp}` is the sampling frequency,
:math:`f_{rev}` is the revolution frequency,
:math:`n` is the current turn number and :math:`n_0` is the first turn recorded,
:math:`\zeta=(s-\beta_0\cdot c_0\cdot t)` is the longitudinal ``zeta`` coordinate of the particle,
:math:`\beta_0` is the relativistic beta factor of the particle
and :math:`c_0` is the speed of light.
For non-circular lines :math:`n` is always zero and :math:`f_{rev}` can be omitted.

Note that the index is rounded, i.e. the result array represents data of particles
equally distributed around the reference particle, which is useful for bunched beams.
For example, if the sampling frequency is twice the revolution frequency,
the first item contains data from particles in the range zeta/circumference = -0.25 .. 0.25,
the second item in the range 0.25 .. 0.75 and so on.

.. code-block:: python

    monitor = xt.BeamPositionMonitor(
        #particle_id_range=(5, 42),        # optional, defaults to all particles if not given
        start_at_turn=5, stop_at_turn=10,  # turn refers to the synchronous particle (at zeta=0)
        frev=1e6,                          # revolution frequency (only for circular lines)
        sampling_frequency=2e6,            # sampling frequency
    )

    ... # track

    print(monitor.count)   # waveform of number of particles (intensity)
    print(monitor.x_mean)  # waveform of horizontal centroid positions (alias monitor.x_cen)
    print(monitor.y_mean)  # waveform of vertical centroid positions (alias monitor.y_cen)

The result arrays can be understood as waveforms recorded at the specified sampling frequency.
In the special case where sampling frequency was set to the same value as the revolution frequency,
the indices are identical to the recorded turn numbers (of the synchronous particle).


Beam size monitor
-----------------

The :class:`xtrack.BeamSizeMonitor` records transverse beam sizes,
i.e. it stores the standard deviation of the particles x and y positions.

Like the :ref:`MonitorBPM` also the beam size monitor is based on particle arrival time and an arbitrary sampling frequency.

.. code-block:: python

    monitor = xt.BeamSizeMonitor(
        #particle_id_range=(5, 42),        # optional, defaults to all particles if not given
        start_at_turn=5, stop_at_turn=10,  # turn refers to the synchronous particle (at zeta=0)
        frev=1e6,                          # revolution frequency (only for circular lines)
        sampling_frequency=2e6,            # sampling frequency
    )

    ... # track

    print(monitor.count)   # waveform of number of particles (intensity)
    print(monitor.x_mean)  # waveform of horizontal centroid positions
    print(monitor.y_std)   # waveform of vertical position standard deviation (i.e. beam size)
    print(monitor.x_var)   # waveform of horizontal position variances



Beam profile monitor
--------------------


The :class:`xtrack.BeamProfileMonitor` records transverse beam profiles,
i.e. it stores the number of particles on a defined raster (like a histogram).

Like the :ref:`MonitorBPM` also the beam profile monitor is based on particle arrival time and an arbitrary sampling frequency.

.. code-block:: python

    monitor = xt.BeamProfileMonitor(
        #particle_id_range=(5, 42),        # optional, defaults to all particles if not given
        start_at_turn=5, stop_at_turn=10,  # turn refers to the synchronous particle (at zeta=0)
        frev=1e6,                          # revolution frequency (only for circular lines)
        sampling_frequency=2e6,            # sampling frequency
        n=100,                             # number of bins in the profile (can also specify nx and ny separately)
        x_range=(-4,2),                    # save horizontal profile extending from -4 to 2
        y_range=5,                         # shorthand for (-2.5, 2.5)
    )

    ... # track

    print(monitor.x_edges)      # the bin edges
    print(monitor.x_grid)       # the bin midpoints
    print(monitor.x_intensity)  # the actual profile (particle count per bin)

The recorded profiles are 2D arrays of shape ``(sample_size, n)``
where ``sample_size = round(( stop_at_turn - start_at_turn ) * sampling_frequency / frev)``.
I.e. ``monitor.x_intensity[0,:]`` is the first recorded profile and ``monitor.x_intensity[-1,:]`` the last.


