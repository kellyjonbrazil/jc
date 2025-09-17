import os
import unittest
import json
from typing import Dict
from jc.parsers.net_user import parse

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'windows_xp_net_user': (
                'fixtures/windows/windows-xp/net_user.out',
                'fixtures/windows/windows-xp/net_user.json'),
            'windows_7_net_user': (
                'fixtures/windows/windows-7/net_user.out',
                'fixtures/windows/windows-7/net_user.json'),
            'windows_2008_net_user': (
                'fixtures/windows/windows-2008/net_user.out',
                'fixtures/windows/windows-2008/net_user.json'),
            'windows_2016_net_user': (
                'fixtures/windows/windows-2016/net_user.out',
                'fixtures/windows/windows-2016/net_user.json'),
            'windows_10_net_user': (
                'fixtures/windows/windows-10/net_user.out',
                'fixtures/windows/windows-10/net_user.json'),
            'windows_11_net_user': (
                'fixtures/windows/windows-11/net_user.out',
                'fixtures/windows/windows-11/net_user.json'),
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_net_user_nodata(self):
        """
        Test 'net_user' with no data
        """
        self.assertEqual(parse('', quiet=True), {})


    def test_net_user_windows_xp(self):
        """
        Test 'net_user' on Windows XP
        """
        self.assertEqual(
            parse(self.f_in['windows_xp_net_user'], quiet=True),
            self.f_json['windows_xp_net_user']
        )


    def test_net_user_windows_7(self):
        """
        Test 'net_user' on Windows 7
        """
        self.assertEqual(
            parse(self.f_in['windows_7_net_user'], quiet=True),
            self.f_json['windows_7_net_user']
        )


    def test_net_user_windows_2008(self):
        """
        Test 'net_user' on Windows 2008
        """
        self.assertEqual(
            parse(self.f_in['windows_2008_net_user'], quiet=True),
            self.f_json['windows_2008_net_user']
        )


    def test_net_user_windows_2016(self):
        """
        Test 'net_user' on Windows 2016
        """
        self.assertEqual(
            parse(self.f_in['windows_2016_net_user'], quiet=True),
            self.f_json['windows_2016_net_user']
        )


    def test_net_user_windows_10(self):
        """
        Test 'net_user' on Windows 10
        """
        self.assertEqual(
            parse(self.f_in['windows_10_net_user'], quiet=True),
            self.f_json['windows_10_net_user']
        )


    def test_net_user_windows_11(self):
        """
        Test 'net_user' on Windows 11
        """
        self.assertEqual(
            parse(self.f_in['windows_11_net_user'], quiet=True),
            self.f_json['windows_11_net_user']
        )


if __name__ == '__main__':
    unittest.main()
