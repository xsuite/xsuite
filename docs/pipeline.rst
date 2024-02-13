Pipeline for multibunch simulations
===================================

Xsuite can be used to simulate multiple bunches interacting through collective forces, such as beam-beam interactions or wakefields. The :class:`xtrack.pipeline.MultiTracker` handles the tracking of multiple :class:`xpart.particles.Particles` objects through their own :class:`xtrack.Line` (e.g. each of the two rings in a circular collider). Each Particles instance and its Line make a :class:`xtrack.pipeline.Branch`. The MultiTracker will iteratively track its branches until an :class:`xtrack.beam_elements.Element` which requires communication is reached (e.g. a strong-strong beam-beam collision, where information about the other beam's charge distribution is required). At this point the MultiTracker will use the :class:`xtrack.pipeline.PipelineManager` to establish communication between the branches that need to exchange information. If the communication cannot take place, e.g. because one of the two branches is not ready, the Multitracker resumes tracking with another branch.

The PipelineManager is aware of the communication required by the different Elements and the different Particles instances (e.g. in a collider with many bunches and many interactions points, the PipelineManager knows which bunch collides with which and where.) By default the PipelineManager uses a dummy communicator which does not require MPI, but an MPI communicator can be provided instead thus enabling tracking on multiple CPUs.

It is important that the Particles instances as well as the Element instances in the line that require communication through the pipeline are attributed a uniquely defined name. 

The pipeline algorithm is detailed in https://doi.org/10.1016/j.cpc.2019.06.006.

The following example illustrates how to configure and run a simulation with two bunches colliding at two interaction points using MPI. It must be run like a MPI application

.. code-block:: bash

    mpirun -np 2 python example.py

Example
-------

.. literalinclude:: generated_code_snippets/pipeline.py
   :language: python

.. figure:: figures/beambeam_sigmapi.png
    :width: 80%
    :align: center

If the communicator is not specified when instantiating the PipelineManager, it will not use MPI:

.. code-block:: python

    pipeline_manager = xt.PipelineManager()
