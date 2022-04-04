==================
Particles monitors
==================

.. contents:: Table of Contents
    :depth: 3

The easy way
============

When starting a tracking simulation with the Xtrack Tracker object, the easiest
way of logging the coordinates of all particles for all turns is to enable the
default turn-by-turn monitor, as illustrated by the following example.
Note: this mode requires that ```particles.at_turn``` is ```0``` for all particles
at the beginning of the simulation.

.. literalinclude:: generated_code_snippets/quick_monitor.py
   :language: python

Custom particles monitor
========================

In order to record the particles coordinates only in a selecter range of turns
a custom monitor object can be built and passed to the ```Tracker.track```
function, as illustrated by the following example.

.. literalinclude:: generated_code_snippets/custom_monitor.py
   :language: python

The monitoring can also be limited to a selected range of particles IDs,
by using the argument ```particle_id_range``` of the ```ParticlesMonitor``` class
to provide a tuple defining the range to be recorded. In that case the
```num_particles``` input of the monitor is omitted.

Multi-frame particles monitor
=============================

.. literalinclude:: generated_code_snippets/multiframe_monitor.py
   :language: python

Particles monitor as beam elements
==================================

.. literalinclude:: generated_code_snippets/monitors_as_beam_elements.py
   :language: python

Particles monitor in stand-alone mode
=====================================

.. literalinclude:: generated_code_snippets/monitor_standalone.py
   :language: python