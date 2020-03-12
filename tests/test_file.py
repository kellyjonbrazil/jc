import os
import unittest
import json
import jc.parsers.file

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/file.out'), 'r', encoding='utf-8') as f:
            self.centos_7_7_file = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/file.out'), 'r', encoding='utf-8') as f:
            self.ubuntu_18_4_file = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/file.out'), 'r', encoding='utf-8') as f:
            self.osx_10_14_6_file = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/file2.out'), 'r', encoding='utf-8') as f:
            self.osx_10_14_6_file2 = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/file.json'), 'r', encoding='utf-8') as f:
            self.centos_7_7_file_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/file.json'), 'r', encoding='utf-8') as f:
            self.ubuntu_18_4_file_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/file.json'), 'r', encoding='utf-8') as f:
            self.osx_10_14_6_file_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/file2.json'), 'r', encoding='utf-8') as f:
            self.osx_10_14_6_file2_json = json.loads(f.read())

    def test_file_centos_7_7(self):
        """
        Test 'file *' on Centos 7.7
        """
        self.assertEqual(jc.parsers.file.parse(self.centos_7_7_file, quiet=True), self.centos_7_7_file_json)

    def test_file_ubuntu_18_4(self):
        """
        Test 'file *' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.file.parse(self.ubuntu_18_4_file, quiet=True), self.ubuntu_18_4_file_json)

    def test_file_osx_10_14_6(self):
        """
        Test 'file *' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.file.parse(self.osx_10_14_6_file, quiet=True), self.osx_10_14_6_file_json)

    def test_file2_osx_10_14_6(self):
        """
        Test 'file *' with filetpe descriptions including colons on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.file.parse(self.osx_10_14_6_file2, quiet=True), self.osx_10_14_6_file2_json)


if __name__ == '__main__':
    unittest.main()
