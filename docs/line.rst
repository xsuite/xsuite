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

Inspecting a line with ``Line.get_table()``
===========================================

Bla

References and deferred expressions
===================================

Accelerators and beam lines have complex control paterns. For example, a single
high-level parameter can be used to control groups of accelerator components
(e.g., sets of magnets in series, groups of RF cavities, etc.) following complex
dependency relations. Xsuite allows including these dependencies in the simulation
model so that  changes in the high-level parameters are automatically propagated
down to the line elements properties. Furthermore, the dependency relations can
be created, inspected and modified at run time, as illustrated in the following example:

.. literalinclude:: generated_code_snippets/expressions_basics.py
   :language: python


``Line.attr``
=============

Bla

Element slicing
===============

Bla
