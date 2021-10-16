=====================
Numerical portability
=====================

In general Xsuite does not not guarantee the numerical portability of the computation, in the sense that results obtained on different CPUs/GPUs or with different compilers will be different at the level of the machine precision.
This is mostly due to the fact that the underlying python libraries, and in particular numpy and scipy are observed not to be numerically portable. Xsuite compiled code is observed to be numerically portable, if compiled with the same set of compilers. CPU and GPU code context are expected to give results that differ at the level of the machine precision.

We have identified a recipe that allows obtaining numerically portable results from Xsuite. This requires compiling numpy and scipy in a special way, disabling certain vectorization optimizationd and using unoptimized BLAS and LAPACK libraries (impact on numpy and scipy performance is significant).
We underline that such a recipe is observed to yield numerically portable results in the analyzed case of interest and ot the CPUs that we had available but **is not guaranteed to do so in all possible cases**.
We cannot commit on keeping such a features in the future, as this depends on characteristics of underlying libraries that we do not control.
