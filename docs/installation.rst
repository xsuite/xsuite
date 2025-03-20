.. _installation-page:

============
Installation
============

We assume that you have a recent python installation (python 3.8+). It this is not the case you can make one following the dedicated section on :ref:`how to get a miniforge installation<miniforge>`.

.. contents:: Table of Contents
    :depth: 3

Basic installation
==================

If you do not have a Python installation, please follow the instructions in
:ref:`this section<miniforge>` to get a Miniforge environment and install Xsuite.

Instead, if you already have a Python installation, the Xsuite packages can be
installed using pip:

.. code-block:: bash

    pip install xsuite

This installation allows using Xsuite on CPU in most scenarios. In order
to handle more complicated cases it may be necessary to install compilers with
``conda install compilers``. To use Xsuite on GPU, with the cupy and/or pyopencl
you need to install the corresponding packages, as described in the
:ref:`dedicated section<gpuinst>`.

.. note::
    On most machines, when using Xsuite installed from PyPI, there is no longer
    a need to run ``xsuite-prebuild`` to precompile the kernels. The precompiled
    kernels are automatically downloaded and installed with the ``xsuite``
    package. See the :ref:`relevant section<prebuiltkernels>` of the developer
    guide below for more details.


Usage in Microsoft Windows
--------------------------

Xsuite is developed and tested on Linux and macOS. However, it can also be used
on Windows.
If you are working on a Windows machine, you can install Xsuite under
Windows Subsystem for Linux using the same instructions as for a vanilla Linux
machine. To install WSL, follow the `steps outlined by Microsoft <https://learn.microsoft.com/en-us/windows/wsl/install>`_
(at the time of writing it suffices to run ``wsl --install`` in an administrator
PowerShell or CMD prompt and follow the instructions).


Developer installation
======================

If you need to develop Xsuite, you can clone the packages from GitHub and install them with pip in editable mode:

.. code-block:: bash

    git clone https://github.com/xsuite/xobjects
    pip install -e xobjects

    git clone https://github.com/xsuite/xdeps
    pip install -e xdeps

    git clone https://github.com/xsuite/xpart
    pip install -e xpart

    git clone https://github.com/xsuite/xtrack
    pip install -e xtrack

    git clone https://github.com/xsuite/xfields
    pip install -e xfields


This installation allows using Xsuite on CPU. To use Xsuite on GPU, with the cupy and/or pyopencl you need to install the corresponding packages, as described in the :ref:`dedicated section<gpuinst>`.

Testing
-------

If all of the optional dependencies have also been installed, we can
verify our installation. To install test dependencies for an xsuite
package, one can replace the ``pip install -e some_package`` commands in
the above snippet with ``pip install -e 'some_package[tests]'``. Once
the test dependecies are also installed, we can run the tests to check
if xsuite works correctly:

.. code:: bash

   cd ..
   PKGS=(xobjects xdeps xpart xtrack xfields)
   for PKG in ${PKGS[@]}; do
   python -m pytest xsuite/$PKG/tests
   done

.. _prebuiltkernels:

Prebuilt kernels
----------------

The ``xsuite`` package provides a set of precompiled kernels, so that commonly
used tracking scenarios can be run without the need to run the compiler on the
target machine. The precompiled kernels are distributed as binary Python wheels
on PyPI.

When the package is installed on a supported machine pip will automatically
download the appropriate kernel files and install them in the correct location,
so that Xtrack can use them. If the right versions of kernels are not installed,
Xtrack will fall back to the default behaviour of compiling the kernels on the fly.

This can happen, e.g., if the package is installed from source (e.g. by cloning
the repository or downloading the source distribution in case of an unsupported
platform). In such a case, the kernels will be compiled automatically during the
installation process when running ``pip install -e`` (see setup.py).

In order to perform tracking on CPU,
a C compiler needs to be installed on the system: when using conda, this is provided
by the ``compilers`` package (``conda install compilers``).

After the installation, you can choose to precompile some often-used kernels, in
order to reduce the waiting time spent on running the simulations later on. This
can be accomplished simply by running the following command:

.. code-block:: bash

    xsuite-prebuild regenerate



Optional dependencies
=====================

MAD-X and cpymad
----------------

To import MAD-X lattices you will need the cpymad package, which can be installed as follow:

.. code-block:: bash

    pip install cpymad

Sixtracktools
-------------

To import lattices from a set of sixtrack input files (fort.2, fort.3, etc.) you will need the sixtracktools package, which can be installed as follow:

.. code-block:: bash

    git clone https://github.com/sixtrack/sixtracktools
    pip install -e sixtracktools

PyHEADTAIL
----------

To use the PyHEADTAIL interface in Xsuite, PyHEADTAIL needs to be installed:

.. code-block:: bash

    git clone https://github.com/pycomplete/pyheadtail
    pip install cython h5py
    pip install -e pyheadtail

Other useful packages
---------------------

* ``pip install tqdm`` will enable progress bars in Xsuite in CLI and notebooks
* ``pip install cython`` to enable ``xsuite-prebuild`` functionality
* ``pip install matplotlib`` for plots
* ``pip install xplt`` is a `plotting library <https://github.com/eltos/xplt/>`_ for Xsuite and similar accelerator physics tools
* ``pip install jupyter ipympl`` to be able to create and open notebooks with interactive graphs
* ``pip install ipython`` for a better Python interactive CLI
* ``pip install pytest-xdist`` extends pytest with an ``-n N`` option that can be used to run tests on ``N`` cores
* ``pip install gitpython click gh`` needed for various Xsuite-developer related tasks


.. _gpuinst:

GPU/Multithreading support
==========================

In the following section we describe the steps to install the two supported GPU platforms, i.e. cupy and pyopencl, as
well as the multithreading library OpenMP.

Installation of cupy
--------------------

In order to use the :doc:`cupy context<contexts>`, the cupy package needs to be installed.

In Anaconda or Miniconda/Miniforge (if you don't have Anaconda or Miniconda/Miniforge, see dedicated section on :ref:`how to get a miniforge installation<miniforge>`)

this can be done as follows:

.. code-block:: bash

    conda install mamba -n base -c conda-forge
    pip install cupy-cuda11x
    mamba install cudatoolkit=11.8.0



Installation of PyOpenCL
------------------------

In order to use the :doc:`pyopencl context<contexts>`, the PyOpenCL package needs to be installed.
In Anacoda or Miniconda/Miniforge this can be done as follows:

.. code-block:: bash

    conda config --add channels conda-forge  # not needed for Miniforge
    conda install pyopencl


Check that there is an OpenCL installation in the system:

.. code-block:: bash

    ls /etc/OpenCL/vendors


Make the OpenCL installation visible to pyopencl:

.. code-block:: bash

    conda install ocl-icd-system


For the PyOpenCL context we will need the `gpyfft <https://github.com/geggo/gpyfft>`_ and the `clfft <https://github.com/clMathLibraries/clFFT>`_ libraries.
For this purpose we need to install cython.

.. code-block:: bash

    pip install cython


Then we can install clfft.

.. code-block:: bash

    conda install -c conda-forge clfft


We locate the library and headers here:

.. code-block:: bash


    $ ls ~/miniforge3/pkgs/clfft-2.12.2-h83d4a3d_1/

    # gives: include  info  lib

(Or locate the directory via ``find $(dirname $(dirname $(type -P conda)))/pkgs -name "clfft*" -type d`` .)

We obtain gpyfft from github:

.. code-block:: bash

    git clone https://github.com/geggo/gpyfft

and we install gpyfft with pip providing extra flags as follows:

.. code-block:: bash

     pip install --global-option=build_ext --global-option="-I/home/giadarol/miniforge3/pkgs/clfft-2.12.2-h83d4a3d_1/include" --global-option="-L/home/giadarol/miniforge3/pkgs/clfft-2.12.2-h83d4a3d_1/lib" gpyfft/


Alternatively (if the command above does not work) we can edit the ``setup.py`` of gpyfft to provide the right paths to your clfft installation (and potentially the OpenCL directory of your platform):

.. code-block:: python

    if 'Linux' in system:
        CLFFT_DIR = os.path.expanduser('~/miniforge3/pkgs/clfft-2.12.2-h83d4a3d_1/')
        CLFFT_LIB_DIRS = [r'/usr/local/lib64']
        CLFFT_INCL_DIRS = [os.path.join(CLFFT_DIR, 'include'), ] # remove the 'src' part
        CL_INCL_DIRS = ['/opt/rocm-4.0.0/opencl/include']

And install gpyfft locally.

.. code-block:: bash

    pip install -e gpyfft/

Installation of OpenMP
----------------------

On Linux and on Apple Silicon Macs OpenMP support should automatically be
provided with the conda-forge's ``compilers`` package. However, on Intel Macs
it may be necessary to separately install the ``llvm-openmp`` package with
``conda install llvm-openmp``. Similarly, should a manual installation on Linux
be needed, the same functionality (for GCC) is provided by the ``libgomp``
package for GCC.


.. _miniforge:

Install Miniforge
=================

If you don't have a miniconda or miniforge installation, you can quickly get one
with the following steps.




On Linux
--------

.. code-block:: bash

    cd ~
    wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
    bash Miniforge3-Linux-x86_64.sh
    source miniforge3/bin/activate
    pip install numpy scipy matplotlib pandas ipython pytest
    pip install jupyter ipympl # to use jupyter notebooks (optional)
    pip install cpymad # to load MAD-X lattices (optional)
    pip install xsuite

On MacOS
--------

We recommend installing Xsuite inside a conda environment:

.. code-block:: bash

    cd ~
    curl -OL https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-$(uname -m).sh
    bash Miniforge3-MacOSX-$(uname -m).sh
    source miniforge3/bin/activate
    conda create -n xsuite_env python=3.11  # or your preferred version
    conda activate xsuite_env
    conda install compilers
    pip install numpy scipy matplotlib pandas ipython pytest
    pip install jupyter ipympl # to use jupyter notebooks (optional)
    pip install cpymad # to load MAD-X lattices (optional)
    pip install xsuite

Microsoft Windows
-----------------

If you are working on a Windows machine, you can install Miniforge under
Windows Subsystem for Linux using the same instructions as for a vanilla Linux
machine. To install WSL, follow the `steps outlined by Microsoft <https://learn.microsoft.com/en-us/windows/wsl/install>`_
(at the time of writing it suffices to run ``wsl --install`` in an administrator
PowerShell or CMD prompt and follow the instructions).
Once you have WSL installed, you can follow the Linux instructions above.

Miniforge vs Miniconda
----------------------

A miniforge installation is recommended against a miniconda installation as miniforge uses by default the "conda-forge" channel
while miniconda uses the "default" channel (https://repo.anaconda.com/pkgs/). While the "default" channel can require a paid license 
depending on its usage, the "conda-forge" channel is free for all to use (see https://docs.conda.io/projects/conda/en/latest/user-guide/concepts/channels.html).

.. note::

    The current versions of miniconda ship with the `mamba` command, which is a
    much faster reimplementation of `conda` written in C++. It can also be used.

Advanced information for developers
===================================

Building MAD-X and cpymad from source (tested with macOS)
---------------------------------------------------------

First we build ``MAD-X`` and ``cpymad`` (largely following the
recommendations found
`here <https://github.com/hibtc/cpymad/pull/114>`__ and
`here <https://hibtc.github.io/cpymad/installation/macos.html>`__):

.. code:: bash

   conda install compilers cmake

   git clone https://github.com/MethodicalAcceleratorDesign/MAD-X
   pip install --upgrade cmake cython wheel setuptools delocate
   mkdir MAD-X/build && cd MAD-X/build

   cmake .. \
       -DCMAKE_POLICY_DEFAULT_CMP0077=NEW \
       -DCMAKE_POLICY_DEFAULT_CMP0042=NEW \
       -DCMAKE_OSX_ARCHITECTURES=arm64 \
       -DCMAKE_C_COMPILER=clang \
       -DCMAKE_CXX_COMPILER=clang++ \
       -DCMAKE_Fortran_COMPILER=gfortran \
       -DBUILD_SHARED_LIBS=OFF \
       -DMADX_STATIC=OFF \
       -DCMAKE_INSTALL_PREFIX=../dist \
       -DCMAKE_BUILD_TYPE=Release \
       -DMADX_INSTALL_DOC=OFF \
       -DMADX_ONLINE=OFF \
       -DMADX_FORCE_32=OFF \
       -DMADX_X11=OFF
   # Verify in the output of the above command that libraries
   # for BLAS and LAPACK have been found. For this, you may need
   # the macOS SDK, installable with `xcode-select --install`.
   cmake --build . --target install

   cd ../..
   export MADXDIR="$(pwd)"/MAD-X/dist
   git clone https://github.com/hibtc/cpymad.git
   cd cpymad
   export CC=clang
   python setup.py build_ext -lblas -llapack
   python setup.py bdist_wheel
   delocate-wheel dist/*.whl
   pip install dist/cpymad-*.whl

   # Optionally, verify the installation of cpymad:
   pip install pandas pytest
   python -m pytest test

Rosetta installation (x86 emulation on Apple Silicon)
-----------------------------------------------------

Install miniforge as above, and then create an x86 conda environment,
like so:

.. code:: bash

   CONDA_SUBDIR=osx-64 conda create -n xsuite-x86 python=3.10
   conda activate xsuite-x86
   conda config --env --set subdir osx-64
   conda install compilers

.. note::

   You may get some warnings similar to
   ``activate_clang:69: read-only file system: /meson_cross_file.txt'``.
   These may be ignored.

After carrying out the above steps, you can install xsuite using the
usual commands, following either the basic or a developer installation
guide, as given at the top of this page.
