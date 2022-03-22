import os
import unittest
from jc.exceptions import ParseError
import jc.parsers.asciitable

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def test_asciitable_nodata(self):
        """
        Test 'asciitable' with no data
        """
        self.assertEqual(jc.parsers.asciitable.parse('', quiet=True), [])

    def test_asciitable_m_pure_ascii(self):
        """
        Test 'asciitable' with a pure ASCII table
        """
        input = '''
+========+========+========+========+========+========+========+
| type   | tota   | used   | fr ee  | shar   | buff   | avai   |

+========+========+========+========+========+========+========+
| Mem    | 3861   | 2228   | 3364   | 1183   | 2743   | 3389   |
+--------+--------+--------+--------+--------+--------+--------+
|        |        |        |        | test 2 |        |        |
+--------+--------+--------+--------+--------+--------+--------+
| last   | last   | last   | ab cde |        |        | final  |
+========+========+========+========+========+========+========+
        '''
        expected = [
            {
                "type": "Mem",
                "tota": "3861",
                "used": "2228",
                "fr_ee": "3364",
                "shar": "1183",
                "buff": "2743",
                "avai": "3389"
            },
            {
                "type": None,
                "tota": None,
                "used": None,
                "fr_ee": None,
                "shar": "test 2",
                "buff": None,
                "avai": None
            },
            {
                "type": "last",
                "tota": "last",
                "used": "last",
                "fr_ee": "ab cde",
                "shar": None,
                "buff": None,
                "avai": "final"
            }
        ]

        self.assertEqual(jc.parsers.asciitable.parse(input, quiet=True), expected)

    def test_asciitable_m_unicode(self):
        """
        Test 'asciitable' with a unicode table
        """
        input = '''
╒════════╤════════╤════════╤════════╤════════╤════════╤════════╕
│ type   │ total  │ used   │ fr ee  │ shar   │ buff   │ avai   │
╞════════╪════════╪════════╪════════╪════════╪════════╪════════╡
│ Mem    │ 3861   │ 2228   │ 3364   │ 1183   │ 2743   │ 3389   │
├────────┼────────┼────────┼────────┼────────┼────────┼────────┤
│ Swap   │ 2097   │ 0      │ 2097   │        │        │        │
├────────┼────────┼────────┼────────┼────────┼────────┼────────┤
│ last   │ last   │ last   │ ab cde │        │        │ final  │
╘════════╧════════╧════════╧════════╧════════╧════════╧════════╛
        '''
        expected = [
            {
                "type": "Mem",
                "total": "3861",
                "used": "2228",
                "fr_ee": "3364",
                "shar": "1183",
                "buff": "2743",
                "avai": "3389"
            },
            {
                "type": "Swap",
                "total": "2097",
                "used": "0",
                "fr_ee": "2097",
                "shar": None,
                "buff": None,
                "avai": None
            },
            {
                "type": "last",
                "total": "last",
                "used": "last",
                "fr_ee": "ab cde",
                "shar": None,
                "buff": None,
                "avai": "final"
            }
        ]

        self.assertEqual(jc.parsers.asciitable.parse(input, quiet=True), expected)

    def test_asciitable_pure_ascii_extra_spaces(self):
        """
        Test 'asciitable' with a pure ASCII table that has heading and
        trailing spaces and newlines.
        """
        input = '''
    
      
    +========+========+========+========+========+========+========+
    | type   | total  | used   | fr ee  | shar   | buff   | avai        
    +========+========+========+========+========+========+========+   
    | Mem    | 3861   | 2228   | 3364   | 1183   | 2743   | 3389     
    +--------+--------+--------+--------+--------+--------+--------+
             |        |        |        | test 2 |        |
    +--------+--------+--------+--------+--------+--------+--------+       
    | last   | last   | last   | ab cde |        |        | final  |
    +========+========+========+========+========+========+========+    
     
  
        '''
        expected = [
            {
                "type": "Mem",
                "total": "3861",
                "used": "2228",
                "fr_ee": "3364",
                "shar": "1183",
                "buff": "2743",
                "avai": "3389"
            },
            {
                "type": None,
                "total": None,
                "used": None,
                "fr_ee": None,
                "shar": "test 2",
                "buff": None,
                "avai": None
            },
            {
                "type": "last",
                "total": "last",
                "used": "last",
                "fr_ee": "ab cde",
                "shar": None,
                "buff": None,
                "avai": "final"
            }
        ]

        self.assertEqual(jc.parsers.asciitable.parse(input, quiet=True), expected)

    def test_asciitable_unicode_extra_spaces(self):
        """
        Test 'asciitable' with a pure ASCII table that has heading and
        trailing spaces and newlines.
        """
        input = '''
    
  
        ╒════════╤════════╤════════╤════════╤════════╤════════╤════════╕
          type   │ total  │ used   │ free   │ shar   │ buff   │ avai
        ╞════════╪════════╪════════╪════════╪════════╪════════╪════════╡      
          Mem    │ 3861   │ 2228   │ 3364   │ 1183   │ 2743   │ 3389     
        ├────────┼────────┼────────┼────────┼────────┼────────┼────────┤  
          Swap   │ 2097   │ 0      │ 2097   │        │        │
        ╘════════╧════════╧════════╧════════╧════════╧════════╧════════╛
   
 
        '''
        expected = [
            {
                "type": "Mem",
                "total": "3861",
                "used": "2228",
                "free": "3364",
                "shar": "1183",
                "buff": "2743",
                "avai": "3389"
            },
            {
                "type": "Swap",
                "total": "2097",
                "used": "0",
                "free": "2097",
                "shar": None,
                "buff": None,
                "avai": None
            }
        ]

        self.assertEqual(jc.parsers.asciitable.parse(input, quiet=True), expected)

    def test_asciitable_markdown(self):
        """
        Test 'asciitable' with a markdown table
        """
        input = '''
        | type   |   total |   used |    free |   shared |   buff cache |   available |
        |--------|---------|--------|---------|----------|--------------|-------------|
        | Mem    | 3861332 | 222820 | 3364176 |    11832 |       274336 |     3389588 |
        | Swap   | 2097148 |      0 | 2097148 |          |              |             |
        '''
        
        expected = [
            {
                "type": "Mem",
                "total": "3861332",
                "used": "222820",
                "free": "3364176",
                "shared": "11832",
                "buff_cache": "274336",
                "available": "3389588"
            },
            {
                "type": "Swap",
                "total": "2097148",
                "used": "0",
                "free": "2097148",
                "shared": None,
                "buff_cache": None,
                "available": None
            }
        ]

        self.assertEqual(jc.parsers.asciitable.parse(input, quiet=True), expected)

    def test_asciitable_simple(self):
        """
        Test 'asciitable' with a simple table
        """
        input = '''
        type      total    used     free    shared    buff cache    available
        ------  -------  ------  -------  --------  ------------  -----------
        Mem     3861332  222820  3364176     11832        274336      3389588
        Swap    2097148       0  2097148
        '''

        expected = [
            {
                "type": "Mem",
                "total": "3861332",
                "used": "222820",
                "free": "3364176",
                "shared": "11832",
                "buff_cache": "274336",
                "available": "3389588"
            },
            {
                "type": "Swap",
                "total": "2097148",
                "used": "0",
                "free": "2097148",
                "shared": None,
                "buff_cache": None,
                "available": None
            }
        ]

        self.assertEqual(jc.parsers.asciitable.parse(input, quiet=True), expected)


if __name__ == '__main__':
    unittest.main()
