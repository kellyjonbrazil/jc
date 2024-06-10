import os
import json
import unittest
import jc.parsers.stat

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


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

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.04/stat-missing-data.out'), 'r', encoding='utf-8') as f:
        ubuntu_20_4_stat_missing_data = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/stat.json'), 'r', encoding='utf-8') as f:
        centos_7_7_stat_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/stat.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_stat_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/stat.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_stat_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/stat-filename-with-spaces.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_stat_filename_with_spaces_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/stat.json'), 'r', encoding='utf-8') as f:
        freebsd12_stat_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.04/stat-missing-data.json'), 'r', encoding='utf-8') as f:
        ubuntu_20_4_stat_missing_data_json = json.loads(f.read())

    def test_stat_nodata(self):
        """
        Test 'stat' with no data
        """
        self.assertEqual(jc.parsers.stat.parse('', quiet=True), [])

    def test_stat_centos_7_7(self):
        """
        Test 'stat /bin/*' on Centos 7.7
        """
        self.assertEqual(jc.parsers.stat.parse(self.centos_7_7_stat, quiet=True), self.centos_7_7_stat_json)

    def test_stat_ubuntu_18_4(self):
        """
        Test 'stat /bin/*' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.stat.parse(self.ubuntu_18_4_stat, quiet=True), self.ubuntu_18_4_stat_json)

    def test_stat_osx_10_14_6(self):
        """
        Test 'stat /foo/*' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.stat.parse(self.osx_10_14_6_stat, quiet=True), self.osx_10_14_6_stat_json)

    def test_stat_filename_with_spaces_osx_10_14_6(self):
        """
        Test 'stat' filename with spaces on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.stat.parse(self.osx_10_14_6_stat_filename_with_spaces, quiet=True), self.osx_10_14_6_stat_filename_with_spaces_json)

    def test_stat_freebsd12(self):
        """
        Test 'stat /foo/*' on FreeBSD12
        """
        self.assertEqual(jc.parsers.stat.parse(self.freebsd12_stat, quiet=True), self.freebsd12_stat_json)

    def test_stat_missing_data(self):
        """
        Test 'stat /etc/passwd' with missing data.
        """
        self.assertEqual(jc.parsers.stat.parse(self.ubuntu_20_4_stat_missing_data, quiet=True), self.ubuntu_20_4_stat_missing_data_json)


if __name__ == '__main__':
    unittest.main()
