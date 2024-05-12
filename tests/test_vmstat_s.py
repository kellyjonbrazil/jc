import os
import json
import unittest
from jc.exceptions import ParseError
import jc.parsers.vmstat_s

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


# To create streaming output use:
# $ cat vmstat.out | jc --vmstat-s | jello -c > vmstat-streaming.json


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/vmstat.out'), 'r', encoding='utf-8') as f:
        centos_7_7_vmstat = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/vmstat-a.out'), 'r', encoding='utf-8') as f:
        centos_7_7_vmstat_a = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/vmstat-w.out'), 'r', encoding='utf-8') as f:
        centos_7_7_vmstat_w = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/vmstat-at-5-10.out'), 'r', encoding='utf-8') as f:
        centos_7_7_vmstat_at_5_10 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/vmstat-awt.out'), 'r', encoding='utf-8') as f:
        centos_7_7_vmstat_awt = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/vmstat-d.out'), 'r', encoding='utf-8') as f:
        centos_7_7_vmstat_d = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/vmstat-dt.out'), 'r', encoding='utf-8') as f:
        centos_7_7_vmstat_dt = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/vmstat-1-long.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_04_vmstat_1_long = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/vmstat-extra-wide.out'), 'r', encoding='utf-8') as f:
        generic_vmstat_extra_wide = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/vmstat-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_vmstat_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/vmstat-a-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_vmstat_a_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/vmstat-w-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_vmstat_w_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/vmstat-at-5-10-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_vmstat_at_5_10_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/vmstat-awt-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_vmstat_awt_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/vmstat-d-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_vmstat_d_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/vmstat-dt-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_vmstat_dt_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/vmstat-1-long-streaming.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_04_vmstat_1_long_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/vmstat-extra-wide-streaming.json'), 'r', encoding='utf-8') as f:
        generic_vmstat_extra_wide_streaming_json = json.loads(f.read())


    def test_vmstat_s_nodata(self):
        """
        Test 'vmstat' with no data
        """
        self.assertEqual(list(jc.parsers.vmstat_s.parse([], quiet=True)), [])

    def test_vmstat_s_unparsable(self):
        data = 'unparsable data'
        g = jc.parsers.vmstat_s.parse(data.splitlines(), quiet=True)
        with self.assertRaises(ParseError):
            list(g)

    def test_vmstat_s_centos_7_7(self):
        """
        Test 'vmstat' on Centos 7.7
        """
        self.assertEqual(list(jc.parsers.vmstat_s.parse(self.centos_7_7_vmstat.splitlines(), quiet=True)), self.centos_7_7_vmstat_streaming_json)

    def test_vmstat_s_a_centos_7_7(self):
        """
        Test 'vmstat -a' on Centos 7.7
        """
        self.assertEqual(list(jc.parsers.vmstat_s.parse(self.centos_7_7_vmstat_a.splitlines(), quiet=True)), self.centos_7_7_vmstat_a_streaming_json)

    def test_vmstat_s_w_centos_7_7(self):
        """
        Test 'vmstat -w' on Centos 7.7
        """
        self.assertEqual(list(jc.parsers.vmstat_s.parse(self.centos_7_7_vmstat_w.splitlines(), quiet=True)), self.centos_7_7_vmstat_w_streaming_json)

    def test_vmstat_s_at_5_10_centos_7_7(self):
        """
        Test 'vmstat -at 5 10' on Centos 7.7
        """
        self.assertEqual(list(jc.parsers.vmstat_s.parse(self.centos_7_7_vmstat_at_5_10.splitlines(), quiet=True)), self.centos_7_7_vmstat_at_5_10_streaming_json)

    def test_vmstat_s_awt_centos_7_7(self):
        """
        Test 'vmstat -awt' on Centos 7.7
        """
        self.assertEqual(list(jc.parsers.vmstat_s.parse(self.centos_7_7_vmstat_awt.splitlines(), quiet=True)), self.centos_7_7_vmstat_awt_streaming_json)

    def test_vmstat_s_d_centos_7_7(self):
        """
        Test 'vmstat -d' on Centos 7.7
        """
        self.assertEqual(list(jc.parsers.vmstat_s.parse(self.centos_7_7_vmstat_d.splitlines(), quiet=True)), self.centos_7_7_vmstat_d_streaming_json)

    def test_vmstat_s_dt_centos_7_7(self):
        """
        Test 'vmstat -dt' on Centos 7.7
        """
        self.assertEqual(list(jc.parsers.vmstat_s.parse(self.centos_7_7_vmstat_dt.splitlines(), quiet=True)), self.centos_7_7_vmstat_dt_streaming_json)

    def test_vmstat_s_1_long_ubuntu_18_04(self):
        """
        Test 'vmstat -1' (on ubuntu) with long output that reprints the header rows
        """
        self.assertEqual(list(jc.parsers.vmstat_s.parse(self.ubuntu_18_04_vmstat_1_long.splitlines(), quiet=True)), self.ubuntu_18_04_vmstat_1_long_streaming_json)

    def test_vmstat_extra_wide(self):
        """
        Test 'vmstat -w' with extra wide output
        """
        self.assertEqual(list(jc.parsers.vmstat_s.parse(self.generic_vmstat_extra_wide.splitlines(), quiet=True)), self.generic_vmstat_extra_wide_streaming_json)


if __name__ == '__main__':
    unittest.main()
