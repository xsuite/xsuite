================
Unit conventions
================

Xtrack follows a mostly SI-based convention, with accelerator-specific
exceptions for particle energies and momenta. The elementary charge :math:`e`
is the unit charge, and :math:`c = 1` is assumed.

.. note::
   The following are general conventions adopted for Xsuite, however units
   should always be documented on elements and APIs directly. This page should
   especially serve as a guideline for the creation of new elements and APIs.

Core quantities
===============

.. list-table::
   :header-rows: 1

   * - Quantity
     - Unit
   * - Length, position
     - :math:`\text{m}`
   * - Time
     - :math:`\text{s}`
   * - Energy
     - :math:`e\text{V}`
   * - Momentum
     - :math:`e\text{V}/c = e\text{V}`
   * - Mass
     - :math:`e\text{V}/c^2 = e\text{V}`
   * - Charge
     - :math:`e`
   * - Voltage
     - :math:`\text{V}`
   * - Magnetic field strength
     - :math:`\text{m}^{-n}`, with :math:`n = 1` for dipole, :math:`n = 2` for quadrupole, etc.
   * - Frequency
     - :math:`\text{Hz}`
   * - Geometric angle, phase advance
     - :math:`\text{rad}`
   * - RF phase
     - :math:`{}^{\circ}`
