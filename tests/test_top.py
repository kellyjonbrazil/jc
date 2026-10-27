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


    def test_top_no_process_table(self):
        """
        Test 'top -b -n1' output cut before the process table, e.g.
        `top -b -n1 | head -5 | jc --top`. _process() used to index
        item['processes'] unconditionally and raise KeyError.
        """
        summary_only = (
            'top - 10:00:00 up 1 day,  2:03,  1 user,  load average: 0.00, 0.01, 0.05\n'
            'Tasks: 123 total,   1 running, 122 sleeping,   0 stopped,   0 zombie\n'
        )
        parsed = jc.parsers.top.parse(summary_only, quiet=True)
        self.assertIsInstance(parsed, list)

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


    def test_top_line_separator(self):
        """
        Test 'top' with a line-break character other than LF inside a field
        """
        data = 'top - 11:24:50 up 2 min,  2 users,  load average: 0.55, 0.28, 0.11\n\n    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND\n   1183 nobody    20   0    2500    900    800 S   0.0   0.0   0:00.00 x\u2028 999999 root      20   0  167000  11000   8000 S   0.0   0.1   0:01.00 /usr/sbin/sshd -D\n'
        result = jc.parsers.top.parse(data, quiet=True)
        self.assertEqual(len(result[0]['processes']), 1)
        self.assertEqual(result[0]['processes'][0]['pid'], 1183)
        self.assertEqual(result[0]['processes'][0]['command'], 'x\u2028 999999 root      20   0  167000  11000   8000 S   0.0   0.1   0:01.00 /usr/sbin/sshd -D')


if __name__ == '__main__':
    unittest.main()
