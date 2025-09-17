import os
import json
import unittest
import jc.parsers.mount

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

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mount-spaces-in-mountpoint.out'), 'r', encoding='utf-8') as f:
        generic_mount_spaces_in_mountpoint = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mount-spaces-in-filename.out'), 'r', encoding='utf-8') as f:
        generic_mount_spaces_in_filename = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mount-parens-in-filesystem.out'), 'r', encoding='utf-8') as f:
        generic_mount_parens_in_filesystem = f.read()


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

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mount-spaces-in-mountpoint.json'), 'r', encoding='utf-8') as f:
        generic_mount_spaces_in_mountpoint_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mount-spaces-in-filename.json'), 'r', encoding='utf-8') as f:
        generic_mount_spaces_in_filename_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mount-parens-in-filesystem.json'), 'r', encoding='utf-8') as f:
        generic_mount_parens_in_filesystem_json = json.loads(f.read())


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
        self.assertEqual(jc.parsers.mount.parse(self.generic_mount_spaces_in_mountpoint, quiet=True), self.generic_mount_spaces_in_mountpoint_json)

    def test_mount_spaces_in_filename(self):
        """
        Test 'mount' with spaces in the filename
        """
        self.assertEqual(jc.parsers.mount.parse(self.generic_mount_spaces_in_filename, quiet=True), self.generic_mount_spaces_in_filename_json)

    def test_mount_parens_in_filesystem(self):
        """
        Test 'mount' with parenthesis in the filesystem
        """
        self.assertEqual(jc.parsers.mount.parse(self.generic_mount_parens_in_filesystem, quiet=True), self.generic_mount_parens_in_filesystem_json)


if __name__ == '__main__':
    unittest.main()
