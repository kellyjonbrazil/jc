import os
import unittest
import json
from typing import Dict
import jc.parsers.proc_pid_status

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'proc_pid_status': (
                'fixtures/linux-proc/pid_status',
                'fixtures/linux-proc/pid_status.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_proc_pid_status_line_separators(self):
        """
        Test '/proc/<pid>/status' with line-break characters other than LF in the process name
        """
        data = 'Name:\ta\rb\x0bc\x0cd\x1ce\x1df\x1eg\x85h\u2028i\u2029j\nUmask:\t0000\nState:\tS (sleeping)\nPid:\t1\n'
        result = jc.parsers.proc_pid_status.parse(data, quiet=True)
        self.assertEqual(result['Name'], 'a\rb\x0bc\x0cd\x1ce\x1df\x1eg\x85h\u2028i\u2029j')
        self.assertEqual(result['Umask'], '0000')

    def test_proc_pid_status_nodata(self):
        """
        Test 'proc_pid_status' with no data
        """
        self.assertEqual(jc.parsers.proc_pid_status.parse('', quiet=True), {})

    def test_proc_pid_status(self):
        """
        Test '/proc/<pid>/status'
        """
        self.assertEqual(jc.parsers.proc_pid_status.parse(self.f_in['proc_pid_status'], quiet=True),
                                                          self.f_json['proc_pid_status'])


    def test_proc_pid_status_two_word_states(self):
        """
        Test '/proc/<pid>/status' with states that have a two word description
        """
        result = jc.parsers.proc_pid_status.parse('Name:\tgdbserver\nState:\tt (tracing stop)\nPid:\t42\n', quiet=True)
        self.assertEqual(result['State'], 't')
        self.assertEqual(result['State_pretty'], 'tracing stop')
        self.assertEqual(result['Pid'], 42)

        result = jc.parsers.proc_pid_status.parse('State:\tD (disk sleep)\n', quiet=True)
        self.assertEqual(result['State'], 'D')
        self.assertEqual(result['State_pretty'], 'disk sleep')

        result = jc.parsers.proc_pid_status.parse('State:\tS (sleeping)\n', quiet=True)
        self.assertEqual(result['State'], 'S')
        self.assertEqual(result['State_pretty'], 'sleeping')

    def test_proc_pid_status_malformed_uid_gid(self):
        """
        Test '/proc/<pid>/status' with Uid and Gid values that are not numbers
        """
        result = jc.parsers.proc_pid_status.parse('Uid:\t1000\tabc\t1000\t1000\nGid:\t0\t0\t\xff\t0\n', quiet=True)
        self.assertEqual(result['Uid'], [1000, None, 1000, 1000])
        self.assertEqual(result['Gid'], [0, 0, None, 0])


if __name__ == '__main__':
    unittest.main()
