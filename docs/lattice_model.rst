Configure lattice model
=======================

.. contents:: Table of Contents
    :depth: 3

Magnet models and integrators
-----------------------------

Magnetic elements are modeled using symplectic integrators. Users can choose
among different "models," which correspond to various splitting schemes of
the underlying Hamiltonian, and different "integrators," which define the
integration method. It is also possible specify the desired number of kicks (in
case the desired number of kicks is incompatible with the chosen integration scheme,
the number of kicks is automatically increased to the next compatible value).

The list of available models and integrators for a given element or element type
be obtained by calling the methods ``Element.get_available_models()`` and
``Element.get_available_integrators()``, respectively. Information about the different
models and integrators is available in the section "Symplectic integrators" of
the :doc:`Xsuite Physics Guide<physicsguide>`.

The ``Line.set(...)`` method can be used to set the model, integrator and number of
for several elements in a single call.

These features are illustrated in the following example:

.. literalinclude:: generated_code_snippets/models_integrators.py
   :language: python

.. _misalignment_example_label:

Apply misalignments (tilt, shift) to elements
---------------------------------------------

Tilt and shifts misalignments can be applied to beam elements.

The definition of the misalignment parameters (``rot_s_rad``,
``rot_s_rad_no_frame``, ``rot_x_rad``, ``rot_y_rad``, ``shift_x``, ``shift_y``, ``shift_s``)
can be found in the :ref:`element misalignment section <misalignment_label>` of
the reference guide.

The following example illustrates how to apply and inspect misalignments on elements:

.. literalinclude:: generated_code_snippets/compound_transform.py
   :language: python

Transformations are propagated when the elements are sliced and can be updated
also after the slicing by acting on the parent element. This is illustrated in
the following example:

.. literalinclude:: generated_code_snippets/compound_transform_sliced.py
   :language: python

Add multipolar components to elements
-------------------------------------

Multipolar components can be added to thick beam elements, as illustrated in the
following example:

.. literalinclude:: generated_code_snippets/multipolar_components.py
   :language: python

Extend multipolar component order
---------------------------------

By default, the multipolar component order is limited to a given default (typically
dodecapole). However, it is possible to extend the multipolar component order
by using the method :meth:`xtrack.Line.extend_knl_ksl` as illustrated in the following
example:

.. literalinclude:: generated_code_snippets/extend_multipoles.py
   :language: python

Propagation of multipolar components to sliced elements
-------------------------------------------------------

Multipolar components are propagated when the elements are sliced and can be updated
also after the slicing by acting on the parent element. This is illustrated in
the following example:

.. literalinclude:: generated_code_snippets/multipolar_components_sliced.py
   :language: python

Simulation of small rings: drifts, bends, fringe fields
-------------------------------------------------------

The modeling of the body of bending magnets is automatically adapted depending
on the bending radius, hence no special setting is required for this purpose
when simulating small rings with large bending angles.

However, the modeling of the fringe fields and the drifts is not automatically
adapted and appropriate settings need to be provided by the user.

The following example illustrates how to switch to the full model for the fringe
fields and the drifts and compares the effect of different models on the optics
functions and the chromatic properties of the CERN ELENA ring:

.. literalinclude:: generated_code_snippets/elena_chromatic_functions.py
   :language: python

.. figure:: figures/elena_w_chrom.png
    :width: 80%
    :align: center

    Comparison of the simplified and full model for the CERN ELENA ring (the six
    bends of the ring are highlighted in blue). While
    the linear optics is well reproduced by the simplified model, the chromatic
    properties differ significantly (in particular, note the effect of the dipole
    edges).