import os
import json
import unittest
import jc.parsers.sysctl

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/sysctl-a.out'), 'r', encoding='utf-8') as f:
        centos_7_7_sysctl = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/sysctl-a.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_sysctl = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/sysctl-a.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_sysctl = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/sysctl-a.out'), 'r', encoding='utf-8') as f:
        freebsd12_sysctl = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/sysctl-a.json'), 'r', encoding='utf-8') as f:
        centos_7_7_sysctl_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/sysctl-a.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_sysctl_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/sysctl-a.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_sysctl_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/sysctl-a.json'), 'r', encoding='utf-8') as f:
        freebsd12_sysctl_json = json.loads(f.read())


    def test_sysctl_nodata(self):
        """
        Test plain 'sysctl' with no data
        """
        self.assertEqual(jc.parsers.sysctl.parse('', quiet=True), {})

    def test_sysctl_centos_7_7(self):
        """
        Test plain 'sysctl' on Centos 7.7
        """
        self.assertEqual(jc.parsers.sysctl.parse(self.centos_7_7_sysctl, quiet=True), self.centos_7_7_sysctl_json)

    def test_sysctl_ubuntu_18_4(self):
        """
        Test plain 'sysctl' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.sysctl.parse(self.ubuntu_18_4_sysctl, quiet=True), self.ubuntu_18_4_sysctl_json)

    def test_sysctl_osx_10_14_6(self):
        """
        Test plain 'sysctl' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.sysctl.parse(self.osx_10_14_6_sysctl, quiet=True), self.osx_10_14_6_sysctl_json)

    def test_sysctl_freebsd12(self):
        """
        Test plain 'sysctl' on FreeBSD12
        """
        self.assertEqual(jc.parsers.sysctl.parse(self.freebsd12_sysctl, quiet=True), self.freebsd12_sysctl_json)


if __name__ == '__main__':
    unittest.main()
