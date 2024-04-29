====================
IntraBeam Scattering
====================

.. contents:: Table of Contents
    :depth: 3

Analytical Growth Rates
=======================

The following example illustrates how to obtain IntraBeam Scattering growth rates in Xsuite.
The functionality is exposed through the `TwissTable` and can make use of two different formalism, ``Nagaitsev`` and ``Bjorken-Mtingwa``.
The former provides a computationally efficient approach but does not account for vertical dispersion, while the latter accounts for it but is slower.

See also: :meth:`xtrack.twiss.TwissTable.get_ibs_growth_rates`

.. literalinclude:: generated_code_snippets/ibs_rates_with_vdisp.py
   :language: python
