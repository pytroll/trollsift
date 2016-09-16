Changelog
=========

%%version%% (unreleased)
------------------------

- Update changelog. [Martin Raspaud]

- Bump version: 0.1.1 → 0.2.0. [Martin Raspaud]

- Change version to a single string. [Martin Raspaud]

- Add six to the list of rpm dependencies. [Martin Raspaud]

- Add 'six' as a requirement. [Martin Raspaud]

- Add support for unicode. [Martin Raspaud]

- Don't modify keyvals in globify() [Martin Raspaud]

- Add stripping of padding character for strings also. [Martin Raspaud]

- Link to documentation. [Panu Lahtinen]

- Bumbed the version number a bit. [Panu Lahtinen]

- Add bdist_rpm section to setup.cfg for easy rpm package generation.
  [Martin Raspaud]

- Bugfix on timeparsing. This fixes #2. [Martin Raspaud]

- Global dict to uppercase, list of or clauses to list comprehension.
  [Panu Lahtinen]

- Allow more flexible time formating + cleanup. [Martin Raspaud]

  * allow for timestrings that are incomplete (eg %f is just 1 char)
  * correct globify accordingly
  * correct incorrect behaviour with variable length time formats
  (eg %A would give a fixed length depending on the current day)

- Is_one2one improvements. [Hrobjartur Thorsteinsson]

  is_one2one improvements
  look for unwanted patterns, e.g. {:s}{:4s}{:s}


- Merge branch 'master' of https://github.com/pnuu/trollsift.
  [Hrobjartur Thorsteinsson]

- Making landscape a bit happier :-) [Panu Lahtinen]

- Fixing some globify bugs (e.g. no sub) + unittests. [Hrobjartur
  Thorsteinsson]

  fixing some globify bugs (e.g. no sub) + unittests


- Parse extract_values {s}{s4} and {s}{datetime} support + unittests.
  [Hrobjartur Thorsteinsson]

  parse extract_values {s}{s4} and {s}{datetime} support + unittests


- Fixed PyPi download_url. [Panu Lahtinen]

- PyPi integration. [Panu Lahtinen]

- PyPi integration. [Panu Lahtinen]

- Version to 0.1.0. [Panu Lahtinen]

- More syntactic cleanup. [Panu Lahtinen]

- More syntactic cleanup. [Panu Lahtinen]

- Syntax cleanup. [Panu Lahtinen]

- Bugfix with __str__ [Hrobjartur Thorsteinsson]

  bugfirx with __str__


- (s)(s4) testcase removed. [Hrobjartur Thorsteinsson]

  (s)(s4) testcase removed - will attempt to support this kind of parsing
  case later. Dont want broken test in master.


- Further workaround for python2.6 + new unittest(fails) [Hrobjartur
  Thorsteinsson]

  further workaround for python2.6 + new unittest(fails)


- Unittests and bugfixes for free size key extraction + Py2.6 bugfix.
  [Hrobjartur Thorsteinsson]

  unittests and bugfixes for free size key extraction + Py2.6 bugfix
  for format string bug in globify.


- Merge branch 'master' of https://github.com/pnuu/trollsift.
  [Hrobjartur Thorsteinsson]

- Merge branch 'master' of https://github.com/pnuu/trollsift. [Panu
  Lahtinen]

  Conflicts:
  	tests/unittests/test_parser.py
  	trollsift/parser.py


- Parser.globify() and a helper function _collect_keyvals_from_parsedef.
  [Panu Lahtinen]

- Tests for parser.globify and parser._collect_keyvals_from_parsedef.
  [Panu Lahtinen]

- Unittest parser (free size key at end) [Hrobjartur Thorsteinsson]

  uniittest parser, free size key bug at end.
  Also need beginning and other special cases to follow.


- Is_one2one implemented + unittests. [Hrobjartur Thorsteinsson]

  is_one2one function implemented with some elementary unittests.
  Im a little unclear if this is a useful or
  meaningful tool.  Have to create more unittests.


- Validate function and class method implemented w. tests. [Hrobjartur
  Thorsteinsson]

  validate function and class method implemented w. tests.


- Doc type. [Hrobjartur Thorsteinsson]

  doc typo


- Further documentation. [Hrobjartur Thorsteinsson]

  further documentation


- Merge branch 'master' of https://github.com/pnuu/trollsift.
  [Hrobjartur Thorsteinsson]

- Removed testing for 3.0 and 3.1, as these are not supported by Travis.
  [Panu Lahtinen]

- Support for Python 3.x. [Panu Lahtinen]

- Added class Parser and compose() function. [Panu Lahtinen]

- Fixed typos in tests. [Panu Lahtinen]

- Þ to Th. [Panu Lahtinen]

- Parser usage docs started. [Hrobjartur Thorsteinsson]

  parser usage docs started


- Integration test for Parser. [Hrobjartur Thorsteinsson]

  integration test for Parser


- Bug fixes on parse and unittest. [Hrobjartur Thorsteinsson]

  bug fixes on parse and unittest


- Merge branch 'master' of https://github.com/pnuu/trollsift.
  [Hrobjartur Thorsteinsson]

- Merge branch 'master' of https://github.com/pnuu/trollsift. [Panu
  Lahtinen]

- Parse() function. [Panu Lahtinen]

- Unittest for parse. [Hrobjartur Thorsteinsson]

  unittest for parse


- Merge branch 'master' of https://github.com/pnuu/trollsift.
  [Hrobjartur Thorsteinsson]

- Removed a debug print. [Panu Lahtinen]

- Workaround for formatting in Python 2.6. [Panu Lahtinen]

- Own version of assertItemsEqual() to support python 2.6. [Panu
  Lahtinen]

- Removed coverage, added nosetests. [Panu Lahtinen]

- Testing for setup.py. [Panu Lahtinen]

- Initial setup.py. [Panu Lahtinen]

- Initial version. [Panu Lahtinen]

- Travis integration. [Panu Lahtinen]

- Added docs. [Hrobjartur Thorsteinsson]

  added docs


- Remainig unittest fails, bug fixes for _extract_values. [Hrobjartur
  Thorsteinsson]

  remainig unittest fails, bug fixes for _extract_values


- Merge branch 'master' of https://github.com/pnuu/trollsift.
  [Hrobjartur Thorsteinsson]

  Conflicts:
  	trollsift/parser.py


- Implementation of _convert. [Panu Lahtinen]

- Fixed typo in syntax error in assertRaises() in extract_values_fails.
  [Panu Lahtinen]

- Implemented _extract_parsedef(). [Panu Lahtinen]

- Fixed incorrect test result. [Panu Lahtinen]

- Implemented _extract_values helper. [Hrobjartur Thorsteinsson]

  implemented _extract_values helper


- Unittest created for parser. [Hrobjartur Thorsteinsson]

  Unittests created for parser.


- Initial commit with empy files. [Panu Lahtinen]

- Initial commit. [Panu Lahtinen]


