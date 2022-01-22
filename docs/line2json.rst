=============================
Save Xtrack line to json file
=============================

An Xtrack Line object can be transformed into a dictionary and saved in a json file, as
illustrated in the following example. Note that ``xobjects.JEncoder`` needs to
be provided to ``json.dump`` in order to serialize Numpy arrays, which are not
natively supported by json.

.. literalinclude:: generated_code_snippets/tojson.py
   :language: python