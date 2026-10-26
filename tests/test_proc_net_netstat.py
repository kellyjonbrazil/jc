import os
import unittest
import json
from typing import Dict
import jc.parsers.proc_net_netstat

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # new input/output fixtures
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/net_netstat-repeated-rows.out'), 'r', encoding='utf-8') as f:
        generic_net_netstat_repeated_rows = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/net_netstat-repeated-rows.json'), 'r', encoding='utf-8') as f:
        generic_net_netstat_repeated_rows_json = json.loads(f.read())

    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'proc_net_netstat': (
                'fixtures/linux-proc/net_netstat',
                'fixtures/linux-proc/net_netstat.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_proc_net_netstat_nodata(self):
        """
        Test 'proc_net_netstat' with no data
        """
        self.assertEqual(jc.parsers.proc_net_netstat.parse('', quiet=True), [])

    def test_proc_net_netstat(self):
        """
        Test '/proc/net/netstat'
        """
        self.assertEqual(jc.parsers.proc_net_netstat.parse(self.f_in['proc_net_netstat'], quiet=True),
                                                           self.f_json['proc_net_netstat'])


    def test_proc_net_netstat_repeated_rows(self):
        """
        Test '/proc/net/netstat' with repeated data rows for each header
        """
        self.assertEqual(jc.parsers.proc_net_netstat.parse(self.generic_net_netstat_repeated_rows, quiet=True),
                                                           self.generic_net_netstat_repeated_rows_json)

    def test_proc_net_netstat_ragged_rows(self):
        """
        Test '/proc/net/netstat' rows with fewer or more fields than the header
        """
        data = 'TcpExt: A B C\nTcpExt: 1 2\nTcpExt: 3 4 5 6\nIpExt: X\nIpExt: 9'
        expected = [
            {"A": "1", "B": "2", "type": "TcpExt"},
            {"A": "3", "B": "4", "C": "5 6", "type": "TcpExt"},
            {"X": "9", "type": "IpExt"}
        ]
        self.assertEqual(jc.parsers.proc_net_netstat.parse(data, raw=True, quiet=True), expected)

    def test_proc_net_netstat_empty_data_row(self):
        """
        Test '/proc/net/netstat' with a data row that has no values
        """
        data = 'TcpExt: A B\nTcpExt:\nTcpExt: 1 2'
        expected = [
            {"type": "TcpExt"},
            {"A": "1", "B": "2", "type": "TcpExt"}
        ]
        self.assertEqual(jc.parsers.proc_net_netstat.parse(data, raw=True, quiet=True), expected)


if __name__ == '__main__':
    unittest.main()
