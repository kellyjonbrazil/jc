import os
import json
import unittest
import jc.parsers.crontab_u

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/crontab-u.out'), 'r') as f:
            self.ubuntu_18_4_crontab_u = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/crontab-u.out'), 'r') as f:
            self.centos_7_7_crontab_u = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/crontab-u.json'), 'r') as f:
            self.ubuntu_18_4_crontab_u_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/crontab-u.json'), 'r') as f:
            self.centos_7_7_crontab_u_json = json.loads(f.read())

    def test_crontab_u_ubuntu_18_4(self):
        """
        Test 'crontab' on Ubuntu 18.4 (has a user field)
        """
        self.assertEqual(jc.parsers.crontab_u.parse(self.ubuntu_18_4_crontab_u, quiet=True), self.ubuntu_18_4_crontab_u_json)

    def test_crontab_u_centos_7_7(self):
        """
        Test 'crontab' on Centos 7.7 (has a user field)
        """
        self.assertEqual(jc.parsers.crontab_u.parse(self.centos_7_7_crontab_u, quiet=True), self.centos_7_7_crontab_u_json)


if __name__ == '__main__':
    unittest.main()
