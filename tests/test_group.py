import os
import json
import unittest
import jc.parsers.group

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/group.out'), 'r', encoding='utf-8') as f:
        centos_7_7_group = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/group.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_group = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/group.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_group = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/group.json'), 'r', encoding='utf-8') as f:
        centos_7_7_group_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/group.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_group_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/group.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_group_json = json.loads(f.read())


    def test_group_nodata(self):
        """
        Test 'cat /etc/group' with no data
        """
        self.assertEqual(jc.parsers.group.parse('', quiet=True), [])

    def test_group_whitespace_only_line(self):
        """
        Test 'cat /etc/group' with a whitespace-only line
        """
        data = ' \t \nwheel:x:10:jdoe\n'
        expected = [{'group_name': 'wheel', 'password': 'x', 'gid': 10, 'members': ['jdoe']}]
        self.assertEqual(jc.parsers.group.parse(data, quiet=True), expected)

    def test_group_centos_7_7(self):
        """
        Test 'cat /etc/group' on Centos 7.7
        """
        self.assertEqual(jc.parsers.group.parse(self.centos_7_7_group, quiet=True), self.centos_7_7_group_json)

    def test_group_ubuntu_18_4(self):
        """
        Test 'cat /etc/group' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.group.parse(self.ubuntu_18_4_group, quiet=True), self.ubuntu_18_4_group_json)

    def test_group_osx_10_14_6(self):
        """
        Test 'cat /etc/group' on OSX 10.14
        """
        self.assertEqual(jc.parsers.group.parse(self.osx_10_14_6_group, quiet=True), self.osx_10_14_6_group_json)


    def test_group_line_separator(self):
        """
        Test 'group' with a line-break character other than LF inside a field
        """
        data = 'sudo:x:27:joeuser,x\x0c#,www-data\n'
        result = jc.parsers.group.parse(data, quiet=True)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['members'], ['joeuser', 'x\x0c#', 'www-data'])


    def test_group_colon_in_members(self):
        """
        Test 'group' with a colon in the member list
        """
        data = 'sudo:x:27:joeuser,x:,www-data\nempty:x:28::,www-data\n'
        expected = [
            {'group_name': 'sudo', 'password': 'x', 'gid': 27, 'members': ['joeuser', 'x:', 'www-data']},
            {'group_name': 'empty', 'password': 'x', 'gid': 28, 'members': [':', 'www-data']}
        ]
        self.assertEqual(jc.parsers.group.parse(data, quiet=True), expected)

    def test_group_whitespace(self):
        """
        Test 'group' with blanks before members, group names and comments
        """
        data = ('sudo:x:27:joeuser, www-data\n'
                ' \tadm:x:4:\t syslog ,bin\n'
                '  # wheel:x:10:jdoe\n'
                '   #\n'
                'users:x:100: \n')
        self.assertEqual(jc.parsers.group.parse(data, quiet=True), [
            {'group_name': 'sudo', 'password': 'x', 'gid': 27, 'members': ['joeuser', 'www-data']},
            {'group_name': 'adm', 'password': 'x', 'gid': 4, 'members': ['syslog', 'bin']},
            {'group_name': 'users', 'password': 'x', 'gid': 100, 'members': []}
        ])

    def test_group_nul_byte(self):
        """
        Test 'group' with a NUL byte inside an entry
        """
        data = 'dev:x:1\x0023:bob\nops:x:5:amy,bo\x00b\nlast:x:6:z\n'
        self.assertEqual(jc.parsers.group.parse(data, quiet=True), [
            {'group_name': 'dev', 'password': 'x', 'gid': 1, 'members': []},
            {'group_name': 'ops', 'password': 'x', 'gid': 5, 'members': ['amy', 'bo']},
            {'group_name': 'last', 'password': 'x', 'gid': 6, 'members': ['z']}
        ])
        self.assertEqual(jc.parsers.group.parse('dev:x\x00:1:a\n', quiet=True), [
            {'group_name': 'dev', 'password': 'x', 'gid': None, 'members': []}
        ])


if __name__ == '__main__':
    unittest.main()
