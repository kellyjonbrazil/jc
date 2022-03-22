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

    def test_asciitable_pretty_ansi(self):
        """
        Test 'asciitable' with a pretty table with ANSI codes
        """
        input = '''┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┓                                   \n                                   ┃\x1b[1m \x1b[0m\x1b[1mReleased    \x1b[0m\x1b[1m \x1b[0m┃\x1b[1m \x1b[0m\x1b[1mTitle                            \x1b[0m\x1b[1m \x1b[0m┃\x1b[1m \x1b[0m\x1b[1m    Box Office\x1b[0m\x1b[1m \x1b[0m┃                                   \n                                   ┡━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━┩                                   \n                                   │\x1b[36m \x1b[0m\x1b[36mDec 20, 2019\x1b[0m\x1b[36m \x1b[0m│\x1b[35m \x1b[0m\x1b[35mStar Wars: The Rise of Skywalker \x1b[0m\x1b[35m \x1b[0m│\x1b[32m \x1b[0m\x1b[32m  $952,110,690\x1b[0m\x1b[32m \x1b[0m│                                   \n                                   │\x1b[36m \x1b[0m\x1b[36mMay 25, 2018\x1b[0m\x1b[36m \x1b[0m│\x1b[35m \x1b[0m\x1b[35mSolo: A Star Wars Story          \x1b[0m\x1b[35m \x1b[0m│\x1b[32m \x1b[0m\x1b[32m  $393,151,347\x1b[0m\x1b[32m \x1b[0m│                                   \n                                   │\x1b[36m \x1b[0m\x1b[36mDec 15, 2017\x1b[0m\x1b[36m \x1b[0m│\x1b[35m \x1b[0m\x1b[35mStar Wars Ep. V111: The Last Jedi\x1b[0m\x1b[35m \x1b[0m│\x1b[32m \x1b[0m\x1b[32m$1,332,539,889\x1b[0m\x1b[32m \x1b[0m│                                   \n                                   │\x1b[36m \x1b[0m\x1b[36mDec 16, 2016\x1b[0m\x1b[36m \x1b[0m│\x1b[35m \x1b[0m\x1b[35mRogue One: A Star Wars Story     \x1b[0m\x1b[35m \x1b[0m│\x1b[32m \x1b[0m\x1b[32m$1,332,439,889\x1b[0m\x1b[32m \x1b[0m│                                   \n                                   └──────────────┴───────────────────────────────────┴────────────────┘                                   \n'''

        expected = [
            {
                "released": "Dec 20, 2019",
                "title": "Star Wars: The Rise of Skywalker",
                "box_office": "$952,110,690"
            },
            {
                "released": "May 25, 2018",
                "title": "Solo: A Star Wars Story",
                "box_office": "$393,151,347"
            },
            {
                "released": "Dec 15, 2017",
                "title": "Star Wars Ep. V111: The Last Jedi",
                "box_office": "$1,332,539,889"
            },
            {
                "released": "Dec 16, 2016",
                "title": "Rogue One: A Star Wars Story",
                "box_office": "$1,332,439,889"
            }
        ]

        self.assertEqual(jc.parsers.asciitable.parse(input, quiet=True), expected)


if __name__ == '__main__':
    unittest.main()
