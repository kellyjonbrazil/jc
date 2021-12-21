import os
import unittest
import json
import jc.parsers.zipinfo

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/rhel-8/zipinfo.out'), 'r', encoding='utf-8') as f:
            self.rhel_8_zipinfo = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/zipinfo-multi.out'), 'r', encoding='utf-8') as f:
            self.osx_10_14_6_zipinfo_multi = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/rhel-8/zipinfo.json'), 'r', encoding='utf-8') as f:
            self.rhel_8_zipinfo_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/zipinfo-multi.json'), 'r', encoding='utf-8') as f:
            self.osx_10_14_6_zipinfo_multi_json = json.loads(f.read())

    def test_zipinfo_nodata(self):
        """
        Test 'zipinfo' parser with no data
        """
        self.assertEqual(jc.parsers.zipinfo.parse('', quiet=True), [])

    def test_zipinfo_rhel_8(self):
        """
        Test 'zipinfo' on Red Hat 8
        """
        self.assertEqual(jc.parsers.zipinfo.parse(self.rhel_8_zipinfo, quiet=True), self.rhel_8_zipinfo_json)

    def test_zipinfo_multi_osx_10_14_6(self):
        """
        Test 'zipinfo' with multiple archives on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.zipinfo.parse(self.osx_10_14_6_zipinfo_multi, quiet=True), self.osx_10_14_6_zipinfo_multi_json)


if __name__ == '__main__':
    unittest.main()
