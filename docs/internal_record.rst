===============================
Data recording in beam elements
===============================

Xsuite beam elements can store data in dedicated data structures stored in a
specific io_buffer handled by the tracker. This feature is illustrated in the
following three examples.

Recording of an individual table
================================

.. literalinclude:: generated_code_snippets/internal_record.py
   :language: python

Recording of multipole tables
=============================

.. literalinclude:: generated_code_snippets/internal_multirecord.py
   :language: python

Internal record for elements used in standalone mode
====================================================

.. literalinclude:: generated_code_snippets/internal_record_standalone.py
   :language: python