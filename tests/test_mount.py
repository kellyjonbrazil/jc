import os
import json
import unittest
import jc.parsers.mount
from jc.exceptions import ParseError

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/mount.out'), 'r', encoding='utf-8') as f:
        centos_7_7_mount = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/mount.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_mount = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/mount.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_mount = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/mount2.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_mount2 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/aix-7.1/mount.out'), 'r', encoding='utf-8') as f:
        aix_7_1_mount = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mount-linux-spaces-in-mountpoint.out'), 'r', encoding='utf-8') as f:
        generic_mount_linux_spaces_in_mountpoint = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mount-linux-spaces-in-filename.out'), 'r', encoding='utf-8') as f:
        generic_mount_linux_spaces_in_filename = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mount-osx-parens-in-filesystem.out'), 'r', encoding='utf-8') as f:
        generic_mount_osx_parens_in_filesystem = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mount-linux-newline-in-source.out'), 'r', encoding='utf-8') as f:
        generic_mount_linux_newline_in_source = f.read()


    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/mount.json'), 'r', encoding='utf-8') as f:
        centos_7_7_mount_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/mount.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_mount_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/mount.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_mount_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/mount2.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_mount2_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/aix-7.1/mount.json'), 'r', encoding='utf-8') as f:
        aix_7_1_mount_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mount-linux-spaces-in-mountpoint.json'), 'r', encoding='utf-8') as f:
        generic_mount_linux_spaces_in_mountpoint_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mount-linux-spaces-in-filename.json'), 'r', encoding='utf-8') as f:
        generic_mount_linux_spaces_in_filename_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mount-osx-parens-in-filesystem.json'), 'r', encoding='utf-8') as f:
        generic_mount_osx_parens_in_filesystem_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mount-linux-newline-in-source.json'), 'r', encoding='utf-8') as f:
        generic_mount_linux_newline_in_source_json = json.loads(f.read())


    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mount-linux-type-in-mountpoint.out'), 'r', encoding='utf-8') as f:
        generic_mount_linux_type_in_mountpoint = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mount-linux-type-in-mountpoint.json'), 'r', encoding='utf-8') as f:
        generic_mount_linux_type_in_mountpoint_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mount-osx-options-in-mountpoint.out'), 'r', encoding='utf-8') as f:
        generic_mount_osx_options_in_mountpoint = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mount-osx-options-in-mountpoint.json'), 'r', encoding='utf-8') as f:
        generic_mount_osx_options_in_mountpoint_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mount-osx-aix-header-text.out'), 'r', encoding='utf-8') as f:
        generic_mount_osx_aix_header_text = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mount-osx-aix-header-text.json'), 'r', encoding='utf-8') as f:
        generic_mount_osx_aix_header_text_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mount-linux-quoted-and-escaped-commas.out'), 'r', encoding='utf-8') as f:
        generic_mount_linux_quoted_and_escaped_commas = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mount-linux-quoted-and-escaped-commas.json'), 'r', encoding='utf-8') as f:
        generic_mount_linux_quoted_and_escaped_commas_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mount-aix-spaces-in-mountpoint.out'), 'r', encoding='utf-8') as f:
        generic_mount_aix_spaces_in_mountpoint = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mount-aix-spaces-in-mountpoint.json'), 'r', encoding='utf-8') as f:
        generic_mount_aix_spaces_in_mountpoint_json = json.loads(f.read())

    def test_mount_nodata(self):
        """
        Test 'mount' with no data
        """
        self.assertEqual(jc.parsers.mount.parse('', quiet=True), [])

    def test_mount_centos_7_7(self):
        """
        Test 'mount' on Centos 7.7
        """
        self.assertEqual(jc.parsers.mount.parse(self.centos_7_7_mount, quiet=True), self.centos_7_7_mount_json)

    def test_mount_ubuntu_18_4(self):
        """
        Test 'mount' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.mount.parse(self.ubuntu_18_4_mount, quiet=True), self.ubuntu_18_4_mount_json)

    def test_mount_osx_10_14_6(self):
        """
        Test 'mount' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.mount.parse(self.osx_10_14_6_mount, quiet=True), self.osx_10_14_6_mount_json)

    def test_mount2_osx_10_14_6(self):
        """
        Test 'mount' on OSX 10.14.6 #2
        """
        self.assertEqual(jc.parsers.mount.parse(self.osx_10_14_6_mount2, quiet=True), self.osx_10_14_6_mount2_json)

    def test_mount_aix_7_1(self):
        """
        Test 'mount' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.mount.parse(self.aix_7_1_mount, quiet=True), self.aix_7_1_mount_json)

    def test_mount_spaces_in_mountpoint(self):
        """
        Test 'mount' with spaces in the mountpoint
        """
        self.assertEqual(jc.parsers.mount.parse(self.generic_mount_linux_spaces_in_mountpoint, quiet=True), self.generic_mount_linux_spaces_in_mountpoint_json)

    def test_mount_spaces_in_filename(self):
        """
        Test 'mount' with spaces in the filename
        """
        self.assertEqual(jc.parsers.mount.parse(self.generic_mount_linux_spaces_in_filename, quiet=True), self.generic_mount_linux_spaces_in_filename_json)

    def test_mount_parens_in_filesystem(self):
        """
        Test 'mount' with parenthesis in the filesystem
        """
        self.assertEqual(jc.parsers.mount.parse(self.generic_mount_osx_parens_in_filesystem, quiet=True), self.generic_mount_osx_parens_in_filesystem_json)


    def test_mount_line_separator(self):
        """
        Test 'mount' with a line-break character other than LF inside a field
        """
        data = 'none on /tmp/usb type vfat (rw)\u2028/dev/sdb1 on /mnt/backup type ext4 (rw,nosuid,nodev,noexec)\u2028none on /tmp/usb type tmpfs (rw,relatime,inode64)\n'
        result = jc.parsers.mount.parse(data, quiet=True)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['filesystem'], 'none on /tmp/usb type vfat (rw)\u2028/dev/sdb1 on /mnt/backup type ext4 (rw,nosuid,nodev,noexec)\u2028none')
        self.assertEqual(result[0]['mount_point'], '/tmp/usb')
        self.assertEqual(result[0]['type'], 'tmpfs')
        self.assertEqual(result[0]['options'], ['rw', 'relatime', 'inode64'])

    def test_mount_newline_in_source(self):
        """
        Test 'mount' where a newline in a source name leaves a long line that
        repeats ' on ... type ... (' after its last ')'
        """
        self.assertEqual(jc.parsers.mount.parse(self.generic_mount_linux_newline_in_source, quiet=True), self.generic_mount_linux_newline_in_source_json)

    def test_mount_point_ends_in_on(self):
        """
        Test 'mount' with a mount point that ends in ' on' on Linux and macOS
        """
        linux = '/dev/sdb1 on /mnt/turn on type ext4 (rw,relatime)\n'
        osx = '/dev/disk2s1 on /Volumes/turn on (hfs, local, journaled)\n'
        self.assertEqual(
            jc.parsers.mount.parse(linux, quiet=True),
            [{'filesystem': '/dev/sdb1', 'mount_point': '/mnt/turn on', 'type': 'ext4', 'options': ['rw', 'relatime']}]
        )
        self.assertEqual(
            jc.parsers.mount.parse(osx, quiet=True),
            [{'filesystem': '/dev/disk2s1', 'mount_point': '/Volumes/turn on', 'options': ['hfs', 'local', 'journaled']}]
        )

    def test_mount_type_in_mountpoint(self):
        """
        Test 'mount -l' with mount points that contain type and options text
        """
        self.assertEqual(jc.parsers.mount.parse(self.generic_mount_linux_type_in_mountpoint, quiet=True), self.generic_mount_linux_type_in_mountpoint_json)

    def test_mount_options_in_mountpoint_bsd(self):
        """
        Test 'mount' on macOS/BSD with a mount point that contains options text
        """
        self.assertEqual(jc.parsers.mount.parse(self.generic_mount_osx_options_in_mountpoint, quiet=True), self.generic_mount_osx_options_in_mountpoint_json)

    def test_mount_aix_header_text_in_osx(self):
        """
        Test 'mount' on OSX with mount names that contain AIX header words
        """
        self.assertEqual(jc.parsers.mount.parse(self.generic_mount_osx_aix_header_text, quiet=True), self.generic_mount_osx_aix_header_text_json)

    def test_mount_linux_quoted_and_escaped_commas(self):
        """
        Test 'mount' on Linux with quoted and backslash-escaped commas in options
        """
        self.assertEqual(jc.parsers.mount.parse(self.generic_mount_linux_quoted_and_escaped_commas, quiet=True), self.generic_mount_linux_quoted_and_escaped_commas_json)

    def test_mount_aix_spaces_in_mountpoint(self):
        """
        Test 'mount' on AIX with spaces in mount points and remote devices
        """
        self.assertEqual(jc.parsers.mount.parse(self.generic_mount_aix_spaces_in_mountpoint, quiet=True), self.generic_mount_aix_spaces_in_mountpoint_json)

    def test_mount_unrecognized_line(self):
        """
        Test 'mount' with a line that is not a mount entry
        """
        # a newline in a mount point splits the entry into two lines
        data = 'sysfs on /sys type sysfs (rw,nosuid)\n/dev/sda1 on /a\nb type ext4 (rw)\n'
        self.assertRaises(ParseError, jc.parsers.mount.parse, data, quiet=True)
        self.assertRaises(ParseError, jc.parsers.mount.parse, 'foo\n', quiet=True)
        self.assertEqual(jc.parsers.mount.parse('sysfs on /sys type sysfs (rw,nosuid)\n', quiet=True),
                         [{'filesystem': 'sysfs', 'mount_point': '/sys', 'type': 'sysfs', 'options': ['rw', 'nosuid']}])


if __name__ == '__main__':
    unittest.main()
