=========
Xpart API
=========

.. contents:: Table of Contents
    :depth: 3

.. _particlesapi:

The particle class
==================

.. autoclass:: xpart.Particles
    :members:
    :undoc-members:
    :member-order: bysource

The ``build_particles`` function
================================

.. autofunction:: xpart.build_particles

Longitudinal coordinates generation
===================================

.. autofunction:: xpart.generate_longitudinal_coordinates

Normalized transverse coordinates generation
============================================

Gaussian
--------

.. autofunction:: xpart.generate_2D_gaussian

Polar grid
----------

.. autofunction:: xpart.generate_2D_polar_grid

Uniform circular sector
-----------------------

.. autofunction:: xpart.generate_2D_uniform_circular_sector

Pencil
------

.. autofunction:: xpart.generate_2D_pencil

.. autofunction:: xpart.generate_2D_pencil_with_absolute_cut

Gaussian bunch generation (6D)
==============================

.. autofunction:: xpart.generate_matched_gaussian_bunch
