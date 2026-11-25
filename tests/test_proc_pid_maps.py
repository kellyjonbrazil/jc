import os
import unittest
import json
from typing import Dict
import jc.parsers.proc_pid_maps

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'proc_pid_maps': (
                'fixtures/linux-proc/pid_maps',
                'fixtures/linux-proc/pid_maps.json'),
            'proc_pid_maps_line_separator': (
                'fixtures/linux-proc/pid_maps_line_separator',
                'fixtures/linux-proc/pid_maps_line_separator.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_proc_pid_maps_nodata(self):
        """
        Test 'proc_pid_maps' with no data
        """
        self.assertEqual(jc.parsers.proc_pid_maps.parse('', quiet=True), [])

    def test_proc_pid_maps(self):
        """
        Test '/proc/<pid>/maps'
        """
        self.assertEqual(jc.parsers.proc_pid_maps.parse(self.f_in['proc_pid_maps'], quiet=True),
                                                        self.f_json['proc_pid_maps'])

    def test_proc_pid_maps_line_separator(self):
        """
        Test '/proc/<pid>/maps' with a pathname containing U+2028 (LINE
        SEPARATOR): the line must stay a single record
        """
        self.assertEqual(jc.parsers.proc_pid_maps.parse(self.f_in['proc_pid_maps_line_separator'], quiet=True),
                                                        self.f_json['proc_pid_maps_line_separator'])


    def test_proc_pid_maps_pathname_trailing_space(self):
        """
        Test '/proc/<pid>/maps' with white space at the end of a pathname
        """
        data = (
            '7f53b436c000-7f53b4375000 r-xp 00000000 fd:00 798126                     /tmp/plugin.so \n'
            '7f53b4375000-7f53b4376000 rw-p 00000000 fd:00 798127                     /tmp/tab.so\t \n'
            '7f53b4376000-7f53b4377000 rw-p 00000000 00:00 0 \n'
            '7f53b4377000-7f53b4378000 rw-p 00000000 00:00 0                          [heap]\n'
        )
        result = jc.parsers.proc_pid_maps.parse(data, quiet=True)
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0]['pathname'], '/tmp/plugin.so ')
        self.assertEqual(result[0]['inode'], 798126)
        self.assertEqual(result[1]['pathname'], '/tmp/tab.so\t ')
        self.assertNotIn('pathname', result[2])
        self.assertEqual(result[3]['pathname'], '[heap]')
        self.assertEqual(result[3]['start'], '7f53b4377000')


if __name__ == '__main__':
    unittest.main()
