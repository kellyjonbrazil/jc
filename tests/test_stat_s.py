import os
import json
import unittest
from jc.exceptions import ParseError
import jc.parsers.stat_s

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


# To create streaming output use:
# $ cat stat.out | jc --stat-s | jello -c > stat-streaming.json


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/stat.out'), 'r', encoding='utf-8') as f:
        centos_7_7_stat = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/stat.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_stat = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/stat.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_stat = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/stat-filename-with-spaces.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_stat_filename_with_spaces = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/stat.out'), 'r', encoding='utf-8') as f:
        freebsd12_stat = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/stat-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_stat_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/stat-streaming.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_stat_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/stat-streaming.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_stat_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/stat-filename-with-spaces-streaming.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_stat_filename_with_spaces_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/stat-streaming.json'), 'r', encoding='utf-8') as f:
        freebsd12_stat_streaming_json = json.loads(f.read())


    def test_stat_s_nodata(self):
        """
        Test 'stat' with no data
        """
        self.assertEqual(list(jc.parsers.stat_s.parse([], quiet=True)), [])

    def test_stat_s_unparsable(self):
        data = 'unparsable data'
        g = jc.parsers.stat_s.parse(data.splitlines(), quiet=True)
        with self.assertRaises(ParseError):
            list(g)

    def test_stat_s_centos_7_7(self):
        """
        Test 'stat /bin/*' on Centos 7.7
        """
        self.assertEqual(list(jc.parsers.stat_s.parse(self.centos_7_7_stat.splitlines(), quiet=True)), self.centos_7_7_stat_streaming_json)

    def test_stat_s_ubuntu_18_4(self):
        """
        Test 'stat /bin/*' on Ubuntu 18.4
        """
        self.assertEqual(list(jc.parsers.stat_s.parse(self.ubuntu_18_4_stat.splitlines(), quiet=True)), self.ubuntu_18_4_stat_streaming_json)

    def test_stat_s_osx_10_14_6(self):
        """
        Test 'stat /bin/*' on OSX 10.14.6
        """
        self.assertEqual(list(jc.parsers.stat_s.parse(self.osx_10_14_6_stat.splitlines(), quiet=True)), self.osx_10_14_6_stat_streaming_json)

    def test_stat_s_filename_with_spaces_osx_10_14_6(self):
        """
        Test 'stat' filename with spaces on OSX 10.14.6
        """
        self.assertEqual(list(jc.parsers.stat_s.parse(self.osx_10_14_6_stat_filename_with_spaces.splitlines(), quiet=True)), self.osx_10_14_6_stat_filename_with_spaces_streaming_json)

    def test_stat_s_freebsd12(self):
        """
        Test 'stat /foo/*' on FreeBSD12
        """
        self.assertEqual(list(jc.parsers.stat_s.parse(self.freebsd12_stat.splitlines(), quiet=True)), self.freebsd12_stat_streaming_json)


if __name__ == '__main__':
    unittest.main()
