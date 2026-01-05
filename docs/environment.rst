==================
Xsuite environment
==================

.. contents:: Table of Contents
    :depth: 3

Overview
========

An ``xt.Environment`` is the shared container that keeps together:

- **Variables** in ``env.vars``: scalar knobs and deferred expressions used to
  drive elements and lines. Retrieve their current value with ``env['name']``.
- **Elements** in ``env.elements``: magnets, markers, RF cavities, etc. They can
  be reused across multiple lines.
- **Lines** in ``env.lines``: ordered sequences of elements assembled from the
  environment.
- **Additional data** including reference particles and user-defined functions.

Accessing ``env['name']`` returns the *value* of a variable, an element object,
or a line. Accessing ``env.ref['name']`` returns a reference object that keeps
track of expressions; use references whenever you want to build expressions or
inspect dependencies.
The contents of all these containers can be inspected with the ``.get_table()``
method, and a list of all names in each container is available with the ``.keys()``
method.

A simple example illustrating the creation of an environment with variables,
elements, and lines is shown below:

.. code-block:: python

   import xtrack as xt

   # Create an environment
   env = xt.Environment()

   # Define variables
   env['t_turn_s'] = 0.0
   env['l_q'] = 1.0
   env['kq'] = 0.12
   env['kq.trim'] = '0.05 * kq' # deferred expression (is updated when kq changes)
   env['kq.total'] = 'kq + kq.trim' # deferred expression

   # Create elements reusing the variables
   env.new('qf', xt.Quadrupole, length='l_q', k1='kq.total')
   env.new('qd', xt.Quadrupole, length='l_q', k1='-kq.total')
   env.new('dr', xt.Drift, length=6.0)

   # Define two lines from the same elements
   env.new_line(name='fodo', components=['qf', 'dr', 'qd', 'dr'])
   env.new_line(name='half_fodo', components=['qf', 'dr'])

   # Inspect containers
   env.vars.get_table()
   # VarsTable: 5 rows, 3 cols
   # name             value expr
   # t_turn_s             0 None
   # l_q                  1 None
   # kq                0.12 None
   # kq.trim          0.006 (0.05 * kq)
   # kq.total         0.126 (kq + kq.trim)
   env.elements.get_table()
   # Table: 3 rows, 7 cols
   # name element_type isthick isreplica parent_name iscollective ...
   # dr   Drift           True     False None               False
   # qd   Quadrupole      True     False None               False
   # qf   Quadrupole      True     False None               False
   env.lines.get_table()
   # Table: 2 rows, 3 cols
   # name      num_elements mode
   # fodo                 4 normal
   # half_fodo            2 normal

   # Quick name listings
   env.vars.keys()      # is: ['t_turn_s', 'l_q', 'kq', 'kq.trim', 'kq.total']
   env.elements.keys()  # is: ['dr', 'qd', 'qf']
   env.lines.keys()     # is: ['fodo', 'half_fodo']

   # Inspect a deferred expression with references
   env.ref['qf'].k1._info()
   #  element_refs['qf'].k1._get_value()
   #    element_refs['qf'].k1 = 0.126
   #
   #  element_refs['qf'].k1._expr
   #    element_refs['qf'].k1 = vars['kq.total']
   #
   #  element_refs['qf'].k1._expr._get_dependencies()
   #    vars['kq.total'] = 0.126
   #
   #  element_refs['qf'].k1 does not influence any target
   env.ref['kq.total']._info()
   #  vars['kq.total']._get_value()
   #    vars['kq.total'] = 0.126
   #
   #  vars['kq.total']._expr
   #    vars['kq.total'] = (vars['kq'] + vars['kq.trim'])
   #
   #  vars['kq.total']._expr._get_dependencies()
   #    vars['kq.trim'] = 0.006
   #    vars['kq'] = 0.12
   #
   #  vars['kq.total']._find_dependant_targets()
   #    element_refs['qd'].k1
   #    element_refs['qf'].k1


Variables
=========

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

Renaming variables
------------------

Variables can renamed as follows

.. code-block:: python

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
   # Table: 7 rows, 4 cols
   # name  element_type        length           k1l
   # dr0   Drift                  0.4             0
   # dr1   Drift                  0.2             0
   # mq0   Quadrupole               3           0.3
   # mq1   Quadrupole             1.2         0.192
   # mq2   Quadrupole             1.2         0.192
   # mq2.d Quadrupole             1.2        -0.192
   # ms1   Sextupole              0.3             0

Tables support convenient filtering and regex matching:

.. code-block:: python

   tt.rows['mq.*']
   # Table: 4 rows, 124 cols
   # name  element_type isthick isreplica parent_name ...
   # mq0   Quadrupole      True     False None
   # mq1   Quadrupole      True     False None
   # mq2   Quadrupole      True     False None
   # mq2.d Quadrupole      True     False None

   tt.rows.match(element_type='Dr.*|Sext.*')
   # Table: 3 rows, 124 cols
   # name element_type isthick isreplica parent_name ...
   # dr0  Drift           True     False None
   # dr1  Drift           True     False None
   # ms1  Sextupole       True     False None

   tt.rows.match_not(element_type='Dr.*')
   # Table: 5 rows, 124 cols
   # name  element_type isthick isreplica parent_name ...
   # mq0   Quadrupole      True     False None
   # mq1   Quadrupole      True     False None
   # mq2   Quadrupole      True     False None
   # mq2.d Quadrupole      True     False None
   # ms1   Sextupole       True     False None

Setting element properties
--------------------------

``env.set`` assigns numbers or expressions to one or many elements. When a
string is passed, it is treated as a deferred expression.

.. code-block:: python

   env.set('mq2', k1='1.05 * kq.total')
   env.set(['mq2', 'mq2.d'], k1='0.5 * kq.total')     # broadcast over a list

You can also target groups via table filters:

.. code-block:: python

   tt = env.elements.get_table(attr=True)
   tt_quad = tt.rows.match(element_type='Quadrupole')
   tt_quad
   # Table: 4 rows, 124 cols
   # name  element_type isthick isreplica parent_name ...
   # mq0   Quadrupole      True     False None
   # mq1   Quadrupole      True     False None
   # mq2   Quadrupole      True     False None
   # mq2.d Quadrupole      True     False None

   env.set(tt_quad, integrator='yoshida4')  # applies to all quads above

Remove elements
---------------

Elements can be deleted from the environment when they are not used in any line:

.. code-block:: python

   del env.elements['mq2.d']        # or env.elements.remove('mq2.d')

Lines
=====

Create line as list of existing elements
----------------------------------------

The simplest way to create a line is to define it as a sequence of existing
elements:

.. code-block:: python

   env = xt.Environment()
   env.new('qf', xt.Quadrupole, length=1.0, k1=0.1)
   env.new('qd', xt.Quadrupole, length=1.0, k1=-0.1)
   env.new('dr', xt.Drift, length=5.0)

   myline = env.new_line(components=['qf', 'dr', 'qd', 'dr'])

In this case, the line is created but not stored in ``env.lines``. Storing it
ensures it is saved with the environment:

.. code-block:: python

   env.lines['fodo'] = myline

Alternatively, pass a name to store it automatically:

.. code-block:: python

   env.new_line(name='fodo', components=['qf', 'dr', 'qd', 'dr'])

Once stored, it is accessible as ``env['fodo']`` or ``env.fodo``. 




Line inspection
---------------

You can inspect a line using ``line.get_table()``:

.. code-block:: python

   env['fodo'].get_table()
   # Table: 5 rows, 11 cols
   # name                   s element_type isthick isreplica ...
   # qf                     0 Quadrupole      True     False
   # dr::0                  1 Drift           True     False
   # qd                     6 Quadrupole      True     False
   # dr::1                  7 Drift           True     False
   # _end_point            12                False     False

Create line by placing elements
-------------------------------

Lines can also be defined by specifying element positions, either absolute or
relative to other elements:

.. code-block:: python

   env = xt.Environment()
   env['s.q1'] = 3.0
   env['s.q2'] = 5.0
   env['ds.q4'] = 5.0
   env['kquad'] = 0.1
   env['line_length'] = 12.0
   env.new('q1', xt.Quadrupole, length=1.0, k1='kquad')
   env.new('q2', xt.Quadrupole, length=1.0, k1='-kquad')
   env.new('q3', xt.Quadrupole, length=1.0, k1='kquad')
   env.new('q4', xt.Quadrupole, length=1.0, k1='-kquad')
   env.new('s4', xt.Sextupole, length=0.1)

   myline = env.new_line(name='myline', length='line_length', components=[
       env.place('q1', at='s.q1'),                       # center at s=3.0
       env.place('q2', anchor='start', at=5.0),          # start at s=5.0
       env.place('q3', anchor='start', at='q2@end'),     # start at end of q2
       env.place('q4', anchor='center', at='ds.q4',
                 from_='q3@start'),                      # center 5 m from q3 start
       env.place('s4'),                                  # right after previous
   ])

   tt = myline.get_table()
   tt.show(cols=['s_start', 's_center', 's_end'])
   # name             s_start      s_center         s_end
   # ||drift_1              0          1.25           2.5
   # q1                   2.5             3           3.5
   # ||drift_2            3.5          4.25             5
   # q2                     5           5.5             6
   # q3                     6           6.5             7
   # ||drift_3              7          8.75          10.5
   # q4                  10.5            11          11.5
   # s4                  11.5         11.55          11.6
   # ||drift_4           11.6          11.8            12
   # _end_point            12            12            12

Elements can also be created and placed with a single instruction:

.. code-block:: python

   myline2 = env.new_line(name='myline2', length='line_length', components=[
       env.new('q10', xt.Quadrupole, length=1.0, k1='kquad', at='s.q1'),
       env.new('q20', xt.Quadrupole, length=1.0, k1='-kquad',
               anchor='start', at=5.0),
       env.new('q30', xt.Quadrupole, length=1.0, k1='kquad',
               anchor='start', at='q20@end'),
       env.new('q40', xt.Quadrupole, length=1.0, k1='-kquad',
               anchor='center', at='ds.q4', from_='q30@start'),
       env.new('s40', xt.Sextupole, length=0.1),  # placed after previous
   ])

   tt = myline2.get_table()
   tt.show(cols=['s_start', 's_center', 's_end'])
   # name             s_start      s_center         s_end
   # ||drift_4              0          1.25           2.5
   # q10                  2.5             3           3.5
   # ||drift_5            3.5          4.25             5
   # q20                    5           5.5             6
   # q30                    6           6.5             7
   # ||drift_6              7          8.75          10.5
   # q40                 10.5            11          11.5
   # s40                 11.5         11.55          11.6
   # ||drift_7           11.6          11.8            12
   # _end_point            12            12            12

"compose" mode
--------------

When the line contains many element, it is inconvenient to have to specify all
components in a single Python statement. In this case, it is possible to use the
"compose" mode, where each component is added by a separate instruction, as
illustrated in the following example:

.. code-block:: python

   env = xt.Environment()
   env['s.q1'] = 3.0
   env['s.q2'] = 5.0
   env['ds.q4'] = 5.0
   env['kquad'] = 0.1
   env['line_length'] = 12.0
   env.new('q1', xt.Quadrupole, length=1.0, k1='kquad')
   env.new('q2', xt.Quadrupole, length=1.0, k1='-kquad')
   env.new('q3', xt.Quadrupole, length=1.0, k1='kquad')
   env.new('q4', xt.Quadrupole, length=1.0, k1='-kquad')
   env.new('s4', xt.Sextupole, length=0.1)

   myline = env.new_line(name='myline', length='line_length', compose=True)

   myline.place('q1', at='s.q1')                                     # center at s=3.0
   myline.place('q2', anchor='start', at=5.0)                        # start at s=5.0
   myline.place('q3', anchor='start', at='q2@end')                   # start at end of q2
   myline.place('q4', anchor='center', at='ds.q4', from_='q3@start') # center 5 m from q3 start
   myline.place('s4')                                                # right after previous

   myline.end_compose()

   tt = myline.get_table()
   tt.show(cols=['s_start', 's_center', 's_end'])
   # name             s_start      s_center         s_end
   # ||drift_1              0          1.25           2.5
   # q1                   2.5             3           3.5
   # ||drift_2            3.5          4.25             5
   # q2                     5           5.5             6
   # q3                     6           6.5             7
   # ||drift_3              7          8.75          10.5
   # q4                  10.5            11          11.5
   # s4                  11.5         11.55          11.6
   # ||drift_4           11.6          11.8            12
   # _end_point            12            12            12

Also in compose mode, elements can be created inline while placing them:

.. code-block:: python

   myline2 = env.new_line(name='myline2', length='line_length', compose=True)

   myline2.new('q10', xt.Quadrupole, length=1.0, k1='kquad', at='s.q1'),
   myline2.new('q20', xt.Quadrupole, length=1.0, k1='-kquad', anchor='start', at=5.0),
   myline2.new('q30', xt.Quadrupole, length=1.0, k1='kquad', anchor='start', at='q20@end'),
   myline2.new('q40', xt.Quadrupole, length=1.0, k1='-kquad',
               anchor='center', at='ds.q4', from_='q30@start'),
   myline2.new('s40', xt.Sextupole, length=0.1),  # placed after previous

   myline2.end_compose()

   tt = myline2.get_table()
   tt.show(cols=['s_start', 's_center', 's_end'])
   # name             s_start      s_center         s_end
   # ||drift_4              0          1.25           2.5
   # q10                  2.5             3           3.5
   # ||drift_5            3.5          4.25             5
   # q20                    5           5.5             6
   # q30                    6           6.5             7
   # ||drift_6              7          8.75          10.5
   # q40                 10.5            11          11.5
   # s40                 11.5         11.55          11.6
   # ||drift_7           11.6          11.8            12
   # _end_point            12            12            12

Placing sub-lines at given s positions
--------------------------------------

As for normal elements, it is possible to place sublines at given s positions
within a longer line. This is illustrated in the following example:

.. literalinclude:: generated_code_snippets/place_line_at_s.py
   :language: python


Line mirroring and composition
------------------------------

Lines can be mirrored with the unary minus operator and combined with addition
and multiplication:

.. code-block:: python

   env = xt.Environment()
   env.particle_ref = xt.Particles(p0c=2e9, mass0=xt.PROTON_MASS_EV)
   env['pi'] = np.pi
   env['l_bend'] = 3.5
   env['l_quad'] = 1.0
   env['l_cell'] = 20.0
   env['n_bends'] = 24
   env['angle_bend'] = 'pi / n_bends'

   env.new('mq', xt.Quadrupole, length='l_quad')
   env.new('mb', xt.Bend, length='l_bend', angle='angle_bend')
   env.new('mqf', 'mq', k1=0.1)
   env.new('mqd', 'mq', k1=-0.1)

   arc_half_cell = env.new_line(components=[
       env.place('mqf'),
       env.place('mb', at='l_cell/4 - (l_bend/2 + 0.2)', from_='mqf'),
       env.place('mb', at='l_cell/4 + (l_bend/2 + 0.2)', from_='mqf'),
       env.place('mqd', at='l_cell/2 - l_quad/2', from_='mqf'),
   ])

   mirror_arc_half_cell = -arc_half_cell
   mirror_arc_half_cell.get_table()
   # Table: 8 rows, 11 cols
   # name                   s element_type isthick isreplica parent_name ...
   # mqd                    0 Quadrupole      True     False None
   # ||drift_3              1 Drift           True     False None
   # mb::0                1.3 Bend            True     False None
   # ||drift_2            4.8 Drift           True     False None
   # mb::1                5.2 Bend            True     False None
   # ||drift_1            8.7 Drift           True     False None
   # mqf                  9.5 Quadrupole      True     False None
   # _end_point          10.5                False     False None

   arc_cell = -arc_half_cell + arc_half_cell   # mirror then concatenate
   arc_cell.get_table()
   # Table: 15 rows, 11 cols
   # name                     s element_type isthick isreplica parent_name ...
   # mqd::0                   0 Quadrupole      True     False None
   # ||drift_3::0             1 Drift           True     False None
   # mb::0                  1.3 Bend            True     False None
   # ||drift_2::0           4.8 Drift           True     False None
   # mb::1                  5.2 Bend            True     False None
   # ||drift_1::0           8.7 Drift           True     False None
   # mqf::0                 9.5 Quadrupole      True     False None
   # mqf::1                10.5 Quadrupole      True     False None
   # ||drift_1::1          11.5 Drift           True     False None
   # mb::2                 12.3 Bend            True     False None
   # ||drift_2::1          15.8 Drift           True     False None
   # mb::3                 16.2 Bend            True     False None
   # ||drift_3::1          19.7 Drift           True     False None
   # mqd::1                  20 Quadrupole      True     False None
   # _end_point              21                False     False None
   
   arc = 2 * arc_cell
   arc.get_table()
   # Table: 29 rows, 11 cols
   # name                     s element_type isthick isreplica parent_name ...
   # mqd.l::0                 0 Quadrupole      True      True mqd
   # ||drift_3::0             1 Drift           True     False None
   # mb2.l::0               1.3 Bend            True      True mb2
   # ||drift_2::0           4.8 Drift           True     False None
   # mb1.l::0               5.2 Bend            True      True mb1
   # ||drift_1::0           8.7 Drift           True     False None
   # mqf.l::0               9.5 Quadrupole      True      True mqf
   # mqf.r::0              10.5 Quadrupole      True      True mqf
   # ||drift_1::1          11.5 Drift           True     False None
   # mb1.r::0              12.3 Bend            True      True mb1
   # ||drift_2::1          15.8 Drift           True     False None
   # mb2.r::0              16.2 Bend            True      True mb2
   # ||drift_3::1          19.7 Drift           True     False None
   # mqd.r::0                20 Quadrupole      True      True mqd
   # mqd.l::1                21 Quadrupole      True      True mqd
   # ||drift_3::2            22 Drift           True     False None
   # mb2.l::1              22.3 Bend            True      True mb2
   # ||drift_2::2          25.8 Drift           True     False None
   # mb1.l::1              26.2 Bend            True      True mb1
   # ||drift_1::2          29.7 Drift           True     False None
   # mqf.l::1              30.5 Quadrupole      True      True mqf
   # mqf.r::1              31.5 Quadrupole      True      True mqf
   # ||drift_1::3          32.5 Drift           True     False None
   # mb1.r::1              33.3 Bend            True      True mb1
   # ||drift_2::3          36.8 Drift           True     False None
   # mb2.r::1              37.2 Bend            True      True mb2
   # ||drift_3::3          40.7 Drift           True     False None
   # mqd.r::1                41 Quadrupole      True      True mqd
   # _end_point              42                False     False None

Insert elements
---------------

It is possible to insert elements in a line also after its creation. The position
of the new elements can be specified as absolute s position or as relative to
an existing element. This is illustrated in the following example:

.. literalinclude:: generated_code_snippets/insert_element.py
   :language: python

Insert custom elements and elements instantiated by the user
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is possible to insert elements that are created by the user using the class
directly instead of using the `Environment.new` method. This can be done in a single
step or alternatively by first adding the element to the environment and then
inserting it in the line. This is illustrated in the following example:

.. literalinclude:: generated_code_snippets/insert_element_instantiated_by_user.py
   :language: python

Insert a line into another line
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is also possible to insert entire lines, as illustrated in the following example:

.. literalinclude:: generated_code_snippets/insert_line.py
   :language: python

Simplified syntax for single insertion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A compact syntax is available to perform a single insertion in a line. Note that
when multiple insertions need to be made, it is significantly faster to install
all the elements at once, as shown in the previous example. The compact syntax
for single insertion is illustrated in the following example:

.. literalinclude:: generated_code_snippets/insert_element_single.py
   :language: python

Append elements to a line
-------------------------

New elements can also be installed at the end of a line, as illustrated in the
following example:

.. literalinclude:: generated_code_snippets/append_elements.py
   :language: python

Remove elements from a line
---------------------------

Elements can be removed from a line using the `Line.remove` method. Thick elements
are replaced by drift spaces, so that the position of all other elements is
preserved. This is illustrated in the following example:

.. literalinclude:: generated_code_snippets/remove_elements.py
   :language: python

Replace elements in a line
--------------------------

Elements in a line can be replaced with elements having the same length, as
illustrated in the following example:

.. literalinclude:: generated_code_snippets/replace_elements.py
   :language: python

Slice elements in a line
------------------------

It is possible to slice thick element with thin or thick slices, using the Uniform
or the `Teapot <https://cds.cern.ch/record/165372>`_ scheme. This is illustrated
in the following example:

.. literalinclude:: generated_code_snippets/slicing.py
   :language: python

Cut line elements at given s positions
--------------------------------------

The method :meth:`xtrack.Line.cut_at_s` allows for cutting the line elements at the
specified s positions. In the example before we take the same toy ring introduced
in the :ref:`earlier example<createline>` and we cut it into 100 equal length slices:

.. literalinclude:: generated_code_snippets/cut_at_s.py
   :language: python

Remove lines
------------

Lines stored in the environment can be removed with ``del``:

.. code-block:: python

   del env.lines['fodo']

Reference particles
===================

Reference particles define the beam mass, energy, and charge used by optics
tools such as ``Line.twiss``. A reference particle must be set before running
Twiss.

Set directly on a line
----------------------

Assign a built-in species with the desired energy (total energy in eV):

.. code-block:: python

   import xtrack as xt

   env = xt.Environment()

   env['l_quad'] = 1.0
   env['k_quad'] = 0.1
   env.new('qf', xt.Quadrupole, length='l_quad', k1='k_quad')
   env.new('qd', xt.Quadrupole, length='l_quad', k1='-k_quad')
   env.new('dr', xt.Drift, length=5.0)

   line = env.new_line(components=['qf', 'dr', 'qd', 'dr'])

   line.set_particle_ref('proton', energy0=2e9)  # 2 GeV total energy

   # alternative set the momentum, kinetic energy, or gamma
   # line.set_particle_ref('proton', p0c=2e9)
   # line.set_particle_ref('proton', kinetic_energy0=200e6)
   # line.set_particle_ref('proton', gamma0=10.5)

   # set mass0, charge0 instead of particle type
   # line.set_particle_ref(mass0=xt.PROTON_MASS_EV, charge0=1, p0c=2e9)

   tw = line.twiss4d()  # uses the reference particle above

Reuse particles stored in the environment
-----------------------------------------

You can define reusable particles (optionally with deferred expressions) and
attach them as the line reference. Particles can live in the environment and be
driven by variables.

.. code-block:: python

   import xtrack as xt

   env = xt.Environment()
   env['energy_gev'] = 5.0

   env.new_particle(name='my_ref_part',
                    mass0=xt.PROTON_MASS_EV,
                    q0=1,
                    energy0='energy_gev * 1e9')  # deferred expression

   # Inspect stored particles in the environment
   env.particles.get_table()
   # is:
   # Table: 1 row, 7 cols
   # name                mass0       charge0       energy0           p0c ...
   # my_ref_part   9.38272e+08             1      5.25e+09   5.16548e+09

   # Any line built from this environment can reuse the same particle definition
   line = env.new_line(name='ring', components=[
         env.new('qf', xt.Quadrupole, length=1.0, k1=0.1),
         env.new('dr', xt.Drift, length=5.0),
         env.new('qd', xt.Quadrupole, length=1.0, k1=-0.1),
         env.new('dr2', xt.Drift, length=5.0),
      ])

   # Set reference particle for the line
   line.particle_ref = 'my_ref_part'

   env['energy_gev'] = 5.25            # updates reference energy automatically
   tw = line.twiss4d()                 # Twiss now uses the updated reference

   # Inspect the deferred expression on the particle
   env.ref['my_ref_part'].energy0._info()

   #  particles['my_ref_part'].energy0._get_value()
   particles['my_ref_part'].energy0 = [5.25e+09]
   # prints:
   # #  particles['my_ref_part'].energy0._expr
   #    particles['my_ref_part'].energy0 = (vars['energy_gev'] * 1000000000.0)
   #
   # #  particles['my_ref_part'].energy0._expr._get_dependencies()
   #    vars['energy_gev'] = 5.25
   #
   # #  particles['my_ref_part'].energy0 does not influence any target


Link lattice properties to reference particle parameters
--------------------------------------------------------

Lattice parameters can depend on reference particle quantities. For example, you
can tie element strengths to the reference particle rigidity to obtain a normalized
strength corresponding to a fixed magnetic field, independent of the reference momentum.

.. code-block:: python

   import xtrack as xt

   env = xt.Environment()
   env['p0c_optics_gev'] = 1.0  # momentum used for optics (GeV)

   env.new_particle('particle/b1', mass0=xt.PROTON_MASS_EV,
                    q0=1, p0c='p0c_optics_gev * 1e9')

   env['spectrometer_b_tesla'] = 3.0
   env['l.spectrometer'] = 2.0

   env.new('spectrometer.b1', 'Bend', angle=0, length='l.spectrometer',
           k0=env.ref['spectrometer_b_tesla'] / env.ref['particle/b1'].rigidity0[0])

   line = env.new_line(components=['spectrometer.b1'])
   line.particle_ref = 'particle/b1'

   env['spectrometer.b1'].k0        # -> ~0.899 for p0c_optics_gev = 1
   line.particle_ref.p0c = 450e9    # change reference momentum
   env['spectrometer.b1'].k0        # -> ~0.002; field stays 3 T

Remove reference particles
--------------------------

Particles stored in the environment can be removed with ``del``:

.. code-block:: python

   # Remove a stored particle
   del env.particles['my_ref_part']


Saving and loading environment or individual lines
==================================================

Environments (including all elements and lines) can be serialized to JSON and
loaded back, and individual lines can be saved and loaded separately.

.. code-block:: python

   import xtrack as xt

   env = xt.Environment()
   env['k1'] = 0.1
   env.new('qf', xt.Quadrupole, length=1.0, k1='k1')
   env.new('qd', xt.Quadrupole, length=1.0, k1='-k1')
   env.new_line(name='line_a', components=['qf', 'qd'])
   env.new_line(name='line_b', components=['qd', 'qf'])

   # Save whole environment (variables, elements, lines)
   env.to_json('env.json')

   # Reload environment
   env2 = xt.load('env.json')

   # Save a single line (variables and elements are included automatically)
   env['line_a'].to_json('line_a.json')

   # Reload the line
   line_loaded = xt.load('line_a.json')
   env3 = line_loaded.env # get the environment from the line

.. _env_loading_madx_lattices:

Loading MAD-X lattices
======================

Native MAD-X parser (recommended)
---------------------------------

Xsuite can read MAD-X lattice files directly without launching MAD-X. Provide
one or more files (any mix of ``.madx``, ``.seq``, or ``.str``) to
``xt.load``; the parser understands definitions such as variables, sequences,
and lines. Files containing MAD-X computations (``twiss``, ``survey``,
``match``, etc.) are not supported and will raise an error.

.. code-block:: python

   import xtrack as xt

   # The order of files matters if later files depend on earlier definitions
   env = xt.load([
       'ps_sftpro/ps.seq',
       'ps_sftpro/ps_hs_sftpro.str',
   ])

   # Access lines or variables defined in the MAD-X files
   line = env.lines['ring']
   kq = env['kqf1']

You can also pass MAD-X source code directly as a string by specifying the
format explicitly:

.. code-block:: python

   mad_src = '''
   ! Define variables and elements up-front (deferred expressions are supported)
   l_q := 1.0;
   l_cell := 12.0;
   kq  := 0.12;
   kq_f :=  kq;
   kq_d := -kq;

   qf: quadrupole, l:=l_q, k1:=kq_f;
   qd: quadrupole, l:=l_q, k1:=kq_d;

   fodo: sequence, l=l_cell;
     qf, at=0.5 * l_q;                        ! center at s=0.5 * l_q
     qd, at=l_cell/2 + 0.5 * l_q;             ! placed using deferred expressions
   endsequence;
   '''

   env = xt.load(string=mad_src, format='madx')
   line = env['fodo']

This path is the long-term supported way to import MAD-X lattices into Xsuite.

Import via cpymad (legacy)
--------------------------

You can also import a MAD-X sequence using ``cpymad`` by first running MAD-X and
then converting the in-memory sequence to an Xsuite line. This route depends on
MAD-X being available and will be discontinued alongside MAD-X end-of-support
plans.

.. code-block:: python

   from cpymad.madx import Madx
   import xtrack as xt

   mad = Madx()
   # example files from xtrack/test_data/ps_sftpro/
   mad.call('ps_sftpro/ps.seq')
   mad.call('ps_sftpro/ps_hs_sftpro.str')
   mad.use(sequence='ps')

   line = xt.Line.from_madx_sequence(mad.sequence.ps,
                                     deferred_expressions=True)

Choose this approach only when you explicitly need to run MAD-X calculations
before importing; otherwise prefer the native ``xt.load`` parser above.
