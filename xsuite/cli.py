# copyright ################################# #
# This file is part of the Xobjects Package.  #
# Copyright (c) CERN, 2022.                   #
# ########################################### #
from xtrack.prebuild_kernels import regenerate_kernels


def main():
    regenerate_kernels()
    print('Successfully compiled kernels.')
