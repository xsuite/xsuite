==================
Particles monitors
==================

.. contents:: Table of Contents
    :depth: 3

See also: :class:`xtrack.ParticlesMonitor`, :class:`xtrack.LastTurnsMonitor`.

The easy way
============

When starting a tracking simulation with the Xtrack Tracker object, the easiest
way of logging the coordinates of all particles for all turns is to enable the
default turn-by-turn monitor, as illustrated by the following example.
Note: this mode requires that ``particles.at_turn`` is ``0`` for all particles
at the beginning of the simulation.

.. literalinclude:: generated_code_snippets/quick_monitor.py
   :language: python

Custom particles monitor
========================

In order to record the particles coordinates only in a selected range of turns,
a custom monitor object can be built and passed to the ``Tracker.track``
function, as illustrated by the following example.

.. literalinclude:: generated_code_snippets/custom_monitor.py
   :language: python

The monitoring can also be limited to a selected range of particles IDs,
by using the argument ``particle_id_range`` of the ``ParticlesMonitor`` class
to provide a tuple defining the range to be recorded. In that case the
``num_particles`` input of the monitor is omitted.

Multi-frame particles monitor
=============================

The particles monitor can record periodically spaced intervals of turns (frames)
This feature can be activated by providing the arguments ``n_repetitions`` and
``repetition_period`` when creating the monitor.

.. literalinclude:: generated_code_snippets/multiframe_monitor.py
   :language: python

Particles monitor as beam elements
==================================

Particles monitors can be used as regular beam element to record the particle
coordinates at specific locations in the beam line. For this purpose they can be
inserted in the line, as illustrated in the following example.

.. literalinclude:: generated_code_snippets/monitors_as_beam_elements.py
   :language: python

Particles monitor in stand-alone mode
=====================================

As all Xtrack elements, the Particles Monitor has a track method and can be used
in stand-alone mode as illustrated in the following example.

.. literalinclude:: generated_code_snippets/monitor_standalone.py
   :language: python