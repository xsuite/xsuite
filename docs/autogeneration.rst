Code autogeneration
===================

The xsuite library uses code autogeneration to specialize kernel code for the different contexts.
Three contexts are presently available: ``CPU``, ``CUDA``,  and ``OpenCL``.


The developer writes a single C source code using the portability macros
provided by ``xobjects/headers/common.h``. The preferred macro API includes
``GPUFUN`` for functions callable on the GPU device, ``GPUKERN`` for kernels,
``GPUGLMEM`` for pointers to GPU global memory, ``RESTRICT`` for restrict
qualifiers, and ``VECTORIZE_OVER`` / ``END_VECTORIZE`` for context-dependent
loops. Older sources may still use the comment strings described below; these
legacy annotations are kept for compatibility but should not be used in new
handwritten C code. With macros, typos are caught by the compiler instead of
being silently ignored as unknown comments.

``VECTORIZE_OVER`` block
~~~~~~~~~~~~~~~~~~~~~~~~

The preferred macro syntax is the following:

.. code-block:: C

    VECTORIZE_OVER(myvar, myvarlim);

        [MY CODE]

    END_VECTORIZE;

This is translated into a for loop in the CPU implementation and into a
single-particle block in the parallel implementations (cupy, pyopencl). Older
sources may use the legacy ``//vectorize_over`` and ``//end_vectorize``
comments for the same purpose.

The corresponding CPU code will be:

.. code-block:: C

    for (int myvar=0; myvar<myvarlim; myvar++){ //autovectorized
        [MY CODE]
    } //end autovectorized

The corresponding CUDA code will be:

.. code-block:: C

    int myvar; //autovectorized
    myvar = blockDim.x * blockIdx.x + threadIdx.x; //autovectorized
    if (myvar<myvarlim) { //autovectorized
        [MY CODE]
    } //end autovectorized

The corresponding OpenCL code will be:

.. code-block:: C

    int myvar; //autovectorized
    myvar = get_global_id(0); //autovectorized
        [MY CODE]
    //end autovectorized


Context specific code guards
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Context-specific code should be guarded with the ``XO_CONTEXT_*`` macros
defined by Xobjects at compile time. The available context macros are:

``XO_CONTEXT_CPU``
    Defined for both CPU contexts.

``XO_CONTEXT_CPU_SERIAL``
    Defined for the serial CPU context.

``XO_CONTEXT_CPU_OPENMP``
    Defined for the OpenMP CPU context.

``XO_CONTEXT_CUDA``
    Defined for the CUDA GPU context.

``XO_CONTEXT_CL``
    Defined for the OpenCL GPU context.

For example, CPU-only code can be written as:

.. code-block:: C

    #ifdef XO_CONTEXT_CPU
    #include <math.h>
    #endif

and OpenMP-specific code can be written as:

.. code-block:: C

    #ifdef XO_CONTEXT_CPU_OPENMP
    #pragma omp parallel for
    #endif

Older sources may still use the legacy ``//only_for_context`` directive. New
handwritten C code should use the ``XO_CONTEXT_*`` macros instead so that the
code is more readable and so that the typos are caught by the compiler.

``GPUFUN`` directive
~~~~~~~~~~~~~~~~~~~~

``GPUFUN`` marks a C function that can be called from the kernel code.
On CUDA it expands to ``__device__``; on CPU it expands to ``static inline``.
Use it for helper functions and element tracking functions that need to work
across CPU and GPU contexts.

Legacy C sources can use the ``/*gpufun*/`` directive for the same purpose. New
code should include ``xobjects/headers/common.h`` and use the ``GPUFUN`` macro
instead.

``GPUKERN`` directive
~~~~~~~~~~~~~~~~~~~~~

``GPUKERN`` marks an entry-point kernel function launched by an Xobjects
context. On CUDA it expands to ``__global__``; on OpenCL it expands to
``__kernel``; on CPU it is empty.

Legacy C sources can use the ``/*gpukern*/`` directive for the same purpose.
New code should include ``xobjects/headers/common.h`` and use the ``GPUKERN``
macro instead.


``GPUGLMEM`` directive
~~~~~~~~~~~~~~~~~~~~~~~

``GPUGLMEM`` marks a pointer as referring to global memory in GPU contexts. It
expands to ``__global`` on OpenCL and is empty on CUDA and CPU.

Legacy C sources can use the ``/*gpuglmem*/`` directive for the same purpose.
New code should include ``xobjects/headers/common.h`` and use the ``GPUGLMEM``
macro instead.




