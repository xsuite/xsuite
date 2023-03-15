
=========================
Data management in Xsuite
=========================

.. contents:: Table of Contents
    :depth: 3

Hybrid objects, xofields, xobjects
==================================

Beam elements and Particles objects are hybrid objects built with the Xobjects
package. They contain, along with standard python attributes and methods,
also an "xobject" that can be optionally stored on GPU and made accessible to
the C code used in the implementation.

The set of attributes accessible in C and the corresponding types can be found in
the ``xofields`` dictionary attached to the class. For example:

.. code-block:: python

    xtrack.Multipole._xofields

    # contains:
    # {'order': Int64,
    #  'inv_factorial_order': Float64,
    #  'length': Float64,
    #  'hxl': Float64,
    #  'hyl': Float64,
    #  'radiation_flag': Int64,
    #  'knl': <array ArrNFloat64>,
    #  'ksl': <array ArrNFloat64>,
    #  '_internal_record_id': <struct RecordIdentifier>}

Each instance of the class contains an xobject storing the corresponding data.

For example:

.. code-block:: python

    m = xtrack.Multipole(knl=[1,2,3])

    m._xobject.knl # contains [1,2,3]

All attributes of the xobject are automatically exposed as attributes of the beam element.
For example, ``m._xobject.length`` is the same as ``m.length``.

Arrays are exposed as native Xobjects arrays in the ``_xobject``, and
as numpy or numpy-like arrays as attributes of the beam element. For example:

.. code-block:: python

    m = xtrack.Multipole(knl=[1,2,3])

    m._xobject.knl
    # is an xobjects.Array

    m.knl
    # is a numpy array (or numpy-like on GPU contexts)

    m.knl[0] = 5 # can be modified using numpy-like syntax

It should be noted that the two are different views of the same memory area,
hence any modification can be made indifferently on any of them.

The numpy view (or numpy-like on GPU contexts) gives the possibility of using
numpy-compatible functions and features on the array (e.g. slicing, masking, etc.).
This is especially useful to modify data in-place.

Please note that not all numpy features will work for the numpy-like arrays on GPU contexts.
To make use of such features (e.g. ``np.sum``, ``np.mean``, etc.) you can get a copy
of the array as real numpy array (but modifications will not be possible).

.. code-block:: python

    # only for CPU context:
    np.sum(m.knl) # will throw an exception on PyOpenCl context

    # only for GPU context:
    np.sum(m.knl.get()) # get a numpy array as copy

    # for any context:
    np.sum(m._context.nparray_from_context_array(m.knl)) # get a numpy array as copy


Contexts and buffers
====================

The xobjects are allocated in memory buffers managed by the xobjects package.
Buffers can be allocated on the GPU or on the CPU memory depending on the context.

For example the following code creates two buffer in a GPU memory:

.. code-block:: python

    # We create a GPU context
    context = xobjects.ContextCupy()

    buffer1 = ctx.new_buffer()              # using default initial capacity
    buffer2 = ctx.new_buffer(capacity=1000) # specifying initial capacity

A buffer can contain multiple hybrid objects. For example we can allocate two
objects (``mult1`` and ``mult2``) in ``buffer1`` created above:

.. code-block:: python

    mult1 = xt.Multipole(knl=[1, 2, 3], _buffer=buffer1)
    mult2 = xt.Multipole(knl=[1, 2, 3], _buffer=buffer1)

The capacity of the buffer is automatically increased to fit the allocated objects.

Buffers can also be created implicitly when creating the objects. This is done
by passing the context instead of the buffer. For example:

.. code-block:: python

    context = xobjects.ContextCupy()

    mult1 = xt.Multipole(knl=[1, 2, 3], _context=context)
    mult2 = xt.Multipole(knl=[1, 2, 3], _context=context)

In this case a new buffer is created automatically for each of the objects.
If neither a context nor a buffer is specified, the default context (on CPU)
is used.

The buffer and context of an object can be inspected using the ``_buffer`` and
``_context`` attributes:

.. code-block:: python

    mult1._buffer # gives the buffer of the object
    mult2._context # gives the context of the object

Move and copy operations
========================

Xsuite objects have a ``copy`` method tha can be used copy the objects across
buffers and contexts. For example:

.. code-block:: python

    # we create two multipoles in the default context
    mult1 = xt.Multipole(knl=[1, 2, 3])
    mult2 = xt.Multipole(knl=[3, 4, 5])

    # We create a GPU context
    context_gpu = xobjects.ContextCupy()

    # We make copy of the first object in a GPU context (a new buffer in the
    # GPU memory is created automatically)
    mult1_gpu = mult1.copy(_context=context_gpu)

    # We make a copy of the second multipole to a specific GPU buffer
    buffer_gpu = context_gpu.new_buffer()
    mult2_gpu = mult2.copy(_buffer=buffer_gpu)

    # It no argument is passed to the copy method, the copy is made in the same
    # context as the original object (a new buffer is created).
    another_copy = mult2_gpu.copy()


Similarly, the ``move`` method can be used move objects across buffers and contexts.
For example:

.. code-block:: python

    # we create two multipoles in the default context
    mult1 = xt.Multipole(knl=[1, 2, 3])
    mult2 = xt.Multipole(knl=[3, 4, 5])

    # We create a GPU context
    context_gpu = xobjects.ContextCupy()

    # We move the first object in a GPU context (a new buffer in the
    # GPU memory is created automatically)
    mult1.move(_context=context_gpu)

    # We move the second object to a specific GPU buffer
    buffer_gpu = context_gpu.new_buffer()
    mult2.move(_buffer=buffer_gpu)

Memory management in xtrack trackers
====================================

When the tracker is build, all beam elements are moved to one
buffer in the context specified when the tracker is created. For example:

.. code-block:: python

    # We create a few beam elements
    mult1 = xt.Multipole(knl=[1, 2, 3])
    drift1 = xt.Drift(length=1)
    mult2 = xt.Multipole(knl=[3, 4, 5])
    drift2 = xt.Drift(length=1)
    # Each element is allocated in a different buffer in the default context.
    # For example mult1._buffer is not equal to mult2._buffer, etc.

    # we create a line with the above beam elements
    line = xt.Line(elements=[mult1, drift1, mult2, drift2])
    # each element remains in its original buffer

    # we create a tracker with the above line
    context = xobjects.ContextCupy()
    line.build_tracker(_context=context)
    # the tracker can be instpected in line.tracker

    # this creates a new buffer in the memory associated to the context
    # (accessible as line.tracker._buffer) and moves all the elements to this
    # buffer.
    # Now mult1._buffer is equal to mult2._buffer, etc. and they are all equal
    # to line.tracker._buffer.

References
==========

References can be used to have fields of different objects to point to the same
data. To do so all both the referencing objects and the referenced objects must
be in the same buffer. For example:

.. code-block:: python

    import xobjects as xo

    class Inner(xo.HybridClass):
        _xofields = {
            'num': xo.Int64,
        }

    class Outer(xo.HybridClass):
        _xofields = {
            'inner': Inner,
            'ref_to_inner': xo.Ref(Inner), # is reference
        }

    # We create a buffer
    buffer = xo.ContextCupy().new_buffer()

    # We create an object of type Inner
    inner = Inner(num=1, _buffer=buffer)

    # We create two objects of type Outer
    outer1 = Outer(_buffer=buffer)
    outer2 = Outer(_buffer=buffer)

    # We set the reference of outer1 and outer2 to inner
    outer1.ref_to_inner = inner
    outer2.ref_to_inner = inner

    # We change the value of inner.num
    inner.num = 2

    # We check that the value of outer1.inner.num and outer2.inner.num have
    # changed as well
    print(outer1.inner.num) # prints 2
    print(outer2.inner.num) # prints 2

Advanced memory behaviours with HybridClass
===========================================

When instantiating, moving, copying, or assigning values to fields of a
``HybridClass``, especially if such a class contains references, in some
advanced cases the expected behaviour of such operations is not obvious.
Below we present comprehensive set of scenarios that demonstrate when values
are copied, and which operations are disallowed.

We shall use the following example classes throughout this section:

.. code-block:: python

    import xobjects as xo

    class Inner(xo.HybridClass):
        _xofields = {
            'num': xo.Int64,
        }

    class Outer(xo.HybridClass):
        _xofields = {
            'inner': Inner,
            'ref': xo.Ref(Inner),
        }

As well as the following function, which prints a summary of where a
``HybridClass`` is located in memory.

.. code-block:: python

    def whereis(obj: xo.HybridClass, _buffers=[]):
        context = obj._context.__class__.__name__
        if obj._buffer in _buffers:
            buffer_id = _buffers.index(obj._buffer)
        else:
            buffer_id = len(_buffers)
            _buffers.append(obj._buffer)
        offset = obj._offset
        print(f"context={context}, buffer={buffer_id}, offset={offset}")

Initialising nested objects
---------------------------

Below ``Outer`` is instantiated in the same buffer as ``Inner``, and so
the reference field ``outer.ref`` is bound to the same xobject as ``inner``.
Therefore, any changes to one are applied to another.

.. code-block:: python

    buf = xo.context_default.new_buffer()
    inner = Inner(num=42, _buffer=buf)
    outer = Outer(inner=inner, ref=inner, _buffer=buf)

    whereis(outer)          # => context=ContextCpu, buffer=0, offset=8
    whereis(outer.inner)    # ditto, since outer.inner is the first field of outer
    whereis(outer.ref)      # => context=ContextCpu, buffer=0, offset=0
    whereis(inner)          # ditto, since the reference points to the original object

    inner.num = 14          # changing inner...
    print(outer.ref.num)    # (=> 14) changes outer.ref...
    print(outer.inner.num)  # (=> 42) but not the copied outer.inner

Since a reference to an object in a different buffer to the one owning the
reference is disallowed, below, when  ``Outer`` is instantiated with an
``inner`` object coming from a different buffer, an error is produced.

.. code-block:: python

    # If unspecified, every object gets its own buffer:
    inner = Inner(num=7)
    outer = Outer(inner=inner, ref=inner)
    # Gives MemoryError - Cannot make a reference to an object in a different
    #                     buffer.


Same behaviour can be observed when instantiating ``Outer`` with an ``inner``
coming from a different context (and therefore a different buffer):

.. code-block:: python

    context_cpu = xo.ContextCpu()
    context_ocl = xo.ContextPyopencl()

    inner = Inner(num=99, _context=context_cpu)
    outer = Outer(inner=inner, ref=inner, _context=context_ocl)
    # Gives MemoryError - Cannot make a reference to an object in a different
    #                     buffer.

When fields are assigned to an already instantiated hybrid object, as opposed to
doing that in the initialiser, the behaviour is analogous to the above.

Moving (nested objects)
-----------------------

In general, we cannot move the objects of type ``Outer`` from the examples
before, as ``Outer`` contains references:

.. code-block:: python

    buffer = xo.context_default.new_buffer(capacity=256)
    inner = Inner(num=0x1020_3040_5060_7080, _buffer=buffer)
    outer = Outer(inner=inner, ref=inner, _buffer=buffer)

    outer.move(_context=xo.ContextPyopencl())
    # Gives an error as the object cannot be moved, as it contains references
    # to other objects.

We also prohibit moving any of the fields of ``outer``, as they are part of
an underlying fixed structure defined by the ``xo.Struct`` associated with
the hybrid class ``Outer``:

.. code-block:: python

    outer.inner.move(_context=xo.ContextPyopencl())
    # Gives an error as the object cannot be moved, as it contains references
    # to other objects.

In all cases when we move an object specifying ``_offset`` manually, we risk the
corruption of the data in the buffer. See the below example of a potentially
destructive behaviour.

.. code-block:: python

    buffer = xo.context_default.new_buffer(capacity=256)
    inner = Inner(num=0x1122_3344_5566_7788, _buffer=buffer)
    inner2 = Inner(num=0x1020_3040_5060_7080, _buffer=buffer)

    # let us see the value of inner2.num:
    print(inner2.num)  # => 0x1020_3040_5060_7080

    inner.move(_offset=4, _buffer=buffer)

    # as a result of the above move, inner2 is corrupted, as we moved
    # inner such that it overlaps with inner2 in the buffer
    print(inner2.num)  # => 0x1020_3040_1122_3344

When ``_offset`` is not given, ``xsuite`` will automatically move the object
safely to the free space in the buffer, expanding it, if needed.

.. code-block:: python

    inner1 = Inner(num=135)
    inner2 = Inner(num=531)

    whereis(inner1)		# => context=ContextCpu, buffer=6, offset=0
    whereis(inner2)		# => context=ContextCpu, buffer=7, offset=0

    buffer = xo.context_default.new_buffer(capacity=16)

    inner2.move(_buffer=buffer)
    inner1.move(_buffer=buffer)

    # inner1 and inner2 are moved to buffer, safely next to each other:
    whereis(inner1)		# => context=ContextCpu, buffer=8, offset=8
    whereis(inner2)		# => context=ContextCpu, buffer=8, offset=0

The same holds true for moving objects between contexts:

.. code-block:: python

    # We make sure our two objects are on the CPU context:
    inner1 = Inner(num=10, _context=xo.ContextCpu())
    inner2 = Inner(num=-10, _context=xo.ContextCpu())

    inner1.move(_context=xo.ContextPyopencl())
    inner2.move(_context=xo.ContextPyopencl())

    # After we move them to the OpenCL context, they are by default in separate buffers
    whereis(inner1)		# => context=ContextPyopencl, buffer=9, offset=0
    whereis(inner2)		# => context=ContextPyopencl, buffer=10, offset=0

    # We can place them in the same buffer, as before. Let us try the CUDA context:
    context_cuda = xo.ContextCupy()
    buffer = context_cuda.new_buffer(capacity=1) # (note that the buffer will grow)

    inner1.move(_buffer=buffer, _context=context_cuda)
    inner2.move(_buffer=buffer, _context=context_cuda)

    # We can see that the objects are next to each other:
    whereis(inner1)		# => context=ContextCupy, buffer=11, offset=0
    whereis(inner2)		# => context=ContextCupy, buffer=11, offset=8

It is important to know, that some of the types will be different between
contexts. This applies in particular to arrays:

.. code-block:: python

    class TestArrays(xo.HybridClass):
        _xofields = {
            'array': xo.Int8[8],
        }

    test_cpu = TestArrays(array=range(8), _context=xo.ContextCpu())
    test_cl = TestArrays(array=range(8), _context=xo.ContextPyopencl())
    test_cupy = TestArrays(array=range(8), _context=xo.ContextCupy())

    print(test_cpu.array)	# => list(range(8))
    print(test_cl.array)	# ditto
    print(test_cupy.array) 	# ditto

    print([type(x.array) for x in (test_cpu, test_cl, test_cupy)])
                # => [numpy.ndarray, pyopencl.array.Array, cupy.ndarray]


Xobject conventions on memory initialization
--------------------------------------------

Xobject always accepts a combination of `_context`, `_buffer`, `_offset` to indentify and/or allocate the memory to which data is written:


======== ======== ======== ==================================================================================
             Inputs           Output
-------------------------- ----------------------------------------------------------------------------------
_context  _buffer  _offset  xobject
======== ======== ======== ==================================================================================
  None     None     None    `ContextCPU` is used to allocate an new buffer, allocate new memory at 0 offset
not None   None     None    `_context` is used to allocate a new buffer and allocate new memory at 0 offset
  None   not None   None    `_buffer` is used to allocate new memory at the first free offset
  None   not None not None  memory at `_offset` in `_buffer` is used without allocation
======== ======== ======== ==================================================================================

Other combinations are not meaningful and should raise an exception (to be implemented).
