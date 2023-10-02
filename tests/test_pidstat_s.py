import os
import json
import unittest
import jc.parsers.pidstat_s

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

# To create streaming output use:
# $ cat pidstat.out | jc --pidstat-s | jello -c > pidstat-streaming.json


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
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/pidstat-hl-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_pidstat_hl_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/pidstat-hdlrsuw-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_pidstat_hdlrsuw_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/pidstat-hdlrsuw-2-5-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_pidstat_hdlrsuw_2_5_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/pidstat-ht-streaming.json'), 'r', encoding='utf-8') as f:
        generic_pidstat_ht_streaming_json = json.loads(f.read())


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


if __name__ == '__main__':
    unittest.main()
