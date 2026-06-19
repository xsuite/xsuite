===============
Reference guide
===============

.. contents:: Table of Contents
    :depth: 3


Beam elements (xtrack)
======================

Marker
------

.. autoclass:: xtrack.Marker
    :members:
    :member-order: bysource

Drift
-----

.. autoclass:: xtrack.Drift
    :members:
    :member-order: bysource

Bend
----

.. autoclass:: xtrack.Bend
    :members:
    :member-order: bysource

The definition of the misalignment parameters (``rot_s_rad``,
``rot_s_rad_no_frame``, ``rot_x_rad``, ``rot_y_rad``, ``shift_x``, ``shift_y``, ``shift_s``)
can be found in the :ref:`element misalignment section <misalignment_label>`.

.. figure:: ./physics_manual/figures/sbend_edge_definition.png
    :align: center
    :width: 70%

    Sector bend (figure from MAD-X manual).

.. list-table:: Naming convention
   :header-rows: 1
   :align: center

   * - Symbol
     - Xsuite attribute name
   * - :math:`L`
     - ``length``
   * - :math:`\alpha`
     - ``angle``
   * - :math:`h = 1/\rho`
     - ``angle / length``
   * - :math:`e_1`
     - ``edge_entry_angle``
   * - :math:`e_2`
     - ``edge_exit_angle``

RBend
-----

.. autoclass:: xtrack.RBend
    :members:
    :member-order: bysource

The definition of the misalignment parameters (``rot_s_rad``,
``rot_s_rad_no_frame``, ``rot_x_rad``, ``rot_y_rad``, ``shift_x``, ``shift_y``, ``shift_s``)
can be found in the :ref:`element misalignment section <misalignment_label>`.

.. figure:: ./physics_manual/figures/rbend.png
    :align: center
    :width: 80%

    Rectangular with arbitrary face angles and arbitrary placement with respect to
    the reference trajectory.


.. list-table:: Naming convention
   :header-rows: 1
   :align: center

   * - Symbol
     - Xsuite attribute name
   * - :math:`L_\text{straight}`
     - ``length_straight``
   * - :math:`L_\text{curv}`
     - ``length`` (read-only, computed internally)
   * - :math:`\alpha = \alpha_\text{in} + \alpha_\text{out}`
     - ``angle``
   * - :math:`\alpha_\text{diff} = \alpha_\text{out} - \alpha_\text{in}`
     - ``rbend_angle_diff``
   * - :math:`x_\text{mid}`
     - ``rbend_shift`` (+ half of the sagitta if ``rbend_compensate_sagitta`` is ``True``)
   * - :math:`e_1`
     - ``edge_entry_angle``
   * - :math:`e_2`
     - ``edge_exit_angle``

Quadrupole
----------

.. autoclass:: xtrack.Quadrupole
    :members:
    :member-order: bysource

The definition of the misalignment parameters (``rot_s_rad``,
``rot_s_rad_no_frame``, ``rot_x_rad``, ``rot_y_rad``, ``shift_x``, ``shift_y``, ``shift_s``)
can be found in the :ref:`element misalignment section <misalignment_label>`.

Sextupole
---------

.. autoclass:: xtrack.Sextupole
    :members:
    :member-order: bysource

The definition of the misalignment parameters (``rot_s_rad``,
``rot_s_rad_no_frame``, ``rot_x_rad``, ``rot_y_rad``, ``shift_x``, ``shift_y``, ``shift_s``)
can be found in the :ref:`element misalignment section <misalignment_label>`.

Octupole
---------

.. autoclass:: xtrack.Octupole
    :members:
    :member-order: bysource

The definition of the misalignment parameters (``rot_s_rad``,
``rot_s_rad_no_frame``, ``rot_x_rad``, ``rot_y_rad``, ``shift_x``, ``shift_y``, ``shift_s``)
can be found in the :ref:`element misalignment section <misalignment_label>`.

Multipole
---------

.. autoclass:: xtrack.Multipole
    :members:
    :member-order: bysource

The definition of the misalignment parameters (``rot_s_rad``,
``rot_s_rad_no_frame``, ``rot_x_rad``, ``rot_y_rad``, ``shift_x``, ``shift_y``, ``shift_s``)
can be found in the :ref:`element misalignment section <misalignment_label>`.

UniformSolenoid
---------------

.. autoclass:: xtrack.UniformSolenoid
    :members:
    :member-order: bysource

The definition of the misalignment parameters (``rot_s_rad``,
``rot_s_rad_no_frame``, ``rot_x_rad``, ``rot_y_rad``, ``shift_x``, ``shift_y``, ``shift_s``)
can be found in the :ref:`element misalignment section <misalignment_label>`.

VariableSolenoid
----------------

.. autoclass:: xtrack.VariableSolenoid
    :members:
    :member-order: bysource

The definition of the misalignment parameters (``rot_s_rad``,
``rot_s_rad_no_frame``, ``rot_x_rad``, ``rot_y_rad``, ``shift_x``, ``shift_y``, ``shift_s``)
can be found in the :ref:`element misalignment section <misalignment_label>`.

Cavity
------

.. autoclass:: xtrack.Cavity
    :members:
    :member-order: bysource

The definition of the misalignment parameters (``rot_s_rad``,
``rot_s_rad_no_frame``, ``rot_x_rad``, ``rot_y_rad``, ``shift_x``, ``shift_y``, ``shift_s``)
can be found in the :ref:`element misalignment section <misalignment_label>`.

CrabCavity
----------

.. autoclass:: xtrack.CrabCavity
    :members:
    :member-order: bysource

The definition of the misalignment parameters (``rot_s_rad``,
``rot_s_rad_no_frame``, ``rot_x_rad``, ``rot_y_rad``, ``shift_x``, ``shift_y``, ``shift_s``)
can be found in the :ref:`element misalignment section <misalignment_label>`.

RFMultipole
-----------

.. autoclass:: xtrack.RFMultipole
    :members:
    :member-order: bysource

The definition of the misalignment parameters (``rot_s_rad``,
``rot_s_rad_no_frame``, ``rot_x_rad``, ``rot_y_rad``, ``shift_x``, ``shift_y``, ``shift_s``)
can be found in the :ref:`element misalignment section <misalignment_label>`.

ReferenceEnergyIncrease
-----------------------

.. autoclass:: xtrack.ReferenceEnergyIncrease
    :members:
    :member-order: bysource


Exciter
-------

.. autoclass:: xtrack.Exciter
    :members:
    :member-order: bysource

AC-Dipole
---------
.. autoclass:: xtrack.ACDipole
    :members:
    :member-order: bysource

Elens
-----

.. autoclass:: xtrack.Elens
    :members:
    :member-order: bysource

NonLinearLens
-------------

.. autoclass:: xtrack.NonLinearLens
    :members:
    :member-order: bysource

ElectronCooler
--------------

.. autoclass:: xtrack.ElectronCooler
    :members:
    :member-order: bysource

Wire
----

.. autoclass:: xtrack.Wire
    :members:
    :member-order: bysource

FirstOrderTaylorMap
-------------------

.. autoclass:: xtrack.FirstOrderTaylorMap
    :members:
    :member-order: bysource

SecondOrderTaylorMap
--------------------

.. autoclass:: xtrack.SecondOrderTaylorMap
    :members:
    :member-order: bysource

LineSegmentMap
--------------

.. autoclass:: xtrack.LineSegmentMap
    :members:
    :member-order: bysource

Translation
-----------

.. autoclass:: xtrack.Translation
    :members:
    :member-order: bysource

Rotation
--------
.. autoclass:: xtrack.Rotation
    :members:
    :member-order: bysource

TimeDelay
---------
.. autoclass:: xtrack.TimeDelay
    :members:
    :member-order: bysource

XYShift
-------

.. autoclass:: xtrack.XYShift
    :members:
    :member-order: bysource

SRotation
----------

.. autoclass:: xtrack.SRotation
    :members:
    :member-order: bysource

XRotation
---------

.. autoclass:: xtrack.XRotation
    :members:
    :member-order: bysource

YRotation
---------

.. autoclass:: xtrack.YRotation
    :members:
    :member-order: bysource

ZetaShift
---------

.. autoclass:: xtrack.ZetaShift
    :members:
    :member-order: bysource


LimitEllipse
------------

.. autoclass:: xtrack.LimitEllipse
    :members:
    :member-order: bysource

LimitRect
---------

.. autoclass:: xtrack.LimitRect
    :members:
    :member-order: bysource

LimitRectEllipse
----------------

.. autoclass:: xtrack.LimitRectEllipse
    :members:
    :member-order: bysource

LimitRacetrack
--------------

.. autoclass:: xtrack.LimitRacetrack
    :members:
    :member-order: bysource

LimitPolygon
------------

.. autoclass:: xtrack.LimitPolygon
    :members:
    :member-order: bysource

LongitudinalLimitRect
---------------------

.. autoclass:: xtrack.LongitudinalLimitRect
    :members:
    :member-order: bysource

ParticlesMonitor
----------------

.. autoclass:: xtrack.ParticlesMonitor
    :members:
    :member-order: bysource

LastTurnsMonitor
----------------

.. autoclass:: xtrack.LastTurnsMonitor
    :members:
    :member-order: bysource

BeamPositionMonitor
----------------

.. autoclass:: xtrack.BeamPositionMonitor
    :members:
    :member-order: bysource

BeamProfileMonitor
----------------

.. autoclass:: xtrack.BeamProfileMonitor
    :members:
    :member-order: bysource

BeamSizeMonitor
----------------

.. autoclass:: xtrack.BeamSizeMonitor
    :members:
    :member-order: bysource



Beam elements (xfields)
======================


Beam-beam Bi-Gaussian 2D
------------------------

.. autoclass:: xfields.BeamBeamBiGaussian2D
    :members:
    :member-order: bysource

Beam-beam Bi-Gaussian 3D
------------------------

.. autoclass:: xfields.BeamBeamBiGaussian3D
    :members:
    :member-order: bysource

Space Charge Bi-Gaussian
------------------------

.. autoclass:: xfields.SpaceChargeBiGaussian
    :members:
    :member-order: bysource

Space Charge 3D
---------------

.. autoclass:: xfields.SpaceCharge3D
    :members:
    :member-order: bysource

Intra-Beam Scattering Kicks
---------------------------

.. autoclass:: xfields.IBSAnalyticalKick
    :members:
    :member-order: bysourcef

.. autoclass:: xfields.IBSKineticKick
    :members:
    :member-order: bysource

.. _xwakes_section:

Beam elements (xwakes)
======================

See also the :ref:`Xwakes section <xwakes_user_guide_section>` in User's guide.

.. include:: wakedefs.rst

WakeResonator
-------------

.. autoclass:: xwakes.WakeResonator
    :members:
    :member-order: bysource

WakeThickResistiveWall
----------------------

.. autoclass:: xwakes.WakeThickResistiveWall
    :members:
    :member-order: bysource

WakeFromTable
-------------

.. autoclass:: xwakes.WakeFromTable
    :members:
    :member-order: bysource

Wake
----

.. autoclass:: xwakes.Wake
    :members:
    :member-order: bysource

Utilities
---------

.. autofunction:: xwakes.read_headtail_file

.. _misalignment_label:

Element misalignment
====================

Most Xsuite beam elements support misalignments. The different misalignment
parameters are defined as illustrated in the following table and figures.

See also the :ref:`misalignment section <misalignment_example_label>` in User's guide.

.. list-table:: Naming convention
   :header-rows: 1
   :align: center

   * - Symbol
     - Xsuite attribute name
   * - :math:`\Delta s_\text{anchor}`
     - ``rot_shift_anchor``
   * - :math:`\Delta \psi`
     - ``rot_s_rad`` or ``rot_s_rad_no_frame``
   * - :math:`\Delta \theta`
     - ``rot_y_rad``
   * - :math:`\Delta \phi`
     - ``rot_x_rad``
   * - :math:`\Delta x`
     - ``shift_x``
   * - :math:`\Delta y`
     - ``shift_y``
   * - :math:`\Delta s`
     - ``shift_s``


.. figure:: ./physics_manual/figures/align_roll.png
    :align: center
    :width: 50%

    Misalignment in the the x-y plane.

.. figure:: ./physics_manual/figures/align_yaw.png
    :align: center
    :width: 70%

    Misalignment in the the s-x plane.

.. figure:: ./physics_manual/figures/align_pitch.png
    :align: center
    :width: 70%

    Misalignment in the the s-y plane.


.. _environment-api-reference:

xtrack.Environment class
========================

The Xsuite environment manages variables and elements that can be shared by
different lines and can be used to create elements and line objects. See
:ref:`Xsuite environment <environment-user-guide>` in the User's guide for
tutorial examples.

.. contents::
    :depth: 2
    :local:

.. include:: environment_api.rst

Environment containers
----------------------

.. autoclass:: xtrack.environment.EnvVars
    :members:
    :member-order: bysource

.. autoclass:: xtrack.environment.EnvElements
    :members:
    :member-order: bysource

.. autoclass:: xtrack.environment.EnvParticles
    :members:
    :member-order: bysource

.. autoclass:: xtrack.environment.EnvLines
    :members:
    :member-order: bysource

.. autoclass:: xtrack.environment.EnvRef
    :members:
    :member-order: bysource

.. autoclass:: xtrack.environment.EnvParticleRef
    :members:
    :member-order: bysource

.. autoclass:: xtrack.environment.EnvXfields
    :members:
    :member-order: bysource

.. _varstable-api-reference:

VarsTable
~~~~~~~~~

The :class:`xtrack.environment.VarsTable` class is the table returned by
environment variable table methods such as ``env.vars.get_table()``.

See :doc:`Working with tables <tables>` in the User's guide for an overview
of the features offered by Table objects.

.. autoclass:: xtrack.environment.VarsTable
    :members:
    :inherited-members:
    :member-order: alphabetical

.. _line-api-reference:

xtrack.Line class
=================

The Xsuite ``Line`` class represents an ordered sequence of beam elements used
for tracking, optics calculations, matching, and lattice manipulation. A line
stores the sequence of element names and resolves them in its associated
environment, available as ``line.env``. The environment owns the named elements,
variables, particles, and other lines that can be shared across lattice
descriptions.

A line can be in normal mode or in compose mode, as indicated by ``line.mode``.
In compose mode, elements are placed with ``line.place(...)`` and
``line.new(...)`` by their longitudinal position and/or relative to each other;
the line is resolved later with ``line.end_compose()``.

For most new lattices it is convenient to create an
:class:`xtrack.Environment` and build lines with ``env.new_line(...)``. The
``Line`` constructor can also be used directly when the element objects and
their order are already available. See :ref:`Lines <line-user-guide>` in the
User's guide for tutorial examples on building and inspecting lines.

.. contents::
    :depth: 2
    :local:

.. include:: line_api.rst

.. _linetable-api-reference:

LineTable class
---------------

The :class:`xtrack.line.LineTable` class is the table returned by
:meth:`xtrack.Line.get_table`.

See :doc:`Working with tables <tables>` in the User's guide for an overview
of the features offered by Table objects.

.. autoclass:: xtrack.line.LineTable
    :members:
    :inherited-members:
    :member-order: alphabetical

.. _track_method_label:

Track
=====
See also: :doc:`Single particle tracking <singlepart>`,
:doc:`Tracking with collective elements <collective>`.

.. automethod:: xtrack.Line.track


.. _twiss_method_label:
.. _twiss-api-reference:

Twiss
=====

See also: :ref:`Twiss <twiss-user-guide>` in the User's guide.

.. automethod:: xtrack.Line.twiss

.. _twisstable-api-reference:

TwissTable class
----------------

The :class:`xtrack.TwissTable` class is the table returned by
:meth:`xtrack.Line.twiss`.

See :doc:`Working with tables <tables>` in the User's guide for an overview
of the features offered by Table objects.

.. autoclass:: xtrack.TwissTable
    :members:
    :inherited-members:
    :member-order: alphabetical

.. _survey_method_label:
.. _survey-api-reference:

Survey
======

See also: :ref:`Survey <survey-user-guide>` and
:doc:`Working with tables <tables>` in the User's guide.

.. automethod:: xtrack.Line.survey

.. _surveytable-api-reference:

SurveyTable class
-----------------

The :class:`xtrack.survey.SurveyTable` class is the table returned by
:meth:`xtrack.Line.survey`.

See :doc:`Working with tables <tables>` in the User's guide for an overview
of the features offered by Table objects.

.. autoclass:: xtrack.survey.SurveyTable
    :members:
    :inherited-members:
    :member-order: alphabetical

Match
=====

See also: :doc:`Match<match>` in the User's guide. 

.. automethod:: xtrack.Line.match

.. _optimize-api-reference:

.. autoclass:: xdeps.Optimize
    :members:
    :member-order: bysource


.. _vary_target_label:

Vary and Target
---------------

.. autoclass:: xtrack.Vary
    :members:
    :member-order: bysource

.. autoclass:: xtrack.VaryList
    :members:
    :member-order: bysource

.. autoclass:: xtrack.Target
    :members:
    :member-order: bysource

.. autoclass:: xtrack.TargetSet
    :members:
    :member-order: bysource

.. autoclass:: xtrack.TargetRelPhaseAdvance
    :members:
    :member-order: bysource


Trajectory correction
=====================

.. autoclass:: xtrack.TrajectoryCorrection
    :members:
    :member-order: bysource


.. _build_particles_method_label:

Build particles
===============

See also: :doc:`Working with Particles objects <particlesmanip>`.

.. automethod:: xtrack.Line.build_particles


Particles class
===============

Xsuite Particles classes, including the default xtrack.Particles class, expose
the API described in the following (for more info on how to manipulate Particles
objects, see the :doc:`Particles section in the user's guide <particlesmanip>`).


.. autoclass:: xtrack.Particles
    :members:
    :inherited-members:
    :member-order: bysource


Generation of particles distributions
=====================================

See also :doc:`Particles section in the user's guide <particlesmanip>`.

Gaussian bunch generation (6D)
------------------------------

.. autofunction:: xpart.generate_matched_gaussian_bunch

Longitudinal coordinates generation
-----------------------------------

.. autofunction:: xpart.generate_longitudinal_coordinates

Normalized transverse coordinates generation
--------------------------------------------

Gaussian
~~~~~~~~

.. autofunction:: xpart.generate_2D_gaussian

Polar grid
~~~~~~~~~~

.. autofunction:: xpart.generate_2D_polar_grid

Uniform circular sector
~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: xpart.generate_2D_uniform_circular_sector

Pencil
~~~~~~

.. autofunction:: xpart.generate_2D_pencil

.. autofunction:: xpart.generate_2D_pencil_with_absolute_cut

.. _table-api-reference:

Table class
===========

The :class:`xtrack.Table` class is the base table used by xtrack table outputs
and provides selection, display, and serialization helpers. Row and column
selection is available through the inherited :attr:`~xdeps.Table.rows` and
:attr:`~xdeps.Table.cols` accessors.

See :ref:`Working with tables <tables-user-guide>` in the User's guide for
tutorial examples.

.. autoclass:: xtrack.Table
    :members:
    :inherited-members:
    :member-order: alphabetical

Table subclasses
----------------

The following xtrack table classes inherit from :class:`xtrack.Table`:

- :class:`xtrack.environment.VarsTable`
- :class:`xtrack.line.LineTable`
- :class:`xtrack.TwissTable`
- :class:`xtrack.survey.SurveyTable`

Table row and column accessors
------------------------------

The :attr:`xtrack.Table.rows` and :attr:`xtrack.Table.cols` properties return
accessor objects exposing row-selection and column-selection helpers.

.. autoclass:: xdeps.table._RowView
    :members:
    :member-order: alphabetical

.. autoclass:: xdeps.table._ColView
    :members:
    :member-order: alphabetical

CPU and GPU contexts
====================

See also :doc:`Getting Started Guide <singlepart>`

Xsuite supports different plaforms allowing the exploitation of different kinds of hardware (CPUs and GPUs).
A context is initialized by instanciating objects from one of the context classes available Xobjects, which is then passed to the other Xsuite components (see example in :doc:`Getting Started Guide <gettingstarted>`).
Contexts are interchangeable as they expose the same API.
Custom kernel functions can be added to the contexts. General source code with annotations can be provided to define the kernels, which is then automatically specialized for the chosen platform (see :doc:`dedicated section <autogeneration>`).

Three contexts are presently available:

 - The :ref:`Cupy context<cupy_context>`, based on `cupy`_-`cuda`_ to run on NVidia GPUs
 - The :ref:`Pyopencl context<pyopencl_context>`, bases on `PyOpenCL`_, to run on CPUs or GPUs throught PyOPENCL library.
 - The :ref:`CPU context<cpu_context>`, to use conventional CPUs

The corresponfig API is described in the following subsections.

.. _cupy: https://cupy.dev
.. _cuda: https://developer.nvidia.com/cuda-zone
.. _PyOpenCL: https://documen.tician.de/pyopencl/


.. _cupy_context:

Cupy context
-------------

.. autoclass:: xobjects.ContextCupy
    :members:
    :member-order: bysource
    :inherited-members:

.. _pyopencl_context:

PyOpenCL context
----------------
.. autoclass:: xobjects.ContextPyopencl
    :members:
    :member-order: bysource
    :inherited-members:


.. _cpu_context:

CPU context
-----------

.. autoclass:: xobjects.ContextCpu
    :members:
    :member-order: bysource
    :inherited-members:

Configuration tools
===================

xtrack.Multisetter class
------------------------

See also: :doc:`Fast lattice changes<fast_lattice_changes>`

.. autoclass:: xtrack.MultiSetter
    :members:
    :member-order: bysource

Space charge configuration
--------------------------

See also: :doc:`Space charge <spacechargeauto>`

.. autofunction:: xfields.install_spacecharge_frozen

.. autofunction:: xfields.replace_spacecharge_with_quasi_frozen

.. autofunction:: xfields.replace_spacecharge_with_PIC

Loss location refinement
------------------------

See also: :doc:`Loss location refinement <collimation>`

.. autoclass:: xtrack.LossLocationRefinement
    :members:
    :member-order: bysource
