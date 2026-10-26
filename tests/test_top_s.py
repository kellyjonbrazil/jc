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


if __name__ == '__main__':
    unittest.main()
