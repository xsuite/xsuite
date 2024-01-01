====
Line
====

.. contents:: Table of Contents
    :depth: 3

Create a Line object
====================

Bla

Importing a line from MAD-X
===========================

Bla

Save and reload lines
=====================

An Xtrack Line object can be transformed into a dictionary and saved in a json file, as
illustrated in the following example. Note that ``xobjects.JEncoder`` needs to
be provided to ``json.dump`` in order to serialize Numpy arrays, which are not
natively supported by json.

.. literalinclude:: generated_code_snippets/tojson.py
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

Element insertion
=================
Bla

Element slicing
===============

It is possible to slice thick element with thin or thick slices, using the Uniform
or the `Teapot <https://cds.cern.ch/record/165372>`_ scheme. This is illustrated
in the following example:

.. literalinclude:: generated_code_snippets/slicing.py
   :language: python

