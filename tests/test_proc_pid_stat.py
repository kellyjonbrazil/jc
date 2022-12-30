import os
import unittest
import json
from typing import Dict
import jc.parsers.proc_pid_stat

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'proc_pid_stat': (
                'fixtures/linux-proc/pid_stat',
                'fixtures/linux-proc/pid_stat.json'),
            'pid_stat_w_space_and_nl_in_comm': (
                'fixtures/linux-proc/pid_stat_w_space_and_nl_in_comm',
                'fixtures/linux-proc/pid_stat_w_space_and_nl_in_comm.json'),
            'pid_stat_hack': (
                'fixtures/linux-proc/pid_stat_hack',
                'fixtures/linux-proc/pid_stat_hack.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_proc_pid_stat_nodata(self):
        """
        Test 'proc_pid_stat' with no data
        """
        self.assertEqual(jc.parsers.proc_pid_stat.parse('', quiet=True), {})

    def test_proc_pid_stat(self):
        """
        Test '/proc/<pid>/stat'
        """
        self.assertEqual(jc.parsers.proc_pid_stat.parse(self.f_in['proc_pid_stat'], quiet=True),
                                                        self.f_json['proc_pid_stat'])

    def test_proc_pid_stat_w_space_and_nl(self):
        """
        Test '/proc/<pid>/stat' with command with spaces and newline
        """
        self.assertEqual(jc.parsers.proc_pid_stat.parse(self.f_in['pid_stat_w_space_and_nl_in_comm'], quiet=True),
                                                        self.f_json['pid_stat_w_space_and_nl_in_comm'])

    def test_proc_pid_stat_hack(self):
        """
        Test '/proc/<pid>/stat' with evil command hack
        """
        self.assertEqual(jc.parsers.proc_pid_stat.parse(self.f_in['pid_stat_hack'], quiet=True),
                                                        self.f_json['pid_stat_hack'])


if __name__ == '__main__':
    unittest.main()
