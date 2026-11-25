import os
import json
import unittest
import jc.parsers.w
from jc.exceptions import ParseError

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/w.out'), 'r', encoding='utf-8') as f:
        centos_7_7_w = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/w.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_w = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/w.out'), 'r', encoding='utf-8') as f:
        osx_10_11_6_w = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/w.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_w = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/nixos/w.out'), 'r', encoding='utf-8') as f:
        nixos_w = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/w.json'), 'r', encoding='utf-8') as f:
        centos_7_7_w_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/w.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_w_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/w.json'), 'r', encoding='utf-8') as f:
        osx_10_11_6_w_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/w.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_w_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/nixos/w.json'), 'r', encoding='utf-8') as f:
        nixos_w_json = json.loads(f.read())


    def test_w_nodata(self):
        """
        Test 'w' with no data
        """
        self.assertEqual(jc.parsers.w.parse('', quiet=True), [])

    def test_w_centos_7_7(self):
        """
        Test 'w' on Centos 7.7
        """
        self.assertEqual(jc.parsers.w.parse(self.centos_7_7_w, quiet=True), self.centos_7_7_w_json)

    def test_w_ubuntu_18_4(self):
        """
        Test 'w' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.w.parse(self.ubuntu_18_4_w, quiet=True), self.ubuntu_18_4_w_json)

    def test_w_osx_10_11_6(self):
        """
        Test 'w' on OSX 10.11.6
        """
        self.assertEqual(jc.parsers.w.parse(self.osx_10_11_6_w, quiet=True), self.osx_10_11_6_w_json)

    def test_w_osx_10_14_6(self):
        """
        Test 'w' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.w.parse(self.osx_10_14_6_w, quiet=True), self.osx_10_14_6_w_json)

    def test_w_nixos(self):
        """
        Test 'w' on nixos
        """
        self.assertEqual(jc.parsers.w.parse(self.nixos_w, quiet=True), self.nixos_w_json)

    def test_w_uptime_line_only(self):
        """
        Test 'w' with only the uptime line (e.g. `w | head -1`) raises
        ParseError instead of leaking an IndexError
        """
        uptime_line = '10:15  up 20 days, 19:44, 8 users, load averages: 0.86 0.45 0.37\n'
        with self.assertRaises(ParseError):
            jc.parsers.w.parse(uptime_line, quiet=True)

    def test_w_uptime_line_with_blank_line(self):
        """
        Test 'w' with the uptime line followed by an empty line raises the same
        ParseError as the uptime line on its own
        """
        data = '10:15  up 20 days, 19:44, 8 users, load averages: 0.86 0.45 0.37\n\n'
        with self.assertRaises(ParseError):
            jc.parsers.w.parse(data, quiet=True)

    def test_w_row_cut_before_from_column(self):
        """
        Test 'w' with output cut off after the header, inside a row that has
        not reached the FROM column (e.g. `w | head -c 120`), returns the
        columns that are present instead of raising IndexError
        """
        data = (
            '10:15  up 20 days, 19:44, 8 users, load averages: 0.86 0.45 0.37\n'
            'USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT\n'
            'kbrazil  pts/0\n'
        )
        self.assertEqual(jc.parsers.w.parse(data, quiet=True), [{'user': 'kbrazil', 'tty': 'pts/0'}])

    def test_w_blank_rows_are_skipped(self):
        """
        Test 'w' skips blank and whitespace-only rows instead of raising
        IndexError
        """
        data = (
            '10:15  up 20 days, 19:44, 8 users, load averages: 0.86 0.45 0.37\n'
            'USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT\n'
            '\n'
            '   \n'
            'kbrazil  pts/0    192.168.1.5      09:12    1.00s  0.05s  0.01s w\n'
        )
        self.assertEqual(jc.parsers.w.parse(data, quiet=True), [{
            'user': 'kbrazil',
            'tty': 'pts/0',
            'from': '192.168.1.5',
            'login_at': '09:12',
            'idle': '1.00s',
            'jcpu': '0.05s',
            'pcpu': '0.01s',
            'what': 'w'
        }])


if __name__ == '__main__':
    unittest.main()
