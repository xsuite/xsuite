# copyright ############################### #
# This file is part of the Xsuite project.  #
# Copyright (c) CERN, 2024.                 #
# ######################################### #
import os
from pathlib import Path

from setuptools import setup
from setuptools.command.build_ext import build_ext
from setuptools.dist import Distribution


class BinaryDistribution(Distribution):
    """Force a binary distribution when building wheels.

    Since we don't use extensions in the package, the wheel would be built as a
    source wheel, without the platform tags, by default. This way we force the
    wheel to be built as a binary wheel.
    """
    def has_ext_modules(_):  # noqa
        return True


class CustomBuildExtCommand(build_ext):
    """Custom build_ext that generates kernel binaries to be added to bdist.

    The building of the kernels can be skipped by setting the environment
    variable SKIP_KERNEL_BUILD to a non-empty value. This is useful when
    performing an editable install, as the kernels pip runs the build script in
    a temporary environment and the kernels in such case might not be compatible
    with the currently installed packages (e.g. packages with potentially
    compatible version numbers but different as they are under development).
    """
    def run(self):
        super().run()

        if os.environ.get('SKIP_KERNEL_BUILD', False):
            print('Skipping kernel build as requested by environment variable.')
            return

        # Override number of threads for parallel building
        if os.environ.get('XSK_N_THREADS', None) is not None:
            n_threads = int(os.environ['XSK_N_THREADS'])
        else:
            n_threads = None

        # Modern setuptools/pip don't guarantee that building happens in the
        # package directory. As we need the kernel generation code here, we
        # add the package directory to the path to be able to import it.
        import sys
        sys.path.append(str(Path(__file__).parent))
        from xsuite.prebuild_kernels import regenerate_kernels

        # Regenerate the kernels in the build directory so that they are
        # included in the binary wheel, unless we're installing in editable
        # mode, in which case the kernels are generated in the source (default).
        if not self.editable_mode:
            location = str(Path(self.build_lib) / 'xsuite/lib')
            regenerate_kernels(location=location, n_threads=n_threads)
        else:
            regenerate_kernels(n_threads=n_threads)


setup(
    distclass=BinaryDistribution,
    cmdclass={
        'build_ext': CustomBuildExtCommand,
    },
    extras_require={
        'notebooks': ['jupyter', 'ipympl', 'xplt'],
        'full_env': ['cpymad', 'nafflib', 'pytest', 'pytest-mock',
                     'jupyter', 'ipympl', 'xplt', 'ipython'],
    },
)
