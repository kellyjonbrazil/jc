import os
import json
import unittest
import jc.parsers.route

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/route.out'), 'r') as f:
            self.centos_7_7_route = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/route.out'), 'r') as f:
            self.ubuntu_18_4_route = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/route-vn.out'), 'r') as f:
            self.centos_7_7_route_vn = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/route-vn.out'), 'r') as f:
            self.ubuntu_18_4_route_vn = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/route.json'), 'r') as f:
            self.centos_7_7_route_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/route.json'), 'r') as f:
            self.ubuntu_18_4_route_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/route-vn.json'), 'r') as f:
            self.centos_7_7_route_vn_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/route-vn.json'), 'r') as f:
            self.ubuntu_18_4_route_vn_json = json.loads(f.read())

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


if __name__ == '__main__':
    unittest.main()
