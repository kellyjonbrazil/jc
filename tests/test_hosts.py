import os
import json
import unittest
import jc.parsers.hosts

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/hosts.out'), 'r', encoding='utf-8') as f:
        centos_7_7_hosts = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/hosts.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_hosts = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/hosts.json'), 'r', encoding='utf-8') as f:
        centos_7_7_hosts_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/hosts.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_hosts_json = json.loads(f.read())


    def test_hosts_nodata(self):
        """
        Test 'cat /etc/hosts' with no data
        """
        self.assertEqual(jc.parsers.hosts.parse('', quiet=True), [])

    def test_hosts_whitespace_only_line(self):
        """
        Test 'cat /etc/hosts' with a whitespace-only line
        """
        data = ' \t \n127.0.0.1 localhost\n'
        expected = [{'ip': '127.0.0.1', 'hostname': ['localhost']}]
        self.assertEqual(jc.parsers.hosts.parse(data, quiet=True), expected)

    def test_hosts_centos_7_7(self):
        """
        Test 'cat /etc/hosts' on Centos 7.7
        """
        self.assertEqual(jc.parsers.hosts.parse(self.centos_7_7_hosts, quiet=True), self.centos_7_7_hosts_json)

    def test_hosts_ubuntu_18_4(self):
        """
        Test 'cat /etc/hosts' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.hosts.parse(self.ubuntu_18_4_hosts, quiet=True), self.ubuntu_18_4_hosts_json)


    def test_hosts_line_separator(self):
        """
        Test 'hosts' with a line-break character other than LF inside a field
        """
        data = '203.0.113.66\tmirror.example.net\x0c10.0.0.5\tupdates.example.com\n'
        result = jc.parsers.hosts.parse(data, quiet=True)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['ip'], '203.0.113.66')
        self.assertEqual(result[0]['hostname'], ['mirror.example.net', '10.0.0.5', 'updates.example.com'])

    def test_hosts_cr_line_endings(self):
        """
        Test 'hosts' with CR-only line endings
        """
        data = '127.0.0.1\tlocalhost\r10.0.0.1\thost1 h1\r'
        expected = [{'ip': '127.0.0.1', 'hostname': ['localhost']}, {'ip': '10.0.0.1', 'hostname': ['host1', 'h1']}]
        self.assertEqual(jc.parsers.hosts.parse(data, quiet=True), expected)


    def test_hosts_other_whitespace_in_field(self):
        """
        Test 'hosts' splits fields on ASCII whitespace only
        """
        data = '10.0.0.5\xa0vault.example.com\n0.0.0.0 ads.example.net\xa0tracker.example.net\n'
        expected = [{'ip': '10.0.0.5\xa0vault.example.com', 'hostname': []}, {'ip': '0.0.0.0', 'hostname': ['ads.example.net\xa0tracker.example.net']}]
        self.assertEqual(jc.parsers.hosts.parse(data, quiet=True), expected)

    def test_hosts_comment_inside_word(self):
        """
        Test 'hosts' cuts each line at the first '#' even when it is in the middle of a word
        """
        data = '127.0.0.1 localhost#c\n10.0.0.2#x host2\n10.0.0.3 a b#c d\n10.0.0.4\tvault\t# note\n'
        expected = [
            {'ip': '127.0.0.1', 'hostname': ['localhost']},
            {'ip': '10.0.0.2', 'hostname': []},
            {'ip': '10.0.0.3', 'hostname': ['a', 'b']},
            {'ip': '10.0.0.4', 'hostname': ['vault']}
        ]
        self.assertEqual(jc.parsers.hosts.parse(data, quiet=True), expected)


if __name__ == '__main__':
    unittest.main()
