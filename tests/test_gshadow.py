import os
import json
import unittest
import jc.parsers.gshadow

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/gshadow.out'), 'r', encoding='utf-8') as f:
        centos_7_7_gshadow = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/gshadow.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_gshadow = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/gshadow.json'), 'r', encoding='utf-8') as f:
        centos_7_7_gshadow_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/gshadow.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_gshadow_json = json.loads(f.read())


    def test_gshadow_nodata(self):
        """
        Test 'cat /etc/gshadow' with no data
        """
        self.assertEqual(jc.parsers.gshadow.parse('', quiet=True), [])

    def test_gshadow_whitespace_only_line(self):
        """
        Test 'cat /etc/gshadow' with a whitespace-only line
        """
        data = ' \t \nwheel:::jdoe\n'
        expected = [{'group_name': 'wheel', 'password': '', 'administrators': [], 'members': ['jdoe']}]
        self.assertEqual(jc.parsers.gshadow.parse(data, quiet=True), expected)

    def test_gshadow_centos_7_7(self):
        """
        Test 'cat /etc/gshadow' on Centos 7.7
        """
        self.assertEqual(jc.parsers.gshadow.parse(self.centos_7_7_gshadow, quiet=True), self.centos_7_7_gshadow_json)

    def test_gshadow_ubuntu_18_4(self):
        """
        Test 'cat /etc/gshadow' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.gshadow.parse(self.ubuntu_18_4_gshadow, quiet=True), self.ubuntu_18_4_gshadow_json)


    def test_gshadow_line_separator(self):
        """
        Test 'gshadow' with a line-break character other than LF inside a field
        """
        data = 'ops:!::alice,\u2028#y,carol\nstaff:!::alice\u2028sudo::bob:bob\n'
        result = jc.parsers.gshadow.parse(data, quiet=True)
        self.assertEqual([x['group_name'] for x in result], ['ops', 'staff'])
        self.assertEqual(result[0]['members'], ['alice', '\u2028#y', 'carol'])
        self.assertEqual(result[1]['members'], ['alice\u2028sudo::bob:bob'])


    def test_gshadow_colon_in_members(self):
        """
        Test 'gshadow' with a colon in the member list
        """
        data = 'sudo:*::alice,x:,bob\n'
        expected = [{'group_name': 'sudo', 'password': '*', 'administrators': [], 'members': ['alice', 'x:', 'bob']}]
        self.assertEqual(jc.parsers.gshadow.parse(data, quiet=True), expected)

    def test_gshadow_whitespace(self):
        """
        Test 'gshadow' with blanks before names, members and comments
        """
        data = (' \tsudo:*:root, joe:amy,\t bob\n'
                '  # wheel:*::\n'
                'users:!: :\n')
        self.assertEqual(jc.parsers.gshadow.parse(data, quiet=True), [
            {'group_name': 'sudo', 'password': '*', 'administrators': ['root', 'joe'], 'members': ['amy', 'bob']},
            {'group_name': 'users', 'password': '!', 'administrators': [], 'members': []}
        ])

    def test_gshadow_nul_byte(self):
        """
        Test 'gshadow' with a NUL byte inside an entry
        """
        data = 'dev:*:root\x00:bob\nops:!::amy\n'
        self.assertEqual(jc.parsers.gshadow.parse(data, quiet=True), [
            {'group_name': 'dev', 'password': '*', 'administrators': ['root'], 'members': []},
            {'group_name': 'ops', 'password': '!', 'administrators': [], 'members': ['amy']}
        ])


if __name__ == '__main__':
    unittest.main()
