import os
import unittest
import json
import jc.parsers.pidstat
from jc.exceptions import ParseError

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/pidstat.out'), 'r', encoding='utf-8') as f:
        centos_7_7_pidstat = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/pidstat-hl.out'), 'r', encoding='utf-8') as f:
        centos_7_7_pidstat_hl = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/pidstat-hdlrsuw.out'), 'r', encoding='utf-8') as f:
        centos_7_7_pidstat_hdlrsuw = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/pidstat-hdlrsuw-2-5.out'), 'r', encoding='utf-8') as f:
        centos_7_7_pidstat_hdlrsuw_2_5 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/pidstat-ht.out'), 'r', encoding='utf-8') as f:
        generic_pidstat_ht = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/pidstat-hl.json'), 'r', encoding='utf-8') as f:
        centos_7_7_pidstat_hl_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/pidstat-hdlrsuw.json'), 'r', encoding='utf-8') as f:
        centos_7_7_pidstat_hdlrsuw_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/pidstat-hdlrsuw-2-5.json'), 'r', encoding='utf-8') as f:
        centos_7_7_pidstat_hdlrsuw_2_5_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/pidstat-ht.json'), 'r', encoding='utf-8') as f:
        generic_pidstat_ht_json = json.loads(f.read())


    def test_pidstat_nodata(self):
        """
        Test 'pidstat' with no data
        """
        self.assertEqual(jc.parsers.pidstat.parse('', quiet=True), [])

    def test_pidstat(self):
        """
        Test 'pidstat' without -h... should raise ParseError
        """
        self.assertRaises(ParseError, jc.parsers.pidstat.parse, self.centos_7_7_pidstat, quiet=True)

    def test_pidstat_hl_centos_7_7(self):
        """
        Test 'pidstat -hl' on Centos 7.7
        """
        self.assertEqual(jc.parsers.pidstat.parse(self.centos_7_7_pidstat_hl, quiet=True), self.centos_7_7_pidstat_hl_json)

    def test_pidstat_hdlrsuw_centos_7_7(self):
        """
        Test 'pidstat -hdlrsuw' on Centos 7.7
        """
        self.assertEqual(jc.parsers.pidstat.parse(self.centos_7_7_pidstat_hdlrsuw, quiet=True), self.centos_7_7_pidstat_hdlrsuw_json)

    def test_pidstat_hdlrsuw_2_5_centos_7_7(self):
        """
        Test 'pidstat -hdlrsuw 2 5' on Centos 7.7
        """
        self.assertEqual(jc.parsers.pidstat.parse(self.centos_7_7_pidstat_hdlrsuw_2_5, quiet=True), self.centos_7_7_pidstat_hdlrsuw_2_5_json)

    def test_pidstat_ht(self):
        """
        Test 'pidstat -hT'
        """
        self.assertEqual(jc.parsers.pidstat.parse(self.generic_pidstat_ht, quiet=True), self.generic_pidstat_ht_json)


if __name__ == '__main__':
    unittest.main()
