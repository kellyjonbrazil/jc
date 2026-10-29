import os
import unittest
import json
from typing import Dict
import jc.parsers.proc_net_dev

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'proc_net_dev': (
                'fixtures/linux-proc/net_dev',
                'fixtures/linux-proc/net_dev.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_proc_net_dev_nodata(self):
        """
        Test 'proc_net_dev' with no data
        """
        self.assertEqual(jc.parsers.proc_net_dev.parse('', quiet=True), [])

    def test_proc_net_dev(self):
        """
        Test '/proc/net/dev'
        """
        self.assertEqual(jc.parsers.proc_net_dev.parse(self.f_in['proc_net_dev'], quiet=True),
                                                       self.f_json['proc_net_dev'])


    def test_proc_net_dev_interface_that_looks_like_a_number(self):
        """
        Test '/proc/net/dev' with an interface name that looks like a number
        """
        data = (
            'Inter-|   Receive                                                |  Transmit\n'
            ' face |bytes    packets errs drop fifo frame compressed multicast|bytes    packets errs drop fifo colls carrier compressed\n'
            '  007:   13222     152    0    0    0     0          0         0    13222     152    0    0    0     0       0          0\n'
        )
        result = jc.parsers.proc_net_dev.parse(data, quiet=True)
        self.assertEqual(result[0]['interface'], '007')
        self.assertEqual(result[0]['r_bytes'], 13222)

    def test_proc_net_dev_line_separator_in_name(self):
        """
        Test '/proc/net/dev' with line-break and other whitespace characters inside interface names
        """
        data = (
            'Inter-|   Receive                                                |  Transmit\n'
            ' face |bytes    packets errs drop fifo frame compressed multicast|bytes    packets errs drop fifo colls carrier compressed\n'
            'a\u2028b:     100       2    0    0    0     0          0         0      200       3    0    0    0     0       0          0\n'
            ' c\x1cd:      10       1    0    0    0     0          0         0       20       2    0    0    0     0       0          7\n'
            '    lo:   13222     152    0    0    0     0          0         0    13222     152    0    0    0     0       0          0\n'
        )
        result = jc.parsers.proc_net_dev.parse(data, quiet=True)
        self.assertEqual([x['interface'] for x in result], ['a\u2028b', 'c\x1cd', 'lo'])
        self.assertEqual(result[0]['r_bytes'], 100)
        self.assertEqual(result[0]['t_bytes'], 200)
        self.assertEqual(result[1]['t_compressed'], 7)
        self.assertEqual(result[2]['r_packets'], 152)


if __name__ == '__main__':
    unittest.main()
