import unittest
import datetime as dt

from trollsift.parser import get_convert_dict, regex_formatter
from trollsift.parser import _convert
from trollsift.parser import parse, globify, validate, is_one2one
from trollsift.parser import _extract_parsedef


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
        self.assertEqual(result,
                            ['/somedir/', {'directory': None},
                             '/hrpt_', {'platform': '4s'},
                             {'platnum': '2s'},
                             '_', {'time': '%Y%m%d_%H%M'},
                             '_', {'orbit': '05d'}, '.l1b'])

    def test_get_convert_dict(self):
        # Run
        result = get_convert_dict(self.fmt)
        # Assert
        self.assertDictEqual(result, {
            'directory': '',
            'platform': '4s',
            'platnum': '2s',
            'time': '%Y%m%d_%H%M',
            'orbit': '05d',
        })

    def test_extract_values(self):
        fmt = "/somedir/{directory}/hrpt_{platform:4s}{platnum:2s}_{time:%Y%m%d_%H%M}_{orbit:d}.l1b"
        result = regex_formatter.extract_values(fmt, self.string)
        self.assertDictEqual(result, {'directory': 'otherdir',
                                      'platform': 'noaa', 'platnum': '16',
                                      'time': '20140210_1004', 'orbit': '69022'})

    def test_extract_values_end(self):
        fmt = "/somedir/{directory}/hrpt_{platform:4s}{platnum:2s}_{time:%Y%m%d_%H%M}_{orbit:d}"
        result = regex_formatter.extract_values(fmt, self.string3)
        self.assertDictEqual(result, {'directory': 'otherdir',
                                      'platform': 'noaa', 'platnum': '16',
                                      'time': '20140210_1004', 'orbit': '69022'})

    def test_extract_values_beginning(self):
        fmt = "{directory}/hrpt_{platform:4s}{platnum:2s}_{time:%Y%m%d_%H%M}_{orbit:d}"
        result = regex_formatter.extract_values(fmt, self.string4)
        self.assertDictEqual(result, {'directory': '/somedir/otherdir',
                                      'platform': 'noaa', 'platnum': '16',
                                      'time': '20140210_1004', 'orbit': '69022'})

    def test_extract_values_s4spair(self):
        fmt = "{directory}/hrpt_{platform:4s}{platnum:s}_{time:%Y%m%d_%H%M}_{orbit:d}"
        result = regex_formatter.extract_values(fmt, self.string4)
        self.assertDictEqual(result, {'directory': '/somedir/otherdir',
                                      'platform': 'noaa', 'platnum': '16',
                                      'time': '20140210_1004', 'orbit': '69022'})

    def test_extract_values_ss2pair(self):
        fmt = "{directory}/hrpt_{platform:s}{platnum:2s}_{time:%Y%m%d_%H%M}_{orbit:d}"
        result = regex_formatter.extract_values(fmt, self.string4)
        self.assertDictEqual(result, {'directory': '/somedir/otherdir',
                                      'platform': 'noaa', 'platnum': '16',
                                      'time': '20140210_1004', 'orbit': '69022'})

    def test_extract_values_ss2pair_end(self):
        fmt = "{directory}/hrpt_{platform:s}{platnum:2s}"
        result = regex_formatter.extract_values(fmt, "/somedir/otherdir/hrpt_noaa16")
        self.assertDictEqual(result, {'directory': '/somedir/otherdir',
                                      'platform': 'noaa', 'platnum': '16'})

    def test_extract_values_sdatetimepair_end(self):
        fmt = "{directory}/hrpt_{platform:s}{date:%Y%m%d}"
        result = regex_formatter.extract_values(fmt, "/somedir/otherdir/hrpt_noaa20140212")
        self.assertDictEqual(result, {'directory': '/somedir/otherdir',
                                      'platform': 'noaa', 'date': '20140212'})

    def test_extract_values_everything(self):
        fmt = "{everything}"
        result = regex_formatter.extract_values(fmt, self.string)
        self.assertDictEqual(
            result, {'everything': '/somedir/otherdir/hrpt_noaa16_20140210_1004_69022.l1b'})

    def test_extract_values_padding2(self):
        fmt = "/somedir/{directory}/hrpt_{platform:4s}{platnum:2s}_{time:%Y%m%d_%H%M}_{orbit:0>5d}.l1b"
        # parsedef = ['/somedir/', {'directory': None}, '/hrpt_',
        #             {'platform': '4s'}, {'platnum': '2s'},
        #             '_', {'time': '%Y%m%d_%H%M'}, '_',
        #             {'orbit': '0>5d'}, '.l1b']
        result = regex_formatter.extract_values(fmt, self.string2)
        # Assert
        self.assertDictEqual(result, {'directory': 'otherdir',
                                      'platform': 'noaa', 'platnum': '16',
                                      'time': '20140210_1004', 'orbit': '00022'})

    def test_extract_values_fails(self):
        fmt = '/somedir/{directory}/hrpt_{platform:4s}{platnum:2s}_{time:%Y%m%d_%H%M}_{orbit:4d}.l1b'
        self.assertRaises(ValueError, regex_formatter.extract_values, fmt, self.string)

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

    def test_parse_wildcards(self):
        # Run
        result = parse(
            "hrpt_{platform}{platnum:2s}_{time:%Y%m%d_%H%M}_{orbit:05d}{ext}",
            "hrpt_noaa19_20140212_1412_12345.l1b")
        # Assert
        self.assertDictEqual(result, {'platform': 'noaa', 'platnum': '19',
                                      'time': dt.datetime(2014, 2, 12, 14, 12),
                                      'orbit': 12345,
                                      'ext': '.l1b'})

    def test_parse_align(self):
        filepattern="H-000-{hrit_format:4s}__-{platform_name:4s}________-{channel_name:_<9s}-{segment:_<9s}-{start_time:%Y%m%d%H%M}-__"
        result = parse(filepattern, "H-000-MSG3__-MSG3________-IR_039___-000007___-201506051700-__")
        self.assertDictEqual(result, {'channel_name': 'IR_039',
                                      'hrit_format': 'MSG3',
                                      'platform_name': 'MSG3',
                                      'segment': '000007',
                                      'start_time': dt.datetime(2015, 6, 5, 17, 0)})

    def test_parse_digits(self):
        """Test when a digit field is shorter than the format spec."""
        result = parse(
            "hrpt_{platform}{platnum:2s}_{time:%Y%m%d_%H%M}_{orbit:05d}{ext}",
            "hrpt_noaa19_20140212_1412_02345.l1b")
        self.assertDictEqual(result, {'platform': 'noaa', 'platnum': '19',
                                      'time': dt.datetime(2014, 2, 12, 14, 12),
                                      'orbit': 2345,
                                      'ext': '.l1b'})
        result = parse(
            "hrpt_{platform}{platnum:2s}_{time:%Y%m%d_%H%M}_{orbit:5d}{ext}",
            "hrpt_noaa19_20140212_1412_ 2345.l1b")
        self.assertDictEqual(result, {'platform': 'noaa', 'platnum': '19',
                                      'time': dt.datetime(2014, 2, 12, 14, 12),
                                      'orbit': 2345,
                                      'ext': '.l1b'})
        result = parse(
            "hrpt_{platform}{platnum:2s}_{time:%Y%m%d_%H%M}_{orbit:_>5d}{ext}",
            "hrpt_noaa19_20140212_1412___345.l1b")
        self.assertDictEqual(result, {'platform': 'noaa', 'platnum': '19',
                                      'time': dt.datetime(2014, 2, 12, 14, 12),
                                      'orbit': 345,
                                      'ext': '.l1b'})

    def test_parse_bad_pattern(self):
        """Test when a digit field is shorter than the format spec."""
        self.assertRaises(ValueError, parse,
                          "hrpt_{platform}{platnum:-=2s}_{time:%Y%m%d_%H%M}_{orbit:05d}{ext}",
                          "hrpt_noaa19_20140212_1412_02345.l1b")

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

    def test_compose(self):
        """Test the compose method's custom conversion options."""
        from trollsift import compose
        key_vals = {'a': 'this Is A-Test b_test c test'}

        new_str = compose("{a!c}", key_vals)
        self.assertEqual(new_str, 'This is a-test b_test c test')
        new_str = compose("{a!h}", key_vals)
        self.assertEqual(new_str, 'thisisatestbtestctest')
        new_str = compose("{a!H}", key_vals)
        self.assertEqual(new_str, 'THISISATESTBTESTCTEST')
        new_str = compose("{a!l}", key_vals)
        self.assertEqual(new_str, 'this is a-test b_test c test')
        new_str = compose("{a!R}", key_vals)
        self.assertEqual(new_str, 'thisIsATestbtestctest')
        new_str = compose("{a!t}", key_vals)
        self.assertEqual(new_str, 'This Is A-Test B_Test C Test')
        new_str = compose("{a!u}", key_vals)
        self.assertEqual(new_str, 'THIS IS A-TEST B_TEST C TEST')
        # builtin repr
        new_str = compose("{a!r}", key_vals)
        self.assertEqual(new_str, '\'this Is A-Test b_test c test\'')
        # no formatting
        new_str = compose("{a}", key_vals)
        self.assertEqual(new_str, 'this Is A-Test b_test c test')
        # bad formatter
        self.assertRaises(ValueError, compose, "{a!X}", key_vals)
        self.assertEqual(new_str, 'this Is A-Test b_test c test')


def suite():
    """The suite for test_parser
    """
    loader = unittest.TestLoader()
    mysuite = unittest.TestSuite()
    mysuite.addTest(loader.loadTestsFromTestCase(TestParser))
    return mysuite
