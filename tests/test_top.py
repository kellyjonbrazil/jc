import os
import unittest
import json
import jc.parsers.top

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/top-b-n3.out'), 'r', encoding='utf-8') as f:
        centos_7_7_top_b_n3 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/top-b-n1-gib.out'), 'r', encoding='utf-8') as f:
        centos_7_7_top_b_n1_gib = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/top-b-n1-gib-allfields-w.out'), 'r', encoding='utf-8') as f:
        centos_7_7_top_b_n1_gib_allfields_w = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.10/top-b-n1.out'), 'r', encoding='utf-8') as f:
        ubuntu_20_10_top_b_n1 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.10/top-b-allfields.out'), 'r', encoding='utf-8') as f:
        ubuntu_20_10_top_b_allfields = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/top-b-n3.json'), 'r', encoding='utf-8') as f:
        centos_7_7_top_b_n3_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/top-b-n1-gib.json'), 'r', encoding='utf-8') as f:
        centos_7_7_top_b_n1_gib_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/top-b-n1-gib-allfields-w.json'), 'r', encoding='utf-8') as f:
        centos_7_7_top_b_n1_gib_allfields_w_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.10/top-b-n1.json'), 'r', encoding='utf-8') as f:
        ubuntu_20_10_top_b_n1_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.10/top-b-allfields.json'), 'r', encoding='utf-8') as f:
        ubuntu_20_10_top_b_allfields_json = json.loads(f.read())


    def test_top_nodata(self):
        """
        Test 'top -b' with no data
        """
        self.assertEqual(jc.parsers.top.parse('', quiet=True), [])

    def test_top_centos_7_7(self):
        """
        Test 'top -b -n 3' on Centos 7.7
        """
        self.assertEqual(jc.parsers.top.parse(self.centos_7_7_top_b_n3, quiet=True), self.centos_7_7_top_b_n3_json)

    def test_top_gib_centos_7_7(self):
        """
        Test 'top -b -n 1' with units as GiB on Centos 7.7
        """
        self.assertEqual(jc.parsers.top.parse(self.centos_7_7_top_b_n1_gib, quiet=True), self.centos_7_7_top_b_n1_gib_json)

    def test_top_gib_allfields_wide_centos_7_7(self):
        """
        Test 'top -b -n 1' with units as GiB, all fields selected, and wide output on Centos 7.7
        """
        self.assertEqual(jc.parsers.top.parse(self.centos_7_7_top_b_n1_gib_allfields_w, quiet=True), self.centos_7_7_top_b_n1_gib_allfields_w_json)

    def test_top_ubuntu_20_10(self):
        """
        Test 'top -b -n 1' with units as MiB on Ubuntu 20.10
        """
        self.assertEqual(jc.parsers.top.parse(self.ubuntu_20_10_top_b_n1, quiet=True), self.ubuntu_20_10_top_b_n1_json)

    def test_top_allfields_ubuntu_20_10(self):
        """
        Test 'top -b -n 1' with units as MiB and all fields on Ubuntu 20.10
        """
        self.assertEqual(jc.parsers.top.parse(self.ubuntu_20_10_top_b_allfields, quiet=True), self.ubuntu_20_10_top_b_allfields_json)


if __name__ == '__main__':
    unittest.main()
