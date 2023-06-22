import os
import json
import unittest
import jc.parsers.route

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/route.out'), 'r', encoding='utf-8') as f:
        centos_7_7_route = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/route.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_route = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/route-vn.out'), 'r', encoding='utf-8') as f:
        centos_7_7_route_vn = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/route-vn.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_route_vn = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/nixos/route-ee.out'), 'r', encoding='utf-8') as f:
        nixos_route_ee = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/route-6.out'), 'r', encoding='utf-8') as f:
        centos_7_7_route_6 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/route-6-n.out'), 'r', encoding='utf-8') as f:
        centos_7_7_route_6_n = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/windows/windows-10/route.out'), 'r', encoding='utf-8') as f:
        windows_route = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/route.json'), 'r', encoding='utf-8') as f:
        centos_7_7_route_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/route.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_route_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/route-vn.json'), 'r', encoding='utf-8') as f:
        centos_7_7_route_vn_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/route-vn.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_route_vn_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/nixos/route-ee.json'), 'r', encoding='utf-8') as f:
        nixos_route_ee_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/route-6.json'), 'r', encoding='utf-8') as f:
        centos_7_7_route_6_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/route-6-n.json'), 'r', encoding='utf-8') as f:
        centos_7_7_route_6_n_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/windows/windows-10/route.json'), 'r', encoding='utf-8') as f:
        windows_route_route_json = json.loads(f.read())

    def test_route_nodata(self):
        """
        Test 'route' with no data
        """
        self.assertEqual(jc.parsers.route.parse('', quiet=True), [])

    def test_route_centos_7_7(self):
        """
        Test 'route' on Centos 7.7
        """
        self.assertEqual(jc.parsers.route.parse(self.centos_7_7_route, quiet=True), self.centos_7_7_route_json)

    def test_route_ubuntu_18_4(self):
        """
        Test 'route' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.route.parse(self.ubuntu_18_4_route, quiet=True), self.ubuntu_18_4_route_json)

    def test_route_vn_centos_7_7(self):
        """
        Test 'route -vn' on Centos 7.7
        """
        self.assertEqual(jc.parsers.route.parse(self.centos_7_7_route_vn, quiet=True), self.centos_7_7_route_vn_json)

    def test_route_vn_ubuntu_18_4(self):
        """
        Test 'route -vn' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.route.parse(self.ubuntu_18_4_route_vn, quiet=True), self.ubuntu_18_4_route_vn_json)

    def test_route_ee_nixos(self):
        """
        Test 'route -ee' on NixOS
        """
        self.assertEqual(jc.parsers.route.parse(self.nixos_route_ee, quiet=True), self.nixos_route_ee_json)

    def test_route_6_centos_7_7(self):
        """
        Test 'route -6' on Centos 7.7
        """
        self.assertEqual(jc.parsers.route.parse(self.centos_7_7_route_6, quiet=True), self.centos_7_7_route_6_json)

    def test_route_6_n_centos_7_7(self):
        """
        Test 'route -6 -n' on Centos 7.7
        """
        self.assertEqual(jc.parsers.route.parse(self.centos_7_7_route_6_n, quiet=True), self.centos_7_7_route_6_n_json)

    def test_route_windows(self):
        """
        Test 'route print' on Windows
        """
        self.assertEqual(jc.parsers.route.parse(self.windows_route, quiet=True), self.windows_route_route_json)


if __name__ == '__main__':
    unittest.main()
