Combined CPU - GPU simulations
==============================

When performing simulations on GPU contexts, it is possible to execute on CPU
the computation for specific beam elements, for example PyHEADTAIL elements
that do not support the Xsuite GPU contexts. For that purpose, one needs to set
a ```needs_cpu``` flag on the concerned elements before inserting them in an Xtrack
line. This instructs the Xtrack tracker to handle the required data transfers.

Presently PyHEADTAIL elements are not able to skip lost particles in
the Xtrack Particles objects. This can be handled by setting the flag
```needs_hidden_lost_particles```, which instructs the Xtrack tracker to
temporarily hide the lost particles for the concerned elements.

The following example shows a simulation including the SPS lattice elements,
space-charge elements and wakefields. The lattice tracking and the spacecharge
calculations are performed on GPU with Xtrack/Xfields while the wakefield
computation is performed on CPU with PyHEADTAIL.

.. literalinclude:: generated_code_snippets/combined_cpu_gpu.py
   :language: python