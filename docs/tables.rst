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

Using a built-in preset
-----------------------

The presets in ``xt.format_spec`` define reusable output layouts:

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Preset
     - Contents
   * - ``optics_orbit_v1``
     - Transverse optics and closed orbit, with line length and transverse tunes
       in the header.
   * - ``optics_orbit_strengths_v1``
     - Optics and orbit, plus element types, lengths, bending angles and normal
       and skew integrated strengths through order 5. Requires
       ``strengths=True`` when computing Twiss.
   * - ``madx_twiss_v1``
     - Common optics, orbit and strength columns in a MAD-X-style layout, with
       uppercase names and strings and ``.15e`` numerical formatting. Requires
       ``strengths=True`` and chromaticities. The compact header contains
       ``TYPE``, ``LENGTH``, ``ALFA``, ``Q1``, ``Q2``, ``DQ1`` and ``DQ2``.

For example, the following builds a small ring and exports its periodic Twiss
table using each preset:

.. literalinclude:: generated_code_snippets/tfs_format_spec.py
   :language: python
   :start-after: # start-tfs-presets
   :end-before: # end-tfs-presets

These presets require periodic Twiss scalars. For an open Twiss calculation,
customize the scalar list to select the available fields.

.. note::

   The MAD-X preset specifies a file layout; it preserves the supplied values
   and row order. Xtrack normally reports optics at element entries and uses
   momentum-normalized dispersion and chromaticity. Matching MAD-X's exit-point
   and derivative conventions requires an explicit preparation step. The
   :download:`MAD-X convention example <generated_code_snippets/madx_tfs_format.py>`
   shows this for a complete, forward, on-momentum, periodic 4D Twiss table.
   Strength definitions can also differ: Xtrack includes the design dipole
   strength in ``k0l``, while MAD-X can encode it in ``ANGLE`` and report zero
   ``K0L`` for an implicit design bend.

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

Stable output and customization
-------------------------------

The required ``version`` field is a string. Custom specifications can use
``"1"`` for the current rendering rules. Built-in files carry their full preset
identifiers, such as ``"optics_orbit_strengths_v1"``. Unsupported identifiers
are rejected. Existing preset definitions are kept stable; changing their
contents requires a new preset identifier.

For the same selected values, types and row order, a specification defines the
same output text across Xtrack releases. Additional table fields do not appear
unless explicitly selected. This fixes the output layout and numerical
representation; it does not freeze the results of Twiss calculations.

Built-in presets are immutable. Use ``xt.format_spec.load`` to obtain a mutable
copy for customization or saving as JSON:

.. literalinclude:: generated_code_snippets/tfs_format_spec.py
   :language: python
   :start-after: # start-tfs-customize
   :end-before: # end-tfs-customize

``xt.format_spec.load`` also accepts a user dictionary or a JSON/TOML path and
returns a validated copy with defaults filled in.
