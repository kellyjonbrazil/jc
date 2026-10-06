import os
import json
import unittest
import jc.parsers.time

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/time.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_time = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/time2.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_time2 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/time-p.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_time_p = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/time-verbose.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_time_verbose = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/time.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_time = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/time-l.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_time_l = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/time-p.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_time_p = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/time-lp.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_time_lp = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/time.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_time_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/time2.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_time2_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/time-p.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_time_p_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/time-verbose.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_time_verbose_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/time.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_time_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/time-l.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_time_l_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/time-p.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_time_p_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/time-lp.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_time_lp_json = json.loads(f.read())


    def test_time_nodata(self):
        """
        Test plain 'time' with no data
        """
        self.assertEqual(jc.parsers.time.parse('', quiet=True), {})

    def test_time_ubuntu_18_4(self):
        """
        Test plain 'time' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.time.parse(self.ubuntu_18_4_time, quiet=True), self.ubuntu_18_4_time_json)

    def test_time2_ubuntu_18_4(self):
        """
        Test plain 'time' on Ubuntu 18.4 with ? in CPU%
        """
        self.assertEqual(jc.parsers.time.parse(self.ubuntu_18_4_time2, quiet=True), self.ubuntu_18_4_time2_json)

    def test_time_p_ubuntu_18_4(self):
        """
        Test 'time -p' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.time.parse(self.ubuntu_18_4_time_p, quiet=True), self.ubuntu_18_4_time_p_json)

    def test_time_verbose_ubuntu_18_4(self):
        """
        Test 'time --verbose' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.time.parse(self.ubuntu_18_4_time_verbose, quiet=True), self.ubuntu_18_4_time_verbose_json)

    def test_time_osx_10_14_6(self):
        """
        Test plain 'time' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.time.parse(self.osx_10_14_6_time, quiet=True), self.osx_10_14_6_time_json)

    def test_time_l_osx_10_14_6(self):
        """
        Test 'time -l' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.time.parse(self.osx_10_14_6_time_l, quiet=True), self.osx_10_14_6_time_l_json)

    def test_time_p_osx_10_14_6(self):
        """
        Test 'time -p' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.time.parse(self.osx_10_14_6_time_p, quiet=True), self.osx_10_14_6_time_p_json)

    def test_time_lp_osx_10_14_6(self):
        """
        Test 'time -lp' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.time.parse(self.osx_10_14_6_time_lp, quiet=True), self.osx_10_14_6_time_lp_json)

    def test_time_no_centiseconds(self):
        """
        Test 'time' output with no centiseconds data
        """
        data = '''        Command being timed: "echo"
        User time (seconds): 5156.20
        System time (seconds): 0.05
        Percent of CPU this job got: 99%
        Elapsed (wall clock) time (h:mm:ss or m:ss): 1:25:56
        Average shared text size (kbytes): 0
        Average unshared data size (kbytes): 0
        Average stack size (kbytes): 0
        Average total size (kbytes): 0
        Maximum resident set size (kbytes): 21760
        Average resident set size (kbytes): 0
        Major (requiring I/O) page faults: 0
        Minor (reclaiming a frame) page faults: 4975
        Voluntary context switches: 1
        Involuntary context switches: 8159
        Swaps: 0
        File system inputs: 0
        File system outputs: 6272
        Socket messages sent: 0
        Socket messages received: 0
        Signals delivered: 0
        Page size (bytes): 4096
        Exit status: 0'''

        expected = {"command_being_timed":"echo","user_time":5156.2,"system_time":0.05,"cpu_percent":99,"elapsed_time":"1:25:56","average_shared_text_size":0,"average_unshared_data_size":0,"average_stack_size":0,"average_total_size":0,"maximum_resident_set_size":21760,"average_resident_set_size":0,"major_pagefaults":0,"minor_pagefaults":4975,"voluntary_context_switches":1,"involuntary_context_switches":8159,"swaps":0,"block_input_operations":0,"block_output_operations":6272,"messages_sent":0,"messages_received":0,"signals_delivered":0,"page_size":4096,"exit_status":0,"elapsed_time_hours":1,"elapsed_time_minutes":25,"elapsed_time_seconds":56,"elapsed_time_centiseconds":0,"elapsed_time_total_seconds":5156.0}
        self.assertEqual(jc.parsers.time.parse(data, quiet=True), expected)


if __name__ == '__main__':
    unittest.main()
