import os
import unittest
import json
import jc.parsers.tracepath

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/tracepath.out'), 'r', encoding='utf-8') as f:
        centos_7_7_tracepath = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/tracepath6.out'), 'r', encoding='utf-8') as f:
        centos_7_7_tracepath6 = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/tracepath.json'), 'r', encoding='utf-8') as f:
        centos_7_7_tracepath_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/tracepath6.json'), 'r', encoding='utf-8') as f:
        centos_7_7_tracepath6_json = json.loads(f.read())


    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/tracepath-long-padding.out'), 'r', encoding='utf-8') as f:
        generic_tracepath_long_padding = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/tracepath-long-padding.json'), 'r', encoding='utf-8') as f:
        generic_tracepath_long_padding_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/tracepath-keyword-hostnames.out'), 'r', encoding='utf-8') as f:
        generic_tracepath_keyword_hostnames = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/tracepath-keyword-hostnames.json'), 'r', encoding='utf-8') as f:
        generic_tracepath_keyword_hostnames_json = json.loads(f.read())


    def test_tracepath_nodata(self):
        """
        Test 'tracepath' with no data
        """
        self.assertEqual(jc.parsers.tracepath.parse('', quiet=True), {})

    def test_tracepath_centos_7_7(self):
        """
        Test 'tracepath' on Centos 7.7
        """
        self.assertEqual(jc.parsers.tracepath.parse(self.centos_7_7_tracepath, quiet=True), self.centos_7_7_tracepath_json)

    def test_tracepath6_centos_7_7(self):
        """
        Test 'tracepath6' on Centos 7.7
        """
        self.assertEqual(jc.parsers.tracepath.parse(self.centos_7_7_tracepath6, quiet=True), self.centos_7_7_tracepath6_json)

    def test_tracepath_long_padding(self):
        """
        Test 'tracepath' with a long run of spaces in a hop line
        """
        self.assertEqual(jc.parsers.tracepath.parse(self.generic_tracepath_long_padding, quiet=True), self.generic_tracepath_long_padding_json)

    def test_tracepath_keyword_hostnames(self):
        """
        Test 'tracepath' with host names that start with the hop keywords
        """
        result = jc.parsers.tracepath.parse(self.generic_tracepath_keyword_hostnames, quiet=True)
        self.assertEqual(result, self.generic_tracepath_keyword_hostnames_json)
        self.assertEqual([hop['reached'] for hop in result['hops']], [False, False, False, False, False, False, True])
        self.assertEqual(result['hops'][2]['host'], 'reached.example.net')
        self.assertEqual(result['hops'][3]['asymmetric_difference'], 4)
        self.assertEqual(result['hops'][4]['reply_ms'], 31.207)
        self.assertEqual(result['hops'][5]['pmtu'], 1480)


if __name__ == '__main__':
    unittest.main()
