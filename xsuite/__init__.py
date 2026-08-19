# copyright ################################# #
# This file is part of the Xsuite Package.    #
# Copyright (c) CERN, 2024.                   #
# ########################################### #

from importlib.metadata import version

# Enable lazy loading of the version: during package build Xsuite might not be
# installed, leading to a PackageNotFind error when `version` is called. This
# allows us to import Xsuite even if it's not installed. As long as `__version__`
# is not needed, there will be no errors.
def __getattr__(name: str):
    if name == "__version__":
        value = version("xsuite")
        globals()["__version__"] = value  # Cache after first lookup
        return value

    raise AttributeError(f"Module {__name__!r} has no attribute {name!r}")

from .prebuild_kernels import (
    PrebuiltKernelNotFoundError,
    get_suitable_kernel,
    PREBUILT_KERNELS_LOCATION,
)
