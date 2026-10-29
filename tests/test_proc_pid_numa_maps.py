import os
import unittest
import json
from typing import Dict
import jc.parsers.proc_pid_numa_maps

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'proc_pid_numa_maps': (
                'fixtures/linux-proc/pid_numa_maps',
                'fixtures/linux-proc/pid_numa_maps.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_proc_pid_numa_maps_nodata(self):
        """
        Test 'proc_pid_numa_maps' with no data
        """
        self.assertEqual(jc.parsers.proc_pid_numa_maps.parse('', quiet=True), [])

    def test_proc_pid_numa_maps(self):
        """
        Test '/proc/<pid>/numa_maps'
        """
        self.assertEqual(jc.parsers.proc_pid_numa_maps.parse(self.f_in['proc_pid_numa_maps'], quiet=True),
                                                             self.f_json['proc_pid_numa_maps'])


    def test_proc_pid_numa_maps_other_whitespace_in_file(self):
        """
        Test '/proc/<pid>/numa_maps' splits details on space only
        """
        data = '7f95642e9000 default file=/tmp/libudev.so.1\x1fstack mapped=1 active=0 N0=1 kernelpagesize_kB=4\n'
        expected = [{'address': '7f95642e9000', 'policy': 'default', 'file': '/tmp/libudev.so.1\x1fstack', 'mapped': 1, 'active': 0, 'N0': 1, 'kernelpagesize_kB': 4}]
        self.assertEqual(jc.parsers.proc_pid_numa_maps.parse(data, quiet=True), expected)


    def test_proc_pid_numa_maps_address_that_looks_like_a_number(self):
        """
        Test '/proc/<pid>/numa_maps' with an address that has no hex letters
        """
        data = '00400000 default file=/usr/bin/cat mapped=2 N0=2 kernelpagesize_kB=4\n'
        expected = [{'address': '00400000', 'policy': 'default', 'file': '/usr/bin/cat', 'mapped': 2, 'N0': 2, 'kernelpagesize_kB': 4}]
        self.assertEqual(jc.parsers.proc_pid_numa_maps.parse(data, quiet=True), expected)


if __name__ == '__main__':
    unittest.main()
