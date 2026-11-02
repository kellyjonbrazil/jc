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
        self.assertEqual(result[1]['mount_point'], '/home/u/x\x1e99 1 0:99 / /tmp')
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


    def test_proc_pid_mountinfo_text_super_option_values(self):
        """
        Test '/proc/<pid>/mountinfo' with text values in super options
        """
        data = (
            '448 432 0:55 / /a rw,relatime - proc proc rw,hidepid=invisible\n'
            '453 432 0:58 / /m rw,relatime - overlay ov ro,lowerdir=/x/l1:/x/l2,upperdir=/x/u,opt=a=b,size=4096k,mode=755\n'
        )
        result = jc.parsers.proc_pid_mountinfo.parse(data, quiet=True)
        self.assertEqual(result[0]['super_options'], ['rw'])
        self.assertEqual(result[0]['super_options_fields'], {'hidepid': 'invisible'})
        self.assertEqual(result[1]['super_options'], ['ro'])
        self.assertEqual(result[1]['super_options_fields'],
                         {'lowerdir': '/x/l1:/x/l2', 'upperdir': '/x/u', 'opt': 'a=b', 'size': 4096, 'mode': 755})

    def test_proc_pid_mountinfo_unusual_optional_fields(self):
        """
        Test '/proc/<pid>/mountinfo' with optional fields that are not numbers
        """
        data = '448 432 0:55 / /a rw,relatime shared:1 master:2 foo:bar:baz - proc proc rw\n'
        result = jc.parsers.proc_pid_mountinfo.parse(data, quiet=True)
        self.assertEqual(result[0]['optional_fields'], {'shared': 1, 'master': 2, 'foo': 'bar:baz'})
        self.assertEqual(result[0]['fs_type'], 'proc')

    def test_proc_pid_mountinfo_unbindable_with_other_fields(self):
        """
        Test '/proc/<pid>/mountinfo' with unbindable next to other optional fields
        """
        data = ('64 69 8:2 / /x rw master:1 unbindable - ext4 /dev/sda2 rw\n'
                '65 69 8:3 / /y rw unbindable - ext4 /dev/sda3 rw\n')
        result = jc.parsers.proc_pid_mountinfo.parse(data, quiet=True)
        self.assertEqual(result[0]['optional_fields'], {'master': 1, 'unbindable': 0})
        self.assertEqual(result[1]['optional_fields'], {'unbindable': 0})

    def test_proc_pid_mountinfo_octal_escapes(self):
        """
        Test '/proc/<pid>/mountinfo' with octal escapes in paths, source and options
        """
        data = (
            '36 35 98:0 /my\\040dir /mnt/a\\040b\\011c rw,noatime master:1 - ext3 /dev/my\\040disk rw,data=ord\\054ered,x\\075y=a\\075b\\134c\n'
            '37 35 98:0 / /mnt/d\\134040e rw shared:2 - fuse.my\\040fs src rw\n'
        )
        result = jc.parsers.proc_pid_mountinfo.parse(data, quiet=True)
        self.assertEqual(result[0]['root'], '/my dir')
        self.assertEqual(result[0]['mount_point'], '/mnt/a b\tc')
        self.assertEqual(result[0]['mount_source'], '/dev/my disk')
        self.assertEqual(result[0]['super_options'], ['rw'])
        self.assertEqual(result[0]['super_options_fields'], {'data': 'ord,ered', 'x=y': 'a=b\\c'})
        self.assertEqual(result[1]['mount_point'], '/mnt/d\\040e')
        self.assertEqual(result[1]['fs_type'], 'fuse.my fs')
        self.assertEqual(result[1]['mount_source'], 'src')

        raw = jc.parsers.proc_pid_mountinfo.parse(data, raw=True, quiet=True)
        self.assertEqual(raw[0]['mount_point'], '/mnt/a b\tc')
        self.assertEqual(raw[0]['super_options'], 'rw,data=ord\\054ered,x\\075y=a\\075b\\134c')


if __name__ == '__main__':
    unittest.main()
