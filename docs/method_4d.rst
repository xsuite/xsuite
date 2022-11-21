===============================================
4d method for ``twiss`` and ``build_particles``
===============================================

When the RF cavities are disabled or not included in the lattice or when the
longitudinal motion is artificially frozen, the one-turn matrix of the line is
singular, and it is no possible to use the standard method for the twiss
calculation and to generate particles distributions matched to the lattice.
In these cases, the "4d" method can be used, as illustrated in the following
examples:

.. literalinclude:: generated_code_snippets/method_4d.py
   :language: python