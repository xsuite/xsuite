====================
Line and environment
====================

.. contents:: Table of Contents
    :depth: 3

.. _createline:

Creating a simple Line object
=============================

An Xsuite Line can be created by providing beam line element objects and the
corresponding names, as illustrated in the following example:

.. literalinclude:: generated_code_snippets/toy_ring.py
   :language: python

Save and reload lines
=====================

An Xtrack Line object can be transformed into a dictionary or saved to a json
file, as illustrated in the following example:

.. literalinclude:: generated_code_snippets/tojson.py
   :language: python

Line inspection, ``Line.get_table()``, ``Line.attr[...]``
=========================================================

The following example illustrates how to inspect the properties of a line and
its elements:

.. literalinclude:: generated_code_snippets/line_inspect.py
   :language: python

References and deferred expressions
===================================

Accelerators and beam lines have complex control paterns. For example, a single
high-level parameter can be used to control groups of accelerator components
(e.g., sets of magnets in series, groups of RF cavities, etc.) following complex
dependency relations. Xsuite allows including these dependencies in the simulation
model so that  changes in the high-level parameters are automatically propagated
down to the line elements properties. Furthermore, the dependency relations can
be created, inspected and modified at run time, as illustrated in the following
example:

.. literalinclude:: generated_code_snippets/expressions_basics.py
   :language: python

When importing a MAD-X model, the dependency relations from MAD-X deferred
expressions are automatically imported as well. The following example illustrates
how to inspect the dependency relations in a line imported from MAD-X:

.. literalinclude:: generated_code_snippets/expressions_madx.py
   :language: python


Role of the Environment
=======================

The Xsuite environment manages variables and elements that can be shared by different
lines as illustrated in the following example:

.. literalinclude:: generated_code_snippets/environment.py
   :language: python

.. _seqdef:

Define a line by specifying the s positions of the elements
===========================================================

Instead of specifying explicit drift spaces between the elements, as shown in
section :ref:`createline`, it is possible to define a line by specifying the `s`
positions of the elements elements. When the position
is not specified the element is simply placed right after the previous one.
The following example illustrates this way of defining a line:

.. literalinclude:: generated_code_snippets/sequence.py
   :language: python

Placing sub-lines at given s positions
--------------------------------------

As for normal elements, it is possible to place sublines at given s positions
within a longer line. This is illustrated in the following example:

.. literalinclude:: generated_code_snippets/place_line_at_s.py
   :language: python

.. _madximport:

Repeated elements, replicas and clones
======================================

Xsuite supports the installation of the same element multiple times in the same
line. Furthermore, It is also possible to create replicas and cloneds of an element
Replicas behave in the same way as repeated elements, but have a user-defined name.
Element clones, instead, are full copies of the original element and
inherit all properties of the parent element at the moment of clone creation,
including the controlling expressions. This is illustrated in the following example:

.. literalinclude:: generated_code_snippets/repeated_elements_clones_replicas.py
   :language: python
   
Note that while it would be possible to assign the same element to another name in `elements_dict`,
Replicas make sure that it is impossible to trim different the replicated element
and that the relation is maintained in the `to_dict/from_dict` and `to_json/from_json` methods.


Using line replicas instead of repeated elements
------------------------------------------------

It is possible to use replicas to assemble the ring. This allows using
different names for the different sections and for their elements. This is
illustrated in the following example:

.. literalinclude:: generated_code_snippets/composition_with_replicas.py
   :language: python


Line mirroring and composition
==============================

Lines can be composed by concatenating other line. This can be simply done with
the `+` operator. It is also possible, using the `-` operator to mirror a line
by reversing the order of its elements. This features are particularly useful
when designing beam lines, as illustrated in the following example:

.. literalinclude:: generated_code_snippets/line_composition.py
   :language: python

Insert elements
===============

It is possible to insert elements in a line also after its creation. The position
of the new elements can be specified as absolut s position or as relative to
an existing element. This is illustrated in the following example:

.. literalinclude:: generated_code_snippets/insert_element.py
   :language: python

Insert elements instantiated by the user
----------------------------------------

It is possible to insert elements that are created by the user using the class
directly instead of using the `Environment.new` method. This can be done in a single
step or alternatively by first adding the element to the environment and then
inserting it in the line. This is illustrated in the following example:

.. literalinclude:: generated_code_snippets/insert_element_instantiated_by_user.py
   :language: python

Insert a line into another line
-------------------------------

It is also possible to insert entire lines, as illustrated in the following example:

.. literalinclude:: generated_code_snippets/insert_line.py
   :language: python

Simplified syntax for single insertion
--------------------------------------

A compact syntax is available to perform a single insertion in a line. Note that
when multiple insertions need to be made, it is significantly faster to install
all the elements at once, as shown in the previous example. The compact syntax
for single insertion is illustrated in the following example:

.. literalinclude:: generated_code_snippets/insert_element_single.py
   :language: python

Append elements
===============
New elements can also be installed at the end of a line, as illustrated in the
following example:

.. literalinclude:: generated_code_snippets/append_elements.py
   :language: python

Remove elements
===============
Elements can be removed from a line using the `Line.remove` method. Thick elements
are replaced by drift spaces, so that the position of all other elements is
preserved. This is illustrated in the following example:

.. literalinclude:: generated_code_snippets/remove_elements.py
   :language: python

Replace elements
================
Elements in a line can be replaced with elements having the same length, as
illustrated in the following example:

.. literalinclude:: generated_code_snippets/replace_elements.py
   :language: python

Slice elements
==============

It is possible to slice thick element with thin or thick slices, using the Uniform
or the `Teapot <https://cds.cern.ch/record/165372>`_ scheme. This is illustrated
in the following example:

.. literalinclude:: generated_code_snippets/slicing.py
   :language: python

Cut line elements at given s positions
======================================

The method :meth:`xtrack.Line.cut_at_s` allows for cutting the line elements at the
specified s positions. In the example before we take the same toy ring introduced
in the :ref:`earlier example<createline>` and we cut it into 100 equal length slices:

.. literalinclude:: generated_code_snippets/cut_at_s.py
   :language: python

Apply transformations (tilt, shift) to elements
===============================================

Tilt and shifts transformations can be applied to beam elements, as illustrated
in the following example:

.. literalinclude:: generated_code_snippets/compound_transform.py
   :language: python

Tranfromations are propagated when the elements are sliced and can be updated
also after the slicing by acting on the parent element. This is illustrated in
the following example:

.. literalinclude:: generated_code_snippets/compound_transform_sliced.py
   :language: python

Add multipolar components to elements
=====================================

Multipolar components can be added to thick beam elements, as illustrated in the
following example:

.. literalinclude:: generated_code_snippets/multipolar_components.py
   :language: python

Multipolar components are propagated when the elements are sliced and can be updated
also after the slicing by acting on the parent element. This is illustrated in
the following example:

.. literalinclude:: generated_code_snippets/multipolar_components_sliced.py
   :language: python



Importing a line from MAD-X
===========================

An Xsuite Line object can be imported from an existing MAD-X model, through the
`cpymad <http://hibtc.github.io/cpymad/>`_ interface of MAD-X, using the method
:meth:`xtrack.Line.from_madx_sequence`. The import of certain features of the MAD-X
model (dererred expressions, apertures, thick elements, alignment errors, field
errors, etc.) can be controlled by the user. This is illustrated in the following
example:

.. literalinclude:: generated_code_snippets/madx_import_psb.py
   :language: python

Simulation of small rings: drifts, bends, fringe fields
=======================================================

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

Extraction of second order transfer maps
========================================

The method :meth:`xtrack.Line.get_line_with_second_order_maps` allows modeling portions
of a beam line with second order transfer maps. This is illustrated in the
following example.

See also :meth:`xtrack.SecondOrderTaylorMap.from_line`.

.. literalinclude:: generated_code_snippets/line_with_maps.py
   :language: python

