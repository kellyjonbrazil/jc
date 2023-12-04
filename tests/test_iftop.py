import os
import unittest
import json
import jc.parsers.iftop

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.10/iftop-b-n1.out'), 'r', encoding='utf-8') as f:
        ubuntu_20_10_iftop_b_n1 = f.read()

    # with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.10/iftop-b-n3.out'), 'r', encoding='utf-8') as f:
    #     centos_7_7_iftop_b_n3 = f.read()

    # with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.10/iftop-b-allfields.out'), 'r', encoding='utf-8') as f:
    #     ubuntu_20_10_iftop_b_allfields = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.10/iftop-b-n1.json'), 'r', encoding='utf-8') as f:
        ubuntu_20_10_iftop_b_n1_json = json.loads(f.read())

    # with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.10/iftop-b-n3.json'), 'r', encoding='utf-8') as f:
    #     centos_7_7_iftop_b_n3_json = f.read()

    # with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.10/iftop-b-allfields.json'), 'r', encoding='utf-8') as f:
    #     ubuntu_20_10_iftop_b_allfields_json = json.loads(f.read())


    def test_iftop_nodata(self):
        """
        Test 'iftop -b' with no data
        """
        self.assertEqual(jc.parsers.iftop.parse('', quiet=True), [])

    def test_iftop_ubuntu_20_10(self):
        """
        Test 'iftop -b -n 1' with units as MiB on Ubuntu 20.10
        """
        self.assertEqual(jc.parsers.iftop.parse(self.ubuntu_20_10_iftop_b_n1, quiet=True), self.ubuntu_20_10_iftop_b_n1_json)
    
    # def test_iftop_multiple_runs_ubuntu_20_10(self):
    #     """
    #     Test 'iftop -b -n 3' with units as MiB on Ubuntu 20.10
    #     """
    #     self.assertEqual(jc.parsers.iftop.parse(self.ubuntu_20_10_iftop_b_n3, quiet=True), self.ubuntu_20_10_iftop_b_n3_json)


    # def test_iftop_allfields_ubuntu_20_10(self):
    #     """
    #     Test 'iftop -b -n 1' with units as MiB and all fields on Ubuntu 20.10
    #     """
    #     self.assertEqual(jc.parsers.iftop.parse(self.ubuntu_20_10_iftop_b_allfields, quiet=True), self.ubuntu_20_10_iftop_b_allfields_json)


if __name__ == '__main__':
    unittest.main()
