import os
import unittest
import json
import jc.parsers.nmcli
from jc.exceptions import ParseError

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/nmcli.out'), 'r', encoding='utf-8') as f:
        centos_7_7_nmcli = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/nmcli-connection-all.out'), 'r', encoding='utf-8') as f:
        centos_7_7_nmcli_connection_all = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/nmcli-connection-show-ens33.out'), 'r', encoding='utf-8') as f:
        centos_7_7_nmcli_connection_show_ens33 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/nmcli-connection.out'), 'r', encoding='utf-8') as f:
        centos_7_7_nmcli_connection = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/nmcli-device-all.out'), 'r', encoding='utf-8') as f:
        centos_7_7_nmcli_device_all = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/nmcli-device-show-ens33.out'), 'r', encoding='utf-8') as f:
        centos_7_7_nmcli_device_show_ens33 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/nmcli-device-show-lo.out'), 'r', encoding='utf-8') as f:
        centos_7_7_nmcli_device_show_lo = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/nmcli-device-show.out'), 'r', encoding='utf-8') as f:
        centos_7_7_nmcli_device_show = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/nmcli-device.out'), 'r', encoding='utf-8') as f:
        centos_7_7_nmcli_device = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/nmcli-general-all.out'), 'r', encoding='utf-8') as f:
        centos_7_7_nmcli_general_all = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/nmcli-general-permissions.out'), 'r', encoding='utf-8') as f:
        centos_7_7_nmcli_general_permissions = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/fedora32/nmcli-connection-show-ens33.out'), 'r', encoding='utf-8') as f:
        fedora32_nmcli_connection_show_ens33 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/fedora32/nmcli-device-show-ens33.out'), 'r', encoding='utf-8') as f:
        fedora32_nmcli_device_show_ens33 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/fedora32/nmcli-device-show.out'), 'r', encoding='utf-8') as f:
        fedora32_nmcli_device_show = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/nmcli-team-config.out'), 'r', encoding='utf-8') as f:
        generic_nmcli_team_config = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/nmcli-team-config-blank.out'), 'r', encoding='utf-8') as f:
        generic_nmcli_team_config_blank = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/nmcli-team-port-config.out'), 'r', encoding='utf-8') as f:
        generic_nmcli_team_port_config = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/nmcli-team-port-config-blank.out'), 'r', encoding='utf-8') as f:
        generic_nmcli_team_port_config_blank = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/nmcli-team-and-team-port-config.out'), 'r', encoding='utf-8') as f:
        generic_nmcli_team_and_team_port_config = f.read()


    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/nmcli-connection-all.json'), 'r', encoding='utf-8') as f:
        centos_7_7_nmcli_connection_all_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/nmcli-connection-show-ens33.json'), 'r', encoding='utf-8') as f:
        centos_7_7_nmcli_connection_show_ens33_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/nmcli-connection.json'), 'r', encoding='utf-8') as f:
        centos_7_7_nmcli_connection_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/nmcli-device-all.json'), 'r', encoding='utf-8') as f:
        centos_7_7_nmcli_device_all_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/nmcli-device-show-ens33.json'), 'r', encoding='utf-8') as f:
        centos_7_7_nmcli_device_show_ens33_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/nmcli-device-show-lo.json'), 'r', encoding='utf-8') as f:
        centos_7_7_nmcli_device_show_lo_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/nmcli-device-show.json'), 'r', encoding='utf-8') as f:
        centos_7_7_nmcli_device_show_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/nmcli-device.json'), 'r', encoding='utf-8') as f:
        centos_7_7_nmcli_device_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/nmcli-general-all.json'), 'r', encoding='utf-8') as f:
        centos_7_7_nmcli_general_all_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/nmcli-general-permissions.json'), 'r', encoding='utf-8') as f:
        centos_7_7_nmcli_general_permissions_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/fedora32/nmcli-connection-show-ens33.json'), 'r', encoding='utf-8') as f:
        fedora32_nmcli_connection_show_ens33_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/fedora32/nmcli-device-show-ens33.json'), 'r', encoding='utf-8') as f:
        fedora32_nmcli_device_show_ens33_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/fedora32/nmcli-device-show.json'), 'r', encoding='utf-8') as f:
        fedora32_nmcli_device_show_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/nmcli-team-config.json'), 'r', encoding='utf-8') as f:
        generic_nmcli_team_config_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/nmcli-team-config-blank.json'), 'r', encoding='utf-8') as f:
        generic_nmcli_team_config_blank_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/nmcli-team-port-config.json'), 'r', encoding='utf-8') as f:
        generic_nmcli_team_port_config_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/nmcli-team-port-config-blank.json'), 'r', encoding='utf-8') as f:
        generic_nmcli_team_port_config_blank_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/nmcli-team-and-team-port-config.json'), 'r', encoding='utf-8') as f:
        generic_nmcli_team_and_team_port_config_json = json.loads(f.read())



    def test_nmcli_nodata(self):
        """
        Test 'nmcli' with no data
        """
        self.assertEqual(jc.parsers.nmcli.parse('', quiet=True), [])

    def test_nmcli_centos_7_7(self):
        """
        Test 'nmcli' on Centos 7.7 - this should raise a ParseError exception
        """
        self.assertRaises(ParseError, jc.parsers.nmcli.parse, self.centos_7_7_nmcli, quiet=True)

    def test_nmcli_connection_all_centos_7_7(self):
        """
        Test 'nmcli -f all connection' on Centos 7.7
        """
        self.assertEqual(jc.parsers.nmcli.parse(self.centos_7_7_nmcli_connection_all, quiet=True), self.centos_7_7_nmcli_connection_all_json)

    def test_nmcli_connection_show_ens33_centos_7_7(self):
        """
        Test 'nmcli connection show ens33' on Centos 7.7
        """
        self.assertEqual(jc.parsers.nmcli.parse(self.centos_7_7_nmcli_connection_show_ens33, quiet=True), self.centos_7_7_nmcli_connection_show_ens33_json)

    def test_nmcli_connection_centos_7_7(self):
        """
        Test 'nmcli connection' on Centos 7.7
        """
        self.assertEqual(jc.parsers.nmcli.parse(self.centos_7_7_nmcli_connection, quiet=True), self.centos_7_7_nmcli_connection_json)

    def test_nmcli_device_all_centos_7_7(self):
        """
        Test 'nmcli -f all device' on Centos 7.7
        """
        self.assertEqual(jc.parsers.nmcli.parse(self.centos_7_7_nmcli_device_all, quiet=True), self.centos_7_7_nmcli_device_all_json)

    def test_nmcli_device_show_ens33_centos_7_7(self):
        """
        Test 'nmcli device show ens33' on Centos 7.7
        """
        self.assertEqual(jc.parsers.nmcli.parse(self.centos_7_7_nmcli_device_show_ens33, quiet=True), self.centos_7_7_nmcli_device_show_ens33_json)

    def test_nmcli_device_show_lo_centos_7_7(self):
        """
        Test 'nmcli device show lo' on Centos 7.7
        """
        self.assertEqual(jc.parsers.nmcli.parse(self.centos_7_7_nmcli_device_show_lo, quiet=True), self.centos_7_7_nmcli_device_show_lo_json)

    def test_nmcli_device_show_centos_7_7(self):
        """
        Test 'nmcli device show' on Centos 7.7
        """
        self.assertEqual(jc.parsers.nmcli.parse(self.centos_7_7_nmcli_device_show, quiet=True), self.centos_7_7_nmcli_device_show_json)

    def test_nmcli_device_centos_7_7(self):
        """
        Test 'nmcli device' on Centos 7.7
        """
        self.assertEqual(jc.parsers.nmcli.parse(self.centos_7_7_nmcli_device, quiet=True), self.centos_7_7_nmcli_device_json)

    def test_nmcli_general_all_centos_7_7(self):
        """
        Test 'nmcli -f all general' on Centos 7.7
        """
        self.assertEqual(jc.parsers.nmcli.parse(self.centos_7_7_nmcli_general_all, quiet=True), self.centos_7_7_nmcli_general_all_json)

    def test_nmcli_general_permissions_centos_7_7(self):
        """
        Test 'nmcli general permissions' on Centos 7.7
        """
        self.assertEqual(jc.parsers.nmcli.parse(self.centos_7_7_nmcli_general_permissions, quiet=True), self.centos_7_7_nmcli_general_permissions_json)

    def test_nmcli_connection_show_ens33_fedora32(self):
        """
        Test 'nmcli connection show ens33' on fedora32
        """
        self.assertEqual(jc.parsers.nmcli.parse(self.fedora32_nmcli_connection_show_ens33, quiet=True), self.fedora32_nmcli_connection_show_ens33_json)

    def test_nmcli_device_show_ens33_fedora32(self):
        """
        Test 'nmcli device show ens33' on fedora32
        """
        self.assertEqual(jc.parsers.nmcli.parse(self.fedora32_nmcli_device_show_ens33, quiet=True), self.fedora32_nmcli_device_show_ens33_json)

    def test_nmcli_device_show_fedora32(self):
        """
        Test 'nmcli device show' on fedora32
        """
        self.assertEqual(jc.parsers.nmcli.parse(self.fedora32_nmcli_device_show, quiet=True), self.fedora32_nmcli_device_show_json)

    def test_nmcli_team_config(self):
        """
        Test nmcli with team.config JSON value
        """
        self.assertEqual(jc.parsers.nmcli.parse(self.generic_nmcli_team_config, quiet=True), self.generic_nmcli_team_config_json)

    def test_nmcli_team_config_blank(self):
        """
        Test nmcli with blank team.config JSON value
        """
        self.assertEqual(jc.parsers.nmcli.parse(self.generic_nmcli_team_config_blank, quiet=True), self.generic_nmcli_team_config_blank_json)

    def test_nmcli_team_port_config(self):
        """
        Test nmcli with team-port.config JSON value
        """
        self.assertEqual(jc.parsers.nmcli.parse(self.generic_nmcli_team_port_config, quiet=True), self.generic_nmcli_team_port_config_json)

    def test_nmcli_team_port_config_blank(self):
        """
        Test nmcli with blank team-port.config JSON value
        """
        self.assertEqual(jc.parsers.nmcli.parse(self.generic_nmcli_team_port_config_blank, quiet=True), self.generic_nmcli_team_port_config_blank_json)

    def test_nmcli_team_and_team_port_config_blank(self):
        """
        Test nmcli with both team.config and team-port.config JSON value
        """
        self.assertEqual(jc.parsers.nmcli.parse(self.generic_nmcli_team_and_team_port_config, quiet=True), self.generic_nmcli_team_and_team_port_config_json)


if __name__ == '__main__':
    unittest.main()
