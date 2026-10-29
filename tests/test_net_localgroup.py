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


    def test_net_localgroup_line_separator(self):
        """
        Test 'net_localgroup' with a line-break character other than LF inside a field
        """
        data = 'Alias name     Administrators\r\nComment\r\n\r\nMembers\r\n\r\n-------------------------------------------------------------------------------\r\nAdministrator\r\nCORP\\aa\u2028The command completed successfully.\u2028x\r\nCORP\\Domain Admins\r\nuser1\r\nThe command completed successfully.\r\n'
        result = parse(data, quiet=True)
        self.assertEqual(result['groups'][0]['members'], ['Administrator', 'CORP\\aa\u2028The command completed successfully.\u2028x', 'CORP\\Domain Admins', 'user1'])


    def test_net_localgroup_other_whitespace_in_name(self):
        """
        Test 'net_localgroup' only trims space and tab from member names
        """
        data = 'Alias name     Server Admins\nComment\n\nMembers\n\n-------------------------------------------------------------------------------\n\xa0\nalice\xa0\nThe command completed successfully.\xa0\nbob\nThe command completed successfully.\n'
        result = parse(data, quiet=True)
        self.assertEqual(result['groups'], [{'name': 'Server Admins', 'members': ['\xa0', 'alice\xa0', 'The command completed successfully.\xa0', 'bob']}])


if __name__ == '__main__':
    unittest.main()
