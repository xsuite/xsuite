# copyright ################################# #
# This file is part of the Xobjects Package.  #
# Copyright (c) CERN, 2022.                   #
# ########################################### #
import argparse


def main():
    try:
        from xsuite_kernels.prebuild_kernels import (
            clear_kernels, regenerate_kernels
        )
    except ImportError:
        print("=== ERROR ===\n"
              "The kernel prebuilding functionality has been moved to a new "
              "package: please run `pip install xsuite-kernels` to use it. "
              "Prebuilt kernels are now distributed on PyPI as part of the "
              "`xsuite-kernels` package, and there is no need to run this "
              "script anymore in most cases. ")
        exit(1)

    print("=== WARNING ===\n"
          "If you are using Xsuite packages provided by `pip`, you no longer "
          "need to run this script. The package `xsuite-kernels` provides "
          "prebuilt kernels for the Xsuite packages. If you are developing "
          "Xsuite packages, you can use the `xsuite-kernels` command to "
          "manually manage prebuilt kernels: see `xsuite-kernels --help`.")

    parser = argparse.ArgumentParser(
                    prog='xsuite-prebuild',
                    description='Prebuild Xsuite kernels')
    parser.add_argument('--clean', action='store_true')
    args = parser.parse_args()

    if args.clean:
        print('=> This command has been replaced with `xsuite-kernels clean`.')
        clear_kernels()
        print('Cleaned kernels.')
    else:
        print('=> This command has been replaced with `xsuite-kernels regenerate`.')
        regenerate_kernels()
        print('Successfully compiled kernels.')
