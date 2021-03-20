.. _installation-page:

Installation
============


The packages can be cloned from GitHub and installed with pip:

.. code-block:: bash

    $ git clone https://github.com/xsuite/xobjects
    $ pip install -e xobjects

    $ git clone https://github.com/xsuite/xfields
    $ pip install -e xfields

(The installation without the ``-e`` option is still untested).


Installation of cupy
--------------------

In order to use the :doc:`cupy context<contexts>`, the cupy package needs to be installed.
In Anacoda or Miniconda (if you don't have Anaconda or Miniconda, see dedicated section on :ref:`how to get a miniconda installation<miniconda>`)
this can be done as follows:

.. code-block:: bash

    $ conda install mamba -n base -c conda-forge
    $ pip install cupy-cuda101
    $ mamba install cudatoolkit=10.1.243


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


We install gpyfft install pip providing extra flags as follows:

.. code-block:: bash

    $ git clone https://github.com/geggo/gpyfft
    $ pip install --global-option=build_ext --global-option="-I/home/giadarol/miniconda3/pkgs/clfft-2.12.2-h83d4a3d_1/include" --global-option="-L/home/giadarol/miniconda3/pkgs/clfft-2.12.2-h83d4a3d_1/lib" gpyfft/


.. _miniconda:

Install Miniconda
-----------------

If you don't have a miniconda installation, you can quickly get one with the following steps:

.. code-block:: bash

    $ cd ~
    $ wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    $ bash Miniconda3-latest-Linux-x86_64.sh
    $ source miniconda3/bin/activate
    $ pip install numpy scipy matplotlib pandas ipython
