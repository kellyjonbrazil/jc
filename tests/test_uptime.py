import os
import json
import unittest
import jc.parsers.uptime

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/uptime.out'), 'r', encoding='utf-8') as f:
        centos_7_7_uptime = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/uptime.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_uptime = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/uptime.out'), 'r', encoding='utf-8') as f:
        osx_10_11_6_uptime = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/uptime.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_uptime = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/uptime.json'), 'r', encoding='utf-8') as f:
        centos_7_7_uptime_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/uptime.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_uptime_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/uptime.json'), 'r', encoding='utf-8') as f:
        osx_10_11_6_uptime_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/uptime.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_uptime_json = json.loads(f.read())


    def test_uptime_nodata(self):
        """
        Test 'uptime' with no data
        """
        self.assertEqual(jc.parsers.uptime.parse('', quiet=True), {})

    def test_uptime_centos_7_7(self):
        """
        Test 'uptime' on Centos 7.7
        """
        self.assertEqual(jc.parsers.uptime.parse(self.centos_7_7_uptime, quiet=True), self.centos_7_7_uptime_json)

    def test_uptime_ubuntu_18_4(self):
        """
        Test 'uptime' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.uptime.parse(self.ubuntu_18_4_uptime, quiet=True), self.ubuntu_18_4_uptime_json)

    def test_uptime_osx_10_11_6(self):
        """
        Test 'uptime' on OSX 10.11.6
        """
        self.assertEqual(jc.parsers.uptime.parse(self.osx_10_11_6_uptime, quiet=True), self.osx_10_11_6_uptime_json)

    def test_uptime_osx_10_14_6(self):
        """
        Test 'uptime' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.uptime.parse(self.osx_10_14_6_uptime, quiet=True), self.osx_10_14_6_uptime_json)

    def test_uptime_busybox(self):
        """
        Test 'uptime' on busybox with no user information
        """
        data = '00:03:32 up 3 min,  load average: 0.00, 0.00, 0.00'
        expected = {"time":"00:03:32","uptime":"3 min","load_1m":0.0,"load_5m":0.0,"load_15m":0.0,"time_hour":0,"time_minute":3,"time_second":32,"uptime_days":0,"uptime_hours":0,"uptime_minutes":3,"uptime_total_seconds":180}
        self.assertEqual(jc.parsers.uptime.parse(data, quiet=True), expected)

    def test_uptime_user(self):
        """
        Test 'uptime' with 'user' instead of 'users' in the data
        """
        data = ' 12:44:19 up 1 day, 23:12,  0 user,  load average: 3.94, 4.43, 2.75'
        expected = {"time":"12:44:19","uptime":"1 day, 23:12","users":0,"load_1m":3.94,"load_5m":4.43,"load_15m":2.75,"time_hour":12,"time_minute":44,"time_second":19,"uptime_days":1,"uptime_hours":23,"uptime_minutes":12,"uptime_total_seconds":169920}
        self.assertEqual(jc.parsers.uptime.parse(data, quiet=True), expected)


if __name__ == '__main__':
    unittest.main()
