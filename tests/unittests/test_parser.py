import unittest
import datetime as dt

from trollsift.parser import _extract_parsedef, _extract_values
from trollsift.parser import _convert, _collect_keyvals_from_parsedef
from trollsift.parser import parse, globify, validate, is_one2one


class TestParser(unittest.TestCase):

    def setUp(self):
        self.fmt = "/somedir/{directory}/hrpt_{platform:4s}{platnum:2s}" +\
            "_{time:%Y%m%d_%H%M}_{orbit:05d}.l1b"
        self.string = "/somedir/otherdir/hrpt_noaa16_20140210_1004_69022.l1b"
        self.string2 = "/somedir/otherdir/hrpt_noaa16_20140210_1004_00022.l1b"
        self.string3 = "/somedir/otherdir/hrpt_noaa16_20140210_1004_69022"
        self.string4 = "/somedir/otherdir/hrpt_noaa16_20140210_1004_69022"

    def test_extract_parsedef(self):
        # Run
        result, dummy = _extract_parsedef(self.fmt)
        # Assert
        self.assertItemsEqual(result,
                              ['/somedir/', {'directory': None},
                               '/hrpt_', {'platform': '4s'},
                               {'platnum': '2s'},
                               '_', {'time': '%Y%m%d_%H%M'},
                               '_', {'orbit': '05d'}, '.l1b'])

    def test_extract_values(self):
        # Run
        parsedef = ['/somedir/', {'directory': None}, '/hrpt_',
                    {'platform': '4s'}, {'platnum': '2s'},
                    '_', {'time': '%Y%m%d_%H%M'}, '_',
                    {'orbit': 'd'}, '.l1b']
        result = _extract_values(parsedef, self.string)
        # Assert
        self.assertDictEqual(result, {'directory': 'otherdir',
                                      'platform': 'noaa', 'platnum': '16',
                                      'time': '20140210_1004', 'orbit': '69022'})

    def test_extract_values_end(self):
        # Run
        parsedef = ['/somedir/', {'directory': None}, '/hrpt_',
                    {'platform': '4s'}, {'platnum': '2s'},
                    '_', {'time': '%Y%m%d_%H%M'}, '_',
                    {'orbit': 'd'}]
        result = _extract_values(parsedef, self.string3)
        # Assert
        self.assertDictEqual(result, {'directory': 'otherdir',
                                      'platform': 'noaa', 'platnum': '16',
                                      'time': '20140210_1004', 'orbit': '69022'})

    def test_extract_values_beginning(self):
        # Run
        parsedef = [{'directory': None}, '/hrpt_',
                    {'platform': '4s'}, {'platnum': '2s'},
                    '_', {'time': '%Y%m%d_%H%M'}, '_',
                    {'orbit': 'd'}]
        result = _extract_values(parsedef, self.string4)
        # Assert
        self.assertDictEqual(result, {'directory': '/somedir/otherdir',
                                      'platform': 'noaa', 'platnum': '16',
                                      'time': '20140210_1004', 'orbit': '69022'})

    def test_extract_values_beginning(self):
        # Run
        parsedef = [{'directory': None}, '/hrpt_',
                    {'platform': '4s'}, {'platnum': '2s'},
                    '_', {'time': '%Y%m%d_%H%M'}, '_',
                    {'orbit': 'd'}]
        result = _extract_values(parsedef, self.string4)
        # Assert
        self.assertDictEqual(result, {'directory': '/somedir/otherdir',
                                      'platform': 'noaa', 'platnum': '16',
                                      'time': '20140210_1004', 'orbit': '69022'})

    def test_extract_values_s4spair(self):
        # Run
        parsedef = [{'directory': None}, '/hrpt_',
                    {'platform': '4s'}, {'platnum': 's'},
                    '_', {'time': '%Y%m%d_%H%M'}, '_',
                    {'orbit': 'd'}]
        result = _extract_values(parsedef, self.string4)
        # Assert
        self.assertDictEqual(result, {'directory': '/somedir/otherdir',
                                      'platform': 'noaa', 'platnum': '16',
                                      'time': '20140210_1004', 'orbit': '69022'})

    def test_extract_values_ss2pair(self):
        # Run
        parsedef = [{'directory': None}, '/hrpt_',
                    {'platform': 's'}, {'platnum': 's2'},
                    '_', {'time': '%Y%m%d_%H%M'}, '_',
                    {'orbit': 'd'}]
        result = _extract_values(parsedef, self.string4)
        # Assert
        self.assertDictEqual(result, {'directory': '/somedir/otherdir',
                                      'platform': 'noaa', 'platnum': '16',
                                      'time': '20140210_1004', 'orbit': '69022'})

    def test_extract_values_ss2pair_end(self):
        # Run
        parsedef = [{'directory': None}, '/hrpt_',
                    {'platform': 's'}, {'platnum': 's2'}]
        result = _extract_values(parsedef, "/somedir/otherdir/hrpt_noaa16")
        # Assert
        self.assertDictEqual(result, {'directory': '/somedir/otherdir',
                                      'platform': 'noaa', 'platnum': '16'})

    def test_extract_values_sdatetimepair_end(self):
        # Run
        parsedef = [{'directory': None}, '/hrpt_',
                    {'platform': 's'}, {'date': '%Y%m%d'}]
        result = _extract_values(
            parsedef, "/somedir/otherdir/hrpt_noaa20140212")
        # Assert
        self.assertDictEqual(result, {'directory': '/somedir/otherdir',
                                      'platform': 'noaa', 'date': '20140212'})

    def test_extract_values_everything(self):
        # Run
        parsedef = [{'everything': None}]
        result = _extract_values(parsedef, self.string)
        # Assert
        self.assertDictEqual(
            result, {'everything': '/somedir/otherdir/hrpt_noaa16_20140210_1004_69022.l1b'})

    def test_extract_values_padding2(self):
        # Run
        parsedef = ['/somedir/', {'directory': None}, '/hrpt_',
                    {'platform': '4s'}, {'platnum': '2s'},
                    '_', {'time': '%Y%m%d_%H%M'}, '_',
                    {'orbit': '0>5d'}, '.l1b']
        result = _extract_values(parsedef, self.string2)
        # Assert
        self.assertDictEqual(result, {'directory': 'otherdir',
                                      'platform': 'noaa', 'platnum': '16',
                                      'time': '20140210_1004', 'orbit': '00022'})

    def test_extract_values_fails(self):
        # Run
        parsedef = ['/somedir/', {'directory': None}, '/hrpt_',
                    {'platform': '4s'}, {'platnum': '2s'},
                    '_', {'time': '%Y%m%d_%H%M'}, '_', {'orbit': '4d'}, '.l1b']
        self.assertRaises(ValueError, _extract_values, parsedef, self.string)

    def test_convert_digits(self):
        self.assertEqual(_convert('d', '69022'), 69022)
        self.assertRaises(ValueError, _convert, 'd', '69dsf')
        self.assertEqual(_convert('d', '00022'), 22)
        self.assertEqual(_convert('4d', '69022'), 69022)
        self.assertEqual(_convert('_>10d', '_____69022'), 69022)
        self.assertEqual(_convert('%Y%m%d_%H%M', '20140210_1004'),
                         dt.datetime(2014, 2, 10, 10, 4))

    def test_parse(self):
        # Run
        result = parse(
            self.fmt, "/somedir/avhrr/2014/hrpt_noaa19_20140212_1412_12345.l1b")
        # Assert
        self.assertDictEqual(result, {'directory': 'avhrr/2014',
                                      'platform': 'noaa', 'platnum': '19',
                                      'time': dt.datetime(2014, 2, 12, 14, 12),
                                      'orbit': 12345})

    def test_globify_simple(self):
        # Run
        result = globify('{a}_{b}.end', {'a': 'a', 'b': 'b'})
        # Assert
        self.assertEqual(result, 'a_b.end')

    def test_globify_empty(self):
        # Run
        result = globify('{a}_{b:4d}.end', {})
        # Assert
        self.assertEqual(result, '*_????.end')

    def test_globify_noarg(self):
        # Run
        result = globify('{a}_{b:4d}.end')
        # Assert
        self.assertEqual(result, '*_????.end')

    def test_globify_known_lengths(self):
        # Run
        result = globify('{directory}/{platform:4s}{satnum:2d}/{orbit:05d}',
                         {'directory': 'otherdir',
                          'platform': 'noaa'})
        # Assert
        self.assertEqual(result, 'otherdir/noaa??/?????')

    def test_globify_unknown_lengths(self):
        # Run
        result = globify('hrpt_{platform_and_num}_' +
                         '{date}_{time}_{orbit}.l1b',
                         {'platform_and_num': 'noaa16'})
        # Assert
        self.assertEqual(result, 'hrpt_noaa16_*_*_*.l1b')

    def test_globify_datetime(self):
        # Run
        result = globify('hrpt_{platform}{satnum}_' +
                         '{time:%Y%m%d_%H%M}_{orbit}.l1b',
                         {'platform': 'noaa',
                          'time': dt.datetime(2014, 2, 10, 12, 12)})
        # Assert
        self.assertEqual(result, 'hrpt_noaa*_20140210_1212_*.l1b')

    def test_globify_partial_datetime(self):
        # Run
        result = globify('hrpt_{platform:4s}{satnum:2d}_' +
                         '{time:%Y%m%d_%H%M}_{orbit}.l1b',
                         {'platform': 'noaa',
                          'time': (dt.datetime(2014, 2, 10, 12, 12),
                                   'Ymd')})
        # Assert
        self.assertEqual(result, 'hrpt_noaa??_20140210_????_*.l1b')

    def test_globify_datetime_nosub(self):
        # Run
        result = globify('hrpt_{platform:4s}{satnum:2d}_' +
                         '{time:%Y%m%d_%H%M}_{orbit}.l1b',
                         {'platform': 'noaa'})

        # Assert
        self.assertEqual(result, 'hrpt_noaa??_????????_????_*.l1b')

    def test_collect_keyvals_from_parsedef(self):
        # Run
        keys, vals = _collect_keyvals_from_parsedef(['/somedir/',
                                                     {'directory': None},
                                                     '/hrpt_',
                                                     {'platform': '4s'},
                                                     {'platnum': '2s'}, '_',
                                                     {'time': '%Y%m%d_%H%M'},
                                                     '_', {'orbit': '05d'},
                                                     '.l1b'])
        # Assert
        self.assertEqual(keys, ['directory', 'platform',
                                'platnum', 'time', 'orbit'])
        self.assertEqual(vals, [None, '4s', '2s', '%Y%m%d_%H%M', '05d'])

    def test_validate(self):
        # These cases are True
        self.assertTrue(
            validate(self.fmt, "/somedir/avhrr/2014/hrpt_noaa19_20140212_1412_12345.l1b"))
        self.assertTrue(
            validate(self.fmt, "/somedir/avhrr/2014/hrpt_noaa01_19790530_0705_00000.l1b"))
        self.assertTrue(validate(
            self.fmt, "/somedir/funny-char$dir/hrpt_noaa19_20140212_1412_12345.l1b"))
        self.assertTrue(
            validate(self.fmt, "/somedir//hrpt_noaa19_20140212_1412_12345.l1b"))
        # These cases are False
        self.assertFalse(
            validate(self.fmt, "/somedir/bla/bla/hrpt_noaa19_20140212_1412_1A345.l1b"))
        self.assertFalse(
            validate(self.fmt, "/somedir/bla/bla/hrpt_noaa19_2014021_1412_00000.l1b"))
        self.assertFalse(
            validate(self.fmt, "/somedir/bla/bla/hrpt_noaa19_20140212__412_00000.l1b"))
        self.assertFalse(
            validate(self.fmt, "/somedir/bla/bla/hrpt_noaa19_20140212__1412_00000.l1b"))
        self.assertFalse(
            validate(self.fmt, "/somedir/bla/bla/hrpt_noaa19_20140212_1412_00000.l1"))
        self.assertFalse(
            validate(self.fmt, "/somedir/bla/bla/hrpt_noaa19_20140212_1412_00000"))
        self.assertFalse(
            validate(self.fmt, "{}/somedir/bla/bla/hrpt_noaa19_20140212_1412_00000.l1b"))

    def test_is_one2one(self):
        # These cases are True
        self.assertTrue(is_one2one(
            "/somedir/{directory}/somedata_{platform:4s}_{time:%Y%d%m-%H%M}_{orbit:5d}.l1b"))
        # These cases are False
        self.assertFalse(is_one2one(
            "/somedir/{directory}/somedata_{platform:4s}_{time:%Y%d%m-%H%M}_{orbit:d}.l1b"))

    def assertDictEqual(self, a, b):
        for key in a:
            self.assertTrue(key in b)
            self.assertEqual(a[key], b[key])

        self.assertEqual(len(a), len(b))

    def assertItemsEqual(self, a, b):
        for i in range(len(a)):
            if isinstance(a[i], dict):
                self.assertDictEqual(a[i], b[i])
            else:
                self.assertEqual(a[i], b[i])
        self.assertEqual(len(a), len(b))


def suite():
    """The suite for test_parser
    """
    loader = unittest.TestLoader()
    mysuite = unittest.TestSuite()
    mysuite.addTest(loader.loadTestsFromTestCase(TestParser))
