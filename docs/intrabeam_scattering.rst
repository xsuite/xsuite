=====================
Intra-Beam Scattering
=====================

.. contents:: Table of Contents
    :depth: 3


Analytical Growth Rates
=======================

The following example illustrates how to obtain growth rates from Intra-Beam Scattering  in Xsuite.
The functionality is exposed through the `TwissTable` and can make use of two different formalism, ``Nagaitsev`` and ``Bjorken-Mtingwa``.
The former provides a computationally efficient approach but does not account for vertical dispersion, while the latter accounts for it but is slower.

See also: :meth:`xtrack.twiss.TwissTable.get_ibs_growth_rates`

.. literalinclude:: generated_code_snippets/ibs_rates_with_vdisp.py
   :language: python


IBS Kicks for Tracking
======================

When trying to study the interplay of IBS effects with others such as space charge, e-cloud, beamb-beam etc. analytical growth rates are not enough and tracking becomes necessary.
In Xfields beam elements are provided to model IBS tracking, which apply momenta kicks to particles.
Two kick elements are available:

- ``IBSAnalyticalKick`` (from `R. Bruce <https://journals.aps.org/prab/abstract/10.1103/PhysRevSTAB.13.091001>`_) for kicks based on analytical growth rates;
- ``IBSKineticKick`` (from `P. Zenkevich <https://www.sciencedirect.com/science/article/abs/pii/S0168900206000465>`_) for kicks based on diffusion and friction terms from the kinetic theory of gases.

The following example illustrates how to create a kick element, inserting and configuring it for tracking.
Refer to the :doc:`Reference manual<apireference>` for the full list of parameters and their explanation, and to the :doc:`Physics guide<physicsguide>` for full information.

See also: :meth:`xtrack.Line.configure_intrabeam_scattering`

.. literalinclude:: generated_code_snippets/ibs_kicks_tracking.py
   :language: python
