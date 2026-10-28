import os
import unittest
import json
from typing import Dict
from jc.parsers.ssh_conf import parse

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'ssh_config1': (
                'fixtures/generic/ssh_config1',
                'fixtures/generic/ssh_config1.json'),
            'ssh_config2': (
                'fixtures/generic/ssh_config2',
                'fixtures/generic/ssh_config2.json'),
            'ssh_config3': (
                'fixtures/generic/ssh_config3',
                'fixtures/generic/ssh_config3.json'),
            'ssh_config4': (
                'fixtures/generic/ssh_config4',
                'fixtures/generic/ssh_config4.json'),
            'ssh_config5': (
                'fixtures/generic/ssh_config5',
                'fixtures/generic/ssh_config5.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_ssh_nodata(self):
        """
        Test 'ssh' with no data
        """
        self.assertEqual(parse('', quiet=True), [])


    def test_ssh_config1(self):
        """
        Test 'ssh' config 1
        """
        self.assertEqual(
            parse(self.f_in['ssh_config1'], quiet=True),
            self.f_json['ssh_config1']
        )

    def test_ssh_config2(self):
        """
        Test 'ssh' config 2
        """
        self.assertEqual(
            parse(self.f_in['ssh_config2'], quiet=True),
            self.f_json['ssh_config2']
        )

    def test_ssh_config3(self):
        """
        Test 'ssh' config 3
        """
        self.assertEqual(
            parse(self.f_in['ssh_config3'], quiet=True),
            self.f_json['ssh_config3']
        )

    def test_ssh_config4(self):
        """
        Test 'ssh' config 4
        """
        self.assertEqual(
            parse(self.f_in['ssh_config4'], quiet=True),
            self.f_json['ssh_config4']
        )

    def test_ssh_config5(self):
        """
        Test 'ssh' config 5
        """
        self.assertEqual(
            parse(self.f_in['ssh_config5'], quiet=True),
            self.f_json['ssh_config5']
        )

    def test_ssh_conf_match_case_insensitive(self):
        """
        Test 'ssh_conf' with lowercase and mixed case Match keywords
        """
        data = (
            'Host a\n'
            '    User one\n'
            'match host bastion\n'
            '    User two\n'
            '    Port 2222\n'
            'MATCH   ALL\n'
            '    Compression yes\n'
            'Match host other\n'
            '    Compression no\n'
            'mAtCh\tAll\n'
            '    ForwardAgent no\n'
        )
        expected = [
            {
                'host': 'a',
                'host_list': ['a'],
                'user': 'one',
                'compression': 'yes',
                'forwardagent': 'no'
            }
        ]
        self.assertEqual(parse(data, quiet=True), expected)

    def test_ssh_conf_host_ends_match_block(self):
        """
        Test 'ssh_conf' with Host blocks after a Match block
        """
        data = (
            'Match host bastion\n'
            '    ProxyJump jump.example.com\n'
            '\n'
            'Host prod-*\n'
            '    User root\n'
            '    IdentityFile ~/.ssh/prod_key\n'
            '    StrictHostKeyChecking no\n'
            '\n'
            'Match user admin\n'
            '    Port 2222\n'
            'host *\n'
            '    ServerAliveInterval 60\n'
        )
        expected = [
            {
                'host': 'prod-*',
                'host_list': ['prod-*'],
                'user': 'root',
                'identityfile': ['~/.ssh/prod_key'],
                'stricthostkeychecking': 'no'
            },
            {
                'host': '*',
                'host_list': ['*'],
                'serveraliveinterval': 60
            }
        ]
        self.assertEqual(parse(data, quiet=True), expected)

    def test_ssh_conf_first_value_wins(self):
        """
        Test 'ssh_conf' with repeated keywords
        """
        data = (
            'Host a\n'
            '    User one\n'
            '    User two\n'
            '    StrictHostKeyChecking no\n'
            '    StrictHostKeyChecking yes\n'
            '    IdentityFile ~/.ssh/k1\n'
            '    IdentityFile ~/.ssh/k2\n'
            '    LocalForward 8080 localhost:80\n'
            '    LocalForward 8443 localhost:443\n'
            '    Ciphers +aes128-ctr\n'
            '    Ciphers aes256-ctr\n'
            'Host b\n'
            '    User three\n'
        )
        expected = [
            {
                'host': 'a',
                'host_list': ['a'],
                'user': 'one',
                'stricthostkeychecking': 'no',
                'identityfile': ['~/.ssh/k1', '~/.ssh/k2'],
                'localforward': ['8080 localhost:80', '8443 localhost:443'],
                'ciphers': ['aes128-ctr'],
                'ciphers_strategy': '+'
            },
            {
                'host': 'b',
                'host_list': ['b'],
                'user': 'three'
            }
        ]
        self.assertEqual(parse(data, quiet=True), expected)

    def test_ssh_conf_time_suffixes(self):
        """
        Test 'ssh_conf' with time suffixes
        """
        data = (
            'Host a\n'
            '    ServerAliveInterval 1m30s\n'
            '    ConnectTimeout 10\n'
            '    ForwardX11Timeout 20M\n'
            '    ControlPersist 10m\n'
            '    RekeyLimit 1G 1h\n'
            'Host b\n'
            '    ServerAliveInterval 1.5h\n'
            '    ConnectTimeout none\n'
            '    ForwardX11Timeout 1d\n'
            '    ControlPersist yes\n'
        )
        expected = [
            {
                'host': 'a',
                'host_list': ['a'],
                'serveraliveinterval': 90,
                'connecttimeout': 10,
                'forwardx11timeout': 1200,
                'controlpersist': 600,
                'rekeylimit': 1073741824,
                'rekeylimit_time': 3600
            },
            {
                'host': 'b',
                'host_list': ['b'],
                'serveraliveinterval': None,
                'connecttimeout': None,
                'forwardx11timeout': 86400,
                'controlpersist': 'yes'
            }
        ]
        self.assertEqual(parse(data, quiet=True), expected)

    def test_ssh_conf_forwards_are_lists(self):
        """
        Test 'ssh_conf' with repeated RemoteForward and DynamicForward
        """
        data = (
            'Host a\n'
            '    RemoteForward 9000 localhost:9000\n'
            '    RemoteForward 9001 localhost:9001\n'
            '    DynamicForward 1080\n'
            '    DynamicForward 127.0.0.1:1081\n'
        )
        expected = [
            {
                'host': 'a',
                'host_list': ['a'],
                'remoteforward': ['9000 localhost:9000', '9001 localhost:9001'],
                'dynamicforward': ['1080', '127.0.0.1:1081']
            }
        ]
        self.assertEqual(parse(data, quiet=True), expected)

    def test_ssh_conf_rekeylimit_controlpersist(self):
        """
        Test 'ssh_conf' with RekeyLimit and ControlPersist values
        """
        cases = [
            ('RekeyLimit 0 0', {'rekeylimit': 0, 'rekeylimit_time': 0}),
            ('RekeyLimit 4G', {'rekeylimit': 4294967296}),
            ('RekeyLimit 512m 2h', {'rekeylimit': 536870912, 'rekeylimit_time': 7200}),
            ('RekeyLimit default none', {'rekeylimit': 'default', 'rekeylimit_time': 'none'}),
            ('RekeyLimit 1G none', {'rekeylimit': 1073741824, 'rekeylimit_time': 'none'}),
            ('RekeyLimit 1GB 1.5h', {'rekeylimit': None, 'rekeylimit_time': None}),
            ('ControlPersist yes', {'controlpersist': 'yes'}),
            ('ControlPersist no', {'controlpersist': 'no'}),
            ('ControlPersist 0', {'controlpersist': 0}),
            ('ControlPersist 4h', {'controlpersist': 14400}),
            ('ControlPersist 1h30m', {'controlpersist': 5400}),
            ('ControlPersist soon', {'controlpersist': None})
        ]
        for line, expected in cases:
            with self.subTest(line=line):
                self.assertEqual(parse(line, quiet=True), [expected])

    def test_ssh_conf_hostkeyalgorithms_modifier(self):
        """
        Test 'ssh_conf' with a HostKeyAlgorithms modifier
        """
        data = 'Host a\n    HostKeyAlgorithms +ssh-rsa,ssh-dss\n'
        expected = [
            {
                'host': 'a',
                'host_list': ['a'],
                'hostkeyalgorithms': ['ssh-rsa', 'ssh-dss'],
                'hostkeyalgorithms_strategy': '+'
            }
        ]
        self.assertEqual(parse(data, quiet=True), expected)


if __name__ == '__main__':
    unittest.main()
