import os
import unittest
import json
from typing import Dict
import jc.parsers.proc_consoles
from jc.exceptions import ParseError

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'proc_consoles': (
                'fixtures/linux-proc/consoles',
                'fixtures/linux-proc/consoles.json'),
            'proc_consoles2': (
                'fixtures/linux-proc/consoles2',
                'fixtures/linux-proc/consoles2.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_proc_consoles_nodata(self):
        """
        Test 'proc_consoles' with no data
        """
        self.assertEqual(jc.parsers.proc_consoles.parse('', quiet=True), [])

    def test_proc_consoles(self):
        """
        Test '/proc/consoles'
        """
        self.assertEqual(jc.parsers.proc_consoles.parse(self.f_in['proc_consoles'], quiet=True),
                                                        self.f_json['proc_consoles'])

    def test_proc_consoles2(self):
        """
        Test '/proc/consoles2'
        """
        self.assertEqual(jc.parsers.proc_consoles.parse(self.f_in['proc_consoles2'], quiet=True),
                                                        self.f_json['proc_consoles2'])

    def test_proc_consoles_field_variations(self):
        """
        Test '/proc/consoles' with spaces in the flags, empty flags and extra whitespace
        """
        data = 'ttyS0 -W- (E  p) 4:64\n  tty1\t-WU  ()  4:1  \n'
        result = jc.parsers.proc_consoles.parse(data, quiet=True)
        self.assertEqual([r['device'] for r in result], ['ttyS0', 'tty1'])
        self.assertEqual(result[0]['flags_list'], ['enabled', 'printk buffer'])
        self.assertEqual(result[1]['flags_list'], [])
        self.assertEqual(result[1]['major'], 4)
        self.assertEqual(result[1]['minor'], 1)

    def test_proc_consoles_quote_in_device(self):
        """
        Test '/proc/consoles' with quote and backslash characters, which are
        kept as they are
        """
        data = 'tty\'0\\ -W- (E) 4:5\n'
        result = jc.parsers.proc_consoles.parse(data, quiet=True)
        self.assertEqual(result[0]['device'], 'tty\'0\\')
        self.assertEqual(result[0]['minor'], 5)

    def test_proc_consoles_unexpected_line(self):
        """
        Test '/proc/consoles' with a line that does not match the format
        """
        self.assertRaises(ParseError, jc.parsers.proc_consoles.parse, 'tty0 -W- 4:5\n', quiet=True)


if __name__ == '__main__':
    unittest.main()
