import os
import json
import unittest
import jc.parsers.last

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/last.out'), 'r', encoding='utf-8') as f:
        centos_7_7_last = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/last.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_last = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/last.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_last = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/lastb.out'), 'r', encoding='utf-8') as f:
        centos_7_7_lastb = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/lastb.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_lastb = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/last-w.out'), 'r', encoding='utf-8') as f:
        centos_7_7_last_w = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/last-w.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_last_w = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/fedora32/last.out'), 'r', encoding='utf-8') as f:
        fedora32_last = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/last.out'), 'r', encoding='utf-8') as f:
        freebsd12_last = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.04/last-F.out'), 'r', encoding='utf-8') as f:
        ubuntu_20_4_last_F = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/last-crash.out'), 'r', encoding='utf-8') as f:
        centos_7_7_last_crash = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/last-wF.out'), 'r', encoding='utf-8') as f:
        centos_7_7_last_wF = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/last-wixF.out'), 'r', encoding='utf-8') as f:
        centos_7_7_last_wixF = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/last.json'), 'r', encoding='utf-8') as f:
        centos_7_7_last_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/last.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_last_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/last.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_last_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/lastb.json'), 'r', encoding='utf-8') as f:
        centos_7_7_lastb_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/lastb.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_lastb_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/last-w.json'), 'r', encoding='utf-8') as f:
        centos_7_7_last_w_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/last-w.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_last_w_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/fedora32/last.json'), 'r', encoding='utf-8') as f:
        fedora32_last_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/last.json'), 'r', encoding='utf-8') as f:
        freebsd12_last_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.04/last-F.json'), 'r', encoding='utf-8') as f:
        ubuntu_20_4_last_F_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/last-crash.json'), 'r', encoding='utf-8') as f:
        centos_7_7_last_crash_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/last-wF.json'), 'r', encoding='utf-8') as f:
        centos_7_7_last_wF_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/last-wixF.json'), 'r', encoding='utf-8') as f:
        centos_7_7_last_wixF_json = json.loads(f.read())


    def test_last_nodata(self):
        """
        Test plain 'last' with no data
        """
        self.assertEqual(jc.parsers.last.parse('', quiet=True), [])

    def test_last_centos_7_7(self):
        """
        Test plain 'last' on Centos 7.7
        """
        self.assertEqual(jc.parsers.last.parse(self.centos_7_7_last, quiet=True), self.centos_7_7_last_json)

    def test_last_ubuntu_18_4(self):
        """
        Test plain 'last' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.last.parse(self.ubuntu_18_4_last, quiet=True), self.ubuntu_18_4_last_json)

    def test_last_osx_10_14_6(self):
        """
        Test plain 'last' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.last.parse(self.osx_10_14_6_last, quiet=True), self.osx_10_14_6_last_json)

    def test_lastb_centos_7_7(self):
        """
        Test plain 'lastb' on Centos 7.7
        """
        self.assertEqual(jc.parsers.last.parse(self.centos_7_7_lastb, quiet=True), self.centos_7_7_lastb_json)

    def test_lastb_ubuntu_18_4(self):
        """
        Test plain 'lastb' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.last.parse(self.ubuntu_18_4_lastb, quiet=True), self.ubuntu_18_4_lastb_json)

    def test_last_w_centos_7_7(self):
        """
        Test 'last -w' on Centos 7.7
        """
        self.assertEqual(jc.parsers.last.parse(self.centos_7_7_last_w, quiet=True), self.centos_7_7_last_w_json)

    def test_last_w_ubuntu_18_4(self):
        """
        Test 'last -w' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.last.parse(self.ubuntu_18_4_last_w, quiet=True), self.ubuntu_18_4_last_w_json)

    def test_last_F_ubuntu_20_4(self):
        """
        Test 'last -F' on Ubuntu 20.4
        """
        self.assertEqual(jc.parsers.last.parse(self.ubuntu_20_4_last_F, quiet=True), self.ubuntu_20_4_last_F_json)

    def test_last_fedora32(self):
        """
        Test plain 'last' on Fedora32
        """
        self.assertEqual(jc.parsers.last.parse(self.fedora32_last, quiet=True), self.fedora32_last_json)

    def test_last_freebsd12(self):
        """
        Test plain 'last' on FreeBSD12
        """
        self.assertEqual(jc.parsers.last.parse(self.freebsd12_last, quiet=True), self.freebsd12_last_json)

    def test_last_crash_centos_7_7(self):
        """
        Test plain 'last' on Centos 7.7 with crash entries
        """
        self.assertEqual(jc.parsers.last.parse(self.centos_7_7_last_crash, quiet=True), self.centos_7_7_last_crash_json)

    def test_last_wF_centos_7_7(self):
        """
        Test 'last -wF' on Centos 7.7
        """
        self.assertEqual(jc.parsers.last.parse(self.centos_7_7_last_wF, quiet=True), self.centos_7_7_last_wF_json)

    def test_last_wixF_centos_7_7(self):
        """
        Test 'last -wixF' on Centos 7.7
        """
        self.assertEqual(jc.parsers.last.parse(self.centos_7_7_last_wixF, quiet=True), self.centos_7_7_last_wixF_json)


if __name__ == '__main__':
    unittest.main()
