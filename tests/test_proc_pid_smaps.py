import os
import unittest
import json
from typing import Dict
import jc
import jc.parsers.proc_pid_smaps

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'proc_pid_smaps': (
                'fixtures/linux-proc/pid_smaps',
                'fixtures/linux-proc/pid_smaps.json'),
            'proc_pid_smaps_unknown_flag': (
                'fixtures/linux-proc/pid_smaps_unknown_flag',
                'fixtures/linux-proc/pid_smaps_unknown_flag.json'),
            'proc_pid_smaps_wide_fields': (
                'fixtures/generic/proc-pid-smaps-wide-fields.out',
                'fixtures/generic/proc-pid-smaps-wide-fields.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_proc_pid_smaps_nodata(self):
        """
        Test 'proc_pid_smaps' with no data
        """
        self.assertEqual(jc.parsers.proc_pid_smaps.parse('', quiet=True), [])

    def test_proc_pid_smaps(self):
        """
        Test '/proc/<pid>/smaps'
        """
        self.assertEqual(jc.parsers.proc_pid_smaps.parse(self.f_in['proc_pid_smaps'], quiet=True),
                                                         self.f_json['proc_pid_smaps'])

    def test_proc_pid_smaps_unknown_flag(self):
        """
        Test '/proc/<pid>/smaps' with an unknown flag
        """
        self.assertEqual(jc.parsers.proc_pid_smaps.parse(self.f_in['proc_pid_smaps_unknown_flag'], quiet=True),
                                                         self.f_json['proc_pid_smaps_unknown_flag'])

    def test_proc_pid_smaps_lone_cr_in_pathname(self):
        """
        Test '/proc/<pid>/smaps' with a lone CR inside a pathname
        """
        data = ('55a9e753c000-55a9e7540000 r--p 00000000 fd:00 798126 '
                '/tmp/tool\r7fdead000000-7fdead001000 rwxp 00000000 00:00 0 [heap]\n'
                'Size:                 16 kB\n'
                'Rss:                  16 kB\n'
                'VmFlags: rd mr mw me dw sd\n')
        result = jc.parsers.proc_pid_smaps.parse(data, quiet=True)
        self.assertEqual(1, len(result))
        self.assertEqual('/tmp/tool\r7fdead000000-7fdead001000 rwxp 00000000 00:00 0 [heap]',
                         result[0]['pathname'])
        self.assertEqual('55a9e753c000', result[0]['start'])
        self.assertEqual(['read', 'private'], result[0]['perms'])
        self.assertEqual(16, result[0]['Size'])
        self.assertEqual(result, jc.parse('proc', data, quiet=True))

    def test_proc_pid_smaps_wide_fields(self):
        """
        Test '/proc/<pid>/smaps' with a long offset and a three digit device number
        """
        self.assertEqual(jc.parsers.proc_pid_smaps.parse(self.f_in['proc_pid_smaps_wide_fields'], quiet=True),
                                                         self.f_json['proc_pid_smaps_wide_fields'])


if __name__ == '__main__':
    unittest.main()
