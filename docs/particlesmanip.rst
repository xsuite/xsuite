================================================
Generation and manipulation of Particles objects
================================================


.. contents:: Table of Contents
    :depth: 3


Introduction
============

... The :class:xpart.Particles ...

Building particles with the Particles class
===========================================

.. literalinclude:: generated_code_snippets/basics_part.py
   :language: python

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

Save and load from dictionary
-----------------------------

.. literalinclude:: generated_code_snippets/to_from_dict.py
   :language: python

Save and load from json file
-----------------------------

.. literalinclude:: generated_code_snippets/save_load_json.py
   :language: python

Save and load from pickle file
------------------------------

.. literalinclude:: generated_code_snippets/save_load_pickle.py
   :language: python

Save and load using pandas
--------------------------

.. literalinclude:: generated_code_snippets/save_load_with_pandas.py
   :language: python

Other actions
=============

Merging particles objects
-------------------------

Filtering a particles object
----------------------------

Copying a particles object to a different context
-------------------------------------------------
