import os
import json
import unittest
import jc.parsers.netstat

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    #
    # input
    #

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/netstat-freebsd-protocol-names.out'), 'r', encoding='utf-8') as f:
        generic_netstat_freebsd_protocol_names = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/netstat-freebsd-protocol-names.json'), 'r', encoding='utf-8') as f:
        generic_netstat_freebsd_protocol_names_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/netstat-osx-peer-host-udp.out'), 'r', encoding='utf-8') as f:
        generic_netstat_osx_peer_host_udp = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/netstat-osx-peer-host-udp.json'), 'r', encoding='utf-8') as f:
        generic_netstat_osx_peer_host_udp_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/netstat-freebsd-route-host-names.out'), 'r', encoding='utf-8') as f:
        generic_netstat_freebsd_route_host_names = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/netstat-freebsd-route-host-names.json'), 'r', encoding='utf-8') as f:
        generic_netstat_freebsd_route_host_names_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/netstat-linux-service-port-names.out'), 'r', encoding='utf-8') as f:
        generic_netstat_linux_service_port_names = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/netstat-linux-service-port-names.json'), 'r', encoding='utf-8') as f:
        generic_netstat_linux_service_port_names_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/netstat-linux-proto-text-in-program-name.out'), 'r', encoding='utf-8') as f:
        generic_netstat_linux_proto_text_in_program_name = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/netstat-linux-proto-text-in-program-name.json'), 'r', encoding='utf-8') as f:
        generic_netstat_linux_proto_text_in_program_name_json = json.loads(f.read())

    # netstat
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/netstat.out'), 'r', encoding='utf-8') as f:
        centos_7_7_netstat = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/netstat.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_netstat = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/netstat-l.out'), 'r', encoding='utf-8') as f:
        centos_7_7_netstat_l = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/netstat-l.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_netstat_l = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/netstat-p.out'), 'r', encoding='utf-8') as f:
        centos_7_7_netstat_p = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/netstat-p.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_netstat_p = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/netstat-sudo-lnp.out'), 'r', encoding='utf-8') as f:
        centos_7_7_netstat_sudo_lnp = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/netstat-sudo-lnp.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_netstat_sudo_lnp = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/netstat-sudo-lnp-space.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_netstat_sudo_lnp_space = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/netstat-sudo-aeep.out'), 'r', encoding='utf-8') as f:
        centos_7_7_netstat_sudo_aeep = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/netstat-sudo-aeep.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_netstat_sudo_aeep = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/fedora32/netstat.out'), 'r', encoding='utf-8') as f:
        fedora32_netstat = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/netstat.out'), 'r', encoding='utf-8') as f:
        osx_14_6_netstat = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/netstat-An.out'), 'r', encoding='utf-8') as f:
        osx_14_6_netstat_An = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/netstat-Abn.out'), 'r', encoding='utf-8') as f:
        osx_14_6_netstat_Abn = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/netstat-Aa.out'), 'r', encoding='utf-8') as f:
        freebsd12_netstat_Aa = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/netstat-an.out'), 'r', encoding='utf-8') as f:
        freebsd12_netstat_an = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/netstat-AanP.out'), 'r', encoding='utf-8') as f:
        freebsd12_netstat_AanP = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/netstat-AaT.out'), 'r', encoding='utf-8') as f:
        freebsd12_netstat_AaT = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/netstat-Aax.out'), 'r', encoding='utf-8') as f:
        freebsd12_netstat_Aax = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/netstat-aT.out'), 'r', encoding='utf-8') as f:
        freebsd12_netstat_aT = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/netstat-linux-old.out'), 'r', encoding='utf-8') as f:
        generic_netstat_linux_old = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/netstat-linux-no-state.out'), 'r', encoding='utf-8') as f:
        generic_netstat_linux_no_state = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/windows/windows-10/netstat.out'), 'r', encoding='utf-8') as f:
        windows_netstat = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/windows/windows-10/netstat-an.out'), 'r', encoding='utf-8') as f:
        windows_netstat_an = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/windows/windows-10/netstat-aon.out'), 'r', encoding='utf-8') as f:
        windows_netstat_aon = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/windows/windows-10/netstat-aonb.out'), 'r', encoding='utf-8') as f:
        windows_netstat_aonb = f.read()

    # netstat -r
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/netstat-r.out'), 'r', encoding='utf-8') as f:
        centos_7_7_netstat_r = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/netstat-rne.out'), 'r', encoding='utf-8') as f:
        centos_7_7_netstat_rne = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/netstat-rnee.out'), 'r', encoding='utf-8') as f:
        centos_7_7_netstat_rnee = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/netstat-r.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_netstat_r = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/netstat-rne.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_netstat_rne = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/netstat-rnee.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_netstat_rnee = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/netstat-r.out'), 'r', encoding='utf-8') as f:
        osx_14_6_netstat_r = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/netstat-rnl.out'), 'r', encoding='utf-8') as f:
        osx_14_6_netstat_rnl = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/netstat-r.out'), 'r', encoding='utf-8') as f:
        freebsd12_netstat_r = f.read()

    # netstat -i
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/netstat-i.out'), 'r', encoding='utf-8') as f:
        centos_7_7_netstat_i = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/netstat-i.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_netstat_i = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/netstat-i.out'), 'r', encoding='utf-8') as f:
        osx_14_6_netstat_i = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/netstat-i.out'), 'r', encoding='utf-8') as f:
        freebsd12_netstat_i = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/netstat-ib.out'), 'r', encoding='utf-8') as f:
        freebsd12_netstat_ib = f.read()

    #
    # output
    #

    # netstat
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/netstat.json'), 'r', encoding='utf-8') as f:
        centos_7_7_netstat_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/netstat.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_netstat_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/netstat-l.json'), 'r', encoding='utf-8') as f:
        centos_7_7_netstat_l_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/netstat-l.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_netstat_l_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/netstat-p.json'), 'r', encoding='utf-8') as f:
        centos_7_7_netstat_p_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/netstat-p.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_netstat_p_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/netstat-sudo-lnp.json'), 'r', encoding='utf-8') as f:
        centos_7_7_netstat_sudo_lnp_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/netstat-sudo-lnp.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_netstat_sudo_lnp_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/netstat-sudo-lnp-space.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_netstat_sudo_lnp_space_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/netstat-sudo-aeep.json'), 'r', encoding='utf-8') as f:
        centos_7_7_netstat_sudo_aeep_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/netstat-sudo-aeep.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_netstat_sudo_aeep_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/fedora32/netstat.json'), 'r', encoding='utf-8') as f:
        fedora32_netstat_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/netstat.json'), 'r', encoding='utf-8') as f:
        osx_14_6_netstat_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/netstat-An.json'), 'r', encoding='utf-8') as f:
        osx_14_6_netstat_An_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/netstat-Abn.json'), 'r', encoding='utf-8') as f:
        osx_14_6_netstat_Abn_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/netstat-Aa.json'), 'r', encoding='utf-8') as f:
        freebsd12_netstat_Aa_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/netstat-AanP.json'), 'r', encoding='utf-8') as f:
        freebsd12_netstat_AanP_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/netstat-AaT.json'), 'r', encoding='utf-8') as f:
        freebsd12_netstat_AaT_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/netstat-Aax.json'), 'r', encoding='utf-8') as f:
        freebsd12_netstat_Aax_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/netstat-aT.json'), 'r', encoding='utf-8') as f:
        freebsd12_netstat_aT_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/netstat-an.json'), 'r', encoding='utf-8') as f:
        freebsd12_netstat_an_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/netstat-linux-old.json'), 'r', encoding='utf-8') as f:
        generic_netstat_linux_old_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/netstat-linux-no-state.json'), 'r', encoding='utf-8') as f:
        generic_netstat_linux_no_state_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/windows/windows-10/netstat.json'), 'r', encoding='utf-8') as f:
        windows_netstat_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/windows/windows-10/netstat-an.json'), 'r', encoding='utf-8') as f:
        windows_netstat_an_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/windows/windows-10/netstat-aon.json'), 'r', encoding='utf-8') as f:
        windows_netstat_aon_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/windows/windows-10/netstat-aonb.json'), 'r', encoding='utf-8') as f:
        windows_netstat_aonb_json = json.loads(f.read())

    # netsat -r
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/netstat-r.json'), 'r', encoding='utf-8') as f:
        centos_7_7_netstat_r_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/netstat-rne.json'), 'r', encoding='utf-8') as f:
        centos_7_7_netstat_rne_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/netstat-rnee.json'), 'r', encoding='utf-8') as f:
        centos_7_7_netstat_rnee_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/netstat-r.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_netstat_r_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/netstat-rne.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_netstat_rne_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/netstat-rnee.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_netstat_rnee_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/netstat-r.json'), 'r', encoding='utf-8') as f:
        osx_14_6_netstat_r_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/netstat-rnl.json'), 'r', encoding='utf-8') as f:
        osx_14_6_netstat_rnl_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/netstat-r.json'), 'r', encoding='utf-8') as f:
        freebsd12_netstat_r_json = json.loads(f.read())

    # netstat -i
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/netstat-i.json'), 'r', encoding='utf-8') as f:
        centos_7_7_netstat_i_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/netstat-i.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_netstat_i_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/netstat-i.json'), 'r', encoding='utf-8') as f:
        osx_14_6_netstat_i_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/netstat-i.json'), 'r', encoding='utf-8') as f:
        freebsd12_netstat_i_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/netstat-ib.json'), 'r', encoding='utf-8') as f:
        freebsd12_netstat_ib_json = json.loads(f.read())


    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/netstat-linux-program-name-state-words.out'), 'r', encoding='utf-8') as f:
        generic_netstat_state_words = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/netstat-linux-program-name-state-words-e.out'), 'r', encoding='utf-8') as f:
        generic_netstat_state_words_e = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/netstat-linux-program-name-state-words.json'), 'r', encoding='utf-8') as f:
        generic_netstat_state_words_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/netstat-linux-program-name-state-words-e.json'), 'r', encoding='utf-8') as f:
        generic_netstat_state_words_e_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/netstat-linux-unix-program-name-space.out'), 'r', encoding='utf-8') as f:
        generic_netstat_linux_unix_program_name_space = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/netstat-linux-unix-program-name-space.json'), 'r', encoding='utf-8') as f:
        generic_netstat_linux_unix_program_name_space_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/netstat-linux-unix-brackets.out'), 'r', encoding='utf-8') as f:
        generic_netstat_linux_unix_brackets = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/netstat-linux-unix-brackets.json'), 'r', encoding='utf-8') as f:
        generic_netstat_linux_unix_brackets_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/netstat-linux-unix-path-whitespace.out'), 'r', encoding='utf-8') as f:
        generic_netstat_linux_unix_path_whitespace = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/netstat-linux-unix-path-whitespace.json'), 'r', encoding='utf-8') as f:
        generic_netstat_linux_unix_path_whitespace_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/netstat-windows-service-name-protocol-prefix.out'), 'r', encoding='utf-8') as f:
        generic_netstat_windows_service_name_protocol_prefix = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/netstat-windows-service-name-protocol-prefix.json'), 'r', encoding='utf-8') as f:
        generic_netstat_windows_service_name_protocol_prefix_json = json.loads(f.read())

    def test_netstat_nodata(self):
        """
        Test 'netstat' with no data
        """
        self.assertEqual(jc.parsers.netstat.parse('', quiet=True), [])

    def test_netstat_centos_7_7(self):
        """
        Test 'netstat' on Centos 7.7
        """
        self.assertEqual(jc.parsers.netstat.parse(self.centos_7_7_netstat, quiet=True), self.centos_7_7_netstat_json)

    def test_netstat_ubuntu_18_4(self):
        """
        Test 'netstat' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.netstat.parse(self.ubuntu_18_4_netstat, quiet=True), self.ubuntu_18_4_netstat_json)

    def test_netstat_l_centos_7_7(self):
        """
        Test 'netstat -l' on Centos 7.7
        """
        self.assertEqual(jc.parsers.netstat.parse(self.centos_7_7_netstat_l, quiet=True), self.centos_7_7_netstat_l_json)

    def test_netstat_l_ubuntu_18_4(self):
        """
        Test 'netstat -l' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.netstat.parse(self.ubuntu_18_4_netstat_l, quiet=True), self.ubuntu_18_4_netstat_l_json)

    def test_netstat_p_centos_7_7(self):
        """
        Test 'netstat -l' on Centos 7.7
        """
        self.assertEqual(jc.parsers.netstat.parse(self.centos_7_7_netstat_p, quiet=True), self.centos_7_7_netstat_p_json)

    def test_netstat_p_ubuntu_18_4(self):
        """
        Test 'netstat -l' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.netstat.parse(self.ubuntu_18_4_netstat_p, quiet=True), self.ubuntu_18_4_netstat_p_json)

    def test_netstat_sudo_lnp_centos_7_7(self):
        """
        Test 'sudo netstat -lnp' on Centos 7.7
        """
        self.assertEqual(jc.parsers.netstat.parse(self.centos_7_7_netstat_sudo_lnp, quiet=True), self.centos_7_7_netstat_sudo_lnp_json)

    def test_netstat_sudo_lnp_ubuntu_18_4(self):
        """
        Test 'sudo netstat -lnp' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.netstat.parse(self.ubuntu_18_4_netstat_sudo_lnp, quiet=True), self.ubuntu_18_4_netstat_sudo_lnp_json)

    def test_netstat_sudo_lnp_ubuntu_18_4(self):
        """
        Test 'sudo netstat -lnp' on Ubuntu 18.4 with a space in the process name(special case)
        """
        self.assertEqual(jc.parsers.netstat.parse(self.ubuntu_18_4_netstat_sudo_lnp_space, quiet=True), self.ubuntu_18_4_netstat_sudo_lnp_space_json)

    def test_netstat_sudo_aeep_centos_7_7(self):
        """
        Test 'sudo netstat -aeep' on Centos 7.7
        """
        self.assertEqual(jc.parsers.netstat.parse(self.centos_7_7_netstat_sudo_aeep, quiet=True), self.centos_7_7_netstat_sudo_aeep_json)

    def test_netstat_sudo_aeep_ubuntu_18_4(self):
        """
        Test 'sudo netstat -aeep' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.netstat.parse(self.ubuntu_18_4_netstat_sudo_aeep, quiet=True), self.ubuntu_18_4_netstat_sudo_aeep_json)

    def test_netstat_fedora32(self):
        """
        Test 'netstat' on Fedora32
        """
        self.assertEqual(jc.parsers.netstat.parse(self.fedora32_netstat, quiet=True), self.fedora32_netstat_json)

    def test_netstat_osx_14_6(self):
        """
        Test 'netstat' on OSX 14.6
        """
        self.assertEqual(jc.parsers.netstat.parse(self.osx_14_6_netstat, quiet=True), self.osx_14_6_netstat_json)

    def test_netstat_An_osx_14_6(self):
        """
        Test 'netstat -An' on OSX 14.6
        """
        self.assertEqual(jc.parsers.netstat.parse(self.osx_14_6_netstat_An, quiet=True), self.osx_14_6_netstat_An_json)

    def test_netstat_Abn_osx_14_6(self):
        """
        Test 'netstat -Abn' on OSX 14.6
        """
        self.assertEqual(jc.parsers.netstat.parse(self.osx_14_6_netstat_Abn, quiet=True), self.osx_14_6_netstat_Abn_json)

    def test_netstat_Aa_freebsd12(self):
        """
        Test 'netstat -Aa' on FreeBSD12
        """
        self.assertEqual(jc.parsers.netstat.parse(self.freebsd12_netstat_Aa, quiet=True), self.freebsd12_netstat_Aa_json)

    def test_netstat_AanP_freebsd12(self):
        """
        Test 'netstat -AanP' on FreeBSD12
        """
        self.assertEqual(jc.parsers.netstat.parse(self.freebsd12_netstat_AanP, quiet=True), self.freebsd12_netstat_AanP_json)

    def test_netstat_AaT_freebsd12(self):
        """
        Test 'netstat -AaT' on FreeBSD12
        """
        self.assertEqual(jc.parsers.netstat.parse(self.freebsd12_netstat_AaT, quiet=True), self.freebsd12_netstat_AaT_json)

    def test_netstat_Aax_freebsd12(self):
        """
        Test 'netstat -Aax' on FreeBSD12
        """
        self.assertEqual(jc.parsers.netstat.parse(self.freebsd12_netstat_Aax, quiet=True), self.freebsd12_netstat_Aax_json)

    def test_netstat_aT_freebsd12(self):
        """
        Test 'netstat -aT' on FreeBSD12
        """
        self.assertEqual(jc.parsers.netstat.parse(self.freebsd12_netstat_aT, quiet=True), self.freebsd12_netstat_aT_json)

    def test_netstat_an_freebsd12(self):
        """
        Test 'netstat -an' on FreeBSD12
        """
        self.assertEqual(jc.parsers.netstat.parse(self.freebsd12_netstat_an, quiet=True), self.freebsd12_netstat_an_json)

    def test_netstat_old_generic(self):
        """
        Test 'netstat' with older version of netstat on linux
        """
        self.assertEqual(jc.parsers.netstat.parse(self.generic_netstat_linux_old, quiet=True), self.generic_netstat_linux_old_json)

    def test_netstat_no_state_generic(self):
        """
        Test 'netstat' with no state in network output
        """
        self.assertEqual(jc.parsers.netstat.parse(self.generic_netstat_linux_no_state, quiet=True), self.generic_netstat_linux_no_state_json)

    def test_netstat_r_centos_7_7(self):
        """
        Test 'netstat -r' on Centos 7.7
        """
        self.assertEqual(jc.parsers.netstat.parse(self.centos_7_7_netstat_r, quiet=True), self.centos_7_7_netstat_r_json)

    def test_netstat_rne_centos_7_7(self):
        """
        Test 'netstat -rne' on Centos 7.7
        """
        self.assertEqual(jc.parsers.netstat.parse(self.centos_7_7_netstat_rne, quiet=True), self.centos_7_7_netstat_rne_json)

    def test_netstat_rnee_centos_7_7(self):
        """
        Test 'netstat -rnee' on Centos 7.7
        """
        self.assertEqual(jc.parsers.netstat.parse(self.centos_7_7_netstat_rnee, quiet=True), self.centos_7_7_netstat_rnee_json)

    def test_netstat_r_ubuntu_18_4(self):
        """
        Test 'netstat -r' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.netstat.parse(self.ubuntu_18_4_netstat_r, quiet=True), self.ubuntu_18_4_netstat_r_json)

    def test_netstat_rne_ubuntu_18_4(self):
        """
        Test 'netstat -rne' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.netstat.parse(self.ubuntu_18_4_netstat_rne, quiet=True), self.ubuntu_18_4_netstat_rne_json)

    def test_netstat_rnee_ubuntu_18_4(self):
        """
        Test 'netstat -rnee' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.netstat.parse(self.ubuntu_18_4_netstat_rnee, quiet=True), self.ubuntu_18_4_netstat_rnee_json)

    def test_netstat_r_osx_14_6(self):
        """
        Test 'netstat -r' on OSX 14.6
        """
        self.assertEqual(jc.parsers.netstat.parse(self.osx_14_6_netstat_r, quiet=True), self.osx_14_6_netstat_r_json)

    def test_netstat_rnl_osx_14_6(self):
        """
        Test 'netstat -rnl' on OSX 14.6
        """
        self.assertEqual(jc.parsers.netstat.parse(self.osx_14_6_netstat_rnl, quiet=True), self.osx_14_6_netstat_rnl_json)

    def test_netstat_r_freebsd12(self):
        """
        Test 'netstat -r' on FreeBSD12
        """
        self.assertEqual(jc.parsers.netstat.parse(self.freebsd12_netstat_r, quiet=True), self.freebsd12_netstat_r_json)

    def test_netstat_i_centos_7_7(self):
        """
        Test 'netstat -i' on Centos 7.7
        """
        self.assertEqual(jc.parsers.netstat.parse(self.centos_7_7_netstat_i, quiet=True), self.centos_7_7_netstat_i_json)

    def test_netstat_i_ubuntu_18_4(self):
        """
        Test 'netstat -i' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.netstat.parse(self.ubuntu_18_4_netstat_i, quiet=True), self.ubuntu_18_4_netstat_i_json)

    def test_netstat_i_osx_14_6(self):
        """
        Test 'netstat -i' on OSX 14.6
        """
        self.assertEqual(jc.parsers.netstat.parse(self.osx_14_6_netstat_i, quiet=True), self.osx_14_6_netstat_i_json)

    def test_netstat_i_freebsd12(self):
        """
        Test 'netstat -i' on FreeBSD12
        """
        self.assertEqual(jc.parsers.netstat.parse(self.freebsd12_netstat_i, quiet=True), self.freebsd12_netstat_i_json)

    def test_netstat_ib_freebsd12(self):
        """
        Test 'netstat -ib' on FreeBSD12
        """
        self.assertEqual(jc.parsers.netstat.parse(self.freebsd12_netstat_ib, quiet=True), self.freebsd12_netstat_ib_json)

    def test_netstat_windows(self):
        """
        Test 'netstat' on Windows
        """
        self.assertEqual(jc.parsers.netstat.parse(self.windows_netstat, quiet=True), self.windows_netstat_json)

    def test_netstat_an_windows(self):
        """
        Test 'netstat -an' on Windows
        """
        self.assertEqual(jc.parsers.netstat.parse(self.windows_netstat_an, quiet=True), self.windows_netstat_an_json)

    def test_netstat_aon_windows(self):
        """
        Test 'netstat -aon' on Windows
        """
        self.assertEqual(jc.parsers.netstat.parse(self.windows_netstat_aon, quiet=True), self.windows_netstat_aon_json)

    def test_netstat_aonb_windows(self):
        """
        Test 'netstat -aonb' on Windows
        """
        self.assertEqual(jc.parsers.netstat.parse(self.windows_netstat_aonb, quiet=True), self.windows_netstat_aonb_json)


    def test_netstat_line_separator(self):
        """
        Test 'netstat' with a line-break character other than LF inside a field
        """
        data = 'Active UNIX domain sockets (only servers)\nProto RefCnt Flags       Type       State         I-Node   PID/Program name     Path\nunix  2      [ ACC ]     STREAM     LISTENING     55555    31337/prog           @x\x1eunix  2      [ ACC ]     STREAM     LISTENING     99999    1/init               /run/other.sock\n'
        result = jc.parsers.netstat.parse(data, quiet=True)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['inode'], 55555)
        self.assertEqual(result[0]['pid'], 31337)
        self.assertEqual(result[0]['path'], '@x\x1eunix  2      [ ACC ]     STREAM     LISTENING     99999    1/init               /run/other.sock')


    def test_netstat_other_whitespace_in_program_name(self):
        """
        Test 'netstat' UNIX sockets with tab and non-ASCII whitespace in the program name
        """
        header = 'Active UNIX domain sockets (servers and established)\nProto RefCnt Flags       Type       State         I-Node   PID/Program name     Path\n'
        for name in ('ab\t/dev/log', 'a\t/dev/log', 'ab\xa0/dev/log', 'ab\x1f/dev/log', 'ab\u3000/dev/log'):
            data = header + 'unix  2      [ ]         DGRAM                    34693    1898/' + name + '     /run/user/1000/systemd/notify\n'
            result = jc.parsers.netstat.parse(data, quiet=True)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]['program_name'], name)
            self.assertEqual(result[0]['path'], '/run/user/1000/systemd/notify')

        data = header + 'unix  3      [ ]         STREAM     CONNECTED     34694    1899/ab\t/dev/log     /run/user/1000/bus\n'
        result = jc.parsers.netstat.parse(data, quiet=True)
        self.assertEqual(result[0]['program_name'], 'ab\t/dev/log')
        self.assertEqual(result[0]['state'], 'CONNECTED')
        self.assertEqual(result[0]['path'], '/run/user/1000/bus')

    def test_netstat_program_name_state_words(self):
        """
        Test 'netstat -lnp' with state words in the PID/Program name column
        """
        self.assertEqual(jc.parsers.netstat.parse(self.generic_netstat_state_words, quiet=True), self.generic_netstat_state_words_json)

    def test_netstat_program_name_state_words_e(self):
        """
        Test 'netstat -lnpe' with state words in the PID/Program name column
        """
        self.assertEqual(jc.parsers.netstat.parse(self.generic_netstat_state_words_e, quiet=True), self.generic_netstat_state_words_e_json)

    def test_netstat_freebsd_protocol_names(self):
        """
        Test 'netstat' with tcp46, sctp46 and divert protocol names
        """
        self.assertEqual(jc.parsers.netstat.parse(self.generic_netstat_freebsd_protocol_names, quiet=True), self.generic_netstat_freebsd_protocol_names_json)

    def test_netstat_osx_peer_host_udp(self):
        """
        Test 'netstat -A' with a peer host name that contains 'udp' on a tcp4 row
        """
        self.assertEqual(jc.parsers.netstat.parse(self.generic_netstat_osx_peer_host_udp, quiet=True), self.generic_netstat_osx_peer_host_udp_json)

    def test_netstat_freebsd_route_host_names(self):
        """
        Test 'netstat -r' with route rows for hosts named 'Name' and 'Destination'
        """
        self.assertEqual(jc.parsers.netstat.parse(self.generic_netstat_freebsd_route_host_names, quiet=True), self.generic_netstat_freebsd_route_host_names_json)

    def test_netstat_service_port_names(self):
        """
        Test 'netstat' with service names that contain digits as ports
        """
        self.assertEqual(jc.parsers.netstat.parse(self.generic_netstat_linux_service_port_names, quiet=True), self.generic_netstat_linux_service_port_names_json)



    def test_netstat_linux_proto_text_in_program_name(self):
        """
        Test Linux 'netstat' where a line starting with Proto is not a
        full header line: it is skipped and the header in use is kept
        """
        self.assertEqual(jc.parsers.netstat.parse(self.generic_netstat_linux_proto_text_in_program_name, quiet=True), self.generic_netstat_linux_proto_text_in_program_name_json)

    def test_netstat_linux_unix_program_name_space(self):
        """
        Test Linux 'netstat -xp' with a space near the end of the program name column
        """
        self.assertEqual(jc.parsers.netstat.parse(self.generic_netstat_linux_unix_program_name_space, quiet=True), self.generic_netstat_linux_unix_program_name_space_json)

    def test_netstat_linux_unix_program_name_space_fields(self):
        """
        Test Linux 'netstat -xp' program name and path with a space in the last columns of the name
        """
        data = (
            'Active UNIX domain sockets (servers and established)\n'
            'Proto RefCnt Flags       Type       State         I-Node   PID/Program name     Path\n'
            'unix  2      [ ]         DGRAM                    34693    1899/aaaaaaaaaaa xx  /run/user/1000/systemd/notify\n'
        )
        result = jc.parsers.netstat.parse(data, quiet=True)
        self.assertEqual(result[0]['program_name'], 'aaaaaaaaaaa xx')
        self.assertEqual(result[0]['pid'], 1899)
        self.assertEqual(result[0]['path'], '/run/user/1000/systemd/notify')

    def test_netstat_linux_unix_brackets(self):
        """
        Test Linux 'netstat -xp' with brackets in program names and paths
        """
        self.assertEqual(jc.parsers.netstat.parse(self.generic_netstat_linux_unix_brackets, quiet=True), self.generic_netstat_linux_unix_brackets_json)

    def test_netstat_linux_unix_brackets_fields(self):
        """
        Test Linux 'netstat -xp' keeps brackets outside the Flags column
        """
        data = (
            'Active UNIX domain sockets (servers and established)\n'
            'Proto RefCnt Flags       Type       State         I-Node   PID/Program name     Path\n'
            'unix  2      [ ]         DGRAM                    40001    1898/systemd         /run/[a]/b\n'
            'unix  2      [ ACC ]     STREAM     LISTENING     40003    31337/systemd        [/var/run/docker.sock\n'
        )
        result = jc.parsers.netstat.parse(data, quiet=True)
        self.assertEqual(result[0]['flags'], None)
        self.assertEqual(result[0]['path'], '/run/[a]/b')
        self.assertEqual(result[1]['flags'], 'ACC')
        self.assertEqual(result[1]['path'], '[/var/run/docker.sock')

    def test_netstat_linux_unix_path_whitespace(self):
        """
        Test Linux 'netstat -xp' with whitespace characters in paths on rows with and without a state
        """
        self.assertEqual(jc.parsers.netstat.parse(self.generic_netstat_linux_unix_path_whitespace, quiet=True), self.generic_netstat_linux_unix_path_whitespace_json)

    def test_netstat_linux_unix_path_whitespace_fields(self):
        """
        Test Linux 'netstat -xp' path with a 0x1f character is the same with and without a state
        """
        data = (
            'Active UNIX domain sockets (servers and established)\n'
            'Proto RefCnt Flags       Type       State         I-Node   PID/Program name     Path\n'
            'unix  2      [ ACC ]     STREAM     LISTENING     34696    1898/systemd         /run/bus\x1f/hidden\n'
            'unix  2      [ ]         DGRAM                    34693    1898/systemd         /run/bus\x1f/hidden\n'
        )
        result = jc.parsers.netstat.parse(data, quiet=True)
        self.assertEqual(result[0]['path'], '/run/bus\x1f/hidden')
        self.assertEqual(result[1]['path'], '/run/bus\x1f/hidden')
        self.assertEqual(result[1]['state'], None)
        self.assertEqual(result[1]['inode'], 34693)

    def test_netstat_windows_service_name_protocol_prefix(self):
        """
        Test Windows 'netstat -b' with service names that start with a protocol name
        """
        self.assertEqual(jc.parsers.netstat.parse(self.generic_netstat_windows_service_name_protocol_prefix, quiet=True), self.generic_netstat_windows_service_name_protocol_prefix_json)

    def test_netstat_windows_service_name_protocol_prefix_fields(self):
        """
        Test Windows 'netstat -b' keeps one record per socket for a service named TCPSvc
        """
        data = (
            'Active Connections\n\n'
            '  Proto  Local Address          Foreign Address        State           PID\n'
            '  TCP    0.0.0.0:4325           0.0.0.0:0              LISTENING       5876\n'
            '  TCPSvc\n'
            ' [svchost.exe]\n'
        )
        result = jc.parsers.netstat.parse(data, quiet=True)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['proto'], 'TCP')
        self.assertEqual(result[0]['program_name'], '[svchost.exe]')


if __name__ == '__main__':
    unittest.main()
