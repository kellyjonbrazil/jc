import os
import json
import unittest
import jc.parsers.df

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/df.out'), 'r', encoding='utf-8') as f:
        centos_7_7_df = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/df.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_df = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/df.out'), 'r', encoding='utf-8') as f:
        osx_10_11_6_df = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/df.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_df = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/df-h.out'), 'r', encoding='utf-8') as f:
        centos_7_7_df_h = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/df-h.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_df_h = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/df-h.out'), 'r', encoding='utf-8') as f:
        osx_10_11_6_df_h = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/df-h.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_df_h = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/df-hh.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_df_hh = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/df-linux-long-filesystem.out'), 'r', encoding='utf-8') as f:
        generic_df_linux_long_filesystem = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/df-linux-wide-chars.out'), 'r', encoding='utf-8') as f:
        generic_df_linux_wide_chars = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/df-linux-wide-chars.json'), 'r', encoding='utf-8') as f:
        generic_df_linux_wide_chars_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/df-linux-long-filesystem-in-mount-point.out'), 'r', encoding='utf-8') as f:
        generic_df_linux_long_filesystem_in_mount_point = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/df-linux-long-filesystem-in-mount-point.json'), 'r', encoding='utf-8') as f:
        generic_df_linux_long_filesystem_in_mount_point_json = json.loads(f.read())

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/df.json'), 'r', encoding='utf-8') as f:
        centos_7_7_df_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/df.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_df_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/df.json'), 'r', encoding='utf-8') as f:
        osx_10_11_6_df_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/df.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_df_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/df-h.json'), 'r', encoding='utf-8') as f:
        centos_7_7_df_h_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/df-h.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_df_h_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/df-h.json'), 'r', encoding='utf-8') as f:
        osx_10_11_6_df_h_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/df-h.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_df_h_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/df-hh.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_df_hh_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/df-linux-long-filesystem.json'), 'r', encoding='utf-8') as f:
        generic_df_linux_long_filesystem_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/df-linux-long-filesystem-many-rows.out'), 'r', encoding='utf-8') as f:
        generic_df_linux_long_filesystem_many_rows = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/df-linux-long-filesystem-many-rows.json'), 'r', encoding='utf-8') as f:
        generic_df_linux_long_filesystem_many_rows_json = json.loads(f.read())


    def test_df_nodata(self):
        """
        Test plain 'df' with no data
        """
        self.assertEqual(jc.parsers.df.parse('', quiet=True), [])

    def test_df_centos_7_7(self):
        """
        Test plain 'df' on Centos 7.7
        """
        self.assertEqual(jc.parsers.df.parse(self.centos_7_7_df, quiet=True), self.centos_7_7_df_json)

    def test_df_ubuntu_18_4(self):
        """
        Test plain 'df' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.df.parse(self.ubuntu_18_4_df, quiet=True), self.ubuntu_18_4_df_json)

    def test_df_osx_10_11_6(self):
        """
        Test plain 'df' on OSX 10.11.6
        """
        self.assertEqual(jc.parsers.df.parse(self.osx_10_11_6_df, quiet=True), self.osx_10_11_6_df_json)

    def test_df_osx_10_14_6(self):
        """
        Test plain 'df' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.df.parse(self.osx_10_14_6_df, quiet=True), self.osx_10_14_6_df_json)

    def test_df_h_centos_7_7(self):
        """
        Test 'df -h' on Centos 7.7
        """
        self.assertEqual(jc.parsers.df.parse(self.centos_7_7_df_h, quiet=True), self.centos_7_7_df_h_json)

    def test_df_h_ubuntu_18_4(self):
        """
        Test 'df -h' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.df.parse(self.ubuntu_18_4_df_h, quiet=True), self.ubuntu_18_4_df_h_json)

    def test_df_h_osx_10_11_6(self):
        """
        Test 'df -h' on OSX 10.11.6
        """
        self.assertEqual(jc.parsers.df.parse(self.osx_10_11_6_df_h, quiet=True), self.osx_10_11_6_df_h_json)

    def test_df_h_osx_10_14_6(self):
        """
        Test 'df -h' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.df.parse(self.osx_10_14_6_df_h, quiet=True), self.osx_10_14_6_df_h_json)

    def test_df_hh_osx_10_14_6(self):
        """
        Test 'df -H' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.df.parse(self.osx_10_14_6_df_hh, quiet=True), self.osx_10_14_6_df_hh_json)

    def test_df_long_filesystem(self):
        """
        Test older version of 'df' with long filesystem data
        """
        self.assertEqual(jc.parsers.df.parse(self.generic_df_linux_long_filesystem, quiet=True), self.generic_df_linux_long_filesystem_json)

    def test_df_long_filesystem_in_mount_point(self):
        """
        Test older version of 'df' with a long filesystem name that is also
        part of the mount point
        """
        result = jc.parsers.df.parse(self.generic_df_linux_long_filesystem_in_mount_point, quiet=True)
        self.assertEqual(result, self.generic_df_linux_long_filesystem_in_mount_point_json)
        self.assertEqual(result[0]['filesystem'], '/dev/mapper/VolGroup00-LogVol00')
        self.assertEqual(result[0]['mounted_on'], '/mnt//dev/mapper/VolGroup00-LogVol00')

    def test_df_long_filesystem_many_rows(self):
        """
        Test older version of 'df' with a wide filesystem column and many rows
        """
        self.assertEqual(jc.parsers.df.parse(self.generic_df_linux_long_filesystem_many_rows, quiet=True), self.generic_df_linux_long_filesystem_many_rows_json)

    def test_df_centos_7_7_trailing_newline(self):
        """
        Test plain 'df' on Centos 7.7 with a trailing newline
        """
        cmd_output = self.centos_7_7_df + '\n'
        self.assertEqual(jc.parsers.df.parse(cmd_output, quiet=True), self.centos_7_7_df_json)


    def test_df_line_separator(self):
        """
        Test 'df' with a line-break character other than LF inside a field
        """
        data = 'Filesystem     1K-blocks  Used Available Use% Mounted on\ntmpfs               1024     0      1024   0% /mnt/x\u2028/dev/sda1         100000 99999         1 100% /data\n'
        result = jc.parsers.df.parse(data, quiet=True)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['mounted_on'], '/mnt/x\u2028/dev/sda1         100000 99999         1 100% /data')


    def test_df_wide_chars(self):
        """
        Test 'df' with wide, combining, zero-width and U+2063 characters
        """
        self.assertEqual(jc.parsers.df.parse(self.generic_df_linux_wide_chars, quiet=True), self.generic_df_linux_wide_chars_json)
    def test_df_whitespace_only_line(self):
        """
        Test 'df' with a line that has only spaces between rows
        """
        data = ('Filesystem     1K-blocks    Used Available Use% Mounted on\n'
                '/dev/sda1            100      50        50  50% /\n'
                '   \n'
                'tmpfs                 10       0        10   0% /tmp\n')
        result = jc.parsers.df.parse(data, quiet=True)
        self.assertEqual([x['filesystem'] for x in result], ['/dev/sda1', 'tmpfs'])
        self.assertEqual(result[1]['mounted_on'], '/tmp')


if __name__ == '__main__':
    unittest.main()
