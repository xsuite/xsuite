======================
Match twiss parameters
======================

The Xtrack Tracker class provides a match method that allows to match the twiss parameters of a
to adjust knobs attached to the line in order to obtain desired values 
in the twiss results (see also :meth:`xtrack.Line.match` method documentation).
This feature is illustrated in the following example:

.. literalinclude:: generated_code_snippets/match_tune_chroma.py
   :language: python