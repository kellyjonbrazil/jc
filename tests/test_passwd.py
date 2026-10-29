import os
import json
import unittest
import jc.parsers.passwd

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/passwd.out'), 'r', encoding='utf-8') as f:
        centos_7_7_passwd = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/passwd.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_passwd = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/passwd.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_passwd = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/passwd.json'), 'r', encoding='utf-8') as f:
        centos_7_7_passwd_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/passwd.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_passwd_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/passwd.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_passwd_json = json.loads(f.read())


    def test_passwd_nodata(self):
        """
        Test 'cat /etc/passwd' with no data
        """
        self.assertEqual(jc.parsers.passwd.parse('', quiet=True), [])

    def test_passwd_whitespace_only_line(self):
        """
        Test 'cat /etc/passwd' with a whitespace-only line
        """
        data = ' \t \njdoe:x:1000:1000:test-user:/home/jdoe:/bin/bash\n'
        expected = [{'username': 'jdoe', 'password': 'x', 'uid': 1000, 'gid': 1000, 'comment': 'test-user', 'home': '/home/jdoe', 'shell': '/bin/bash'}]
        self.assertEqual(jc.parsers.passwd.parse(data, quiet=True), expected)

    def test_passwd_centos_7_7(self):
        """
        Test 'cat /etc/passwd' on Centos 7.7
        """
        self.assertEqual(jc.parsers.passwd.parse(self.centos_7_7_passwd, quiet=True), self.centos_7_7_passwd_json)

    def test_passwd_ubuntu_18_4(self):
        """
        Test 'cat /etc/passwd' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.passwd.parse(self.ubuntu_18_4_passwd, quiet=True), self.ubuntu_18_4_passwd_json)

    def test_passwd_osx_10_14_6(self):
        """
        Test 'cat /etc/passwd' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.passwd.parse(self.osx_10_14_6_passwd, quiet=True), self.osx_10_14_6_passwd_json)


    def test_passwd_line_separator(self):
        """
        Test 'passwd' with a line-break character other than LF inside a field
        """
        data = 'alice:x:1000:1000::/home/alice:/bin/sh\n# note\x0ctoor::0:0::/root:/bin/sh\n'
        result = jc.parsers.passwd.parse(data, quiet=True)
        self.assertEqual([x['username'] for x in result], ['alice'])
        self.assertEqual(result, [{'username': 'alice', 'password': 'x', 'uid': 1000, 'gid': 1000, 'comment': '', 'home': '/home/alice', 'shell': '/bin/sh'}])


    def test_passwd_colon_in_shell(self):
        """
        Test 'passwd' with a colon after the shell field
        """
        data = 'svc:x:1001:1001::/home/svc:/usr/sbin/nologin:x\n'
        expected = [{'username': 'svc', 'password': 'x', 'uid': 1001, 'gid': 1001, 'comment': '', 'home': '/home/svc', 'shell': '/usr/sbin/nologin:x'}]
        self.assertEqual(jc.parsers.passwd.parse(data, quiet=True), expected)

    def test_passwd_nul_byte(self):
        """
        Test 'passwd' with a NUL byte inside an entry
        """
        data = ('backup:x:34:0\x0034:backup:/var/backups:/usr/sbin/nologin\n'
                'svc:x:1001:1001::/home/svc:/bin/bash\x00/usr/sbin/nologin\n'
                'short:x:5\x00:5:c:/h:/s\n'
                'ok:x:7:7:c:/h:/bin/sh\n')
        self.assertEqual(jc.parsers.passwd.parse(data, quiet=True), [
            {'username': 'backup', 'password': 'x', 'uid': 34, 'gid': 0, 'comment': '', 'home': '', 'shell': ''},
            {'username': 'svc', 'password': 'x', 'uid': 1001, 'gid': 1001, 'comment': '', 'home': '/home/svc', 'shell': '/bin/bash'},
            {'username': 'short', 'password': 'x', 'uid': 5, 'gid': None, 'comment': '', 'home': '', 'shell': ''},
            {'username': 'ok', 'password': 'x', 'uid': 7, 'gid': 7, 'comment': 'c', 'home': '/h', 'shell': '/bin/sh'}
        ])
        raw = jc.parsers.passwd.parse(data, raw=True, quiet=True)
        self.assertEqual(raw[0]['gid'], '0')
        self.assertEqual(raw[1]['shell'], '/bin/bash')

    def test_passwd_short_line(self):
        """
        Test 'passwd' with an entry that has too few fields
        """
        self.assertEqual(jc.parsers.passwd.parse('nobody:x\n', quiet=True), [
            {'username': 'nobody', 'password': 'x', 'uid': None, 'gid': None, 'comment': '', 'home': '', 'shell': ''}
        ])


if __name__ == '__main__':
    unittest.main()
