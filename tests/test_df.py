import os
import json
import unittest
import jc.parsers.df

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/df.out'), 'r') as f:
            self.centos_7_7_df = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/df.out'), 'r') as f:
            self.ubuntu_18_4_df = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/df.out'), 'r') as f:
            self.osx_10_11_6_df = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/df.out'), 'r') as f:
            self.osx_10_14_6_df = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/df-h.out'), 'r') as f:
            self.centos_7_7_df_h = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/df-h.out'), 'r') as f:
            self.ubuntu_18_4_df_h = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/df-h.out'), 'r') as f:
            self.osx_10_11_6_df_h = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/df-h.out'), 'r') as f:
            self.osx_10_14_6_df_h = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/df.json'), 'r') as f:
            self.centos_7_7_df_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/df.json'), 'r') as f:
            self.ubuntu_18_4_df_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/df.json'), 'r') as f:
            self.osx_10_11_6_df_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/df.json'), 'r') as f:
            self.osx_10_14_6_df_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/df-h.json'), 'r') as f:
            self.centos_7_7_df_h_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/df-h.json'), 'r') as f:
            self.ubuntu_18_4_df_h_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/df-h.json'), 'r') as f:
            self.osx_10_11_6_df_h_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/df-h.json'), 'r') as f:
            self.osx_10_14_6_df_h_json = json.loads(f.read())

    def test_df_centos_7_7(self):
        """
        Test plain 'df' on Centos 7.7
        """
        self.assertEqual(jc.parsers.df.parse(self.centos_7_7_df, quiet=True), self.centos_7_7_df_json)

    def test_df_ubuntu_18_4(self):
        """
        Test plain 'df' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.df.parse(self.ubuntu_18_4_df, quiet=True), self.ubuntu_18_4_df_json)

    def test_df_osx_10_11_6(self):
        """
        Test plain 'df' on OSX 10.11.6
        """
        self.assertEqual(jc.parsers.df.parse(self.osx_10_11_6_df, quiet=True), self.osx_10_11_6_df_json)

    def test_df_osx_10_14_6(self):
        """
        Test plain 'df' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.df.parse(self.osx_10_14_6_df, quiet=True), self.osx_10_14_6_df_json)

    def test_df_h_centos_7_7(self):
        """
        Test 'df -h' on Centos 7.7
        """
        self.assertEqual(jc.parsers.df.parse(self.centos_7_7_df_h, quiet=True), self.centos_7_7_df_h_json)

    def test_df_h_ubuntu_18_4(self):
        """
        Test 'df -h' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.df.parse(self.ubuntu_18_4_df_h, quiet=True), self.ubuntu_18_4_df_h_json)

    def test_df_h_osx_10_11_6(self):
        """
        Test 'df -h' on OSX 10.11.6
        """
        self.assertEqual(jc.parsers.df.parse(self.osx_10_11_6_df_h, quiet=True), self.osx_10_11_6_df_h_json)

    def test_df_h_osx_10_14_6(self):
        """
        Test 'df -h' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.df.parse(self.osx_10_14_6_df_h, quiet=True), self.osx_10_14_6_df_h_json)


if __name__ == '__main__':
    unittest.main()
