===========================================
Compensate radiation energy loss (tapering)
===========================================

Xtrack Tracker provides a method to compensate the energy loss due to the synchrotron
radiation. This is done by configuring the phase of the RF cavities to compensate
for the energy loss, and adapting the strength of the magnets to the local momentum of the
particle on the closed orbit. This is illustrated in the following example:

.. literalinclude:: generated_code_snippets/taper.py
   :language: python
