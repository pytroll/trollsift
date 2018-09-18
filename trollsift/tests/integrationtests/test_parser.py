import unittest
import datetime as dt

from trollsift.parser import Parser


class TestParser(unittest.TestCase):

    def setUp(self):
        self.fmt = "/somedir/{directory}/hrpt_{platform:4s}{platnum:2s}" +\
            "_{time:%Y%m%d_%H%M}_{orbit:05d}.l1b"
        self.string = "/somedir/otherdir/hrpt_noaa16_20140210_1004_69022.l1b"
        self.data = {'directory': 'otherdir', 'platform': 'noaa',
                     'platnum': '16',
                     'time': dt.datetime(2014, 2, 10, 10, 4), 'orbit': 69022}
        self.p = Parser(self.fmt)

    def test_parse(self):
        # Run
        result = self.p.parse(self.string)
        # Assert
        self.assertDictEqual(result, self.data)

    def test_compose(self):
        # Run
        result = self.p.compose(self.data)
        # Assert
        self.assertEqual(result, self.string)

    def test_validate(self):
        # These cases are True
        self.assertTrue(
            self.p.validate("/somedir/avhrr/2014/hrpt_noaa19_20140212_1412_12345.l1b"))
        # These cases are False
        self.assertFalse(
            self.p.validate("/somedir/bla/bla/hrpt_noaa19_20140212__1412_00000.l1b"))

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


class TestParserVIIRSSDR(unittest.TestCase):

    def setUp(self):
        self.fmt = 'SVI01_{platform_shortname}_d{start_time:%Y%m%d_t%H%M%S%f}_e{end_time:%H%M%S%f}_b{orbit:5d}_c{creation_time:%Y%m%d%H%M%S%f}_{source}.h5'
        self.string = 'SVI01_npp_d20120225_t1801245_e1802487_b01708_c20120226002130255476_noaa_ops.h5'
        self.data = {'platform_shortname': 'npp',
                     'start_time': dt.datetime(2012, 2, 25, 18, 1, 24, 500000), 'orbit': 1708,
                     'end_time': dt.datetime(1900, 1, 1, 18, 2, 48, 700000),
                     'source': 'noaa_ops',
                     'creation_time': dt.datetime(2012, 2, 26, 0, 21, 30, 255476)}
        self.p = Parser(self.fmt)

    def test_parse(self):
        # Run
        result = self.p.parse(self.string)
        # Assert
        self.assertDictEqual(result, self.data)


def suite():
    """The suite for test_parser
    """
    loader = unittest.TestLoader()
    mysuite = unittest.TestSuite()
    mysuite.addTest(loader.loadTestsFromTestCase(TestParser))
    mysuite.addTest(loader.loadTestsFromTestCase(TestParserVIIRSSDR))
    return mysuite
