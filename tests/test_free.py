import os
import json
import unittest
import jc.parsers.free

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/free.out'), 'r') as f:
            self.centos_7_7_free = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/free.out'), 'r') as f:
            self.ubuntu_18_4_free = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/free-h.out'), 'r') as f:
            self.centos_7_7_free_h = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/free-h.out'), 'r') as f:
            self.ubuntu_18_4_free_h = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/free.json'), 'r') as f:
            self.centos_7_7_free_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/free.json'), 'r') as f:
            self.ubuntu_18_4_free_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/free-h.json'), 'r') as f:
            self.centos_7_7_free_h_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/free-h.json'), 'r') as f:
            self.ubuntu_18_4_free_h_json = json.loads(f.read())

    def test_free_centos_7_7(self):
        """
        Test 'free' on Centos 7.7
        """
        self.assertEqual(jc.parsers.free.parse(self.centos_7_7_free, quiet=True), self.centos_7_7_free_json)

    def test_free_ubuntu_18_4(self):
        """
        Test 'free' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.free.parse(self.ubuntu_18_4_free, quiet=True), self.ubuntu_18_4_free_json)

    def test_free_h_centos_7_7(self):
        """
        Test 'free -h' on Centos 7.7
        """
        self.assertEqual(jc.parsers.free.parse(self.centos_7_7_free_h, quiet=True), self.centos_7_7_free_h_json)

    def test_free_h_ubuntu_18_4(self):
        """
        Test 'free -h' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.free.parse(self.ubuntu_18_4_free_h, quiet=True), self.ubuntu_18_4_free_h_json)


if __name__ == '__main__':
    unittest.main()
