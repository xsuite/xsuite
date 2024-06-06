Compensate radiation energy loss (tapering)
===========================================

Xtrack Line provides a method to compensate the energy loss due to the synchrotron
radiation. This is done by configuring the phase of the RF cavities to compensate
for the energy loss, and adapting the strength of the magnets to the local momentum of the
particle on the closed orbit. This is illustrated in the following example.

See also: :meth:`xtrack.Line.compensate_radiation_energy_loss`

.. literalinclude:: generated_code_snippets/taper.py
   :language: python
