import os
import json
import unittest
import jc.parsers.shadow

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/shadow.out'), 'r', encoding='utf-8') as f:
        centos_7_7_shadow = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/shadow.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_shadow = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/shadow.json'), 'r', encoding='utf-8') as f:
        centos_7_7_shadow_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/shadow.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_shadow_json = json.loads(f.read())

    def test_shadow_nodata(self):
        """
        Test 'cat /etc/shadow' with no data
        """
        self.assertEqual(jc.parsers.shadow.parse('', quiet=True), [])

    def test_shadow_whitespace_only_line(self):
        """
        Test 'cat /etc/shadow' with a whitespace-only line
        """
        data = ' \t \njdoe:!!:18113:0:99999:7:::\n'
        expected = [{'username': 'jdoe', 'password': '!!', 'last_changed': 18113, 'minimum': 0, 'maximum': 99999, 'warn': 7, 'inactive': None, 'expire': None}]
        self.assertEqual(jc.parsers.shadow.parse(data, quiet=True), expected)

    def test_shadow_centos_7_7(self):
        """
        Test 'cat /etc/shadow' on Centos 7.7
        """
        self.assertEqual(jc.parsers.shadow.parse(self.centos_7_7_shadow, quiet=True), self.centos_7_7_shadow_json)

    def test_shadow_ubuntu_18_4(self):
        """
        Test 'cat /etc/shadow' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.shadow.parse(self.ubuntu_18_4_shadow, quiet=True), self.ubuntu_18_4_shadow_json)


    def test_shadow_line_separator(self):
        """
        Test 'shadow' with a line-break character other than LF inside a field
        """
        data = 'alice:!:19000:0:99999:7:::\n# note\x0ctoor::19000:0:99999:7:::\n'
        result = jc.parsers.shadow.parse(data, quiet=True)
        self.assertEqual([x['username'] for x in result], ['alice'])
        self.assertEqual(result, [{'username': 'alice', 'password': '!', 'last_changed': 19000, 'minimum': 0, 'maximum': 99999, 'warn': 7, 'inactive': None, 'expire': None}])

    def test_shadow_nul_byte(self):
        """
        Test 'shadow' with a NUL byte inside an entry
        """
        data = ('root:$6$abc\x00def:19000:0:99999:7:::\n'
                'ok:*:19000:0:99999:7:::\n')
        self.assertEqual(jc.parsers.shadow.parse(data, quiet=True), [
            {'username': 'root', 'password': '$6$abc', 'last_changed': None, 'minimum': None,
             'maximum': None, 'warn': None, 'inactive': None, 'expire': None},
            {'username': 'ok', 'password': '*', 'last_changed': 19000, 'minimum': 0,
             'maximum': 99999, 'warn': 7, 'inactive': None, 'expire': None}
        ])

    def test_shadow_short_line(self):
        """
        Test 'shadow' with an entry that has too few fields
        """
        result = jc.parsers.shadow.parse('daemon:*\n', quiet=True)
        self.assertEqual(result[0]['username'], 'daemon')
        self.assertEqual(result[0]['password'], '*')
        self.assertEqual(result[0]['expire'], None)


if __name__ == '__main__':
    unittest.main()
