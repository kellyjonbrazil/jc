import os
import unittest
import json
import jc.parsers.ping

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input

        # centos
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping-ip-O.out'), 'r', encoding='utf-8') as f:
            self.centos_7_7_ping_ip_O = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping-ip-O-D.out'), 'r', encoding='utf-8') as f:
            self.centos_7_7_ping_ip_O_D = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping-hostname-O.out'), 'r', encoding='utf-8') as f:
            self.centos_7_7_ping_hostname_O = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping-hostname-O-p.out'), 'r', encoding='utf-8') as f:
            self.centos_7_7_ping_hostname_O_p = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping-hostname-O-D-p-s.out'), 'r', encoding='utf-8') as f:
            self.centos_7_7_ping_hostname_O_D_p_s = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping6-ip-O-p.out'), 'r', encoding='utf-8') as f:
            self.centos_7_7_ping6_ip_O_p = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping6-ip-O-D-p.out'), 'r', encoding='utf-8') as f:
            self.centos_7_7_ping6_ip_O_D_p = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping6-hostname-O-p.out'), 'r', encoding='utf-8') as f:
            self.centos_7_7_ping6_hostname_O_p = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping6-hostname-O-D-p-s.out'), 'r', encoding='utf-8') as f:
            self.centos_7_7_ping6_hostname_O_D_p_s = f.read()

        # ubuntu

        # fedora

        # freebsd

        # osx

        

        # with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ping.out'), 'r', encoding='utf-8') as f:
        #     self.ubuntu_18_4_ping = f.read()

        # with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping-a2.out'), 'r', encoding='utf-8') as f:
        #     self.osx_10_14_6_ping_a2 = f.read()

        # with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/ping-a.out'), 'r', encoding='utf-8') as f:
        #     self.freebsd_ping_a = f.read()

        # output

        # centos
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping-ip-O.json'), 'r', encoding='utf-8') as f:
            self.centos_7_7_ping_ip_O_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping-ip-O-D.json'), 'r', encoding='utf-8') as f:
            self.centos_7_7_ping_ip_O_D_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping-hostname-O.json'), 'r', encoding='utf-8') as f:
            self.centos_7_7_ping_hostname_O_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping-hostname-O-p.json'), 'r', encoding='utf-8') as f:
            self.centos_7_7_ping_hostname_O_p_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping-hostname-O-D-p-s.json'), 'r', encoding='utf-8') as f:
            self.centos_7_7_ping_hostname_O_D_p_s_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping6-ip-O-p.json'), 'r', encoding='utf-8') as f:
            self.centos_7_7_ping6_ip_O_p_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping6-ip-O-D-p.json'), 'r', encoding='utf-8') as f:
            self.centos_7_7_ping6_ip_O_D_p_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping6-hostname-O-p.json'), 'r', encoding='utf-8') as f:
            self.centos_7_7_ping6_hostname_O_p_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ping6-hostname-O-D-p-s.json'), 'r', encoding='utf-8') as f:
            self.centos_7_7_ping6_hostname_O_D_p_s_json = json.loads(f.read())










        # with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ping.json'), 'r', encoding='utf-8') as f:
        #     self.ubuntu_18_4_ping_json = json.loads(f.read())

        # with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/ping-a2.json'), 'r', encoding='utf-8') as f:
        #     self.osx_10_14_6_ping_a2_json = json.loads(f.read())

        # with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/ping-a.json'), 'r', encoding='utf-8') as f:
        #     self.freebsd12_ping_a_json = json.loads(f.read())





    def test_ping_nodata(self):
        """
        Test 'ping' with no data
        """
        self.assertEqual(jc.parsers.ping.parse('', quiet=True), {})

    def test_ping_ip_O_centos_7_7(self):
        """
        Test 'ping <ip> -O' on Centos 7.7
        """
        self.assertEqual(jc.parsers.ping.parse(self.centos_7_7_ping_ip_O, quiet=True), self.centos_7_7_ping_ip_O_json)

    def test_ping_ip_O_D_centos_7_7(self):
        """
        Test 'ping <ip> -O -D' on Centos 7.7
        """
        self.assertEqual(jc.parsers.ping.parse(self.centos_7_7_ping_ip_O_D, quiet=True), self.centos_7_7_ping_ip_O_D_json)

    def test_ping_hostname_O_centos_7_7(self):
        """
        Test 'ping <hostname> -O' on Centos 7.7
        """
        self.assertEqual(jc.parsers.ping.parse(self.centos_7_7_ping_hostname_O, quiet=True), self.centos_7_7_ping_hostname_O_json)

    def test_ping_hostname_O_p_centos_7_7(self):
        """
        Test 'ping <hostname> -O -p' on Centos 7.7
        """
        self.assertEqual(jc.parsers.ping.parse(self.centos_7_7_ping_hostname_O_p, quiet=True), self.centos_7_7_ping_hostname_O_p_json)

    def test_ping_hostname_O_D_p_s_centos_7_7(self):
        """
        Test 'ping <hostname> -O -D -p -s' on Centos 7.7
        """
        self.assertEqual(jc.parsers.ping.parse(self.centos_7_7_ping_hostname_O_D_p_s, quiet=True), self.centos_7_7_ping_hostname_O_D_p_s_json)

    def test_ping6_ip_O_p_centos_7_7(self):
        """
        Test 'ping6 <ip> -O -p' on Centos 7.7
        """
        self.assertEqual(jc.parsers.ping.parse(self.centos_7_7_ping6_ip_O_p, quiet=True), self.centos_7_7_ping6_ip_O_p_json)

    def test_ping6_ip_O_D_p_centos_7_7(self):
        """
        Test 'ping6 <ip> -O -D -p' on Centos 7.7
        """
        self.assertEqual(jc.parsers.ping.parse(self.centos_7_7_ping6_ip_O_D_p, quiet=True), self.centos_7_7_ping6_ip_O_D_p_json)

    def test_ping6_hostname_O_p_centos_7_7(self):
        """
        Test 'ping6 <hostname> -O -p' on Centos 7.7
        """
        self.assertEqual(jc.parsers.ping.parse(self.centos_7_7_ping6_hostname_O_p, quiet=True), self.centos_7_7_ping6_hostname_O_p_json)

    def test_ping6_hostname_O_D_p_s_centos_7_7(self):
        """
        Test 'ping6 <hostname> -O -D -p -s' on Centos 7.7
        """
        self.assertEqual(jc.parsers.ping.parse(self.centos_7_7_ping6_hostname_O_D_p_s, quiet=True), self.centos_7_7_ping6_hostname_O_D_p_s_json)

    # def test_ping_ubuntu_18_4(self):
    #     """
    #     Test 'ping' on Ubuntu 18.4
    #     """
    #     self.assertEqual(jc.parsers.ping.parse(self.ubuntu_18_4_ping, quiet=True), self.ubuntu_18_4_ping_json)

    # def test_ping_a_osx_10_14_6(self):
    #     """
    #     Test 'ping -a' on OSX 10.14.6
    #     """
    #     self.assertEqual(jc.parsers.ping.parse(self.osx_10_14_6_ping_a, quiet=True), self.osx_10_14_6_ping_a_json)

    # def test_ping_a_freebsd12(self):
    #     """
    #     Test 'ping -a' on FreeBSD12
    #     """
    #     self.assertEqual(jc.parsers.ping.parse(self.freebsd_ping_a, quiet=True), self.freebsd12_ping_a_json)


if __name__ == '__main__':
    unittest.main()
