# copyright ################################# #
# This file is part of the Xsuite Package.    #
# Copyright (c) CERN, 2024.                   #
# ########################################### #

from importlib.metadata import version
__version__ = version(__name__)

from .prebuild_kernels import get_suitable_kernel, XSK_PREBUILT_KERNELS_LOCATION
