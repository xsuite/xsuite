=========
Beam line
=========

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

Xtrack allows importing MAD-X deferred expressions and preserving their relationship
with the definition of of the beam line. This feature is implemented through the
xdeps package and is illustrated in the following example:

.. literalinclude:: generated_code_snippets/expressions.py
   :language: python

``Line.attr``
=============

Bla

Element slicing
===============

Bla
