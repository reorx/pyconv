Text File Code Conversion Tool
==============================

A weekend project made on windows & eclipse

pyconv tries to help you detect the right encoding of a text file,
decode it, and convert into the encoding you want.
Or you can just indicate encodings yourself.

pyconv use python's built-in functions to encode and decode,
and it's tolerant to characters that can't be encoded or decoded,
you may see `??` in the result, which probably means an invalid conversion,
and a need to try some other encodings.


Install
-------

Download the package and run::

   	python setup.py install

Then if you want to add the command to right-click menu, run::

    python -m pyconv.addmenu


Usage
-----

Just run it to see the helper informations.

TODO
----

* complete helper information for command

* right-click menu support for Mac