
.. .. sectnum::
..   :depth: 4
..   :start: 2
..   :suffix: .

Usage
-----

Blabla bla bla bla...

Parser
++++++++++
The trollsift string parser module is useful for composing (formatting) and parsing strings 
compatible with the Python string format style. In satellite data file name filtering,
the library is useful for extracting typical information from granule filenames, such
as observation time, platform and instrument names. The trollsift Parser can also
verify that the string formatting is invertible, i.e. specific enough to ensure that
parsing and composing of strings are injective mappings ( aka one-to-one mapping )
which may be essential for some applications.

parsing and composing
^^^^^^^^^^^^^^^^^^^^^^^^^^^
The Parser class holds a format string, allowing us to parse and compose strings,

  >>> from trollsift import Parser
  >>> 
  >>> p = Parser("/somedir/{directory}/hrpt_{platform:4s}{platnum:2s}_{time:%Y%m%d_%H%M}_{orbit:05d}.l1b")
  >>> p.parse("/somedir/otherdir/hrpt_noaa16_20140210_1004_69022.l1b")
  {'directory': 'avhrr/2014', 'platform': 'noaa', 'platnum': '19',
  'time': dt.datetime(2014,02,12,14,12), 'orbit':12345}
  
  
Standalone parse and compose functions
+++++++++++++++++++++++++++++++++++++++++

  >>> from trollsift import ...

Blabla bla bla.

