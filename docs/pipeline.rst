============
Pipeline for multibunch simulations
============

Xsuite can be used to simulate multiple bunches interacting through collective forces, such as beam-beam interactions or wakefields. A so-called MultiTracker handles the tracking of multiple Particles objects through their own line (e.g. each of the two rings in a circular collider). Each Particles object and its line is refered to as a branch. The Multitracker will iteratively track its branches until an element which requires communication is reached (e.g. a stron-strong beam-beam collision, where the information on the other beam's charge distribution is required). At this point it will establish communication between the branches that need to exchange information and resume the tracking.

The exchange of information is handeled by the PipelineManager, which is aware of the required communications. (e.g. in a collider with many bunches and many iteractions points, such as the LHC, the Pipeline manager knows which bunch colliders with which and where.) The PipelineManager uses a communicator which can be MPI, but can also be a dummy communicator if MPI is not available/needed.

It is important that the Particles instances as well as the Elements in the line that require communication through the pipeline are attributed a uniquely defined name. 

The pipeline algorithm is detailed in https://doi.org/10.1016/j.cpc.2019.06.006.

The following example illustrates how to configure and run a simulation with two bunches colliding at two interaction points using MPI. It must be run like a MPI application

mpirun -np 2 python example.py

Example
=======

.. literalinclude:: generated_code_snippets/pipeline.py
   :language: python


