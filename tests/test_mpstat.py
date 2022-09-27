import os
import unittest
import json
import jc.parsers.mpstat

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/mpstat.out'), 'r', encoding='utf-8') as f:
        centos_7_7_mpstat = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/mpstat-A.out'), 'r', encoding='utf-8') as f:
        centos_7_7_mpstat_A = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/mpstat-A-2-5.out'), 'r', encoding='utf-8') as f:
        centos_7_7_mpstat_A_2_5 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/mpstat-A.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_mpstat_A = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/mpstat.json'), 'r', encoding='utf-8') as f:
        centos_7_7_mpstat_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/mpstat-A.json'), 'r', encoding='utf-8') as f:
        centos_7_7_mpstat_A_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/mpstat-A-2-5.json'), 'r', encoding='utf-8') as f:
        centos_7_7_mpstat_A_2_5_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/mpstat-A.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_mpstat_A_json = json.loads(f.read())


    def test_mpstat_nodata(self):
        """
        Test 'mpstat' with no data
        """
        self.assertEqual(jc.parsers.mpstat.parse('', quiet=True), [])

    def test_mpstat_centos_7_7(self):
        """
        Test 'mpstat' on Centos 7.7
        """
        self.assertEqual(jc.parsers.mpstat.parse(self.centos_7_7_mpstat, quiet=True), self.centos_7_7_mpstat_json)

    def test_mpstat_A_centos_7_7(self):
        """
        Test 'mpstat -A' on Centos 7.7
        """
        self.assertEqual(jc.parsers.mpstat.parse(self.centos_7_7_mpstat_A, quiet=True), self.centos_7_7_mpstat_A_json)

    def test_mpstat_A_2_5_centos_7_7(self):
        """
        Test 'mpstat -A 2 5' on Centos 7.7
        """
        self.assertEqual(jc.parsers.mpstat.parse(self.centos_7_7_mpstat_A_2_5, quiet=True), self.centos_7_7_mpstat_A_2_5_json)

    def test_mpstat_A_ubuntu_18_4(self):
        """
        Test 'mpstat -A' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.mpstat.parse(self.ubuntu_18_4_mpstat_A, quiet=True), self.ubuntu_18_4_mpstat_A_json)


if __name__ == '__main__':
    unittest.main()
