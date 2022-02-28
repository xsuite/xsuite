.. _installation-page:

============
Installation
============

We assume that you have a recent python installation (python 3.8+). It this is not the case you can make one following the dedicated section on :ref:`how to get a miniconda installation<miniconda>`.

.. contents:: Table of Contents
    :depth: 3

Basic installation
==================

The Xsuite packages can be installed using pip:

.. code-block:: bash

    pip install xsuite

This installation allows using Xsuite on CPU. To use Xsuite on GPU, with the cupy and/or pyopencl you need to install the corresponding packages, as described in the :ref:`dedicated section<gpuinst>`.


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


Optional dependencies
=====================

To import MAD-X lattices you will need the cpymad package, which can be installed as follow:

.. code-block:: bash

    $ pip install cpymad

To import lattices from a set of sixtrack input files (fort.2, fort.3, etc.) you will need the sixtracktools package, which can be installed as follow:

.. code-block:: bash

    $ git clone https://github.com/sixtrack/sixtracktools
    $ pip install -e sixtracktools

Some of the tests rely on pyheadtail to test the corresponding interface:

.. code-block:: bash

    $ git clone https://github.com/pycomplete/pyheadtail
    $ pip install cython
    $ pip install -e pyheadtail

.. _gpuinst:

GPU support
===========

In the following section we describe the steps to install the two supported GPU platforms, i.e. cupy and pyopencl.

Installation of cupy
--------------------

In order to use the :doc:`cupy context<contexts>`, the cupy package needs to be installed.
In Anaconda or Miniconda (if you don't have Anaconda or Miniconda, see dedicated section on :ref:`how to get a miniconda installation<miniconda>`)
this can be done as follows for example for CUDA version 10.1.243:

.. code-block:: bash

    $ conda install mamba -n base -c conda-forge
    $ pip install cupy-cuda101
    $ mamba install cudatoolkit=10.1.243

Remember to check your CUDA version e.g. via ``$ nvcc --version`` and use the appropriate tag.


Installation of PyOpenCL
------------------------

In order to use the :doc:`pyopencl context<contexts>`, the PyOpenCL package needs to be installed.
In Anacoda or Miniconda this can be done as follows:

.. code-block:: bash

    $ conda config --add channels conda-forge
    $ conda install pyopencl


Check that there is an OpenCL installation in the system:

.. code-block:: bash

    $ ls /etc/OpenCL/vendors


Make the OpenCL installation visible to pyopencl:

.. code-block:: bash

    $ conda install ocl-icd-system


For the PyOpenCL context we will need the `gpyfft <https://github.com/geggo/gpyfft>`_ and the `clfft <https://github.com/clMathLibraries/clFFT>`_ libraries.
For this purpose we need to install cython.

.. code-block:: bash

    $ pip install cython


Then we can install clfft.

.. code-block:: bash

    $ conda install -c conda-forge clfft


We locate the library and headers here:

.. code-block:: bash

    $ ls ~/miniconda3/pkgs/clfft-2.12.2-h83d4a3d_1/
    # gives: include  info  lib

(Or locate the directory via ``find $(dirname $(dirname $(type -P conda)))/pkgs -name "clfft*" -type d`` .)

We obtain gpyfft from github:

.. code-block:: bash

    $ git clone https://github.com/geggo/gpyfft

and we install gpyfft with pip providing extra flags as follows:

.. code-block:: bash

     $ pip install --global-option=build_ext --global-option="-I/home/giadarol/miniconda3/pkgs/clfft-2.12.2-h83d4a3d_1/include" --global-option="-L/home/giadarol/miniconda3/pkgs/clfft-2.12.2-h83d4a3d_1/lib" gpyfft/

Alternatively (if the command above does not work) we can edit the ``setup.py`` of gpyfft to provide the right paths to your clfft installation (and potentially the OpenCL directory of your platform):

.. code-block:: python

    if 'Linux' in system:
        CLFFT_DIR = os.path.expanduser('~/miniconda3/pkgs/clfft-2.12.2-h83d4a3d_1/')
        CLFFT_LIB_DIRS = [r'/usr/local/lib64']
        CLFFT_INCL_DIRS = [os.path.join(CLFFT_DIR, 'include'), ] # remove the 'src' part
        CL_INCL_DIRS = ['/opt/rocm-4.0.0/opencl/include']

And install gpyfft locally.

.. code-block:: bash

    $ pip install -e gpyfft/


.. _miniconda:

Install Miniconda
=================

If you don't have a miniconda installation, you can quickly get one ready for xsuite installation with the following steps.

On Linux
--------

.. code-block:: bash

    $ cd ~
    $ wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    $ bash Miniconda3-latest-Linux-x86_64.sh
    $ source miniconda3/bin/activate
    $ pip install numpy scipy matplotlib pandas ipython pytest

On MacOS
--------

.. code-block:: bash

    $ cd ~
    $ curl https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh > miniconda_inst.sh
    $ bash miniconda_inst.sh
    $ source miniconda3/bin/activate
    $ conda install clang_osx-64
    $ pip install numpy scipy matplotlib pandas ipython pytest