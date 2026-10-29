import os
import unittest
import json
import jc.parsers.blkid

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/blkid.out'), 'r', encoding='utf-8') as f:
        centos_7_7_blkid = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/blkid.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_blkid = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/blkid-sda2.out'), 'r', encoding='utf-8') as f:
        centos_7_7_blkid_sda2 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/blkid-sda2.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_blkid_sda2 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/blkid-ip-udev.out'), 'r', encoding='utf-8') as f:
        centos_7_7_blkid_ip_udev = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/blkid-ip-udev.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_blkid_ip_udev = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/blkid-ip-multi.out'), 'r', encoding='utf-8') as f:
        centos_7_7_blkid_ip_multi = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/blkid-ip-multi.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_blkid_ip_multi = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/blkid-ip-udev-multi.out'), 'r', encoding='utf-8') as f:
        centos_7_7_blkid_ip_udev_multi = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/blkid-ip-udev-multi.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_blkid_ip_udev_multi = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/blkid-label-escapes.out'), 'r', encoding='utf-8') as f:
        generic_blkid_label_escapes = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/blkid.json'), 'r', encoding='utf-8') as f:
        centos_7_7_blkid_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/blkid.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_blkid_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/blkid-sda2.json'), 'r', encoding='utf-8') as f:
        centos_7_7_blkid_sda2_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/blkid-sda2.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_blkid_sda2_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/blkid-ip-udev.json'), 'r', encoding='utf-8') as f:
        centos_7_7_blkid_ip_udev_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/blkid-ip-udev.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_blkid_ip_udev_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/blkid-ip-multi.json'), 'r', encoding='utf-8') as f:
        centos_7_7_blkid_ip_multi_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/blkid-ip-multi.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_blkid_ip_multi_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/blkid-ip-udev-multi.json'), 'r', encoding='utf-8') as f:
        centos_7_7_blkid_ip_udev_multi_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/blkid-ip-udev-multi.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_blkid_ip_udev_multi_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/blkid-label-escapes.json'), 'r', encoding='utf-8') as f:
        generic_blkid_label_escapes_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/blkid-udev-label-colon.out'), 'r', encoding='utf-8') as f:
        generic_blkid_udev_label_colon = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/blkid-udev-label-colon.json'), 'r', encoding='utf-8') as f:
        generic_blkid_udev_label_colon_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/blkid-device-spaces.out'), 'r', encoding='utf-8') as f:
        generic_blkid_device_spaces = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/blkid-device-spaces.json'), 'r', encoding='utf-8') as f:
        generic_blkid_device_spaces_json = json.loads(f.read())

    def test_blkid_nodata(self):
        """
        Test 'blkid' with no data
        """
        self.assertEqual(jc.parsers.blkid.parse('', quiet=True), [])

    def test_blkid_centos_7_7(self):
        """
        Test 'blkid' on Centos 7.7
        """
        self.assertEqual(jc.parsers.blkid.parse(self.centos_7_7_blkid, quiet=True), self.centos_7_7_blkid_json)

    def test_blkid_ubuntu_18_4(self):
        """
        Test 'blkid' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.blkid.parse(self.ubuntu_18_4_blkid, quiet=True), self.ubuntu_18_4_blkid_json)

    def test_blkid_sda2_centos_7_7(self):
        """
        Test 'blkid /dev/sda2' on Centos 7.7
        """
        self.assertEqual(jc.parsers.blkid.parse(self.centos_7_7_blkid_sda2, quiet=True), self.centos_7_7_blkid_sda2_json)

    def test_blkid_sda2_ubuntu_18_4(self):
        """
        Test 'blkid /dev/sda2' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.blkid.parse(self.ubuntu_18_4_blkid_sda2, quiet=True), self.ubuntu_18_4_blkid_sda2_json)

    def test_blkid_ip_udev_centos_7_7(self):
        """
        Test 'blkid -ip -o udev /dev/sda2' on Centos 7.7
        """
        self.assertEqual(jc.parsers.blkid.parse(self.centos_7_7_blkid_ip_udev, quiet=True), self.centos_7_7_blkid_ip_udev_json)

    def test_blkid_ip_udev_ubuntu_18_4(self):
        """
        Test 'blkid -ip -o udev /dev/sda2' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.blkid.parse(self.ubuntu_18_4_blkid_sda2, quiet=True), self.ubuntu_18_4_blkid_sda2_json)

    def test_blkid_ip_multi_centos_7_7(self):
        """
        Test 'blkid -ip /dev/sda1 /dev/sda2' on Centos 7.7
        """
        self.assertEqual(jc.parsers.blkid.parse(self.centos_7_7_blkid_ip_multi, quiet=True), self.centos_7_7_blkid_ip_multi_json)

    def test_blkid_ip_multi_ubuntu_18_4(self):
        """
        Test 'blkid -ip /dev/sda1 /dev/sda2' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.blkid.parse(self.ubuntu_18_4_blkid_ip_multi, quiet=True), self.ubuntu_18_4_blkid_ip_multi_json)

    def test_blkid_ip_udev_multi_centos_7_7(self):
        """
        Test 'blkid -ip -o udev /dev/sda1 /dev/sda2' on Centos 7.7
        """
        self.assertEqual(jc.parsers.blkid.parse(self.centos_7_7_blkid_ip_udev_multi, quiet=True), self.centos_7_7_blkid_ip_udev_multi_json)

    def test_blkid_ip_udev_multi_ubuntu_18_4(self):
        """
        Test 'blkid -ip -o udev /dev/sda1 /dev/sda2' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.blkid.parse(self.ubuntu_18_4_blkid_ip_udev_multi, quiet=True), self.ubuntu_18_4_blkid_ip_udev_multi_json)


    def test_blkid_line_separator(self):
        """
        Test 'blkid' with a line-break character other than LF inside a field
        """
        data = 'ID_FS_LABEL=\x1eID_FS_TYPE=xfs\x1e\nID_FS_UUID=6666\nID_FS_TYPE=ext4\n'
        result = jc.parsers.blkid.parse(data, quiet=True)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['id_fs_label'], '\x1eID_FS_TYPE=xfs\x1e')
        self.assertEqual(result[0]['id_fs_type'], 'ext4')


    def test_blkid_label_escapes(self):
        """
        Test 'blkid' with labels containing quotation marks, backslashes,
        '=' and the 0x1c character (printed as ^\\ without escaping the
        backslash)
        """
        self.assertEqual(jc.parsers.blkid.parse(self.generic_blkid_label_escapes, quiet=True), self.generic_blkid_label_escapes_json)

    def test_blkid_label_caret_backslash(self):
        """
        Test 'blkid' where a label with 0x1c contains text that looks like
        another tag
        """
        data = '/dev/sdb1: LABEL="x^\\\\" DEVICE=/dev/sda1 Z=^\\" UUID="6666" TYPE="btrfs"\n'
        result = jc.parsers.blkid.parse(data, quiet=True)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['device'], '/dev/sdb1')
        self.assertEqual(result[0]['label'], 'x^\\" DEVICE=/dev/sda1 Z=^\\')
        self.assertEqual(result[0]['uuid'], '6666')
        self.assertNotIn('z', result[0])

    def test_blkid_unquoted_values(self):
        """
        Test 'blkid' with hand-written unquoted and mixed values
        """
        data = '/dev/sda1: UUID=abc TYPE=ext4\n/dev/sda2: UUID=def TYPE="xfs" LABEL="my disk"\n/dev/sda3: LABEL=\'single quoted\' TYPE=ext4\n'
        expected = [
            {'device': '/dev/sda1', 'uuid': 'abc', 'type': 'ext4'},
            {'device': '/dev/sda2', 'uuid': 'def', 'type': 'xfs', 'label': 'my disk'},
            {'device': '/dev/sda3', 'label': 'single quoted', 'type': 'ext4'}
        ]
        self.assertEqual(jc.parsers.blkid.parse(data, quiet=True), expected)

    def test_blkid_blank_lines(self):
        """
        Test 'blkid' with blank lines between device lines
        """
        data = '/dev/sda1: UUID="abc" TYPE="ext4"\n\n/dev/sda2: UUID="def" TYPE="xfs"\n'
        expected = [
            {'device': '/dev/sda1', 'uuid': 'abc', 'type': 'ext4'},
            {'device': '/dev/sda2', 'uuid': 'def', 'type': 'xfs'}
        ]
        self.assertEqual(jc.parsers.blkid.parse(data, quiet=True), expected)

    def test_blkid_udev_label_colon(self):
        """
        Test 'blkid -o udev' with a label that ends in ':'
        """
        self.assertEqual(jc.parsers.blkid.parse(self.generic_blkid_udev_label_colon, quiet=True), self.generic_blkid_udev_label_colon_json)

    def test_blkid_device_spaces(self):
        """
        Test 'blkid' with a first device path that contains a space
        """
        self.assertEqual(jc.parsers.blkid.parse(self.generic_blkid_device_spaces, quiet=True), self.generic_blkid_device_spaces_json)


if __name__ == '__main__':
    unittest.main()
