Data recording in beam elements
===============================

.. contents:: Table of Contents
    :depth: 3

Introduction
------------

Xsuite beam elements can store data in dedicated data structures allocated in a
specific io_buffer handled by the tracker. This feature is illustrated in the
following three examples, which cover the storage of data into one or multiple
data tables for a given element type and the usage of data recording for elements
used within a tracker and in standalone mode.

Recording of an individual table
--------------------------------

.. literalinclude:: generated_code_snippets/internal_record.py
   :language: python

Recording of multiple tables
----------------------------

.. literalinclude:: generated_code_snippets/internal_multirecord.py
   :language: python

Internal record for elements used in standalone mode
----------------------------------------------------

.. literalinclude:: generated_code_snippets/internal_record_standalone.py
   :language: python