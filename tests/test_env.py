import os
import unittest
import jc.parsers.env

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/env.out'), 'r') as f:
            self.centos_7_7_env = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/env.out'), 'r') as f:
            self.ubuntu_18_4_env = f.read()

    def test_env_centos_7_7(self):
        """
        Test 'env' on Centos 7.7
        """
        self.assertEqual(jc.parsers.env.parse(self.centos_7_7_env)['SSH_CONNECTION'], '192.168.71.1 58727 192.168.71.137 22')

    def test_env_ubuntu_18_4(self):
        """
        Test 'env' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.env.parse(self.ubuntu_18_4_env)['SSH_CONNECTION'], '192.168.71.1 65159 192.168.71.131 22')


if __name__ == '__main__':
    unittest.main()
