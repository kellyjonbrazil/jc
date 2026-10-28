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
                'fixtures/linux-proc/pid_mountinfo.json'),
            'proc_pid_mountinfo_long_optional': (
                'fixtures/generic/proc-pid-mountinfo-long-optional.out',
                'fixtures/generic/proc-pid-mountinfo-long-optional.json'),
            'proc_pid_mountinfo_empty_source': (
                'fixtures/generic/proc-pid-mountinfo-empty-source.out',
                'fixtures/generic/proc-pid-mountinfo-empty-source.json')
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

    def test_proc_pid_mountinfo_long_optional(self):
        """
        Test '/proc/<pid>/mountinfo' with a line that has many optional fields and no separator
        """
        self.assertEqual(jc.parsers.proc_pid_mountinfo.parse(self.f_in['proc_pid_mountinfo_long_optional'], quiet=True),
                                                             self.f_json['proc_pid_mountinfo_long_optional'])


    def test_proc_pid_mountinfo_line_separator(self):
        """
        Test 'proc_pid_mountinfo' with a line-break character other than LF inside a field
        """
        data = '24 30 0:22 / /sys rw,nosuid - sysfs sysfs rw\n429 30 0:55 / /home/u/x\x1e99 1 0:99 / /tmp rw,nosuid,nodev,noexec - tmpfs tmpfs rw rw,relatime - tmpfs tmpfs rw,inode64\n'
        result = jc.parsers.proc_pid_mountinfo.parse(data, quiet=True)
        self.assertNotIn(99, [x['mount_id'] for x in result])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['mount_id'], 24)
        self.assertEqual(result[0]['mount_point'], '/sys')

        # the same mount point as the kernel prints it, with spaces escaped
        data = '24 30 0:22 / /sys rw,nosuid - sysfs sysfs rw\n429 30 0:55 / /home/u/x\x1e99\\0401\\0400:99\\040/\\040/tmp rw,relatime - tmpfs tmpfs rw,inode64\n'
        result = jc.parsers.proc_pid_mountinfo.parse(data, quiet=True)
        self.assertEqual([x['mount_id'] for x in result], [24, 429])
        self.assertEqual(result[1]['mount_point'], '/home/u/x\x1e99\\0401\\0400:99\\040/\\040/tmp')
        self.assertEqual(result[1]['mount_options'], ['rw', 'relatime'])
        self.assertEqual(result[1]['fs_type'], 'tmpfs')
        self.assertEqual(result[1]['mount_source'], 'tmpfs')


    def test_proc_pid_mountinfo_other_whitespace_in_field(self):
        """
        Test 'proc_pid_mountinfo' splits fields on ASCII whitespace only
        """
        data = '429 30 0:55 / /home/u/x\x1frw,nosuid,nodev,noexec\x1f-\x1fext4\x1f/dev/sda9\x1frw rw,relatime - tmpfs tmpfs rw,inode64\n430 30 0:56 / /tmp/a\xa0b rw,relatime - tmpfs /dev/sda1\xa0ro,nosuid rw,inode64\n'
        result = jc.parsers.proc_pid_mountinfo.parse(data, quiet=True)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['mount_point'], '/home/u/x\x1frw,nosuid,nodev,noexec\x1f-\x1fext4\x1f/dev/sda9\x1frw')
        self.assertEqual(result[0]['mount_options'], ['rw', 'relatime'])
        self.assertEqual(result[0]['fs_type'], 'tmpfs')
        self.assertEqual(result[0]['mount_source'], 'tmpfs')
        self.assertEqual(result[0]['super_options'], ['rw', 'inode64'])
        self.assertEqual(result[1]['mount_point'], '/tmp/a\xa0b')
        self.assertEqual(result[1]['mount_source'], '/dev/sda1\xa0ro,nosuid')
        self.assertEqual(result[1]['super_options'], ['rw', 'inode64'])

    def test_proc_pid_mountinfo_empty_source(self):
        """
        Test '/proc/<pid>/mountinfo' with lines that have an empty mount source
        """
        self.assertEqual(jc.parsers.proc_pid_mountinfo.parse(self.f_in['proc_pid_mountinfo_empty_source'], quiet=True),
                                                             self.f_json['proc_pid_mountinfo_empty_source'])


if __name__ == '__main__':
    unittest.main()
