Space charge
============

Xsuite can be used to perform simulations including space-charge effects. Three
modes can  be used to simulate the space-charge forces:
 - **Frozen:**  A fixed Gaussian bunch distribution is used to compute the space-charge forces.
 - **Quasi-frozen:** Forces are computed assuming a Gaussian distribution. The properties of the distribution (transverse r.m.s. sizes,transverse positions) are updated at each interaction based on the particle distribution.
 - **PIC:** The Particle In Cell method is used to compute the forces acting among particles. No assumption is made on the bunch shape.

The last two options constitute collective interactions. As discussed
in the :doc:`dedicated section <collective>`, the Xtrack Line works such that particles are tracked asynchronously by separate threads in the non-collective sections of the sequence and are regrouped at each collective element (in PIC or quasi-frozen space-charge lenses).

The following example illustrates how to configure and run a space-charge simulation.
The variable ``mode`` is used to switch between frozen, quasi-frozen and PIC.

See also: :func:`xfields.install_spacecharge_frozen`,
:func:`xfields.replace_spacecharge_with_quasi_frozen`,
:func:`xfields.replace_spacecharge_with_PIC`.

Example
-------

.. literalinclude:: generated_code_snippets/spacecharge.py
   :language: python


