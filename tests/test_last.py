import os
import json
import unittest
import jc.parsers.last

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/last.out'), 'r', encoding='utf-8') as f:
            self.centos_7_7_last = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/last.out'), 'r', encoding='utf-8') as f:
            self.ubuntu_18_4_last = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/last.out'), 'r', encoding='utf-8') as f:
            self.osx_10_14_6_last = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/lastb.out'), 'r', encoding='utf-8') as f:
            self.centos_7_7_lastb = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/lastb.out'), 'r', encoding='utf-8') as f:
            self.ubuntu_18_4_lastb = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/last-w.out'), 'r', encoding='utf-8') as f:
            self.centos_7_7_last_w = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/last-w.out'), 'r', encoding='utf-8') as f:
            self.ubuntu_18_4_last_w = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/last.json'), 'r', encoding='utf-8') as f:
            self.centos_7_7_last_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/last.json'), 'r', encoding='utf-8') as f:
            self.ubuntu_18_4_last_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/last.json'), 'r', encoding='utf-8') as f:
            self.osx_10_14_6_last_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/lastb.json'), 'r', encoding='utf-8') as f:
            self.centos_7_7_lastb_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/lastb.json'), 'r', encoding='utf-8') as f:
            self.ubuntu_18_4_lastb_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/last-w.json'), 'r', encoding='utf-8') as f:
            self.centos_7_7_last_w_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/last-w.json'), 'r', encoding='utf-8') as f:
            self.ubuntu_18_4_last_w_json = json.loads(f.read())

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


if __name__ == '__main__':
    unittest.main()
