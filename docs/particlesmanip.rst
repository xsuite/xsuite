================================================
Generation and manipulation of Particles objects
================================================


.. contents:: Table of Contents
    :depth: 3


Introduction
============

Collections of particles for tracking simulations are generated in Xsuite using
the xpart modules. Such collections are stored as instances of the
:class:`xpart.Particles` class. Definitions of all quantities stored by the 
Particles objexts are available in the :ref:`class documentation<particlesapi>`.

The following sections illustrate:

 - How to create Particles objects on CPU or GPU, providing the coordinates in
   the form of arrays or using the xpart generators to generated specific
   distributions (e.g. Gaussian, halo, pencil).
 - How to copy Particles objects (optionally across contexts, e.g GPU to CPU)
 - How to merge Particles objects
 - How to filter Particles objects to select a subset of particles satisfying a
   logical condition defined by the user.

Building particles with the Particles class
===========================================

If all the coordinates of the particles are known, a Particles object can be
created directly with the :class:`xpart.Particles` calls. For example:

.. literalinclude:: generated_code_snippets/basics_part.py
   :language: python


The ``build_particles`` function
================================

It is often convenient to generate new Particles objects starting from a given
reference particle which defines for example the particle type (charge and mass)
and the reference energy and momentum with respect to which the coordinates.
This can be accomplished using the :meth:`xpart.build_particles` function.

.. literalinclude:: generated_code_snippets/build_particles_set.py
   :language: python

.. literalinclude:: generated_code_snippets/build_particles_shift.py
   :language: python

.. literalinclude:: generated_code_snippets/build_particles_normalized.py
   :language: python

Generating particles distributions
==================================

Example: Pencil beam
----------------------

.. literalinclude:: generated_code_snippets/pencil.py
   :language: python

.. figure:: figures/pencil.png
    :width: 75%
    :align: center

    Particle distribution in normalized coordinates (left) and physical coordinates (right).

Example: Halo beam
--------------------
.. literalinclude:: generated_code_snippets/halo.py
   :language: python

.. figure:: figures/halo.png
    :width: 75%
    :align: center

    Particle distribution in normalized coordinates (left) and physical coordinates (right).

Example: Gaussian bunch
-------------------------
.. literalinclude:: generated_code_snippets/gaussian.py
   :language: python

.. figure:: figures/gaussian.png
    :width: 75%
    :align: center


Copying a Particles object (optionally across contexts)
=======================================================

.. literalinclude:: generated_code_snippets/copy.py
   :language: python


Saving and loading Particles objects to/from dictionary or file
===============================================================

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

Merging and filtering Particles objects
=======================================

Merging Particles objects
-------------------------

.. literalinclude:: generated_code_snippets/merge.py
   :language: python

Filtering a Particles object
----------------------------
.. literalinclude:: generated_code_snippets/filter.py
   :language: python
