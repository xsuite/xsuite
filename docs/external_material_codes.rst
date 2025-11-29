.. _external_material_codes:

================================================
Linking external codes for material Interactions
================================================

.. contents:: Table of Contents
    :depth: 3


Introduction
============
Xcoll's internal material interaction model ``Everest`` is adequate for simulating
proton beams. In this model, no secondary particles are generated, and scattering
processes are modelled semi-continously to limit computation time. In case one is
performing simulations with heavy ions or electrons, where the production of secondary
particles becomes important as they could survive significant distances in the
accelerator, or if one requires a more accurate description of the scattering processes,
it is advisable to link Xcoll to an external material interaction code that supports
all particle types and performs a stepwise integration of the scattering processes.

In doing so, tracking is performed in Xsuite as usual but when a particle enters a
material block or collimator, its coordinates and momenta are passed to the external
code, which then performs the tracking through the material block, including the
generation of secondary particles. After exiting the material block, the updated
coordinates and momenta of the primary and secondary particles are passed back to
Xsuite for further tracking.


.. figure:: figures/xcoll_external.png
    :width: 55%
    :align: center


Managing the connection: the Engine
====================================
Managing the external code, both its execution and the communication with Xcoll/Xsuite,
is handled by a dedicated :class:`Engine` in Xcoll. This engine is responsible for
launching the external code, defining the physics parameters to be considered, sending
and retrieving the particle data, and cleaning up after the simulation. The main methods
of the engine are:

.. code-block:: python

	Engine.start(line=None, elements=None, names=None, input_file=None, cwd=None,
                     clean=True, **kwargs)

	Engine.stop(clean=False)

To start the engine, there are multiple options:

 - ``Engine.start(line=line)``: the engine will link all relevant elements in the line
 - ``Engine.start(line=line, names=names)``: the engine will only link the elements ``names`` (which should be present in the line)
 - ``Engine.start(elements=elements)``: the engine will link the provided list of elements
 - ``Engine.start(..., input_file=input_file)``: the engine will use the provided input file instead of auto-generating one (its elements need to match those provided)

It is possible to specify the working directory ``cwd`` where the external code will be executed and where input/output files and logs will be stored.
If ``clean=True``, the working directory will be cleaned up.

If more control over the input file is desired, it is possible to pre-generate it on a list of elements using:

.. code-block:: python

    Engine.generate_input_file(line=None, elements=None, names=None, filename=None, clean=True, **kwargs)

such that it can be manually modified before starting the engine with it.

There are many arguments that can be passed to the engine when starting it, or when generating the input file.
Furthermore, these arguments can also be set as attributes of the engine before starting it.
The difference lies in the fact that arguments passed to the ``start()`` or ``generate_input_file()``
methods will only be used for that specific call, while attributes set on the engine will persist
for future calls as well.

The following options can be set:

.. code-block:: python

    particle_ref: xpart.Particles  # Required
    seed: int64                    # optional (default None)
    verbose: bool                  # optional (default False)
    input_file: str | Path         # optional (default None)
    return_all: bool               # optional (default None)
    return_none: bool              # optional (default None)
    return_leptons: bool           # optional (default False)
    return_mesons: bool            # optional (default False)
    return_exotics: bool           # optional (default False)
    return_baryons: bool           # optional (default False)
    return_neutral: bool           # optional (default False)
    return_photons: bool           # optional (default False)
    return_electrons: bool         # optional (default True)
    return_muons: bool             # optional (default True)
    return_tauons: bool            # optional (default False)
    return_neutrinos: bool         # optional (default False)
    return_protons: bool           # optional (default True)
    return_neutrons: bool          # optional (default False)
    return_ions: bool              # optional (default True)

The return flags can be combined arbitrarily to select which particle types should be
returned to Xsuite after the interaction. In particular, ``return_none`` and ``return_all``
can be used to specify only a few particles that will resp. won't be returned.

Note that it is important that only one instance of the engine is active at any
given time, as multiple instances could lead to conflicts in the communication with
the external code. Therefore, one should never directly call any :class:`Engine` (like
:class:`Geant4Engine(...)`). Instead, for each external code there is a dedicated engine
instantiated at Xcoll import time, which can be accessed directly on the package. For
instance, the Geant4 engine is accessed as ``xcoll.geant4.engine``.

Geant4 via BDSIM
================
To use Geant4 as external code for material interactions in Xcoll, we use the `Beam Delivery SIMulation (BDSIM) <https://bdsim-collaboration.github.io/web/>`_, which is a Geant4-based particle
interaction code, which wraps around Geant4 and is specifically designed for accelerator applications.
To link Xcoll to BDSIM/Geant4, a full installation of both is required. The easiest way to install BDSIM is via `Conda/Mamba <https://docs.conda.io/en/latest/>`_.
After installing Conda, one can create a dedicated environment for BDSIM/Geant4 and install it via:

.. code-block:: bash

   mamba create -n bdsim -c conda-forge bdsim-g4
   conda activate bdsim

Running an Xcoll simulation is, after installing BDSIM/Geant4, straightforward. Below is an example snippet where a Geant4 collimator is created and linked to the Geant4 engine in Xcoll:

.. code-block:: python

    import xtrack as xt
    import xpart as xp
    import xcoll as xc

    num_part = 10000
    capacity = num_part*10  # allocate extra capacity for secondaries

    coll = xc.Geant4Collimator(length=0.4, material='MoGR')
    coll.jaw = 0.001

    # Connect to Geant4
    xc.geant4.engine.particle_ref = xt.Particles('Pb208', p0c=6.8e12*82)
    xc.geant4.engine.start(elements=coll, relative_energy_cut=1e-3, return_all=True, clean=True, verbose=False)

    x_init   = np.random.normal(loc=0.002, scale=0.2e-3, size=num_part)
    part_init = xp.build_particles(x=x_init, particle_ref=xc.geant4.engine.particle_ref,
                                   _capacity=capacity)
    part = part_init.copy()

    # Do the tracking in Geant4
    coll.track(part)

    # stop the engine
    xc.geant4.engine.stop()

    # Print out the results
    mask = (part.state > 0) | (part.particle_id >= num_part)
    pdg_ids = np.unique(part.pdg_id[mask], return_counts=True)
    idx = np.argsort(pdg_ids[1])[::-1]
    print(f"Returned {np.sum(mask)} particles ({np.sum(part.particle_id >= num_part)} secondaries):")
    for pdg_id, num in zip(pdg_ids[0][idx], pdg_ids[1][idx]):
        try:
            name = pdg.get_name_from_pdg_id(pdg_id, long_name=False)
        except ValueError:
            name = 'unknown'
        print(f"  {num:6} {name:12}   (PDG ID: {pdg_id:5})")

More examples can be found in the `Xcoll examples repository <https://github.com/xsuite/xcoll/tree/main/examples>`_.
