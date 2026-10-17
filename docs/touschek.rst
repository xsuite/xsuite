Touschek scattering
===================

Touschek scattering describes single Coulomb scattering events between particles
in the same bunch. In low-emittance lepton rings, these events can transfer
transverse momentum into longitudinal momentum. Particles whose momentum
deviation exceeds the local momentum acceptance can then be lost, either
immediately or after tracking through the nonlinear lattice and aperture model.

The xfields Touschek workflow is managed by a
:class:`xfields.TouschekGenerator`, available as ``line.xfields.touschek``.
The computation is performed through the following steps:

- install passive :class:`xfields.TouschekMarker` elements with
  ``line.xfields.touschek.install_markers(at=...)``. Each marker represents
  the section from the preceding marker to itself; by default, a marker is
  also added at the end of the line so that the sections cover the whole ring;
- compute the local momentum acceptance at the marker locations with
  :meth:`xtrack.Line.get_local_momentum_acceptance`;
- configure the markers with ``line.xfields.touschek.configure(...)``, supplying
  the momentum acceptance, beam parameters and Monte Carlo settings;
- generate particles at each marker with
  ``line.xfields.touschek.generate(at=name)``, track them with
  ``line.track(..., ele_start=name, ele_stop=name, num_turns=...)``, and merge
  the samples with :meth:`xtrack.Particles.merge`. Calling
  ``line.xfields.touschek.analyse(particles)`` returns a
  :class:`xfields.TouschekResult` with scattering rates and lifetimes and
  tracking-based loss rates and lifetimes.

The configured markers are saved with the line, so generation can be reproduced
after a JSON round trip or split into independent jobs by marker and replica.
For a combined generation, tracking and analysis workflow, use
``line.xfields.touschek.run(n_turns=...)``.

The following example builds a small electron ring, inserts Touschek scattering
markers, computes the local momentum acceptance, configures the markers,
generates and tracks the scattered particles, and analyses the merged sample
to obtain the loss rate, lifetime and loss map.

See also: :doc:`Physics guide <physicsguide>`,
:class:`xfields.TouschekGenerator`, :class:`xfields.TouschekMarker`,
and :class:`xfields.TouschekResult`.

Example
-------

.. literalinclude:: generated_code_snippets/touschek_toy_ring.py
   :language: python
