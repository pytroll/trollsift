
.. .. sectnum::
..   :depth: 4
..   :start: 2
..   :suffix: .

.. _string-format: https://docs.python.org/2/library/string.html#format-string-syntax

Usage
-----

Trollsift include collection of modules that assist with formatting, parsing and filtering satellite granule file names. These modules are useful and necessary for writing higher level applications and api’s for satellite batch processing. Currently we are implementing the string parsing and composing functionality. Watch this space for further modules to do with various types of filtering of satellite data granules.

Parser
++++++++++
The trollsift string parser module is useful for composing (formatting) and parsing strings 
compatible with the Python string-format_ style. In satellite data file name filtering,
the library is useful for extracting typical information from granule filenames, such
as observation time, platform and instrument names. The trollsift Parser can also
verify that the string formatting is invertible, i.e. specific enough to ensure that
parsing and composing of strings are bijective mappings ( aka one-to-one correspondence )
which may be essential for some applications, such as predicting granule 

parsing
^^^^^^^^^^^^^^^^^^^^^^^^^^^
The Parser object holds a format string, allowing us to parse and compose strings,

  >>> from trollsift import Parser
  >>> 
  >>> p = Parser("/somedir/{directory}/hrpt_{platform:4s}{platnum:2s}_{time:%Y%m%d_%H%M}_{orbit:05d}.l1b")
  >>> data = p.parse("/somedir/otherdir/hrpt_noaa16_20140210_1004_69022.l1b")
  >>> print data
  {'directory': 'otherdir', 'platform': 'noaa', 'platnum': '16',
  'time': datetime.datetime(2014,02,12,14,12), 'orbit':69022}
  
composing
^^^^^^^^^^^^^^^^^^^^^^^^^^^
The reverse operation is called 'compose', and is equivalent to the Python string
class format method.  Here we change the time stamp of the data, and write out 
a new file name,

  >>> from datetime import datetime
  >>> data['time'] = datetime(2012, 1, 1, 1, 1)
  >>> p.compose(data)
  '/somedir/otherdir/hrpt_noaa16_20120101_0101_69022.l1b'


standalone parse and compose
+++++++++++++++++++++++++++++++++++++++++

The parse and compose methods also exist as standalone functions,
depending on your requirements you can call,

  >>> from trollsift import parse, compose
  >>> fmt = "/somedir/{directory}/hrpt_{platform:4s}{platnum:2s}_{time:%Y%m%d_%H%M}_{orbit:05d}.l1b"
  >>> data = parse( fmt, "/somedir/otherdir/hrpt_noaa16_20140210_1004_69022.l1b" )
  >>> data['time'] = datetime(2012, 1, 1, 1, 1)
  >>> compose(fmt, data)
  '/somedir/otherdir/hrpt_noaa16_20120101_0101_69022.l1b'

And achieve the exact same result as in the Parse object example above.



