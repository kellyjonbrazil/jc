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
            'generic_net_user_header_like_names': (
                'fixtures/generic/net_user-header-like-names.out',
                'fixtures/generic/net_user-header-like-names.json'),
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


    def test_net_user_line_separator(self):
        """
        Test 'net_user' with a line-break character other than LF inside a field
        """
        data = "User name                    Administrator\r\nUser's comment               x\x0cAccount active               No\x0cThe command completed\x0cUser name                    svc_backup\r\nAccount active               Yes\r\nThe command completed successfully.\r\n"
        result = parse(data, quiet=True)
        self.assertEqual(len(result['user_accounts']), 1)
        self.assertEqual(result['user_accounts'][0]['user_name'], 'Administrator')
        self.assertEqual(result['user_accounts'][0]['account_active'], True)
        self.assertEqual(result['user_accounts'][0]['users_comment'], 'x\x0cAccount active               No\x0cThe command completed\x0cUser name                    svc_backup')

    def test_net_user_group_line_without_group_list(self):
        """
        Test 'net_user' group membership lines whose value is not a group list
        """
        data = "User name                    x\nLocal Group Memberships      " + "Local Group Memberships".ljust(29) * 50 + "\nGlobal Group memberships     *Users\nThe command completed successfully.\n"
        result = parse(data, quiet=True)
        self.assertEqual(result['user_accounts'][0]['local_group_memberships'], [])
        self.assertEqual(result['user_accounts'][0]['global_group_memberships'], ['Users'])


    def test_net_user_header_like_names(self):
        """
        Test 'net_user' with user names that look like the header or the dashed line
        """
        self.assertEqual(
            parse(self.f_in['generic_net_user_header_like_names'], quiet=True),
            self.f_json['generic_net_user_header_like_names']
        )


if __name__ == '__main__':
    unittest.main()
