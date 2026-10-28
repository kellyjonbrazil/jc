import os
import unittest
import json
import jc.parsers.mpstat
from jc.exceptions import ParseError

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # new input/output fixtures
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mpstat-linux-stray-line.out'), 'r', encoding='utf-8') as f:
        generic_mpstat_stray_line = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mpstat-many-cpus.out'), 'r', encoding='utf-8') as f:
        generic_mpstat_many_cpus = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mpstat-many-cpus.json'), 'r', encoding='utf-8') as f:
        generic_mpstat_many_cpus_json = json.loads(f.read())


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


    def test_mpstat_many_cpus(self):
        """
        Test 'mpstat -P ALL' with many CPUs and repeated samples
        """
        self.assertEqual(jc.parsers.mpstat.parse(self.generic_mpstat_many_cpus, quiet=True), self.generic_mpstat_many_cpus_json)

    def test_mpstat_stray_line(self):
        """
        Test 'mpstat' with a line that is not mpstat data after the header. Should raise ParseError
        """
        self.assertRaises(ParseError, jc.parsers.mpstat.parse, self.generic_mpstat_stray_line, quiet=True)

    def test_mpstat_ragged_rows(self):
        """
        Test 'mpstat' rows with fewer or more fields than the header. Each should raise ParseError
        """
        for bad in ('12:00:02 AM  all   1.50', '12:00:02 AM    0   2.50   3.50   4.50', 'random'):
            self.assertRaises(ParseError, jc.parsers.mpstat.parse, '12:00:01 AM  CPU    %usr   %nice\n' + bad, quiet=True)

    def test_mpstat_whitespace_only_line(self):
        """
        Test 'mpstat' with whitespace-only lines after the header. They are skipped like blank lines
        """
        data = '12:00:01 AM  CPU    %usr   %nice\n12:00:02 AM  all   1.50   2.50\n   \n\t\n12:00:02 AM    0   3.50   4.50\n'
        self.assertEqual([d['cpu'] for d in jc.parsers.mpstat.parse(data, quiet=True)], ['all', '0'])


if __name__ == '__main__':
    unittest.main()
