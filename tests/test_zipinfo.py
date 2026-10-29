import os
import unittest
import json
import jc.parsers.zipinfo

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/rhel-8/zipinfo.out'), 'r', encoding='utf-8') as f:
        rhel_8_zipinfo = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/zipinfo-multi.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_zipinfo_multi = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/rhel-8/zipinfo-space-in-name.out'), 'r', encoding='utf-8') as f:
        rhel_8_zipinfo_space_in_name = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/rhel-8/zipinfo.json'), 'r', encoding='utf-8') as f:
        rhel_8_zipinfo_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/zipinfo-multi.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_zipinfo_multi_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/rhel-8/zipinfo-space-in-name.json'), 'r', encoding='utf-8') as f:
        rhel_8_zipinfo_space_in_name_json = json.loads(f.read())


    def test_zipinfo_line_separators(self):
        """
        Test 'zipinfo' with line-break characters other than LF in a file name
        """
        data = 'Archive:  log4j-core-2.16.0.jar\nZip file size: 1789565 bytes, number of entries: 2\n-rw-r--r--  2.0 unx    19810 bl defN 21-Dec-12 23:35 META-INF/a\rb\x0bc\x0cd\x1ce\x1df\x1eg\x85h\u2028i\u2029j\ndrwxr-xr-x  2.0 unx        0 b- stor 21-Dec-12 23:35 org/\n2 files, 19810 bytes uncompressed, 19810 bytes compressed:  0.0%\n'
        result = jc.parsers.zipinfo.parse(data, quiet=True)
        self.assertEqual(result[0]['files'][0]['filename'], 'META-INF/a\rb\x0bc\x0cd\x1ce\x1df\x1eg\x85h\u2028i\u2029j')
        self.assertEqual(result[0]['files'][1]['filename'], 'org/')

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

    def test_zipinfo_rhel_8_space_in_name(self):
        """
        Test 'zipinfo' on Red Hat 8 with spaces in the file path
        """
        self.assertEqual(jc.parsers.zipinfo.parse(self.rhel_8_zipinfo_space_in_name, quiet=True), self.rhel_8_zipinfo_space_in_name_json)

    def test_zipinfo_unzip_summary_line(self):
        """
        Test 'zipinfo' with the unzip summary line, which is not a file
        """
        data = self.rhel_8_zipinfo + '\n2 archives were successfully processed.\n'
        self.assertEqual(jc.parsers.zipinfo.parse(data, quiet=True), self.rhel_8_zipinfo_json)


if __name__ == '__main__':
    unittest.main()
