===================
Working with tables
===================

Several methods Xsuite return information in the form of Table objects. Examples
of such methods are :meth:`xtrack.Line.get_table`, :meth:`xtrack.Line.twiss`,
:meth:`xtrack.Line.survey`, :meth:`xtrack.Line.vars.get_table`,
:meth:`xtrack.Environment.vars.get_table`.

Table objects offer several capabilities to access data, for example by selecting
rows and columns in various ways. This is illustrated in the following example:

.. literalinclude:: generated_code_snippets/work_with_table.py
    :language: python