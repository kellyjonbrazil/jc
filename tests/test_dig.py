import os
import json
import unittest
import jc.parsers.dig

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/dig.out'), 'r', encoding='utf-8') as f:
            self.centos_7_7_dig = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/dig.out'), 'r', encoding='utf-8') as f:
            self.ubuntu_18_4_dig = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/dig-x.out'), 'r', encoding='utf-8') as f:
            self.centos_7_7_dig_x = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/dig-x.out'), 'r', encoding='utf-8') as f:
            self.ubuntu_18_4_dig_x = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/dig-aaaa.out'), 'r', encoding='utf-8') as f:
            self.centos_7_7_dig_aaaa = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/dig-aaaa.out'), 'r', encoding='utf-8') as f:
            self.ubuntu_18_4_dig_aaaa = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/dig-axfr.out'), 'r', encoding='utf-8') as f:
            self.centos_7_7_dig_axfr = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/dig-axfr.out'), 'r', encoding='utf-8') as f:
            self.ubuntu_18_4_dig_axfr = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/dig.out'), 'r', encoding='utf-8') as f:
            self.osx_10_11_6_dig = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/dig-x.out'), 'r', encoding='utf-8') as f:
            self.osx_10_11_6_dig_x = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/dig-aaaa.out'), 'r', encoding='utf-8') as f:
            self.osx_10_11_6_dig_aaaa = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/dig.out'), 'r', encoding='utf-8') as f:
            self.osx_10_14_6_dig = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/dig-x.out'), 'r', encoding='utf-8') as f:
            self.osx_10_14_6_dig_x = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/dig-aaaa.out'), 'r', encoding='utf-8') as f:
            self.osx_10_14_6_dig_aaaa = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/dig-axfr.out'), 'r', encoding='utf-8') as f:
            self.osx_10_14_6_dig_axfr = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/dig.json'), 'r', encoding='utf-8') as f:
            self.centos_7_7_dig_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/dig.json'), 'r', encoding='utf-8') as f:
            self.ubuntu_18_4_dig_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/dig-x.json'), 'r', encoding='utf-8') as f:
            self.centos_7_7_dig_x_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/dig-x.json'), 'r', encoding='utf-8') as f:
            self.ubuntu_18_4_dig_x_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/dig-aaaa.json'), 'r', encoding='utf-8') as f:
            self.centos_7_7_dig_aaaa_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/dig-aaaa.json'), 'r', encoding='utf-8') as f:
            self.ubuntu_18_4_dig_aaaa_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/dig-axfr.json'), 'r', encoding='utf-8') as f:
            self.centos_7_7_dig_axfr_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/dig-axfr.json'), 'r', encoding='utf-8') as f:
            self.ubuntu_18_4_dig_axfr_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/dig.json'), 'r', encoding='utf-8') as f:
            self.osx_10_11_6_dig_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/dig-x.json'), 'r', encoding='utf-8') as f:
            self.osx_10_11_6_dig_x_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/dig-aaaa.json'), 'r', encoding='utf-8') as f:
            self.osx_10_11_6_dig_aaaa_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/dig.json'), 'r', encoding='utf-8') as f:
            self.osx_10_14_6_dig_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/dig-x.json'), 'r', encoding='utf-8') as f:
            self.osx_10_14_6_dig_x_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/dig-aaaa.json'), 'r', encoding='utf-8') as f:
            self.osx_10_14_6_dig_aaaa_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/dig-axfr.json'), 'r', encoding='utf-8') as f:
            self.osx_10_14_6_dig_axfr_json = json.loads(f.read())

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

    def test_dig_axfr_centos_7_7(self):
        """
        Test 'dig axfr' on Centos 7.7
        """
        self.assertEqual(jc.parsers.dig.parse(self.centos_7_7_dig_axfr, quiet=True), self.centos_7_7_dig_axfr_json)

    def test_dig_axfr_ubuntu_18_4(self):
        """
        Test 'dig axfr' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.dig.parse(self.ubuntu_18_4_dig_axfr, quiet=True), self.ubuntu_18_4_dig_axfr_json)

    def test_dig_osx_10_11_6(self):
        """
        Test 'dig' on OSX 10.11.6
        """
        self.assertEqual(jc.parsers.dig.parse(self.osx_10_11_6_dig, quiet=True), self.osx_10_11_6_dig_json)

    def test_dig_x_osx_10_11_6(self):
        """
        Test 'dig -x' on OSX 10.11.6
        """
        self.assertEqual(jc.parsers.dig.parse(self.osx_10_11_6_dig_x, quiet=True), self.osx_10_11_6_dig_x_json)

    def test_dig_aaaa_osx_10_11_6(self):
        """
        Test 'dig -aaaa' on OSX 10.11.6
        """
        self.assertEqual(jc.parsers.dig.parse(self.osx_10_11_6_dig_aaaa, quiet=True), self.osx_10_11_6_dig_aaaa_json)

    def test_dig_osx_10_14_6(self):
        """
        Test 'dig' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.dig.parse(self.osx_10_14_6_dig, quiet=True), self.osx_10_14_6_dig_json)

    def test_dig_x_osx_10_14_6(self):
        """
        Test 'dig -x' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.dig.parse(self.osx_10_14_6_dig_x, quiet=True), self.osx_10_14_6_dig_x_json)

    def test_dig_aaaa_osx_10_14_6(self):
        """
        Test 'dig -aaaa' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.dig.parse(self.osx_10_14_6_dig_aaaa, quiet=True), self.osx_10_14_6_dig_aaaa_json)

    def test_dig_axfr_osx_10_14_6(self):
        """
        Test 'dig axfr' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.dig.parse(self.osx_10_14_6_dig_axfr, quiet=True), self.osx_10_14_6_dig_axfr_json)


if __name__ == '__main__':
    unittest.main()
