============
Pipeline for multibunch simulations
============

Xsuite can be used to simulate multiple bunches interacting through collective forces, such as beam-beam interactions or wakefields.

The pipeline algorithm implemented allows to setup the required communication between multiple Particles instances using MPI or not. The Particles instances as well as the Elements in the line that require communication through the pipeline are attributed a uniquely defined name. 

The pipeline algorithm is detailed in https://doi.org/10.1016/j.cpc.2019.06.006. 

The following example illustrates how to configure and run a multibunch simulation with beam-beam interactions.

Example
=======

.. literalinclude:: generated_code_snippets/spacecharge.py
   :language: python


