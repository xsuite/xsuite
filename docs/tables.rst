.. _tables-user-guide:

===================
Working with tables
===================

Several Xsuite methods return information in the form of Table objects. Examples
of such methods are :meth:`xtrack.Line.get_table`, :meth:`xtrack.Line.twiss`,
:meth:`xtrack.Line.survey`, :meth:`xtrack.Line.vars.get_table`,
:meth:`xtrack.Environment.vars.get_table`.

See :ref:`Table class <table-api-reference>` in the Reference guide for the base
table API.

Table objects offer several capabilities to access data, for example by selecting
rows and columns in various ways. This is illustrated in the following example:

.. literalinclude:: generated_code_snippets/work_with_table.py
    :language: python

.. _tfs-output-user-guide:

Writing tables in TFS format
============================

Tables can be exported to TFS with :meth:`xtrack.Table.to_tfs`, including the
Twiss tables returned by ``line.twiss()``. The optional ``format_spec`` argument
controls which columns and scalar headers are written, their order and names,
and the numerical formatting. It accepts a Python dictionary, a JSON or TOML
file path, or a built-in preset. Calls without ``format_spec`` retain the default
TFS export behavior.

For the same selected values, types and row order, a specification defines the
same output text across Xtrack releases. Additional table fields do not appear
unless explicitly selected.

Selecting and formatting fields
-------------------------------

A dictionary gives full control over the output. ``columns`` and ``scalars``
are required ordered lists; only the listed fields are written. Scalars become
TFS ``@`` headers. An empty list selects no fields in that category.

.. literalinclude:: generated_code_snippets/tfs_format_spec.py
   :language: python
   :start-after: # start-tfs-dictionary
   :end-before: # end-tfs-dictionary

Each field requires ``name``, which specifies the output name. ``source_name``
is optional and defaults to ``name``. For example, the entry for ``Q1`` reads
``tw.qx`` and writes a header named ``Q1``. A scalar entry can instead provide
a constant ``value``, as with ``TYPE`` above; ``value`` and ``source_name`` cannot
be combined.

The following options control formatting:

* ``float_format`` sets the default for floating-point columns and scalars.
  A field's ``format`` overrides it. Python notation such as ``.9f`` (nine
  decimal places), ``.16e`` (scientific notation with sixteen decimal places)
  and ``.12g`` (twelve significant digits) is supported. The default is ``.16e``.
* ``case`` defaults to ``"preserve"``; ``"upper"`` and ``"lower"`` convert output
  field names and string values, including element names. Source lookup remains
  case-sensitive and happens before conversion. Numeric notation is unaffected.
* ``type`` optionally fixes a field's TFS type: ``string``, ``float``, ``int``,
  ``bool`` or ``complex``. Explicit types are useful for long-lived specifications
  and empty object arrays. Otherwise the type is inferred from the data.
* A column's ``width`` sets its minimum character width. The top-level
  ``default_column_width`` and ``numeric_column_width`` set minimum widths for
  all columns and numeric columns respectively (defaults: 0 and 16). Widths
  expand to fit the output; values are never truncated.

Rows retain their order in the input table. To select or reorder rows, use the
table's row selection methods before exporting. No additional class, version,
timestamp or other metadata is added automatically. Missing fields, duplicate
output names, unknown keys and invalid formats raise errors before the output
file is opened. A specification cannot be combined with the legacy selection
or formatting arguments such as ``include``, ``exclude`` or ``float_precision``.

Saving a specification in a file
--------------------------------

A specification can be saved as JSON and passed directly to ``to_tfs``:

.. literalinclude:: generated_code_snippets/tfs_format_spec.py
   :language: python
   :start-after: # start-tfs-json
   :end-before: # end-tfs-json

TOML is convenient for hand-maintained files because it supports comments. The
same specification can be saved as ``tfs_format_spec.toml``:

.. literalinclude:: generated_code_snippets/tfs_format_spec.toml
   :language: toml
   :end-before: # Complete source:

The file can then be used as follows:

.. literalinclude:: generated_code_snippets/tfs_format_spec.py
   :language: python
   :start-after: # start-tfs-toml
   :end-before: # end-tfs-toml

Built-in format specifications
------------------------------

``xt.format_spec`` provides ready-to-use specifications: ``optics_orbit_v1``
for optics and closed orbit, ``optics_orbit_strengths_v1`` to also include
integrated strengths, and ``madx_twiss_v1`` for a MAD-X-style layout.
For a periodic Twiss table computed with ``strengths=True``:

.. literalinclude:: generated_code_snippets/tfs_format_spec.py
   :language: python
   :start-after: # Stable built-in layouts. The strengths preset requires strengths=True.
   :end-before: # end-tfs-presets

The MAD-X preset controls the layout without converting physics conventions;
see the :download:`MAD-X convention example <generated_code_snippets/madx_tfs_format.py>`
for preparing the values.
