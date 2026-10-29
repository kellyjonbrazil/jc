import os
import unittest
import json
import jc.parsers.pidstat
from jc.exceptions import ParseError

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # new input fixtures
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/pidstat-linux-stray-line.out'), 'r', encoding='utf-8') as f:
        generic_pidstat_stray_line = f.read()

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


    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/pidstat-hl-hash-line.out'), 'r', encoding='utf-8') as f:
        generic_pidstat_hl_hash_line = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/pidstat-hl-hash-line.json'), 'r', encoding='utf-8') as f:
        generic_pidstat_hl_hash_line_json = json.loads(f.read())

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

    def test_pidstat_hl_hash_line(self):
        """
        Test 'pidstat -hl' with a '#' line that is not the pidstat header
        """
        self.assertEqual(jc.parsers.pidstat.parse(self.generic_pidstat_hl_hash_line, quiet=True), self.generic_pidstat_hl_hash_line_json)


    def test_pidstat_stray_line(self):
        """
        Test 'pidstat -hl' with a line that is not pidstat data after the header. Should raise ParseError
        """
        self.assertRaises(ParseError, jc.parsers.pidstat.parse, self.generic_pidstat_stray_line, quiet=True)

    def test_pidstat_ragged_rows(self):
        """
        Test 'pidstat' rows with fewer or more fields than the header. Fewer should raise ParseError, more go into the last column
        """
        header = '# Time UID PID Command\n'
        for bad in ('1646857494   0', 'random'):
            self.assertRaises(ParseError, jc.parsers.pidstat.parse, header + bad, quiet=True)

        data = header + '  1646857494   0   2 kthreadd\n  1646857494   0   3\n   \n  1646857494   0   4 a command with spaces\n'
        expected = [
            {"time": 1646857494, "uid": 0, "pid": 2, "command": "kthreadd"},
            {"time": 1646857494, "uid": 0, "pid": 3},
            {"time": 1646857494, "uid": 0, "pid": 4, "command": "a command with spaces"}
        ]
        self.assertEqual(jc.parsers.pidstat.parse(data, quiet=True), expected)

    def test_pidstat_line_break_chars_in_command(self):
        """
        Test 'pidstat -hl' with CR and other line-break characters inside the command. Should stay in one row
        """
        header = '#      Time   UID       PID    %usr %system  %guest    %CPU   CPU  Command\n'
        for sep in ('\r', '\x0b', '\x0c', '\x1c', '\x85', ' '):
            data = header + ' 1646859134     0         6    0.00    0.00    0.00    0.03     0  foo' + sep + 'bar baz\n'
            result = jc.parsers.pidstat.parse(data, quiet=True)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]['command'], 'foo' + sep + 'bar baz')
            self.assertEqual(result[0]['percent_cpu'], 0.03)


if __name__ == '__main__':
    unittest.main()
