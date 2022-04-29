Code autogeneration
===================

The xsuite library uses code autogeneration to specialize kernel code for the different contexts.
Three contexts are presently available: ``cpu``, ``cuda``,  and ``opencl``.


The developer writes a single C source code, providing additional information through the comment strings (annotations) described in the following.

``vectorize_over`` block
~~~~~~~~~~~~~~~~~~~~~~~~

The syntax is the following:

.. code-block:: C

    for (int myvar=0; myvar<myvarlim; myvar++){ //vectorize_over myvar myvarlim

        [MY CODE]

    }//end_vectorize

This is translated into a for loop in the CPU implementation and in a kernel function for the parallel implementations (cupy, pyopencl).

The generated cpu code will be:

.. code-block:: C

    for (int myvar=0; myvar<myvarlim; myvar++){ //autovectorized

        [MY CODE]

        }//end autovectorized

The generated CUDA code will be:

.. code-block:: C

    int myvar; //autovectorized
    myvar = blockDim.x * blockIdx.x + threadIdx.x; //autovectorized
    if (myvar<myvarlim) { //autovectorized

        [MY CODE]

    }//end autovectorized

The corresponding generated OpenCL code will be:

.. code-block:: C

    int myvar; //autovectorized
    myvar = get_global_id(0); //autovectorized

        [MY CODE]

    //end autovectorized


``only_for_context`` directive
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The ``\\only_for_context`` directive can be used to include a givem line only for a certain context.
For example with the following code the line marked line is included only in the GPU implementation.

.. code-block:: C

    #include <atomicadd.h> //only_for_context cpu

``gpufun`` directive
    ~~~~~~~~~~~~~~~~~~~~~
    
    The ``\*gpufun*\`` directive is used to qualify device functions. The code generator replaces it with ``__device__`` in the CUDA code.
    

``gpukern`` directive
~~~~~~~~~~~~~~~~~~~~~

The ``\*gpukern*\`` directive is used to qualify kernel functions. The code generator replaces it with ``__global__`` in the CUDA code and with ``__kernel`` in the OpenCL code.


``gpuglmem`` directive
~~~~~~~~~~~~~~~~~~~~~~~

The ``\*gpuglmem*\`` directive is used to qualify pointers to locations in the device global memoru. The code generator replaces it with ``__global`` in the OpenCL code.










