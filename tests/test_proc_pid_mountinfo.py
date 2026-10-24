import os
import unittest
import json
from typing import Dict
import jc.parsers.proc_pid_mountinfo

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'proc_pid_mountinfo': (
                'fixtures/linux-proc/pid_mountinfo',
                'fixtures/linux-proc/pid_mountinfo.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_proc_pid_mountinfo_nodata(self):
        """
        Test 'proc_pid_mountinfo' with no data
        """
        self.assertEqual(jc.parsers.proc_pid_mountinfo.parse('', quiet=True), [])

    def test_proc_pid_mountinfo(self):
        """
        Test '/proc/<pid>/mountinfo'
        """
        self.assertEqual(jc.parsers.proc_pid_mountinfo.parse(self.f_in['proc_pid_mountinfo'], quiet=True),
                                                             self.f_json['proc_pid_mountinfo'])


    def test_proc_pid_mountinfo_line_separator(self):
        """
        Test 'proc_pid_mountinfo' with a line-break character other than LF inside a field
        """
        data = '24 30 0:22 / /sys rw,nosuid - sysfs sysfs rw\n429 30 0:55 / /home/u/x\x1e99 1 0:99 / /tmp rw,nosuid,nodev,noexec - tmpfs tmpfs rw rw,relatime - tmpfs tmpfs rw,inode64\n'
        result = jc.parsers.proc_pid_mountinfo.parse(data, quiet=True)
        self.assertNotIn(99, [x['mount_id'] for x in result])


if __name__ == '__main__':
    unittest.main()
