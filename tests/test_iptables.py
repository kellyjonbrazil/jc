import os
import json
import unittest
import jc.parsers.iptables

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iptables-filter.out'), 'r') as f:
            self.centos_7_7_iptables_filter = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/iptables-filter.out'), 'r') as f:
            self.ubuntu_18_4_iptables_filter = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iptables-filter-line-numbers.out'), 'r') as f:
            self.centos_7_7_iptables_filter_line_numbers = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/iptables-filter-line-numbers.out'), 'r') as f:
            self.ubuntu_18_4_iptables_filter_line_numbers = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iptables-filter-nv.out'), 'r') as f:
            self.centos_7_7_iptables_filter_nv = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/iptables-filter-nv.out'), 'r') as f:
            self.ubuntu_18_4_iptables_filter_nv = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iptables-mangle.out'), 'r') as f:
            self.centos_7_7_iptables_mangle = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/iptables-mangle.out'), 'r') as f:
            self.ubuntu_18_4_iptables_mangle = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iptables-nat.out'), 'r') as f:
            self.centos_7_7_iptables_nat = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/iptables-nat.out'), 'r') as f:
            self.ubuntu_18_4_iptables_nat = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iptables-raw.out'), 'r') as f:
            self.centos_7_7_iptables_raw = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/iptables-raw.out'), 'r') as f:
            self.ubuntu_18_4_iptables_raw = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iptables-filter.json'), 'r') as f:
            self.centos_7_7_iptables_filter_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/iptables-filter.json'), 'r') as f:
            self.ubuntu_18_4_iptables_filter_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iptables-filter-line-numbers.json'), 'r') as f:
            self.centos_7_7_iptables_filter_line_numbers_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/iptables-filter-line-numbers.json'), 'r') as f:
            self.ubuntu_18_4_iptables_filter_line_numbers_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iptables-filter-nv.json'), 'r') as f:
            self.centos_7_7_iptables_filter_nv_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/iptables-filter-nv.json'), 'r') as f:
            self.ubuntu_18_4_iptables_filter_nv_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iptables-mangle.json'), 'r') as f:
            self.centos_7_7_iptables_mangle_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/iptables-mangle.json'), 'r') as f:
            self.ubuntu_18_4_iptables_mangle_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iptables-nat.json'), 'r') as f:
            self.centos_7_7_iptables_nat_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/iptables-nat.json'), 'r') as f:
            self.ubuntu_18_4_iptables_nat_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iptables-raw.json'), 'r') as f:
            self.centos_7_7_iptables_raw_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/iptables-raw.json'), 'r') as f:
            self.ubuntu_18_4_iptables_raw_json = json.loads(f.read())

    def test_iptables_filter_centos_7_7(self):
        """
        Test 'sudo iptables -L -t filter' on Centos 7.7
        """
        self.assertEqual(jc.parsers.iptables.parse(self.centos_7_7_iptables_filter, quiet=True), self.centos_7_7_iptables_filter_json)

    def test_iptables_filter_ubuntu_18_4(self):
        """
        Test 'sudo iptables -L -t filter' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.iptables.parse(self.ubuntu_18_4_iptables_filter, quiet=True), self.ubuntu_18_4_iptables_filter_json)

    def test_iptables_filter_line_numbers_centos_7_7(self):
        """
        Test 'sudo iptables --line-numbers -L -t filter' on Centos 7.7
        """
        self.assertEqual(jc.parsers.iptables.parse(self.centos_7_7_iptables_filter_line_numbers, quiet=True), self.centos_7_7_iptables_filter_line_numbers_json)

    def test_iptables_filter_line_numbers_ubuntu_18_4(self):
        """
        Test 'sudo iptables --line-numbers -L -t filter' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.iptables.parse(self.ubuntu_18_4_iptables_filter_line_numbers, quiet=True), self.ubuntu_18_4_iptables_filter_line_numbers_json)

    def test_iptables_filter_nv_centos_7_7(self):
        """
        Test 'sudo iptables -nvL -t filter' on Centos 7.7
        """
        self.assertEqual(jc.parsers.iptables.parse(self.centos_7_7_iptables_filter_nv, quiet=True), self.centos_7_7_iptables_filter_nv_json)

    def test_iptables_filter_nv_ubuntu_18_4(self):
        """
        Test 'sudo iptables -nvL -t filter' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.iptables.parse(self.ubuntu_18_4_iptables_filter_nv, quiet=True), self.ubuntu_18_4_iptables_filter_nv_json)

    def test_iptables_mangle_centos_7_7(self):
        """
        Test 'sudo iptables -L -t mangle' on Centos 7.7
        """
        self.assertEqual(jc.parsers.iptables.parse(self.centos_7_7_iptables_mangle, quiet=True), self.centos_7_7_iptables_mangle_json)

    def test_iptables_mangle_ubuntu_18_4(self):
        """
        Test 'sudo iptables -L -t mangle' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.iptables.parse(self.ubuntu_18_4_iptables_mangle, quiet=True), self.ubuntu_18_4_iptables_mangle_json)

    def test_iptables_nat_centos_7_7(self):
        """
        Test 'sudo iptables -L -t nat' on Centos 7.7
        """
        self.assertEqual(jc.parsers.iptables.parse(self.centos_7_7_iptables_nat, quiet=True), self.centos_7_7_iptables_nat_json)

    def test_iptables_nat_ubuntu_18_4(self):
        """
        Test 'sudo iptables -L -t nat' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.iptables.parse(self.ubuntu_18_4_iptables_nat, quiet=True), self.ubuntu_18_4_iptables_nat_json)

    def test_iptables_raw_centos_7_7(self):
        """
        Test 'sudo iptables -L -t raw' on Centos 7.7
        """
        self.assertEqual(jc.parsers.iptables.parse(self.centos_7_7_iptables_raw, quiet=True), self.centos_7_7_iptables_raw_json)

    def test_iptables_raw_ubuntu_18_4(self):
        """
        Test 'sudo iptables -L -t raw' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.iptables.parse(self.ubuntu_18_4_iptables_raw, quiet=True), self.ubuntu_18_4_iptables_raw_json)


if __name__ == '__main__':
    unittest.main()
