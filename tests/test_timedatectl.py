import os
import unittest
import json
import jc.parsers.timedatectl

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/timedatectl.out'), 'r', encoding='utf-8') as f:
            self.centos_7_7_timedatectl = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/timedatectl.out'), 'r', encoding='utf-8') as f:
            self.ubuntu_18_4_timedatectl = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/timedatectl.json'), 'r', encoding='utf-8') as f:
            self.centos_7_7_timedatectl_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/timedatectl.json'), 'r', encoding='utf-8') as f:
            self.ubuntu_18_4_timedatectl_json = json.loads(f.read())

    def test_timedatectl_centos_7_7(self):
        """
        Test 'timedatectl' on Centos 7.7
        """
        self.assertEqual(jc.parsers.timedatectl.parse(self.centos_7_7_timedatectl, quiet=True), self.centos_7_7_timedatectl_json)

    def test_timedatectl_ubuntu_18_4(self):
        """
        Test 'timedatectl' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.timedatectl.parse(self.ubuntu_18_4_timedatectl, quiet=True), self.ubuntu_18_4_timedatectl_json)


if __name__ == '__main__':
    unittest.main()
