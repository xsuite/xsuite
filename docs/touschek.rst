Touschek scattering
===================

Touschek scattering describes single Coulomb scattering events between particles
in the same bunch. In low-emittance lepton rings, these events can transfer
transverse momentum into longitudinal momentum. Particles whose momentum
deviation exceeds the local momentum acceptance can then be lost, either
immediately or after tracking through the nonlinear lattice and aperture model.

The xfields Touschek workflow has three main steps:

- place :class:`xfields.TouschekScattering` elements at the longitudinal
  locations where the local Touschek rate should be sampled;
- compute the local momentum acceptance at those locations;
- configure a :class:`xfields.TouschekStudy` with
  ``line.xfields.touschek_configure(...)`` and call ``run(...)`` to obtain
  scattering rates and lifetimes, and, when tracking is enabled, tracking-based
  loss rates and lifetimes. Generated particle samples are retained in the
  result only when ``keep_particles=True`` is passed to ``run(...)``.

The following example builds a small electron ring, inserts Touschek scattering
markers, computes the local momentum acceptance, configures the Touschek study
through the ``line.xfields`` facade, tracks the generated scattered particles,
keeps the particle sample, and plots the resulting loss map.

See also: :doc:`Physics guide <physicsguide>`,
:class:`xfields.TouschekStudy`, and :class:`xfields.TouschekScattering`.

Example
-------

.. literalinclude:: generated_code_snippets/touschek_toy_ring.py
   :language: python
