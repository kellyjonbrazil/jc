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

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/nmcli-device-wifi-list.out'), 'r', encoding='utf-8') as f:
        generic_nmcli_device_wifi_list = f.read()


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

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/nmcli-device-wifi-list.json'), 'r', encoding='utf-8') as f:
        generic_nmcli_device_wifi_list_json = json.loads(f.read())



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

    def test_nmcli_device_wifi_list(self):
        """
        Test 'nmcli -t device wifi list' with escaped values
        """
        self.assertEqual(jc.parsers.nmcli.parse(self.generic_nmcli_device_wifi_list, quiet=True), self.generic_nmcli_device_wifi_list_json)


    def test_nmcli_line_separator(self):
        """
        Test 'nmcli' with a line-break character other than LF inside a field
        """
        data = 'GENERAL.DEVICE:      wlan0\nGENERAL.CONNECTION:  Cafe\x0cGENERAL.DEVICE:tun0\nIP4.ADDRESS[1]:      10.0.0.5/24\n'
        result = jc.parsers.nmcli.parse(data, quiet=True)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['device'], 'wlan0')
        self.assertEqual(result[0]['connection'], 'Cafe\x0cGENERAL.DEVICE:tun0')

    def test_nmcli_remove_text_long_blank_run(self):
        """
        Test removing a trailing '(text)' summary from values with long runs of blanks
        """
        blanks = ' ' * 20000
        self.assertEqual(jc.parsers.nmcli._remove_text_from_value('x' + blanks + 'y (b)'), 'x' + blanks + 'y')
        self.assertEqual(jc.parsers.nmcli._remove_text_from_value('100' + blanks + '(connected)'), '100')
        self.assertEqual(jc.parsers.nmcli._remove_text_from_value('x' + blanks + 'y'), 'x' + blanks + 'y')


    def test_nmcli_quoted_values(self):
        """
        Test 'nmcli' with values that contain double quote characters
        """
        data = 'connection.id:                          "CorpNet"\nconnection.uuid:                        ""\n'
        result = jc.parsers.nmcli.parse(data, quiet=True)
        self.assertEqual(result[0]['connection_id'], '"CorpNet"')
        self.assertEqual(result[0]['connection_uuid'], '')

        data = 'NAME       UUID  TYPE  DEVICE\n"CorpNet"  a1    wifi  wlp1\nCorpNet    b2    wifi  wlp2\n'
        result = jc.parsers.nmcli.parse(data, quiet=True)
        self.assertEqual([x['name'] for x in result], ['"CorpNet"', 'CorpNet'])

    def test_nmcli_non_finite_values(self):
        """
        Test 'nmcli device show' with values too large for a float: the text is kept
        """
        data = (
            'GENERAL.DEVICE:                         enp0s3\n'
            'GENERAL.TYPE:                           1.0e999\n'
            'GENERAL.MTU:                            1500\n'
            'IP4.ROUTE[1]:                           dst = 0.0.0.0/0, nh = 1.0e999, mt = 100\n'
        )
        expected = [{
            'device': 'enp0s3',
            'type': '1.0e999',
            'mtu': 1500,
            'ip4_route_1': {'dst': '0.0.0.0/0', 'nh': '1.0e999', 'mt': 100}
        }]
        self.assertEqual(jc.parsers.nmcli.parse(data, quiet=True), expected)

    def test_nmcli_equals_in_values(self):
        """
        Test 'nmcli' with '=' characters in DHCP option and route values
        """
        data = (
            'GENERAL.DEVICE:                         ens33\n'
            'IP4.ADDRESS[1]:                         192.168.71.180/24\n'
            'DHCP4.OPTION[1]:                        domain_search = a=b.example.com\n'
            'DHCP4.OPTION[2]:                        ip_address = 192.168.71.180\n'
            'IP4.ROUTE[1]:                           dst = 192.168.71.0/24, nh = 0.0.0.0, mt = 100\n'
        )
        result = jc.parsers.nmcli.parse(data, quiet=True)
        self.assertEqual(result[0]['dhcp4_option_1'], {'name': 'domain_search', 'value': 'a=b.example.com'})
        self.assertEqual(result[0]['dhcp4_option_2'], {'name': 'ip_address', 'value': '192.168.71.180'})
        self.assertEqual(result[0]['ip4_route_1'], {'dst': '192.168.71.0/24', 'nh': '0.0.0.0', 'mt': 100})
        self.assertEqual(jc.parsers.nmcli._split_routes('dst = 1.2.3.0/24, nh = a=b, mt = 100'), {'dst': '1.2.3.0/24', 'nh': 'a=b', 'mt': '100'})


if __name__ == '__main__':
    unittest.main()
