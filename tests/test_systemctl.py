import os
import json
import unittest
import jc.parsers.systemctl

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/systemctl.out'), 'r', encoding='utf-8') as f:
        centos_7_7_systemctl = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/systemctl.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_systemctl = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/systemctl.json'), 'r', encoding='utf-8') as f:
        centos_7_7_systemctl_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/systemctl.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_systemctl_json = json.loads(f.read())


    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/systemctl-description-load.out'), 'r', encoding='utf-8') as f:
        generic_systemctl_description_load = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/systemctl-description-load.json'), 'r', encoding='utf-8') as f:
        generic_systemctl_description_load_json = json.loads(f.read())

    def test_systemctl_line_separators(self):
        """
        Test 'systemctl' with line-break characters other than LF in a unit description
        """
        data = '  UNIT                                LOAD      ACTIVE   SUB       DESCRIPTION\n  dev-cdrom.device                    loaded    active   plugged   Drive a\rb\x0bc\x0cd\x1ce\x1df\x1eg CDROM\n  sshd.service                        loaded    active   running   OpenSSH\n'
        result = jc.parsers.systemctl.parse(data, quiet=True)
        self.assertEqual(result[0]['description'], 'Drive a\rb\x0bc\x0cd\x1ce\x1df\x1eg CDROM')
        self.assertEqual(result[1]['unit'], 'sshd.service')

    def test_systemctl_legend_footer(self):
        """
        Test 'systemctl --failed' with the 'Legend:' footer of newer systemd
        """
        data = (
            '  UNIT                      LOAD   ACTIVE SUB    DESCRIPTION\n'
            '\u25cf logrotate.service         loaded failed failed Rotate log files\n'
            '\n'
            'Legend: LOAD   \u2192 Reflects whether the unit definition was properly loaded.\n'
            '        ACTIVE \u2192 The high-level unit activation state, i.e. generalization of SUB.\n'
            '        SUB    \u2192 The low-level unit activation state, values depend on unit type.\n'
            '\n'
            '1 loaded units listed.\n'
        )
        self.assertEqual(jc.parsers.systemctl.parse(data, quiet=True), [{
            'unit': 'logrotate.service', 'load': 'loaded', 'active': 'failed',
            'sub': 'failed', 'description': 'Rotate log files'
        }])

    def test_systemctl_nodata(self):
        """
        Test 'systemctl' with no data
        """
        self.assertEqual(jc.parsers.systemctl.parse('', quiet=True), [])

    def test_systemctl_centos_7_7(self):
        """
        Test 'systemctl -a' on Centos 7.7
        """
        self.assertEqual(jc.parsers.systemctl.parse(self.centos_7_7_systemctl, quiet=True), self.centos_7_7_systemctl_json)

    def test_systemctl_ubuntu_18_4(self):
        """
        Test 'systemctl -a' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.systemctl.parse(self.ubuntu_18_4_systemctl, quiet=True), self.ubuntu_18_4_systemctl_json)

    def test_systemctl_description_load(self):
        """
        Test 'systemctl' with a unit description that contains the legend text
        """
        self.assertEqual(jc.parsers.systemctl.parse(self.generic_systemctl_description_load, quiet=True), self.generic_systemctl_description_load_json)



if __name__ == '__main__':
    unittest.main()
