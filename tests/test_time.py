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


if __name__ == '__main__':
    unittest.main()
