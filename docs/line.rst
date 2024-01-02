====
Line
====

.. contents:: Table of Contents
    :depth: 3

Creating a Line object
======================

An Xsuite Line can be created by providing beam line element objects and the
corresponding names, as illustrated in the following example:

.. literalinclude:: generated_code_snippets/toy_ring.py
   :language: python

Importing a line from MAD-X
===========================

An Xsuite Line object can be importing from an existing MAD-X model, using the method
:meth:`xtrack.Line.from_madx_sequence`. The import of certain features of the MAD-X
model (dererred expressions, apertures, thick elements, alignment errors, field
errors, etc.) can be controlled by the user. This is illustrated in the following
example:

.. literalinclude:: generated_code_snippets/madx_import_psb.py
   :language: python


Line inspection, ``Line.get_table()``, ``Line.attr[...]``
========================================================

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

Save and reload lines
=====================

An Xtrack Line object can be transformed into a dictionary or saved to a json
file, as illustrated in the following example:

.. literalinclude:: generated_code_snippets/tojson.py
   :language: python

Element insertion
=================

.. literalinclude:: generated_code_snippets/insert_element.py
   :language: python

Element slicing
===============

It is possible to slice thick element with thin or thick slices, using the Uniform
or the `Teapot <https://cds.cern.ch/record/165372>`_ scheme. This is illustrated
in the following example:

.. literalinclude:: generated_code_snippets/slicing.py
   :language: python

