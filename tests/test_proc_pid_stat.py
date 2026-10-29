import os
import unittest
import json
from typing import Dict
import jc.parsers.proc_pid_stat
from jc.exceptions import ParseError

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
                'fixtures/linux-proc/pid_stat_hack.json'),
            'pid_stat_signed_fields': (
                'fixtures/linux-proc/pid_stat_signed_fields',
                'fixtures/linux-proc/pid_stat_signed_fields.json')
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

    def test_proc_pid_stat_signed_fields(self):
        """
        Test '/proc/<pid>/stat' with an empty comm, negative priority and nice, and an exit signal of -1
        """
        self.assertEqual(jc.parsers.proc_pid_stat.parse(self.f_in['pid_stat_signed_fields'], quiet=True),
                                                       self.f_json['pid_stat_signed_fields'])

    def test_proc_pid_stat_bad_line(self):
        """
        Test '/proc/<pid>/stat' with a line that does not match
        """
        with self.assertRaises(ParseError):
            jc.parsers.proc_pid_stat.parse('1 (systemd) S 0 1 1', quiet=True)


    def test_proc_pid_stat_comm_that_looks_like_a_number(self):
        """
        Test '/proc/<pid>/stat' with a process name that looks like a number
        """
        data = self.f_in['proc_pid_stat'].replace('(systemd)', '(007)', 1)
        result = jc.parsers.proc_pid_stat.parse(data, quiet=True)
        self.assertEqual(result['comm'], '007')
        self.assertEqual(result['pid'], 1)
        self.assertEqual(result['state'], 'S')


if __name__ == '__main__':
    unittest.main()
