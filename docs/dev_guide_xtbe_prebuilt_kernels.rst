Prebuilt kernel definitions
===========================

Xsuite distributes prebuilt kernels for common tracking configurations. These
kernels let users run many standard cases without compiling C code on first use.
When a new beam element, helper structure, or package-level C source is added,
the prebuilt-kernel definitions may need to be updated so that the generated
kernel shared objects contain the required code.

The definitions live in two places:

* package-local ``prebuilt_kernel_definitions`` modules, which expose element
  classes and optional constructor defaults;
* ``xsuite/kernel_definitions.py``, which combines those package-local lists
  into the actual prebuilt kernel configurations built by ``xsuite-prebuild``.

Package-local definitions
-------------------------

Each package that contributes elements to the default Xsuite kernels keeps its
own lists under ``<package>/prebuilt_kernel_definitions``. For example, Xtrack
exports:

.. code-block:: python

    # xtrack/prebuilt_kernel_definitions/__init__.py
    from .element_types import (
        ONLY_XTRACK_ELEMENTS,
        NO_SYNRAD_ELEMENTS,
        NON_TRACKING_ELEMENTS,
    )
    from .element_inits import XTRACK_ELEMENTS_INIT_DEFAULTS

The element-type module contains the classes to make available in prebuilt
kernels. Tracking elements go in the lists used as ``classes`` in
``xsuite/kernel_definitions.py``. Helper structures and elements that are not
part of the line, but whose APIs or extra kernels need to be present, go in
``extra_classes`` through a package-local list such as ``NON_TRACKING_ELEMENTS``.

Some classes cannot be instantiated with an empty constructor. For those,
provide minimal build-time arguments in the package-local
``*_ELEMENTS_INIT_DEFAULTS`` dictionary:

.. code-block:: python

    XTRACK_ELEMENTS_INIT_DEFAULTS = {
        'LimitPolygon': {
            'x_vertices': np.array([0, 1, 1, 0]),
            'y_vertices': np.array([0, 0, 1, 1]),
        },
    }

These objects are only used to build representative trackers for kernel
generation. Keep the defaults as small and inert as possible.

Adding a class to Xsuite kernels
--------------------------------

After adding the class to the package-local definitions, make sure it is
available in the appropriate configuration in ``xsuite/kernel_definitions.py``.
For an existing Xsuite package this usually means adding the class to one of
the lists already imported by ``xsuite/kernel_definitions.py``. For a new
package, ``xsuite/kernel_definitions.py`` must import that package's
prebuilt-kernel lists and include them in the selected configurations.

Each entry has this shape:

.. code-block:: python

    ('default_base_config', {
        'config': BASE_CONFIG,
        'classes': XTRACK_ELEMENTS + DEFAULT_XFIELDS_ELEMENTS,
        'extra_classes': [xt.Particles],
    }),

``classes``
    Beam elements that are placed in the temporary ``xt.Line`` used to build the
    tracker kernel.

``extra_classes``
    Xobjects classes that are not line elements for this configuration, but
    whose C API or ``_kernels`` need to be compiled into the module.
    ``xt.Particles`` is normally included here.

``config``
    Tracker configuration values used when building the prebuilt kernel. At run
    time, prebuilt kernels are selected only when the requested config matches
    the metadata exactly.

The order of ``kernel_definitions`` matters. Runtime selection tries the entries
in order and uses the first compatible prebuilt kernel, so more-specific or
higher-priority definitions should stay above broader ones.

Making C headers discoverable
-----------------------------

If a package provides C headers that are included by kernel sources, Xobjects
needs to know where that package's sources are installed. Register an
``xobjects`` entry point named ``include`` in the package's ``pyproject.toml``.

.. code-block:: toml

    [project.entry-points.xobjects]
    include = "my_package"

Xobjects loads entry points from the ``xobjects`` group with the name
``include`` and adds the parent directory of the imported package to the C
include path. This makes includes such as the following work from kernel
sources:

.. code-block:: c

    #include "my_package/path/to/header.h"

The hook only provides include paths. The headers still need to be part of the
installed package or source distribution.

Regenerating and checking
-------------------------

After changing definitions, regenerate the prebuilt kernels locally:

.. code-block:: bash

    xsuite-prebuild regenerate

Set ``XSUITE_VERBOSE`` when checking runtime selection. With this environment
variable set, Xsuite prints which prebuilt kernels it considers and why each
candidate is accepted or rejected.
