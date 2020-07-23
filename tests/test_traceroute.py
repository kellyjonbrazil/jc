import os
import unittest
import json
import jc.parsers.traceroute

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/traceroute.out'), 'r', encoding='utf-8') as f:
            self.centos_7_7_traceroute = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/traceroute-a.out'), 'r', encoding='utf-8') as f:
            self.osx_10_14_6_traceroute_a = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/traceroute-a2.out'), 'r', encoding='utf-8') as f:
            self.osx_10_14_6_traceroute_a2 = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/traceroute.json'), 'r', encoding='utf-8') as f:
            self.centos_7_7_traceroute_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/traceroute-a.json'), 'r', encoding='utf-8') as f:
            self.osx_10_14_6_traceroute_a_json = json.loads(f.read())

    def test_traceroute_nodata(self):
        """
        Test 'traceroute' with no data
        """
        self.assertEqual(jc.parsers.traceroute.parse('', quiet=True), [])

    def test_traceroute_noheader(self):
        """
        Test 'traceroute' with missing header row. Should generate a ParseError exception
        """
        pass

    def test_traceroute_centos_7_7(self):
        """
        Test 'traceroute' on Centos 7.7
        """
        self.assertEqual(jc.parsers.traceroute.parse(self.centos_7_7_traceroute, quiet=True), self.centos_7_7_traceroute_json)

    def test_traceroute_a_osx_10_14_6(self):
        """
        Test 'traceroute -a' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.traceroute.parse(self.osx_10_14_6_traceroute_a, quiet=True), self.osx_10_14_6_traceroute_a_json)


if __name__ == '__main__':
    unittest.main()
