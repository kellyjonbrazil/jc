import os
import json
import unittest
import jc.parsers.crontab

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/crontab.out'), 'r') as f:
            self.centos_7_7_crontab = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/crontab.out'), 'r') as f:
            self.ubuntu_18_4_crontab = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/crontab.json'), 'r') as f:
            self.centos_7_7_crontab_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/crontab.json'), 'r') as f:
            self.ubuntu_18_4_crontab_json = json.loads(f.read())

    def test_crontab_centos_7_7(self):
        """
        Test 'crontab' on Centos 7.7
        """
        self.assertEqual(jc.parsers.crontab.parse(self.centos_7_7_crontab, quiet=True), self.centos_7_7_crontab_json)

    def test_crontab_ubuntu_18_4(self):
        """
        Test 'crontab' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.crontab.parse(self.ubuntu_18_4_crontab, quiet=True), self.ubuntu_18_4_crontab_json)


if __name__ == '__main__':
    unittest.main()
