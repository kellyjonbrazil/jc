import os
import json
import unittest
import jc.parsers.ifconfig

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ifconfig.out'), 'r', encoding='utf-8') as f:
        centos_7_7_ifconfig = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-16.04/ifconfig.out'), 'r', encoding='utf-8') as f:
        ubuntu_16_4_ifconfig = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ifconfig.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ifconfig = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/ifconfig.out'), 'r', encoding='utf-8') as f:
        osx_10_11_6_ifconfig = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/ifconfig2.out'), 'r', encoding='utf-8') as f:
        osx_10_11_6_ifconfig2 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ifconfig.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ifconfig = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ifconfig2.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ifconfig2 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/ifconfig-extra-fields.out'), 'r', encoding='utf-8') as f:
        osx_freebsd12_ifconfig_extra_fields = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/ifconfig-extra-fields2.out'), 'r', encoding='utf-8') as f:
        osx_freebsd12_ifconfig_extra_fields2 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/ifconfig-extra-fields3.out'), 'r', encoding='utf-8') as f:
        osx_freebsd12_ifconfig_extra_fields3 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/ifconfig-extra-fields4.out'), 'r', encoding='utf-8') as f:
        osx_freebsd12_ifconfig_extra_fields4 = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ifconfig.json'), 'r', encoding='utf-8') as f:
        centos_7_7_ifconfig_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-16.04/ifconfig.json'), 'r', encoding='utf-8') as f:
        ubuntu_16_4_ifconfig_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ifconfig.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ifconfig_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/ifconfig.json'), 'r', encoding='utf-8') as f:
        osx_10_11_6_ifconfig_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/ifconfig2.json'), 'r', encoding='utf-8') as f:
        osx_10_11_6_ifconfig2_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ifconfig.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ifconfig_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ifconfig2.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_ifconfig2_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/ifconfig-extra-fields.json'), 'r', encoding='utf-8') as f:
        freebsd12_ifconfig_extra_fields_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/ifconfig-extra-fields2.json'), 'r', encoding='utf-8') as f:
        freebsd12_ifconfig_extra_fields2_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/ifconfig-extra-fields3.json'), 'r', encoding='utf-8') as f:
        freebsd12_ifconfig_extra_fields3_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/ifconfig-extra-fields4.json'), 'r', encoding='utf-8') as f:
        freebsd12_ifconfig_extra_fields4_json = json.loads(f.read())

    def test_ifconfig_nodata(self):
        """
        Test 'ifconfig' with no data
        """
        self.assertEqual(jc.parsers.ifconfig.parse('', quiet=True), [])

    def test_ifconfig_centos_7_7(self):
        """
        Test 'ifconfig' on Centos 7.7
        """
        self.assertEqual(jc.parsers.ifconfig.parse(self.centos_7_7_ifconfig, quiet=True), self.centos_7_7_ifconfig_json)

    def test_ifconfig_ubuntu_16_4(self):
        """
        Test 'ifconfig' on Ubuntu 16.4
        """
        self.assertEqual(jc.parsers.ifconfig.parse(self.ubuntu_16_4_ifconfig, quiet=True), self.ubuntu_16_4_ifconfig_json)

    def test_ifconfig_ubuntu_18_4(self):
        """
        Test 'ifconfig' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.ifconfig.parse(self.ubuntu_18_4_ifconfig, quiet=True), self.ubuntu_18_4_ifconfig_json)

    def test_ifconfig_osx_10_11_6(self):
        """
        Test 'ifconfig' on OSX 10.11.6
        """
        self.assertEqual(jc.parsers.ifconfig.parse(self.osx_10_11_6_ifconfig, quiet=True), self.osx_10_11_6_ifconfig_json)

    def test_ifconfig_osx_10_11_6_2(self):
        """
        Test 'ifconfig' on OSX 10.11.6
        """
        self.assertEqual(jc.parsers.ifconfig.parse(self.osx_10_11_6_ifconfig2, quiet=True), self.osx_10_11_6_ifconfig2_json)

    def test_ifconfig_osx_10_14_6(self):
        """
        Test 'ifconfig' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.ifconfig.parse(self.osx_10_14_6_ifconfig, quiet=True), self.osx_10_14_6_ifconfig_json)

    def test_ifconfig_osx_10_14_6_2(self):
        """
        Test 'ifconfig' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.ifconfig.parse(self.osx_10_14_6_ifconfig2, quiet=True), self.osx_10_14_6_ifconfig2_json)

    def test_ifconfig_freebsd_extra_fields(self):
        """
        Test 'ifconfig' on freebsd12
        """
        self.assertEqual(jc.parsers.ifconfig.parse(self.osx_freebsd12_ifconfig_extra_fields, quiet=True), self.freebsd12_ifconfig_extra_fields_json)

    def test_ifconfig_freebsd_extra_fields2(self):
        """
        Test 'ifconfig' on freebsd12 with other fields
        """
        self.assertEqual(jc.parsers.ifconfig.parse(self.osx_freebsd12_ifconfig_extra_fields2, quiet=True), self.freebsd12_ifconfig_extra_fields2_json)

    def test_ifconfig_freebsd_extra_fields3(self):
        """
        Test 'ifconfig' on freebsd12 with other extra fields
        """
        self.assertEqual(jc.parsers.ifconfig.parse(self.osx_freebsd12_ifconfig_extra_fields3, quiet=True), self.freebsd12_ifconfig_extra_fields3_json)

    def test_ifconfig_freebsd_extra_fields4(self):
        """
        Test 'ifconfig' on freebsd12 with lane fields
        """
        self.assertEqual(jc.parsers.ifconfig.parse(self.osx_freebsd12_ifconfig_extra_fields4, quiet=True), self.freebsd12_ifconfig_extra_fields4_json)

    def test_ifconfig_utun_ipv4(self):
        """
        Test 'ifconfig' with ipv4 utun addresses (macOS)
        """
        data = r'''utun2: flags=8051<UP,POINTOPOINT,RUNNING,MULTICAST> mtu 1400
    inet 10.85.40.243 --> 10.85.40.243 netmask 0xffffffff
    inet6 fe80::3af9:d3ff:fe69:1732%utun2 prefixlen 64 scopeid 0xd
    inet6 fdae:f7e0:9f37:64::146 prefixlen 128
    nd6 options=201<PERFORMNUD,DAD>'''
        expected = [{"name":"utun2","flags":8051,"state":["UP","POINTOPOINT","RUNNING","MULTICAST"],"mtu":1400,"type":None,"mac_addr":None,"ipv4_addr":"10.85.40.243","ipv4_mask":"255.255.255.255","ipv4_bcast":None,"ipv6_addr":"fdae:f7e0:9f37:64::146","ipv6_mask":128,"ipv6_scope":None,"ipv6_type":None,"metric":None,"rx_packets":None,"rx_errors":None,"rx_dropped":None,"rx_overruns":None,"rx_frame":None,"tx_packets":None,"tx_errors":None,"tx_dropped":None,"tx_overruns":None,"tx_carrier":None,"tx_collisions":None,"rx_bytes":None,"tx_bytes":None,"ipv6_scope_id":None,"nd6_options":201,"nd6_flags":["PERFORMNUD","DAD"],"ipv4":[{"address":"10.85.40.243","mask":"255.255.255.255"}],"ipv6":[{"address":"fe80::3af9:d3ff:fe69:1732","scope_id":"utun2","mask":64,"scope":"0xd"},{"address":"fdae:f7e0:9f37:64::146","scope_id":None,"mask":128,"scope":None}]}]
        self.assertEqual(jc.parsers.ifconfig.parse(self.osx_freebsd12_ifconfig_extra_fields4, quiet=True), self.freebsd12_ifconfig_extra_fields4_json)

if __name__ == '__main__':
    unittest.main()
