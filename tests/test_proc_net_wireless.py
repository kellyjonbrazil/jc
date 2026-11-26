import os
import unittest
import json
from typing import Dict
import jc.parsers.proc_net_wireless
from jc.exceptions import ParseError

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'proc_net_wireless': (
                'fixtures/linux-proc/net_wireless',
                'fixtures/linux-proc/net_wireless.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_proc_net_wireless_nodata(self):
        """
        Test 'proc_net_wireless' with no data
        """
        self.assertEqual(jc.parsers.proc_net_wireless.parse('', quiet=True), [])

    def test_proc_net_wireless(self):
        """
        Test '/proc/net/wireless'
        """
        self.assertEqual(jc.parsers.proc_net_wireless.parse(self.f_in['proc_net_wireless'], quiet=True),
                                                             self.f_json['proc_net_wireless'])

    def test_proc_net_wireless_no_interfaces(self):
        """
        Test '/proc/net/wireless' with only the header lines
        """
        data = ''.join(self.f_in['proc_net_wireless'].splitlines(keepends=True)[:2])
        self.assertEqual(jc.parsers.proc_net_wireless.parse(data, quiet=True), [])

    def test_proc_net_wireless_raw(self):
        """
        Test '/proc/net/wireless' raw output keeps the hex status and the dots
        """
        result = jc.parsers.proc_net_wireless.parse(self.f_in['proc_net_wireless'], raw=True, quiet=True)
        self.assertEqual([(x['interface'], x['status'], x['quality_link']) for x in result],
                         [('wlp0s20f3', '0000', '58.'), ('wlan0', '0000', '0'), ('wlan1', '000a', '70.')])

    def test_proc_net_wireless_invalid_line(self):
        """
        Test '/proc/net/wireless' with a line that is cut short
        """
        data = ''.join(self.f_in['proc_net_wireless'].splitlines(keepends=True)[:3]) + ' wlan9: 0000   70.\n'
        with self.assertRaises(ParseError):
            jc.parsers.proc_net_wireless.parse(data, quiet=True)


if __name__ == '__main__':
    unittest.main()
