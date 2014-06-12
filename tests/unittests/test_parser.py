import unittest
import datetime as dt

from trollsift.parser import _extract_parsedef, _extract_values, _convert, parse, validate, is_one2one

class TestParser(unittest.TestCase):
    
    def setUp(self):
        self.fmt = "/somedir/{directory}/hrpt_{platform:4s}{platnum:2s}" +\
            "_{time:%Y%m%d_%H%M}_{orbit:05d}.l1b"
        self.string = "/somedir/otherdir/hrpt_noaa16_20140210_1004_69022.l1b"
        self.string2 = "/somedir/otherdir/hrpt_noaa16_20140210_1004_00022.l1b"

    def test_extract_parsedef(self):
        # Run
        result,dummy = _extract_parsedef(self.fmt)
        # Assert
        self.assertItemsEqual(result,
                              ['/somedir/', {'directory':None},
                               '/hrpt_', {'platform': '4s'},
                               {'platnum': '2s'}, 
                               '_', {'time': '%Y%m%d_%H%M'},
                               '_', {'orbit': '05d'}, '.l1b'])
        
    def test_extract_values(self):
        # Run
        parsedef = ['/somedir/',{'directory':None}, '/hrpt_',
                    {'platform': '4s'}, {'platnum': '2s'}, 
                    '_', {'time': '%Y%m%d_%H%M'}, '_',
                    {'orbit': 'd'}, '.l1b']
        result = _extract_values(parsedef, self.string)
        # Assert
        self.assertDictEqual(result, {'directory':'otherdir',
                                      'platform':'noaa', 'platnum':'16',
                                      'time':'20140210_1004','orbit':'69022'})

    def test_extract_values_padding(self):
        # Run
        parsedef = ['/somedir/',{'directory':None}, '/hrpt_',
                    {'platform': '4s'}, {'platnum': '2s'}, 
                    '_', {'time': '%Y%m%d_%H%M'}, '_', {'orbit': '05d'},
                    '.l1b']
        result = _extract_values(parsedef, self.string2)
        # Assert
        self.assertDictEqual(result, {'directory':'otherdir',
                                      'platform':'noaa', 'platnum':'16',
                                      'time':'20140210_1004','orbit':'00022'})

    def test_extract_values_padding2(self):
        # Run
        parsedef = ['/somedir/',{'directory':None}, '/hrpt_',
                    {'platform': '4s'}, {'platnum': '2s'}, 
                    '_', {'time': '%Y%m%d_%H%M'}, '_',
                    {'orbit': '0>5d'}, '.l1b' ]
        result = _extract_values( parsedef, self.string2 )
        # Assert
        self.assertDictEqual(result, {'directory':'otherdir',
                                      'platform':'noaa', 'platnum':'16',
                                      'time':'20140210_1004','orbit':'00022'})

    def test_extract_values_fails(self):
        # Run
        parsedef = ['/somedir/',{'directory':None}, '/hrpt_',
                    {'platform': '4s'}, {'platnum': '2s'}, 
                    '_', {'time': '%Y%m%d_%H%M'}, '_', {'orbit': '4d'}, '.l1b']
        self.assertRaises(ValueError, _extract_values, parsedef, self.string)

    def test_convert_digits(self):
        self.assertEqual(_convert('d','69022'), 69022)
        self.assertRaises(ValueError , _convert, 'd','69dsf')
        self.assertEqual(_convert('d','00022'), 22)
        self.assertEqual(_convert('4d','69022'), 69022)
        self.assertEqual(_convert('_>10d','_____69022'), 69022)
        self.assertEqual(_convert('%Y%m%d_%H%M', '20140210_1004'),
                         dt.datetime(2014, 2, 10, 10, 4))

    def test_parse(self):
        # Run
        result = parse(self.fmt, "/somedir/avhrr/2014/hrpt_noaa19_20140212_1412_12345.l1b")
        # Assert
        self.assertDictEqual(result, {'directory': 'avhrr/2014',
                                      'platform': 'noaa', 'platnum': '19',
                                      'time': dt.datetime(2014, 2, 12, 14, 12),
                                      'orbit':12345})

    def test_validate(self):
        # These cases are True
        self.assertTrue( validate( self.fmt, "/somedir/avhrr/2014/hrpt_noaa19_20140212_1412_12345.l1b") )
        self.assertTrue( validate( self.fmt, "/somedir/avhrr/2014/hrpt_noaa01_19790530_0705_00000.l1b") )
        self.assertTrue( validate( self.fmt, "/somedir/funny-char$dir/hrpt_noaa19_20140212_1412_12345.l1b") )
        self.assertTrue( validate( self.fmt, "/somedir//hrpt_noaa19_20140212_1412_12345.l1b") )
        # These cases are False
        self.assertFalse( validate( self.fmt, "/somedir/bla/bla/hrpt_noaa19_20140212_1412_1A345.l1b") )
        self.assertFalse( validate( self.fmt, "/somedir/bla/bla/hrpt_noaa19_2014021_1412_00000.l1b") )
        self.assertFalse( validate( self.fmt, "/somedir/bla/bla/hrpt_noaa19_20140212__412_00000.l1b") )
        self.assertFalse( validate( self.fmt, "/somedir/bla/bla/hrpt_noaa19_20140212__1412_00000.l1b") )
        self.assertFalse( validate( self.fmt, "/somedir/bla/bla/hrpt_noaa19_20140212_1412_00000.l1") )
        self.assertFalse( validate( self.fmt, "/somedir/bla/bla/hrpt_noaa19_20140212_1412_00000") )
        self.assertFalse( validate( self.fmt, "{}/somedir/bla/bla/hrpt_noaa19_20140212_1412_00000.l1b") )

    def test_is_one2one(self):
        # These cases are True
        self.assertTrue( is_one2one("/somedir/{directory}/somedata_{platform:4s}_{time:%Y%d%m-%H%M}_{orbit:5d}.l1b") )
        # These cases are False
        self.assertFalse( is_one2one("/somedir/{directory}/somedata_{platform:4s}_{time:%Y%d%m-%H%M}_{orbit:d}.l1b") )

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
