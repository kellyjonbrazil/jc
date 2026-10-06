import os
import unittest
import json
from typing import Dict
from jc.parsers.net_localgroup import parse

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'windows_xp_net_localgroup': (
                'fixtures/windows/windows-xp/net_localgroup.out',
                'fixtures/windows/windows-xp/net_localgroup.json'),
            'windows_xp_net_localgroup_administrators': (
                'fixtures/windows/windows-xp/net_localgroup.administrators.out',
                'fixtures/windows/windows-xp/net_localgroup.administrators.json'),
            'windows_7_net_localgroup': (
                'fixtures/windows/windows-7/net_localgroup.out',
                'fixtures/windows/windows-7/net_localgroup.json'),
            'windows_7_net_localgroup_administrators': (
                'fixtures/windows/windows-7/net_localgroup.administrators.out',
                'fixtures/windows/windows-7/net_localgroup.administrators.json'),
            'windows_2008_net_localgroup': (
                'fixtures/windows/windows-2008/net_localgroup.out',
                'fixtures/windows/windows-2008/net_localgroup.json'),
            'windows_2008_net_localgroup_administrators': (
                'fixtures/windows/windows-2008/net_localgroup.administrators.out',
                'fixtures/windows/windows-2008/net_localgroup.administrators.json'),
            'windows_2016_net_localgroup': (
                'fixtures/windows/windows-2016/net_localgroup.out',
                'fixtures/windows/windows-2016/net_localgroup.json'),
            'windows_2016_net_localgroup_administrators': (
                'fixtures/windows/windows-2016/net_localgroup.administrators.out',
                'fixtures/windows/windows-2016/net_localgroup.administrators.json'),
            'windows_10_net_localgroup': (
                'fixtures/windows/windows-10/net_localgroup.out',
                'fixtures/windows/windows-10/net_localgroup.json'),
            'windows_10_net_localgroup_administrators': (
                'fixtures/windows/windows-10/net_localgroup.administrators.out',
                'fixtures/windows/windows-10/net_localgroup.administrators.json'),
            'windows_11_net_localgroup': (
                'fixtures/windows/windows-11/net_localgroup.out',
                'fixtures/windows/windows-11/net_localgroup.json'),
            'windows_11_net_localgroup_administrators': (
                'fixtures/windows/windows-11/net_localgroup.administrators.out',
                'fixtures/windows/windows-11/net_localgroup.administrators.json'),
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_net_localgroup_nodata(self):
        """
        Test 'net_localgroup' with no data
        """
        self.assertEqual(parse('', quiet=True), {})


    def test_net_localgroup_windows_xp(self):
        """
        Test 'net_localgroup' on Windows XP
        """
        self.assertEqual(
            parse(self.f_in['windows_xp_net_localgroup'], quiet=True),
            self.f_json['windows_xp_net_localgroup']
        )

    def test_net_localgroup_administrators_windows_xp(self):
        """
        Test 'net_localgroup' administrators on Windows XP
        """
        self.assertEqual(
            parse(self.f_in['windows_xp_net_localgroup_administrators'], quiet=True),
            self.f_json['windows_xp_net_localgroup_administrators']
        )

    def test_net_localgroup_windows_7(self):
        """
        Test 'net_localgroup' on Windows 7
        """
        self.assertEqual(
            parse(self.f_in['windows_7_net_localgroup'], quiet=True),
            self.f_json['windows_7_net_localgroup']
        )

    def test_net_localgroup_administrators_windows_7(self):
        """
        Test 'net_localgroup' administrators on Windows 7
        """
        self.assertEqual(
            parse(self.f_in['windows_7_net_localgroup_administrators'], quiet=True),
            self.f_json['windows_7_net_localgroup_administrators']
        )

    def test_net_localgroup_windows_2008(self):
        """
        Test 'net_localgroup' on Windows 2008
        """
        self.assertEqual(
            parse(self.f_in['windows_2008_net_localgroup'], quiet=True),
            self.f_json['windows_2008_net_localgroup']
        )

    def test_net_localgroup_administrators_windows_2008(self):
        """
        Test 'net_localgroup' administrators on Windows 2008
        """
        self.assertEqual(
            parse(self.f_in['windows_2008_net_localgroup_administrators'], quiet=True),
            self.f_json['windows_2008_net_localgroup_administrators']
        )

    def test_net_localgroup_windows_2016(self):
        """
        Test 'net_localgroup' on Windows 2016
        """
        self.assertEqual(
            parse(self.f_in['windows_2016_net_localgroup'], quiet=True),
            self.f_json['windows_2016_net_localgroup']
        )

    def test_net_localgroup_administrators_windows_2016(self):
        """
        Test 'net_localgroup' administrators on Windows 2016
        """
        self.assertEqual(
            parse(self.f_in['windows_2016_net_localgroup_administrators'], quiet=True),
            self.f_json['windows_2016_net_localgroup_administrators']
        )

    def test_net_localgroup_windows_10(self):
        """
        Test 'net_localgroup' on Windows 10
        """
        self.assertEqual(
            parse(self.f_in['windows_10_net_localgroup'], quiet=True),
            self.f_json['windows_10_net_localgroup']
        )

    def test_net_localgroup_administrators_windows_10(self):
        """
        Test 'net_localgroup' administrators on Windows 10
        """
        self.assertEqual(
            parse(self.f_in['windows_10_net_localgroup_administrators'], quiet=True),
            self.f_json['windows_10_net_localgroup_administrators']
        )

    def test_net_localgroup_windows_11(self):
        """
        Test 'net_localgroup' on Windows 11
        """
        self.assertEqual(
            parse(self.f_in['windows_11_net_localgroup'], quiet=True),
            self.f_json['windows_11_net_localgroup']
        )

    def test_net_localgroup_administrators_windows_11(self):
        """
        Test 'net_localgroup' administrators on Windows 11
        """
        self.assertEqual(
            parse(self.f_in['windows_11_net_localgroup_administrators'], quiet=True),
            self.f_json['windows_11_net_localgroup_administrators']
        )


if __name__ == '__main__':
    unittest.main()
