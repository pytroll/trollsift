import unittest
import datetime as dt

from trollsift.parser import _extract_parsedef, _extract_values, _convert

class TestParser(unittest.TestCase):
    
    def setUp(self):
        self.fmt = "/somedir/{directory}/hrpt_{platform:4s}{platnum:2s}" +\
            "_{time:%Y%m%d_%H%M}_{orbit:05d}.l1b"
        self.string = "/somedir/otherdir/hrpt_noaa16_20140210_1004_69022.l1b"
        self.string2 = "/somedir/otherdir/hrpt_noaa16_20140210_1004_00022.l1b"

    def test_extract_keys(self):
        # Run
        result = _extract_parsedef(self.fmt)
        # Assert
        self.assertItemsEqual(result, ['/somedir/', {'directory':None},
                                       '/hrpt_', {'platform': '4s'},
                                       {'platnum': '2s'}, 
                                      '_', {'time': '%Y%m%d_%H%M'},
                                       '_', {'orbit': '05d'}, '.l1b' ] )

    def test_extract_values(self):
        # Run
        parsedef = ['/somedir/',{'directory':None}, '/hrpt_', {'platform': '4s'}, {'platnum': '2s'}, 
                                      '_', {'time': '%Y%m%d_%H%M'}, '_', {'orbit': 'd'}, '.l1b' ]
        result = _extract_values( parsedef, self.string )
        # Assert
        self.assertDictEqual(result, {'directory':'otherdir', 'platform':'noaa', 'platnum':'16', 'time':'20140210_1004','orbit':'69022'})

    def test_extract_values_padding(self):
        # Run
        parsedef = ['/somedir/',{'directory':None}, '/hrpt_', {'platform': '4s'}, {'platnum': '2s'}, 
                                      '_', {'time': '%Y%m%d_%H%M'}, '_', {'orbit': '05d'}, '.l1b' ]
        result = _extract_values( parsedef, self.string2 )
        # Assert
        self.assertDictEqual(result, {'directory':'otherdir', 'platform':'noaa', 'platnum':'16', 'time':'20140210_1004','orbit':'00022'})

    def test_extract_values_padding2(self):
        # Run
        parsedef = ['/somedir/',{'directory':None}, '/hrpt_', {'platform': '4s'}, {'platnum': '2s'}, 
                                      '_', {'time': '%Y%m%d_%H%M'}, '_', {'orbit': '0>5d'}, '.l1b' ]
        result = _extract_values( parsedef, self.string2 )
        # Assert
        self.assertDictEqual(result, {'directory':'otherdir', 'platform':'noaa', 'platnum':'16', 'time':'20140210_1004','orbit':'00022'})

    def test_extract_values_fails(self):
        # Run
        parsedef = ['/somedir/',{'directory':None}, '/hrpt_', {'platform': '4s'}, {'platnum': '2s'}, 
                                      '_', {'time': '%Y%m%d_%H%M'}, '_', {'orbit': '4d'}, '.l1b' ]
        self.assertRaises(ValueError, _extract_values, parsedef, self.string )

    def test_convert_digits(self):
        self.assertEqual(_convert('d','69022'), 69022)
        self.assertRaises(ValueError , _convert, 'd','69dsf')
        self.assertEqual(_convert('d','00022'), 22)
        self.assertEqual(_convert('4d','69022'), 69022)
        self.assertEqual(_convert('_>10d','_____69022'), 69022)
        self.assertEqual(_convert('%Y%m%d_%H%M', '20140210_1004'),
                         dt.datetime(2014, 2, 10, 10, 4))

    def assertDictEqual(self, a, b):
        for key in a:
            self.assertTrue( key in b )
            self.assertEqual(a[key],b[key])

        self.assertEqual(len(a),len(b))
