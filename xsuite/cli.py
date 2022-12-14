# copyright ################################# #
# This file is part of the Xobjects Package.  #
# Copyright (c) CERN, 2022.                   #
# ########################################### #
from xtrack.prebuild_kernels import clear_kernels, regenerate_kernels
import argparse


def main():
    parser = argparse.ArgumentParser(
                    prog = 'ProgramName',
                    description = 'What the program does',
                    epilog = 'Text at the bottom of help')
    parser.add_argument('--clean', action='store_true')
    args = parser.parse_args()

    if args.clean:
        clear_kernels()
        print('Cleaned kernels.')
    else:
        regenerate_kernels()
        print('Successfully compiled kernels.')
