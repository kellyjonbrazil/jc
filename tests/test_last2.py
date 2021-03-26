import os
import json
import unittest
import jc.parsers.last

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.04/last-F.out'), 'r', encoding='utf-8') as f:
            self.ubuntu_20_4_last_F = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/last-wF.out'), 'r', encoding='utf-8') as f:
            self.centos_7_7_last_wF = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.04/last-F.json'), 'r', encoding='utf-8') as f:
            self.ubuntu_20_4_last_F_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/last-wF.json'), 'r', encoding='utf-8') as f:
            self.centos_7_7_last_wF_json = json.loads(f.read())

    def test_last_F_ubuntu_20_4(self):
        """
        Test 'last -F' on Ubuntu 20.4
        """
        self.assertEqual(jc.parsers.last.parse(self.ubuntu_20_4_last_F, quiet=True), self.ubuntu_20_4_last_F_json)

    def test_last_wF_centos_7_7(self):
        """
        Test 'last -wF' on Centos 7.7
        """
        self.assertEqual(jc.parsers.last.parse(self.centos_7_7_last_wF, quiet=True), self.centos_7_7_last_wF_json)


if __name__ == '__main__':
    unittest.main()
