import os
import json
import unittest
import jc.parsers.env

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/env.out'), 'r') as f:
            self.centos_7_7_env = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/env.out'), 'r') as f:
            self.ubuntu_18_4_env = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/env.json'), 'r') as f:
            self.centos_7_7_env_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/env.json'), 'r') as f:
            self.ubuntu_18_4_env_json = json.loads(f.read())

    def test_env_centos_7_7(self):
        """
        Test 'env' on Centos 7.7
        """
        self.assertEqual(jc.parsers.env.parse(self.centos_7_7_env, quiet=True), self.centos_7_7_env_json)

    def test_env_ubuntu_18_4(self):
        """
        Test 'env' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.env.parse(self.ubuntu_18_4_env, quiet=True), self.ubuntu_18_4_env_json)


if __name__ == '__main__':
    unittest.main()
