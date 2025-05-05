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
        data = '''connection.id:                          Team connection 1
connection.uuid:                        258e02c2-d9f9-44bb-8d27-887e11aa1828
connection.stable-id:                   --
connection.type:                        team
connection.interface-name:              team0
connection.autoconnect:                 yes
connection.autoconnect-priority:        0
connection.autoconnect-retries:         -1 (default)
connection.multi-connect:               0 (default)
connection.auth-retries:                -1
connection.timestamp:                   0
connection.read-only:                   no
connection.permissions:                 --
connection.zone:                        --
connection.master:                      --
connection.slave-type:                  --
connection.autoconnect-slaves:          -1 (default)
connection.secondaries:                 --
connection.gateway-ping-timeout:        0
connection.metered:                     unknown
connection.lldp:                        default
connection.mdns:                        -1 (default)
connection.llmnr:                       -1 (default)
connection.dns-over-tls:                -1 (default)
connection.wait-device-timeout:         -1
ipv4.method:                            auto
ipv4.dns:                               --
ipv4.dns-search:                        --
ipv4.dns-options:                       --
ipv4.dns-priority:                      0
ipv4.addresses:                         --
ipv4.gateway:                           --
ipv4.routes:                            --
ipv4.route-metric:                      -1
ipv4.route-table:                       0 (unspec)
ipv4.routing-rules:                     --
ipv4.ignore-auto-routes:                no
ipv4.ignore-auto-dns:                   no
ipv4.dhcp-client-id:                    --
ipv4.dhcp-iaid:                         --
ipv4.dhcp-timeout:                      0 (default)
ipv4.dhcp-send-hostname:                yes
ipv4.dhcp-hostname:                     --
ipv4.dhcp-fqdn:                         --
ipv4.dhcp-hostname-flags:               0x0 (none)
ipv4.never-default:                     no
ipv4.may-fail:                          yes
ipv4.required-timeout:                  -1 (default)
ipv4.dad-timeout:                       -1 (default)
ipv4.dhcp-vendor-class-identifier:      --
ipv4.dhcp-reject-servers:               --
ipv6.method:                            auto
ipv6.dns:                               --
ipv6.dns-search:                        --
ipv6.dns-options:                       --
ipv6.dns-priority:                      0
ipv6.addresses:                         --
ipv6.gateway:                           --
ipv6.routes:                            --
ipv6.route-metric:                      -1
ipv6.route-table:                       0 (unspec)
ipv6.routing-rules:                     --
ipv6.ignore-auto-routes:                no
ipv6.ignore-auto-dns:                   no
ipv6.never-default:                     no
ipv6.may-fail:                          yes
ipv6.required-timeout:                  -1 (default)
ipv6.ip6-privacy:                       -1 (unknown)
ipv6.addr-gen-mode:                     stable-privacy
ipv6.ra-timeout:                        0 (default)
ipv6.dhcp-duid:                         --
ipv6.dhcp-iaid:                         --
ipv6.dhcp-timeout:                      0 (default)
ipv6.dhcp-send-hostname:                yes
ipv6.dhcp-hostname:                     --
ipv6.dhcp-hostname-flags:               0x0 (none)
ipv6.token:                             --
team.config:                            {
    "runner": {
        "name": "roundrobin"
    },
    "link_watch": {
        "name": "ethtool"
    }
}
team.notify-peers-count:                -1 (unset)
team.notify-peers-interval:             -1 (unset)
team.mcast-rejoin-count:                -1 (unset)
team.mcast-rejoin-interval:             -1 (unset)
team.runner:                            roundrobin
team.runner-hwaddr-policy:              --
team.runner-tx-hash:                    --
team.runner-tx-balancer:                --
team.runner-tx-balancer-interval:       -1 (unset)
team.runner-active:                     yes
team.runner-fast-rate:                  no
team.runner-sys-prio:                   -1 (unset)
team.runner-min-ports:                  -1 (unset)
team.runner-agg-select-policy:          --
team.link-watchers:                     name=ethtool
proxy.method:                           none
proxy.browser-only:                     no
proxy.pac-url:                          --
proxy.pac-script:                       --'''
        expected = [{'connection_id': 'Team connection 1', 'connection_uuid': '258e02c2-d9f9-44bb-8d27-887e11aa1828', 'connection_stable_id': None, 'connection_type': 'team', 'connection_interface_name': 'team0', 'connection_autoconnect': 'yes', 'connection_autoconnect_priority': 0, 'connection_autoconnect_retries': -1, 'connection_autoconnect_retries_text': 'default', 'connection_multi_connect': 0, 'connection_multi_connect_text': 'default', 'connection_auth_retries': -1, 'connection_timestamp': 0, 'connection_read_only': 'no', 'connection_permissions': None, 'connection_zone': None, 'connection_master': None, 'connection_slave_type': None, 'connection_autoconnect_slaves': -1, 'connection_autoconnect_slaves_text': 'default', 'connection_secondaries': None, 'connection_gateway_ping_timeout': 0, 'connection_metered': 'unknown', 'connection_lldp': 'default', 'connection_mdns': -1, 'connection_mdns_text': 'default', 'connection_llmnr': -1, 'connection_llmnr_text': 'default', 'connection_dns_over_tls': -1, 'connection_dns_over_tls_text': 'default', 'connection_wait_device_timeout': -1, 'ipv4_method': 'auto', 'ipv4_dns': None, 'ipv4_dns_search': None, 'ipv4_dns_options': None, 'ipv4_dns_priority': 0, 'ipv4_addresses': None, 'ipv4_gateway': None, 'ipv4_routes': None, 'ipv4_route_metric': -1, 'ipv4_route_table': 0, 'ipv4_route_table_text': 'unspec', 'ipv4_routing_rules': None, 'ipv4_ignore_auto_routes': 'no', 'ipv4_ignore_auto_dns': 'no', 'ipv4_dhcp_client_id': None, 'ipv4_dhcp_iaid': None, 'ipv4_dhcp_timeout': 0, 'ipv4_dhcp_timeout_text': 'default', 'ipv4_dhcp_send_hostname': 'yes', 'ipv4_dhcp_hostname': None, 'ipv4_dhcp_fqdn': None, 'ipv4_dhcp_hostname_flags': '0x0', 'ipv4_dhcp_hostname_flags_text': 'none', 'ipv4_never_default': 'no', 'ipv4_may_fail': 'yes', 'ipv4_required_timeout': -1, 'ipv4_required_timeout_text': 'default', 'ipv4_dad_timeout': -1, 'ipv4_dad_timeout_text': 'default', 'ipv4_dhcp_vendor_class_identifier': None, 'ipv4_dhcp_reject_servers': None, 'ipv6_method': 'auto', 'ipv6_dns': None, 'ipv6_dns_search': None, 'ipv6_dns_options': None, 'ipv6_dns_priority': 0, 'ipv6_addresses': None, 'ipv6_gateway': None, 'ipv6_routes': None, 'ipv6_route_metric': -1, 'ipv6_route_table': 0, 'ipv6_route_table_text': 'unspec', 'ipv6_routing_rules': None, 'ipv6_ignore_auto_routes': 'no', 'ipv6_ignore_auto_dns': 'no', 'ipv6_never_default': 'no', 'ipv6_may_fail': 'yes', 'ipv6_required_timeout': -1, 'ipv6_required_timeout_text': 'default', 'ipv6_ip6_privacy': -1, 'ipv6_ip6_privacy_text': 'unknown', 'ipv6_addr_gen_mode': 'stable-privacy', 'ipv6_ra_timeout': 0, 'ipv6_ra_timeout_text': 'default', 'ipv6_dhcp_duid': None, 'ipv6_dhcp_iaid': None, 'ipv6_dhcp_timeout': 0, 'ipv6_dhcp_timeout_text': 'default', 'ipv6_dhcp_send_hostname': 'yes', 'ipv6_dhcp_hostname': None, 'ipv6_dhcp_hostname_flags': '0x0', 'ipv6_dhcp_hostname_flags_text': 'none', 'ipv6_token': None, 'team_config': {'runner': {'name': 'roundrobin'}, 'link_watch': {'name': 'ethtool'}}, 'team_notify_peers_count': -1, 'team_notify_peers_count_text': 'unset', 'team_notify_peers_interval': -1, 'team_notify_peers_interval_text': 'unset', 'team_mcast_rejoin_count': -1, 'team_mcast_rejoin_count_text': 'unset', 'team_mcast_rejoin_interval': -1, 'team_mcast_rejoin_interval_text': 'unset', 'team_runner': 'roundrobin', 'team_runner_hwaddr_policy': None, 'team_runner_tx_hash': None, 'team_runner_tx_balancer': None, 'team_runner_tx_balancer_interval': -1, 'team_runner_tx_balancer_interval_text': 'unset', 'team_runner_active': 'yes', 'team_runner_fast_rate': 'no', 'team_runner_sys_prio': -1, 'team_runner_sys_prio_text': 'unset', 'team_runner_min_ports': -1, 'team_runner_min_ports_text': 'unset', 'team_runner_agg_select_policy': None, 'team_link_watchers': 'name=ethtool', 'proxy_method': 'none', 'proxy_browser_only': 'no', 'proxy_pac_url': None, 'proxy_pac_script': None}]
        self.assertEqual(jc.parsers.nmcli.parse(data, quiet=True), expected)


if __name__ == '__main__':
    unittest.main()
