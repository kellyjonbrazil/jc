import os
import json
import unittest
import jc.parsers.top_s
from jc.exceptions import ParseError

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

# To create streaming output use:
# $ cat top.out | jc --top-s | jq -cs > top-streaming.json


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
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/top-b-n3-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_top_b_n3_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/top-b-n1-gib-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_top_b_n1_gib_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/top-b-n1-gib-allfields-w-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_top_b_n1_gib_allfields_w_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.10/top-b-n1-streaming.json'), 'r', encoding='utf-8') as f:
        ubuntu_20_10_top_b_n1_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.10/top-b-allfields-streaming.json'), 'r', encoding='utf-8') as f:
        ubuntu_20_10_top_b_allfields_streaming_json = json.loads(f.read())


    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/top-b-bad-state.out'), 'r', encoding='utf-8') as f:
        generic_top_b_bad_state = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/top-b-bad-state-streaming.json'), 'r', encoding='utf-8') as f:
        generic_top_b_bad_state_streaming_json = json.loads(f.read())

    def test_top_s_nodata(self):
        """
        Test 'top' with no data
        """
        self.assertEqual(list(jc.parsers.top_s.parse([], quiet=True)), [])

    def test_top_s_unparsable(self):
        data = 'unparsable data'
        g = jc.parsers.top_s.parse(data.splitlines(), quiet=True)
        with self.assertRaises(ParseError):
            list(g)

    def test_top_s_b_n3_centos_7_7(self):
        """
        Test 'top -b -n3' on Centos 7.7
        """
        self.assertEqual(list(jc.parsers.top_s.parse(self.centos_7_7_top_b_n3.splitlines(), quiet=True)), self.centos_7_7_top_b_n3_streaming_json)

    def test_top_s_b_n1_gib_centos_7_7(self):
        """
        Test 'top -b -n1' with GiB units on Centos 7.7
        """
        self.assertEqual(list(jc.parsers.top_s.parse(self.centos_7_7_top_b_n1_gib.splitlines(), quiet=True)), self.centos_7_7_top_b_n1_gib_streaming_json)

    def test_top_s_b_n1_gib_allfields_w_centos_7_7(self):
        """
        Test 'top -b -n1 -w' with GiB units, all fields selected and wide output on Centos 7.7
        """
        self.assertEqual(list(jc.parsers.top_s.parse(self.centos_7_7_top_b_n1_gib_allfields_w.splitlines(), quiet=True)), self.centos_7_7_top_b_n1_gib_allfields_w_streaming_json)

    def test_top_s_b_n1_ubuntu_20_10(self):
        """
        Test 'top -b -n1' with MiB units on Ubuntu 20.10
        """
        self.assertEqual(list(jc.parsers.top_s.parse(self.ubuntu_20_10_top_b_n1.splitlines(), quiet=True)), self.ubuntu_20_10_top_b_n1_streaming_json)

    def test_top_s_b_allfields_ubuntu_20_10(self):
        """
        Test 'top -b -n1' with MiB units and all fields on Ubuntu 20.10
        """
        self.assertEqual(list(jc.parsers.top_s.parse(self.ubuntu_20_10_top_b_allfields.splitlines(), quiet=True)), self.ubuntu_20_10_top_b_allfields_streaming_json)

    def test_top_s_bad_record_ignore_exceptions(self):
        """
        Test 'top -b' where the first sample has an unknown process state: one
        error record is emitted and the following samples parse normally
        """
        result = list(jc.parsers.top_s.parse(self.generic_top_b_bad_state.splitlines(), quiet=True, ignore_exceptions=True))
        self.assertEqual(result, self.generic_top_b_bad_state_streaming_json)
        self.assertEqual([r['_jc_meta']['success'] for r in result], [False, True, True])

    def test_top_s_bad_last_record_ignore_exceptions(self):
        """
        Test 'top -b' where the final sample is bad: the error is yielded and not raised
        """
        last_bad = self.centos_7_7_top_b_n3.splitlines()
        idx = max(i for i, l in enumerate(last_bad) if l.startswith('     1 '))
        last_bad[idx] = last_bad[idx].replace(' S ', ' X ', 1)
        result = list(jc.parsers.top_s.parse(last_bad, quiet=True, ignore_exceptions=True))
        self.assertEqual([r['_jc_meta']['success'] for r in result], [True, True, False])

    def test_top_s_bad_record_raises(self):
        """
        Test 'top -b' with a bad record still raises when ignore_exceptions is not set
        """
        with self.assertRaises(KeyError):
            list(jc.parsers.top_s.parse(self.generic_top_b_bad_state.splitlines(), quiet=True))


    def test_top_s_glued_summary_fields(self):
        """
        Test 'top -b' summary lines where a full-width number touches its label
        """
        data = ('top - 11:10:47 up  1:08,  2 users,  load average: 0.00, 0.01, 0.05\n'
                'Tasks:12345 total,1000 running,11345 sleeping,   0 stopped,   0 zombie\n'
                '%Cpu(s):100.0 us,  0.0 sy,  0.0 ni,100.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st\n'
                'KiB Mem :1234567890 total,1234567891 free,1234567892 used,1234567893 buff/cache\n'
                'KiB Swap:1234567894 total,1234567895 free,1234567896 used.1234567897 avail Mem \n')
        result = list(jc.parsers.top_s.parse(data.splitlines(True), raw=True, quiet=True))
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
