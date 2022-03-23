import os
import unittest
from jc.exceptions import ParseError
import jc.parsers.asciitable_m

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def test_asciitable_m_nodata(self):
        """
        Test 'asciitable_m' with no data
        """
        self.assertEqual(jc.parsers.asciitable_m.parse('', quiet=True), [])

    def test_asciitable_m_pure_ascii(self):
        """
        Test 'asciitable_m' with a pure ASCII table
        """
        input = '''
+========+========+========+========+========+========+========+
| type   | tota   | used   | fr ee  | shar   | buff   | avai   |
|        | l      |        |        | ed     | _cac   | labl   |
|        |        |        |        |        | he     | e      |
+========+========+========+========+========+========+========+
| Mem    | 3861   | 2228   | 3364   | 1183   | 2743   | 3389   |
|        | 332    | 20     | 176    | 2      | 36     | 588    |
+--------+--------+--------+--------+--------+--------+--------+
|        |        |        |        |        |        |        |
|        |        |        |        | test 2 |        |        |
+--------+--------+--------+--------+--------+--------+--------+
| last   | last   | last   | ab cde |        |        | final  |
+========+========+========+========+========+========+========+
        '''
        expected = [
            {
                "type": "Mem",
                "tota_l": "3861\n332",
                "used": "2228\n20",
                "fr_ee": "3364\n176",
                "shar_ed": "1183\n2",
                "buff_cac_he": "2743\n36",
                "avai_labl_e": "3389\n588"
            },
            {
                "type": None,
                "tota_l": None,
                "used": None,
                "fr_ee": None,
                "shar_ed": "test 2",
                "buff_cac_he": None,
                "avai_labl_e": None
            },
            {
                "type": "last",
                "tota_l": "last",
                "used": "last",
                "fr_ee": "ab cde",
                "shar_ed": None,
                "buff_cac_he": None,
                "avai_labl_e": "final"
            }
        ]

        self.assertEqual(jc.parsers.asciitable_m.parse(input, quiet=True), expected)

    def test_asciitable_m_unicode(self):
        """
        Test 'asciitable_m' with a unicode table
        """
        input = '''
╒════════╤════════╤════════╤════════╤════════╤════════╤════════╕
│ type   │ tota   │ used   │ fr ee  │ shar   │ buff   │ avai   │
│        │ l      │        │        │ ed     │ _cac   │ labl   │
│        │        │        │        │        │ he     │ e      │
╞════════╪════════╪════════╪════════╪════════╪════════╪════════╡
│ Mem    │ 3861   │ 2228   │ 3364   │ 1183   │ 2743   │ 3389   │
│        │ 332    │ 20     │ 176    │ 2      │ 36     │ 588    │
├────────┼────────┼────────┼────────┼────────┼────────┼────────┤
│ Swap   │ 2097   │ 0      │ 2097   │        │        │        │
│        │ 148    │        │ 148    │        │        │        │
│        │        │        │ kb     │        │        │        │
├────────┼────────┼────────┼────────┼────────┼────────┼────────┤
│ last   │ last   │ last   │ ab cde │        │        │ final  │
╘════════╧════════╧════════╧════════╧════════╧════════╧════════╛
        '''
        expected = [
            {
                "type": "Mem",
                "tota_l": "3861\n332",
                "used": "2228\n20",
                "fr_ee": "3364\n176",
                "shar_ed": "1183\n2",
                "buff_cac_he": "2743\n36",
                "avai_labl_e": "3389\n588"
            },
            {
                "type": "Swap",
                "tota_l": "2097\n148",
                "used": "0",
                "fr_ee": "2097\n148\nkb",
                "shar_ed": None,
                "buff_cac_he": None,
                "avai_labl_e": None
            },
            {
                "type": "last",
                "tota_l": "last",
                "used": "last",
                "fr_ee": "ab cde",
                "shar_ed": None,
                "buff_cac_he": None,
                "avai_labl_e": "final"
            }
        ]

        self.assertEqual(jc.parsers.asciitable_m.parse(input, quiet=True), expected)

    def test_asciitable_m_pure_ascii_extra_spaces(self):
        """
        Test 'asciitable_m' with a pure ASCII table that has heading and
        trailing spaces and newlines.
        """
        input = '''
    
      
    +========+========+========+========+========+========+========+
    | type   | tota   | used   | fr ee  | shar   | buff   | avai  
    |        | l      |        |        | ed     | _cac   | labl         
    |        |        |        |        |        | he     | e      |
    +========+========+========+========+========+========+========+   
    | Mem    | 3861   | 2228   | 3364   | 1183   | 2743   | 3389   |
    |        | 332    | 20     | 176    | 2      | 36     | 588    |
    +--------+--------+--------+--------+--------+--------+--------+
    |        |        |        |        |        |        |        |
    |        |        |        |        | test 2 |        |        |     
    +--------+--------+--------+--------+--------+--------+--------+
    | last   | last   | last   | ab cde |        |        | final     
    +========+========+========+========+========+========+========+    
     
  
        '''
        expected = [
            {
                "type": "Mem",
                "tota_l": "3861\n332",
                "used": "2228\n20",
                "fr_ee": "3364\n176",
                "shar_ed": "1183\n2",
                "buff_cac_he": "2743\n36",
                "avai_labl_e": "3389\n588"
            },
            {
                "type": None,
                "tota_l": None,
                "used": None,
                "fr_ee": None,
                "shar_ed": "test 2",
                "buff_cac_he": None,
                "avai_labl_e": None
            },
            {
                "type": "last",
                "tota_l": "last",
                "used": "last",
                "fr_ee": "ab cde",
                "shar_ed": None,
                "buff_cac_he": None,
                "avai_labl_e": "final"
            }
        ]

        self.assertEqual(jc.parsers.asciitable_m.parse(input, quiet=True), expected)

    def test_asciitable_m_unicode_extra_spaces(self):
        """
        Test 'asciitable_m' with a pure ASCII table that has heading and
        trailing spaces and newlines.
        """
        input = '''
    
  
        ╒════════╤════════╤════════╤════════╤════════╤════════╤════════╕
          type   │ tota   │ used   │ free   │ shar   │ buff   │ avai   
                 │ l      │        │        │ ed     │ _cac   │ labl   
                 │        │        │        │        │ he     │ e        
        ╞════════╪════════╪════════╪════════╪════════╪════════╪════════╡      
          Mem    │ 3861   │ 2228   │ 3364   │ 1183   │ 2743   │ 3389   
                 │ 332    │ 20     │ 176    │ 2      │ 36     │ 588  
        ├────────┼────────┼────────┼────────┼────────┼────────┼────────┤  
          Swap   │ 2097   │ 0      │ 2097   │        │        │            
                 │ 148    │        │ 148    │        │        │        
        ╘════════╧════════╧════════╧════════╧════════╧════════╧════════╛
   
 
        '''
        expected = [
            {
                "type": "Mem",
                "tota_l": "3861\n332",
                "used": "2228\n20",
                "free": "3364\n176",
                "shar_ed": "1183\n2",
                "buff_cac_he": "2743\n36",
                "avai_labl_e": "3389\n588"
            },
            {
                "type": "Swap",
                "tota_l": "2097\n148",
                "used": "0",
                "free": "2097\n148",
                "shar_ed": None,
                "buff_cac_he": None,
                "avai_labl_e": None
            }
        ]

        self.assertEqual(jc.parsers.asciitable_m.parse(input, quiet=True), expected)

    def test_asciitable_m_pretty_ansi(self):
        """
        Test 'asciitable-m' with a pretty table with ANSI codes
        """
        input = '''
┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┓                                   
┃\x1b[1m \x1b[0m\x1b[1mReleased    \x1b[0m\x1b[1m \x1b[0m┃\x1b[1m \x1b[0m\x1b[1mTitle                            \x1b[0m\x1b[1m \x1b[0m┃\x1b[1m \x1b[0m\x1b[1m    Box Office\x1b[0m\x1b[1m \x1b[0m┃                                   
┡━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━┩                                   
│\x1b[36m \x1b[0m\x1b[36mDec 20, 2019\x1b[0m\x1b[36m \x1b[0m│\x1b[35m \x1b[0m\x1b[35mStar Wars: The Rise of Skywalker \x1b[0m\x1b[35m \x1b[0m│\x1b[32m \x1b[0m\x1b[32m  $952,110,690\x1b[0m\x1b[32m \x1b[0m│                                   
│\x1b[36m \x1b[0m\x1b[36mMay 25, 2018\x1b[0m\x1b[36m \x1b[0m│\x1b[35m \x1b[0m\x1b[35mSolo: A Star Wars Story          \x1b[0m\x1b[35m \x1b[0m│\x1b[32m \x1b[0m\x1b[32m  $393,151,347\x1b[0m\x1b[32m \x1b[0m│                                   
│\x1b[36m \x1b[0m\x1b[36mDec 15, 2017\x1b[0m\x1b[36m \x1b[0m│\x1b[35m \x1b[0m\x1b[35mStar Wars Ep. V111: The Last Jedi\x1b[0m\x1b[35m \x1b[0m│\x1b[32m \x1b[0m\x1b[32m$1,332,539,889\x1b[0m\x1b[32m \x1b[0m│                                   
│\x1b[36m \x1b[0m\x1b[36mDec 16, 2016\x1b[0m\x1b[36m \x1b[0m│\x1b[35m \x1b[0m\x1b[35mRogue One: A Star Wars Story     \x1b[0m\x1b[35m \x1b[0m│\x1b[32m \x1b[0m\x1b[32m$1,332,439,889\x1b[0m\x1b[32m \x1b[0m│                                   
└──────────────┴───────────────────────────────────┴────────────────┘                                   
'''
        expected = [
            {
                "released": "Dec 20, 2019\nMay 25, 2018\nDec 15, 2017\nDec 16, 2016",
                "title": "Star Wars: The Rise of Skywalker\nSolo: A Star Wars Story\nStar Wars Ep. V111: The Last Jedi\nRogue One: A Star Wars Story",
                "box_office": "$952,110,690\n$393,151,347\n$1,332,539,889\n$1,332,439,889"
            }
        ]

        self.assertEqual(jc.parsers.asciitable_m.parse(input, quiet=True), expected)

    def test_asciitable_m_special_chars_in_header(self):
        """
        Test 'asciitable_m' with a pure ASCII table that has special
        characters in the header. These should be converted to underscores
        and no trailing or consecutive underscores should end up in the
        resulting key names.
        """
        input = '''
+----------+------------+-----------+----------------+-------+--------------------+
| Protocol | Address    | Age (min) | Hardware Addr  | Type  | Interface          |
|          |            | of int    |                |       |                    |
+----------+------------+-----------+----------------+-------+--------------------+
| Internet | 10.12.13.1 |       98  | 0950.5785.5cd1 | ARPA  | FastEthernet2.13   |
+----------+------------+-----------+----------------+-------+--------------------+
        '''
        expected = [
            {
                "protocol": "Internet",
                "address": "10.12.13.1",
                "age_min_of_int": "98",
                "hardware_addr": "0950.5785.5cd1",
                "type": "ARPA",
                "interface": "FastEthernet2.13"
            }
        ]

        self.assertEqual(jc.parsers.asciitable_m.parse(input, quiet=True), expected)

    def test_asciitable_m_markdown(self):
        """
        Test 'asciitable_m' with a markdown table. Should raise a ParseError
        """
        input = '''
        | type   |   total |   used |    free |   shared |   buff cache |   available |
        |--------|---------|--------|---------|----------|--------------|-------------|
        | Mem    | 3861332 | 222820 | 3364176 |    11832 |       274336 |     3389588 |
        | Swap   | 2097148 |      0 | 2097148 |          |              |             |
        '''

        self.assertRaises(ParseError, jc.parsers.asciitable_m.parse, input, quiet=True)

    def test_asciitable_m_simple(self):
        """
        Test 'asciitable_m' with a simple table. Should raise a ParseError
        """
        input = '''
        type      total    used     free    shared    buff cache    available
        ------  -------  ------  -------  --------  ------------  -----------
        Mem     3861332  222820  3364176     11832        274336      3389588
        Swap    2097148       0  2097148
        '''

        self.assertRaises(ParseError, jc.parsers.asciitable_m.parse, input, quiet=True)


if __name__ == '__main__':
    unittest.main()
