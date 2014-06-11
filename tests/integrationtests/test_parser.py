import unittest
import datetime as dt

from trollsift.parser import Parser

class TestParser(unittest.TestCase):
    
    def setUp(self):
        self.fmt = "/somedir/{directory}/hrpt_{platform:4s}{platnum:2s}" +\
            "_{time:%Y%m%d_%H%M}_{orbit:05d}.l1b"
        self.string = "/somedir/otherdir/hrpt_noaa16_20140210_1004_69022.l1b"
        self.data = {'directory': 'avhrr/2014', 'platform': 'noaa', 'platnum': '19',
                     'time': dt.datetime(2014,02,12,14,12), 'orbit':12345}
        self.p = Parser(self.fmt)

    def test_parse(self):
        # Run
        result = p.parse(self.string)
        # Assert
        self.assertDictEqual(result, self.data)

    def test_compose(self):
        # Run
        result = p.compose(self.data)
        # Assert
        self.assertDictEqual(result, self.string)
        
    def assertDictEqual(self, a, b):
        for key in a:
            self.assertTrue( key in b )
            self.assertEqual(a[key],b[key])

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
