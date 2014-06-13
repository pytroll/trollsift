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
        self.assertTrue( self.p.validate( "/somedir/avhrr/2014/hrpt_noaa19_20140212_1412_12345.l1b") )
        # These cases are False
        self.assertFalse( self.p.validate( "/somedir/bla/bla/hrpt_noaa19_20140212__1412_00000.l1b") )


        
    def assertDictEqual(self, a, b):
        for key in a:
            self.assertTrue( key in b )
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
