================================================
Generation and manipulation of Particles objects
================================================


.. contents:: Table of Contents
    :depth: 3


Introduction
============

Building particles with the Particles class
===========================================


Generating particles distributions
==================================

The ``build_particles`` function
--------------------------------


Example 1: Gaussian bunch
-------------------------

Example 2: Halo beam
--------------------
.. literalinclude:: generated_code_snippets/halo.py
   :language: python

.. figure:: figures/halo.png
    :width: 75%
    :align: center

    Particle distribution in normalized coordinates (left) and physical coordinates (right).

Example 3: Pencil beam
----------------------

.. literalinclude:: generated_code_snippets/pencil.py
   :language: python

.. figure:: figures/pencil.png
    :width: 75%
    :align: center

    Particle distribution in normalized coordinates (left) and physical coordinates (right).




Saving and loading Particles objects from dictionary or file
=============================================================

.. literalinclude:: generated_code_snippets/save_load.py
   :language: python

Other actions
=============

Merging particles objects
-------------------------

Filtering a particles object
----------------------------

Copying a particles object to a different context
-------------------------------------------------
