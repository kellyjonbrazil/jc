import os
import json
import unittest
from jc.exceptions import ParseError
import jc.parsers.mpstat_s

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

# To create streaming output use:
# $ cat mpstat.out | jc --mpstat-s | jello -c > mpstat-streaming.json


class MyTests(unittest.TestCase):

    # new input/output fixtures
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mpstat-linux-stray-line.out'), 'r', encoding='utf-8') as f:
        generic_mpstat_stray_line = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mpstat-many-cpus.out'), 'r', encoding='utf-8') as f:
        generic_mpstat_many_cpus = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/mpstat-many-cpus-streaming.json'), 'r', encoding='utf-8') as f:
        generic_mpstat_many_cpus_streaming_json = json.loads(f.read())


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
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/mpstat-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_mpstat_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/mpstat-A-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_mpstat_A_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/mpstat-A-2-5-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_mpstat_A_2_5_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/mpstat-A-streaming.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_mpstat_A_streaming_json = json.loads(f.read())


    def test_mpstat_s_nodata(self):
        """
        Test 'mpstat' with no data
        """
        self.assertEqual(list(jc.parsers.mpstat_s.parse([], quiet=True)), [])

    def test_mpstat_s_centos_7_7(self):
        """
        Test 'mpstat' on Centos 7.7
        """
        self.assertEqual(list(jc.parsers.mpstat_s.parse(self.centos_7_7_mpstat.splitlines(), quiet=True)), self.centos_7_7_mpstat_streaming_json)

    def test_mpstat_s_A_centos_7_7(self):
        """
        Test 'mpstat -A' on Centos 7.7
        """
        self.assertEqual(list(jc.parsers.mpstat_s.parse(self.centos_7_7_mpstat_A.splitlines(), quiet=True)), self.centos_7_7_mpstat_A_streaming_json)

    def test_mpstat_s_A_2_5_centos_7_7(self):
        """
        Test 'mpstat -A 2 5' on Centos 7.7
        """
        self.assertEqual(list(jc.parsers.mpstat_s.parse(self.centos_7_7_mpstat_A_2_5.splitlines(), quiet=True)), self.centos_7_7_mpstat_A_2_5_streaming_json)

    def test_mpstat_s_A_ubuntu_18_4(self):
        """
        Test 'mpstat -A' on Ubuntu 18.4
        """
        self.assertEqual(list(jc.parsers.mpstat_s.parse(self.ubuntu_18_4_mpstat_A.splitlines(), quiet=True)), self.ubuntu_18_4_mpstat_A_streaming_json)


    def test_mpstat_s_many_cpus(self):
        """
        Test 'mpstat -P ALL' with many CPUs and repeated samples
        """
        self.assertEqual(list(jc.parsers.mpstat_s.parse(self.generic_mpstat_many_cpus.splitlines(), quiet=True)), self.generic_mpstat_many_cpus_streaming_json)

    def test_mpstat_s_stray_line(self):
        """
        Test 'mpstat' with a line that is not mpstat data after the header. Should raise ParseError
        """
        self.assertRaises(ParseError, list, jc.parsers.mpstat_s.parse(self.generic_mpstat_stray_line.splitlines(), quiet=True))

    def test_mpstat_s_stray_line_ignore_exceptions(self):
        """
        Test 'mpstat' with a line that is not mpstat data after the header. Should yield an error record for that line and continue
        """
        result = list(jc.parsers.mpstat_s.parse(self.generic_mpstat_stray_line.splitlines(), quiet=True, ignore_exceptions=True))
        self.assertEqual([r.get('cpu') for r in result], ['all', None, 'all'])
        self.assertEqual(result[1], {"_jc_meta": {"success": False, "error": "ParseError: Not mpstat data", "line": "cp: cannot stat 'backup.tar': No such file or directory"}})

    def test_mpstat_s_ragged_rows(self):
        """
        Test 'mpstat' rows with fewer or more fields than the header. Each should raise ParseError and a good row after it still parses
        """
        header = '12:00:01 AM  CPU    %usr   %nice'
        for bad in ('12:00:02 AM  all   1.50', '12:00:02 AM    0   2.50   3.50   4.50', 'random'):
            with self.assertRaises(ParseError):
                list(jc.parsers.mpstat_s.parse([header, bad], quiet=True))

        result = list(jc.parsers.mpstat_s.parse([header, '12:00:02 AM  all   1.50', '12:00:02 AM    0   2.50   3.50\r'], quiet=True, ignore_exceptions=True))
        self.assertEqual(result[1], {"cpu": "0", "percent_usr": 2.5, "percent_nice": 3.5, "type": "cpu", "time": "12:00:02 AM", "_jc_meta": {"success": True}})
        self.assertEqual(len(result), 2)


if __name__ == '__main__':
    unittest.main()
