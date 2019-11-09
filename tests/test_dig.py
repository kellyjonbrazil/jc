import os
import json
import unittest
import jc.parsers.dig

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/dig.out'), 'r') as f:
            self.centos_7_7_dig = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/dig.out'), 'r') as f:
            self.ubuntu_18_4_dig = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/dig-x.out'), 'r') as f:
            self.centos_7_7_dig_x = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/dig-x.out'), 'r') as f:
            self.ubuntu_18_4_dig_x = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/dig-aaaa.out'), 'r') as f:
            self.centos_7_7_dig_aaaa = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/dig-aaaa.out'), 'r') as f:
            self.ubuntu_18_4_dig_aaaa = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/dig.json'), 'r') as f:
            self.centos_7_7_dig_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/dig.json'), 'r') as f:
            self.ubuntu_18_4_dig_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/dig-x.json'), 'r') as f:
            self.centos_7_7_dig_x_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/dig-x.json'), 'r') as f:
            self.ubuntu_18_4_dig_x_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/dig-aaaa.json'), 'r') as f:
            self.centos_7_7_dig_aaaa_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/dig-aaaa.json'), 'r') as f:
            self.ubuntu_18_4_dig_aaaa_json = json.loads(f.read())

    def test_dig_centos_7_7(self):
        """
        Test 'dig' on Centos 7.7
        """
        self.assertEqual(jc.parsers.dig.parse(self.centos_7_7_dig, quiet=True), self.centos_7_7_dig_json)

    def test_dig_ubuntu_18_4(self):
        """
        Test 'dig' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.dig.parse(self.ubuntu_18_4_dig, quiet=True), self.ubuntu_18_4_dig_json)

    def test_dig_x_centos_7_7(self):
        """
        Test 'dig -x' on Centos 7.7
        """
        self.assertEqual(jc.parsers.dig.parse(self.centos_7_7_dig_x, quiet=True), self.centos_7_7_dig_x_json)

    def test_dig_x_ubuntu_18_4(self):
        """
        Test 'dig -x' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.dig.parse(self.ubuntu_18_4_dig_x, quiet=True), self.ubuntu_18_4_dig_x_json)

    def test_dig_aaaa_centos_7_7(self):
        """
        Test 'dig AAAA' on Centos 7.7
        """
        self.assertEqual(jc.parsers.dig.parse(self.centos_7_7_dig_aaaa, quiet=True), self.centos_7_7_dig_aaaa_json)

    def test_dig_aaaa_ubuntu_18_4(self):
        """
        Test 'dig AAAA' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.dig.parse(self.ubuntu_18_4_dig_aaaa, quiet=True), self.ubuntu_18_4_dig_aaaa_json)


if __name__ == '__main__':
    unittest.main()
