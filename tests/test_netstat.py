import os
import json
import unittest
import jc.parsers.netstat

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/netstat.out'), 'r') as f:
            self.centos_7_7_netstat = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/netstat.out'), 'r') as f:
            self.ubuntu_18_4_netstat = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/netstat-l.out'), 'r') as f:
            self.centos_7_7_netstat_l = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/netstat-l.out'), 'r') as f:
            self.ubuntu_18_4_netstat_l = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/netstat-p.out'), 'r') as f:
            self.centos_7_7_netstat_p = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/netstat-p.out'), 'r') as f:
            self.ubuntu_18_4_netstat_p = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/netstat-sudo-lnp.out'), 'r') as f:
            self.centos_7_7_netstat_sudo_lnp = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/netstat-sudo-lnp.out'), 'r') as f:
            self.ubuntu_18_4_netstat_sudo_lnp = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/netstat-sudo-aeep.out'), 'r') as f:
            self.centos_7_7_netstat_sudo_aeep = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/netstat-sudo-aeep.out'), 'r') as f:
            self.ubuntu_18_4_netstat_sudo_aeep = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/netstat.json'), 'r') as f:
            self.centos_7_7_netstat_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/netstat.json'), 'r') as f:
            self.ubuntu_18_4_netstat_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/netstat-l.json'), 'r') as f:
            self.centos_7_7_netstat_l_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/netstat-l.json'), 'r') as f:
            self.ubuntu_18_4_netstat_l_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/netstat-p.json'), 'r') as f:
            self.centos_7_7_netstat_p_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/netstat-p.json'), 'r') as f:
            self.ubuntu_18_4_netstat_p_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/netstat-sudo-lnp.json'), 'r') as f:
            self.centos_7_7_netstat_sudo_lnp_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/netstat-sudo-lnp.json'), 'r') as f:
            self.ubuntu_18_4_netstat_sudo_lnp_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/netstat-sudo-aeep.json'), 'r') as f:
            self.centos_7_7_netstat_sudo_aeep_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/netstat-sudo-aeep.json'), 'r') as f:
            self.ubuntu_18_4_netstat_sudo_aeep_json = json.loads(f.read())

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


if __name__ == '__main__':
    unittest.main()
