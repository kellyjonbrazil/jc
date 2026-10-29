import os
import json
import unittest
from jc.exceptions import ParseError
import jc.parsers.pidstat_s

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

# To create streaming output use:
# $ cat pidstat.out | jc --pidstat-s | jello -c > pidstat-streaming.json


class MyTests(unittest.TestCase):

    # new input/output fixtures
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/pidstat-linux-stray-line.out'), 'r', encoding='utf-8') as f:
        generic_pidstat_stray_line = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/pidstat-many-processes.out'), 'r', encoding='utf-8') as f:
        generic_pidstat_many_processes = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/pidstat-many-processes-streaming.json'), 'r', encoding='utf-8') as f:
        generic_pidstat_many_processes_streaming_json = json.loads(f.read())


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
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/pidstat-hl-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_pidstat_hl_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/pidstat-hdlrsuw-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_pidstat_hdlrsuw_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/pidstat-hdlrsuw-2-5-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_pidstat_hdlrsuw_2_5_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/pidstat-ht-streaming.json'), 'r', encoding='utf-8') as f:
        generic_pidstat_ht_streaming_json = json.loads(f.read())


    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/pidstat-hl-hash-line.out'), 'r', encoding='utf-8') as f:
        generic_pidstat_hl_hash_line = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/pidstat-hl-hash-line-streaming.json'), 'r', encoding='utf-8') as f:
        generic_pidstat_hl_hash_line_streaming_json = json.loads(f.read())

    def test_pidstat_s_nodata(self):
        """
        Test 'pidstat' with no data
        """
        self.assertEqual(list(jc.parsers.pidstat_s.parse([], quiet=True)), [])

    def test_pidstat_s_centos_7_7(self):
        """
        Test 'pidstat' on Centos 7.7. Should be no output since only -h is supported
        """
        self.assertEqual(list(jc.parsers.pidstat_s.parse(self.centos_7_7_pidstat.splitlines(), quiet=True)), [])

    def test_pidstat_s_hl_centos_7_7(self):
        """
        Test 'pidstat -hl' on Centos 7.7
        """
        self.assertEqual(list(jc.parsers.pidstat_s.parse(self.centos_7_7_pidstat_hl.splitlines(), quiet=True)), self.centos_7_7_pidstat_hl_streaming_json)

    def test_pidstat_s_hdlrsuw_centos_7_7(self):
        """
        Test 'pidstat -hdlrsuw' on Centos 7.7
        """
        self.assertEqual(list(jc.parsers.pidstat_s.parse(self.centos_7_7_pidstat_hdlrsuw.splitlines(), quiet=True)), self.centos_7_7_pidstat_hdlrsuw_streaming_json)

    def test_pidstat_s_hdlrsuw_2_5_centos_7_7(self):
        """
        Test 'pidstat -hdlrsuw 2 5' on Centos 7.7
        """
        self.assertEqual(list(jc.parsers.pidstat_s.parse(self.centos_7_7_pidstat_hdlrsuw_2_5.splitlines(), quiet=True)), self.centos_7_7_pidstat_hdlrsuw_2_5_streaming_json)

    def test_pidstat_s_ht(self):
        """
        Test 'pidstat -hT'
        """
        self.assertEqual(list(jc.parsers.pidstat_s.parse(self.generic_pidstat_ht.splitlines(), quiet=True)), self.generic_pidstat_ht_streaming_json)


    def test_pidstat_s_many_processes(self):
        """
        Test 'pidstat -h' with many processes and repeated samples
        """
        self.assertEqual(list(jc.parsers.pidstat_s.parse(self.generic_pidstat_many_processes.splitlines(), quiet=True)), self.generic_pidstat_many_processes_streaming_json)

    def test_pidstat_s_stray_line(self):
        """
        Test 'pidstat -hl' with a line that is not pidstat data after the header. Should raise ParseError
        """
        self.assertRaises(ParseError, list, jc.parsers.pidstat_s.parse(self.generic_pidstat_stray_line.splitlines(), quiet=True))

    def test_pidstat_s_stray_line_ignore_exceptions(self):
        """
        Test 'pidstat -hl' with a line that is not pidstat data after the header. Should yield an error record for that line and continue
        """
        result = list(jc.parsers.pidstat_s.parse(self.generic_pidstat_stray_line.splitlines(), quiet=True, ignore_exceptions=True))
        self.assertEqual([r.get('pid') for r in result], [1, None, 6])
        self.assertEqual(result[1], {"_jc_meta": {"success": False, "error": "ParseError: Not pidstat data", "line": "cp: cannot stat 'backup.tar': No such file or directory"}})

    def test_pidstat_s_short_row_after_empty_command(self):
        """
        Test 'pidstat -h' with a row that has no command followed by a short line. The row is kept and the short line should raise ParseError
        """
        data = [
            '# Time        UID       PID    %usr %system  %guest   %wait    %CPU   CPU  Command',
            '1692579199   1000      1852    0.01    0.00    0.00    0.00    0.01     0  ',
            '1 0 1 99 99 99'
        ]
        result = list(jc.parsers.pidstat_s.parse(data, quiet=True, ignore_exceptions=True))
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['pid'], 1852)
        self.assertNotIn('command', result[0])
        self.assertEqual(result[1], {"_jc_meta": {"success": False, "error": "ParseError: Not pidstat data", "line": "1 0 1 99 99 99"}})
        self.assertRaises(ParseError, list, jc.parsers.pidstat_s.parse(data, quiet=True))

    def test_pidstat_s_ragged_rows(self):
        """
        Test 'pidstat' rows with fewer or more fields than the header. Fewer should raise ParseError, more go into the last column
        """
        header = '# Time UID PID Command'
        for bad in ('1646857494   0', 'random'):
            with self.assertRaises(ParseError):
                list(jc.parsers.pidstat_s.parse([header, bad], quiet=True))

        data = [header, '  1646857494   0   2 kthreadd', '  1646857494   0   3', '  1646857494   0   4 a command with spaces\r']
        expected = [
            {"time": 1646857494, "uid": 0, "pid": 2, "command": "kthreadd"},
            {"time": 1646857494, "uid": 0, "pid": 3},
            {"time": 1646857494, "uid": 0, "pid": 4, "command": "a command with spaces"}
        ]
        self.assertEqual(list(jc.parsers.pidstat_s.parse(data, quiet=True)), expected)


if __name__ == '__main__':
    unittest.main()
