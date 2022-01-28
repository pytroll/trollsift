Usage
=====

Trollsift include collection of modules that assist with formatting, parsing and filtering satellite granule file names. These modules are useful and necessary for writing higher level applications and api’s for satellite batch processing. Currently we are implementing the string parsing and composing functionality. Watch this space for further modules to do with various types of filtering of satellite data granules.

Parser
------
The trollsift string parser module is useful for composing (formatting) and parsing strings
compatible with the Python :ref:`python:formatstrings`. In satellite data file name filtering,
the library is useful for extracting typical information from granule filenames, such
as observation time, platform and instrument names. The trollsift Parser can also
verify that the string formatting is invertible, i.e. specific enough to ensure that
parsing and composing of strings are bijective mappings ( aka one-to-one correspondence )
which may be essential for some applications, such as predicting granule 

parsing
^^^^^^^
The Parser object holds a format string, allowing us to parse and compose strings:

  >>> from trollsift import Parser
  >>> 
  >>> p = Parser("/somedir/{directory}/hrpt_{platform:4s}{platnum:2s}_{time:%Y%m%d_%H%M}_{orbit:05d}.l1b")
  >>> data = p.parse("/somedir/otherdir/hrpt_noaa16_20140210_1004_69022.l1b")
  >>> print(data) # doctest: +NORMALIZE_WHITESPACE
  {'directory': 'otherdir', 'platform': 'noaa', 'platnum': '16',
   'time': datetime.datetime(2014, 2, 10, 10, 4), 'orbit': 69022}

Parsing in trollsift is not "greedy". This means that in the case of ambiguous
patterns it will match the shortest portion of the string possible. For example:

  >>> from trollsift import Parser
  >>>
  >>> p = Parser("{field_one}_{field_two}")
  >>> data = p.parse("abc_def_ghi")
  >>> print(data)
  {'field_one': 'abc', 'field_two': 'def_ghi'}

So even though the first field could have matched to "abc_def", the non-greedy
parsing chose the shorter possible match of "abc".

composing
^^^^^^^^^
The reverse operation is called 'compose', and is equivalent to the Python
string class format method.  Here we take the filename pattern from earlier,
change the time stamp of the data, and write out a new file name,

  >>> from datetime import datetime
  >>>
  >>> p = Parser("/somedir/{directory}/hrpt_{platform:4s}{platnum:2s}_{time:%Y%m%d_%H%M}_{orbit:05d}.l1b")
  >>> data = {'directory': 'otherdir', 'platform': 'noaa', 'platnum': '16', 'time': datetime(2012, 1, 1, 1, 1), 'orbit': 69022}
  >>> p.compose(data)
  '/somedir/otherdir/hrpt_noaa16_20120101_0101_69022.l1b'

It is also possible to compose only partially, i.e., compose by specifying values
for only a subset of the parameters in the format string. Example:

  >>> p = Parser("/somedir/{directory}/hrpt_{platform:4s}{platnum:2s}_{time:%Y%m%d_%H%M}_{orbit:05d}.l1b")
  >>> data = {'directory':'my_dir'}
  >>> p.compose(data, allow_partial=True)
  '/somedir/my_dir/hrpt_{platform:4s}{platnum:2s}_{time:%Y%m%d_%H%M}_{orbit:05d}.l1b'

In addition to python's builtin string formatting functionality trollsift also
provides extra conversion options such as making all characters lowercase:

  >>> my_parser = Parser("{platform_name!l}")
  >>> my_parser.compose({'platform_name': 'NPP'})
  'npp'

For all of the options see :class:`~trollsift.parser.StringFormatter`.

standalone parse and compose
----------------------------

The parse and compose methods also exist as standalone functions,
depending on your requirements you can call,

  >>> from trollsift import parse, compose
  >>> fmt = "/somedir/{directory}/hrpt_{platform:4s}{platnum:2s}_{time:%Y%m%d_%H%M}_{orbit:05d}.l1b"
  >>> data = parse( fmt, "/somedir/otherdir/hrpt_noaa16_20140210_1004_69022.l1b" )
  >>> data['time'] = datetime(2012, 1, 1, 1, 1)
  >>> compose(fmt, data)
  '/somedir/otherdir/hrpt_noaa16_20120101_0101_69022.l1b'

And achieve the exact same result as in the Parse object example above.



