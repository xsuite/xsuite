============
Environment
============

.. contents:: Table of Contents
    :depth: 3

What an Environment stores
==========================

An ``xt.Environment`` is the shared container that keeps together:

- **Variables** in ``env.vars``: scalar knobs and deferred expressions used to
  drive elements and lines. Retrieve their current value with ``env['name']``.
- **Elements** in ``env.elements``: magnets, markers, RF cavities, etc. They can
  be reused across multiple lines.
- **Lines** in ``env.lines``: ordered sequences of elements assembled from the
  environment.
- **Reference particles** in ``env.particle_ref`` (and ``env.particles`` for
  additional species): used whenever optics, tracking or conversion to tracks
  requires beam energy or mass information.

Accessing ``env['name']`` returns the *value* of a variable, an element object,
or a line. Accessing ``env.ref['name']`` returns a reference object that keeps
track of expressions; use references whenever you want to build expressions or
inspect dependencies.

Working with variables
======================

Defining variables and deferred expressions
-------------------------------------------

Variables can be provided by direct item assignment. Strings are parsed as
expressions and can mix Python, NumPy, and other variables in the environment.

.. code-block:: python

   import numpy as np
   import xtrack as xt

   env = xt.Environment()
   env['l_q'] = 1.2
   env['kq'] = 0.08
   env['phi'] = np.pi / 8
   env['kq.trim'] = '1.1 * kq'           # deferred expression
   env['kq.total'] = 'kq + kq.trim'

   env['kq.total']                      # -> 0.168

Expressions provided as strings stay deferred: changing an upstream variable
updates all dependents automatically.

.. code-block:: python

   env['kq'] = 0.2
   env['kq.trim']                      # -> 0.22 (recomputed)

Inspecting variables
--------------------

``env.vars.get_table()`` summarizes current values and expressions:

.. code-block:: python

   env.vars.get_table()
   # name      value    expr
   # l_q       1.2      None
   # kq        0.08     None
   # kq.trim   0.088    (1.1 * kq)
   # kq.total  0.168    (kq + kq.trim)

To understand dependencies, fetch the reference and ask for its info:

.. code-block:: python

   env.ref['kq.total']._info()
   # prints:
   # #  vars['kq.total']._get_value()
   #    vars['kq.total'] = 0.168
   #
   # #  vars['kq.total']._expr
   #    vars['kq.total'] = (vars['kq'] + vars['kq.trim'])
   #
   # #  vars['kq.total']._expr._get_dependencies()
   #    vars['kq.trim'] = 0.08800000000000001
   #    vars['kq'] = 0.08
   #
   # #  vars['kq.total'] does not influence any target


   env.ref['kq']._info()
   # prints:
   # #  vars['kq']._get_value()
   #    vars['kq'] = 0.08
   #
   # #  vars['kq']._expr is None
   #
   # #  vars['kq']._find_dependant_targets()
   #    vars['kq.trim']
   #    vars['kq.total']

Deleting and renaming variables
-------------------------------

Variables can be removed or renamed without recreating the environment:

.. code-block:: python

   del env.vars['kq.trim']          # or env.vars.remove('kq.trim')
   env.vars.rename('kq', 'kq.main') # updates expressions automatically

Elements
========

Creating elements
-----------------

Elements can be added directly to ``env.elements`` or created with
``env.new(...)``. The most direct way is to instantiate an element and store it:

.. code-block:: python

   import xtrack as xt

   env = xt.Environment()
   env['kq'] = 0.08
   env['kq.trim'] = '1.1 * kq'
   env['kq.total'] = 'kq + kq.trim'

   env.elements['mq0'] = xt.Quadrupole(length=3.0, k1=0.1)
   env['mq0'].k1 = '0.5 * kq.total'   # attach a deferred expression

Elements can also be created using ``Environment.new``. Deferred expressions can
be specified directly in the constructor:

.. code-block:: python

   env['l_q'] = 1.2
   env['kq'] = 0.08
   env['kq.total'] = '2 * kq'

   env.new('mq1', xt.Quadrupole, length='l_q', k1='kq.total')
   env.new('ms1', xt.Sextupole, length=0.3, k2='-0.5*kq.total')

``env.new`` can also clone an existing element; the parent becomes the prototype
for the new one:

.. code-block:: python

   env.new('mq2', xt.Quadrupole, length='l_q', k1='kq.total')
   env.new('mq2.d', 'mq2', k1='-kq.total')     # clone 'mq2' and override k1

   env['mq2.d'].length      # -> expression 'l_q', inherited from 'mq2'
   env['mq2.d'].k1          # -> expression '-kq.total' (override)

Inspecting deferred attributes
------------------------------

You can inspect deferred attributes the same way as variables:

.. code-block:: python

   env.ref['mq0'].k1._info()
   #  element_refs['mq0'].k1._get_value()
   #    element_refs['mq0'].k1 = 0.084
   #
   #  element_refs['mq0'].k1._expr
   #    element_refs['mq0'].k1 = (0.5 * vars['kq.total'])
   #
   #  element_refs['mq0'].k1._expr._get_dependencies()
   #    vars['kq.total'] = 0.168
   #
   #  element_refs['mq0'].k1 does not influence any target

Listing elements
----------------

To get a table with all the elements stored in the environment (including
attributes), use ``env.elements.get_table(attr=True)``:

.. code-block:: python

   env = xt.Environment()
   env['l_q'] = 1.2
   env['kq'] = 0.08
   env['kq.total'] = '2 * kq'
   env.elements['mq0'] = xt.Quadrupole(length=3.0, k1=0.1)
   env.elements['dr0'] = xt.Drift(length=0.4)
   env.new('mq1', xt.Quadrupole, length='l_q', k1='kq.total')
   env.new('ms1', xt.Sextupole, length=0.3, k2='-0.5*kq.total')
   env.new('dr1', xt.Drift, length=0.2)
   env.new('mq2', xt.Quadrupole, length='l_q', k1='kq.total')
   env.new('mq2.d', 'mq2', k1='-kq.total')

   tt = env.elements.get_table(attr=True)
   tt.cols['name element_type length k1l']
   # Table: 5 rows, 4 cols
   # name  element_type        length           k1l
   # mq0   Quadrupole               3           0.3
   # mq1   Quadrupole             1.2         0.192
   # mq2   Quadrupole             1.2         0.192
   # mq2.d Quadrupole             1.2        -0.192
   # ms1   Sextupole              0.3             0

Setting element properties
--------------------------

``env.set`` assigns numbers or expressions to one or many elements. When a
string is passed, it is treated as a deferred expression.

.. code-block:: python

   env.set('mq2', k1='1.05 * kq.total')
   env.set(['mq2', 'mq2.d'], k2='0.5 * k1')     # broadcast over a list

Removal
-------

Elements can be deleted from the environment:

.. code-block:: python

   del env.elements['mq2.d']        # or env.elements.remove('mq2.d')

Lines
=====

Creating lines
--------------

Lines are assembled from environment elements, other lines, or ``Place`` objects
returned by ``env.new``. They are automatically registered in ``env.lines`` when
given a ``name``.

.. code-block:: python

   cell = env.new_line(name='cell', components=[
       env.place('mq2', at=0.0),
       env.place('mq2.d', at='l_q + 0.5', from_='mq2'),
   ])

You can also create an unnamed line inline:

.. code-block:: python

   arc = env.new_line(['mq2', 'mq2.d', 'mq2'])

Placing with positions and anchors
----------------------------------

Positions accept numbers or expressions. ``from_`` selects the reference
element, and ``anchor``/``from_anchor`` choose whether the start, center
(``'center'``/``'centre'``), or end is used.

.. code-block:: python

   env.new('ip', xt.Marker, at=50)
   env.new('ms', xt.Sextupole, length=0.3,
           at='5', from_='ip', anchor='end', from_anchor='start')

Composing and reusing lines
---------------------------

Lines support algebraic composition (concatenation, repetition, mirroring):

.. code-block:: python

   half_cell = env.new_line([env.place('mq2'), env.place('mq2.d', at='5', from_='mq2')])
   full_cell = -half_cell + half_cell
   ring = 6 * full_cell

In ``compose=True`` mode, the line keeps a composer that can be regenerated when
variables change:

.. code-block:: python

   l = env.new_line(name='l1', compose=True)
   l.new('q1', 'Quadrupole', at='0.5*l_q')
   l.new('q2', 'q1', at='4*l_q', from_='q1@center')

   env['l_q'] = 1.8
   l.regenerate_from_composer()   # rebuilds placements with updated variables

Line inspection
---------------

Use ``line.get_table(attr=True)`` for placement and attribute information, and
``env.lines.get_table()`` for an overview of the lines stored in the
environment.
