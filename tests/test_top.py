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


    def test_top_line_separator(self):
        """
        Test 'top' with a line-break character other than LF inside a field
        """
        data = 'top - 11:24:50 up 2 min,  2 users,  load average: 0.55, 0.28, 0.11\n\n    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND\n   1183 nobody    20   0    2500    900    800 S   0.0   0.0   0:00.00 x\u2028 999999 root      20   0  167000  11000   8000 S   0.0   0.1   0:01.00 /usr/sbin/sshd -D\n'
        result = jc.parsers.top.parse(data, quiet=True)
        self.assertEqual(len(result[0]['processes']), 1)
        self.assertEqual(result[0]['processes'][0]['pid'], 1183)
        self.assertEqual(result[0]['processes'][0]['command'], 'x\u2028 999999 root      20   0  167000  11000   8000 S   0.0   0.1   0:01.00 /usr/sbin/sshd -D')


    def test_top_glued_summary_fields(self):
        """
        Test 'top -b' summary lines where a full-width number touches its label
        """
        data = ('top - 11:10:47 up  1:08,  2 users,  load average: 0.00, 0.01, 0.05\n'
                'Tasks:12345 total,1000 running,11345 sleeping,   0 stopped,   0 zombie\n'
                '%Cpu(s):100.0 us,  0.0 sy,  0.0 ni,100.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st\n'
                'KiB Mem :1234567890 total,1234567891 free,1234567892 used,1234567893 buff/cache\n'
                'KiB Swap:1234567894 total,1234567895 free,1234567896 used.1234567897 avail Mem \n')
        result = jc.parsers.top.parse(data, raw=True, quiet=True)
        r = result[0]
        self.assertEqual((r['tasks_total'], r['tasks_running'], r['tasks_sleeping'], r['tasks_stopped'], r['tasks_zombie']),
                         ('12345', '1000', '11345', '0', '0'))
        self.assertEqual((r['cpu_user'], r['cpu_sys'], r['cpu_nice'], r['cpu_idle'], r['cpu_wait'], r['cpu_hardware'], r['cpu_software'], r['cpu_steal']),
                         ('100.0', '0.0', '0.0', '100.0', '0.0', '0.0', '0.0', '0.0'))
        self.assertEqual((r['mem_total'], r['mem_free'], r['mem_used'], r['mem_buff_cache']),
                         ('1234567890', '1234567891', '1234567892', '1234567893'))
        self.assertEqual((r['swap_total'], r['swap_free'], r['swap_used'], r['mem_available']),
                         ('1234567894', '1234567895', '1234567896', '1234567897'))


if __name__ == '__main__':
    unittest.main()
