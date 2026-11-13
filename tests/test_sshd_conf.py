import os
import unittest
import json
from typing import Dict
import jc.parsers.sshd_conf

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'sshd_t': (
                'fixtures/generic/sshd-T.out',
                'fixtures/generic/sshd-T.json'),
            'sshd_t_2': (
                'fixtures/generic/sshd-T-2.out',
                'fixtures/generic/sshd-T-2.json'),
            'sshd_config': (
                'fixtures/generic/sshd_config',
                'fixtures/generic/sshd_config.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_sshd_conf_line_separators(self):
        """
        Test 'sshd config file' with line-break characters other than LF in a value
        """
        data = 'Banner /etc/a\rb\x0bc\x0cd\x1ce\x1df\x1eg\x85h\u2028i\u2029j\nPort 22\n'
        result = jc.parsers.sshd_conf.parse(data, quiet=True)
        self.assertEqual(result['banner'], '/etc/a\rb\x0bc\x0cd\x1ce\x1df\x1eg\x85h\u2028i\u2029j')
        self.assertEqual(result['port'], [22])

    def test_sshd_conf_nodata(self):
        """
        Test 'sshd_conf' with no data
        """
        self.assertEqual(jc.parsers.sshd_conf.parse('', quiet=True), {})

    def test_sshd_T(self):
        """
        Test 'sshd -T'
        """
        self.assertEqual(jc.parsers.sshd_conf.parse(self.f_in['sshd_t'], quiet=True),
                                                    self.f_json['sshd_t'])

    def test_sshd_T_2(self):
        """
        Test 'sshd -T' with another sample
        """
        self.assertEqual(jc.parsers.sshd_conf.parse(self.f_in['sshd_t_2'], quiet=True),
                                                    self.f_json['sshd_t_2'])

    def test_sshd_config(self):
        """
        Test 'cat sshd_config'
        """
        self.assertEqual(jc.parsers.sshd_conf.parse(self.f_in['sshd_config'], quiet=True),
                                                    self.f_json['sshd_config'])

    def test_sshd_conf_match_case_insensitive(self):
        """
        Test 'sshd_conf' with lowercase and mixed case Match keywords
        """
        data = (
            'PermitRootLogin yes\n'
            'match User nobody\n'
            '    PermitRootLogin no\n'
            '    Banner none\n'
            'MATCH   ALL\n'
            'PasswordAuthentication yes\n'
            'Match user other\n'
            '    PasswordAuthentication no\n'
            'mAtCh\tAll\n'
            'X11Forwarding no\n'
        )
        expected = {
            'permitrootlogin': 'yes',
            'passwordauthentication': 'yes',
            'x11forwarding': 'no'
        }
        self.assertEqual(jc.parsers.sshd_conf.parse(data, quiet=True), expected)

    def test_sshd_conf_first_value_wins(self):
        """
        Test 'sshd_conf' with repeated keywords
        """
        data = (
            'Port 22\n'
            'PermitRootLogin yes\n'
            'PasswordAuthentication yes\n'
            'Ciphers +aes128-ctr\n'
            'Subsystem sftp /usr/lib/openssh/sftp-server\n'
            'AllowUsers alice bob\n'
            'AllowUsers carol\n'
            'DenyUsers dave\n'
            'AllowGroups staff\n'
            'DenyGroups guests\n'
            'DenyGroups temps\n'
            'Port 2222\n'
            'PermitRootLogin no\n'
            'PasswordAuthentication no\n'
            'Ciphers aes256-ctr\n'
            'Subsystem sftp internal-sftp\n'
            'HostKey /etc/ssh/ssh_host_rsa_key\n'
            'HostKey /etc/ssh/ssh_host_ed25519_key\n'
            'ListenAddress 0.0.0.0\n'
            'ListenAddress ::\n'
            'AcceptEnv LANG\n'
            'AcceptEnv LC_*\n'
        )
        expected = {
            'port': [22, 2222],
            'permitrootlogin': 'yes',
            'passwordauthentication': 'yes',
            'ciphers': ['aes128-ctr'],
            'ciphers_strategy': '+',
            'subsystem': 'sftp',
            'subsystem_command': '/usr/lib/openssh/sftp-server',
            'allowusers': 'alice bob carol',
            'denyusers': 'dave',
            'allowgroups': 'staff',
            'denygroups': 'guests temps',
            'hostkey': ['/etc/ssh/ssh_host_rsa_key', '/etc/ssh/ssh_host_ed25519_key'],
            'listenaddress': ['0.0.0.0', '::'],
            'acceptenv': ['LANG', 'LC_*']
        }
        self.assertEqual(jc.parsers.sshd_conf.parse(data, quiet=True), expected)

    def test_sshd_conf_sshd_T_repeated_allow_deny(self):
        """
        Test 'sshd -T' output with one AllowUsers line per user
        """
        data = (
            'allowusers alice\n'
            'allowusers bob\n'
            'denygroups guests\n'
            'denygroups temps\n'
        )
        expected = {'allowusers': 'alice bob', 'denygroups': 'guests temps'}
        self.assertEqual(jc.parsers.sshd_conf.parse(data, quiet=True), expected)

    def test_sshd_conf_time_and_size_suffixes(self):
        """
        Test 'sshd_conf' with time and size suffixes
        """
        data = (
            'LoginGraceTime 2m\n'
            'ClientAliveInterval 1h30m\n'
            'RekeyLimit 1G 1H\n'
        )
        expected = {
            'logingracetime': 120,
            'clientaliveinterval': 5400,
            'rekeylimit': 1073741824,
            'rekeylimit_time': 3600
        }
        self.assertEqual(jc.parsers.sshd_conf.parse(data, quiet=True), expected)

    def test_sshd_conf_time_formats(self):
        """
        Test 'sshd_conf' with each time qualifier, upper case qualifiers and invalid times
        """
        cases = [
            ('90', 90),
            ('0', 0),
            ('1s', 1),
            ('2m', 120),
            ('1h', 3600),
            ('1d', 86400),
            ('1w', 604800),
            ('1W2D3H4M5S', 604800 + 2 * 86400 + 3 * 3600 + 4 * 60 + 5),
            ('1m30s', 90),
            ('1h30', 3630),
            ('300 # keepalive', 300),
            ('1.5h', None),
            ('-1', None),
            ('2x', None),
            ('m', None),
            ('1m 30s', 60),
            ('99999999999w', None),
            ('9' * 5000, None)
        ]
        for value, seconds in cases:
            with self.subTest(value=value):
                result = jc.parsers.sshd_conf.parse('LoginGraceTime ' + value, quiet=True)
                self.assertEqual(result, {'logingracetime': seconds})

    def test_sshd_conf_rekeylimit_formats(self):
        """
        Test 'sshd_conf' with RekeyLimit sizes and times
        """
        cases = [
            ('0 0', 0, 0),
            ('4096', 4096, None),
            ('1K', 1024, None),
            ('2m 10m', 2097152, 600),
            ('1g 1d', 1073741824, 86400),
            ('1.5G', 1610612736, None),
            ('default none', None, None),
            ('1GB 1h', None, 3600),
            ('1G 1.5h', 1073741824, None)
        ]
        for value, size, seconds in cases:
            with self.subTest(value=value):
                result = jc.parsers.sshd_conf.parse('RekeyLimit ' + value, quiet=True)
                expected = {'rekeylimit': size}
                if seconds is not None or ' ' in value:
                    expected['rekeylimit_time'] = seconds
                self.assertEqual(result, expected)

    def test_sshd_conf_time_suffixes_raw(self):
        """
        Test 'sshd_conf' raw output keeps time and size strings
        """
        data = 'LoginGraceTime 2m\nRekeyLimit 1G 1h\n'
        expected = {'logingracetime': '2m', 'rekeylimit': '1G 1h'}
        self.assertEqual(jc.parsers.sshd_conf.parse(data, raw=True, quiet=True), expected)

    def test_sshd_conf_keyword_without_value(self):
        """
        Test 'sshd_conf' with lines that have only one word
        """
        data = 'Port\nBanner\nPermitRootLogin no\nAllowUsers\n'
        self.assertEqual(jc.parsers.sshd_conf.parse(data, quiet=True), {'permitrootlogin': 'no'})


if __name__ == '__main__':
    unittest.main()
