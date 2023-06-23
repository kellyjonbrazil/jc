import os
import json
import unittest
import jc.parsers.ip_route

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # INPUT
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ip_route.out'), 'r',
              encoding='utf-8') as f:
        ubuntu_18_4_ip_route = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ip_route.out'), 'r',
              encoding='utf-8') as f:
        centos_7_7_ip_route = f.read()

    # OUTPUT
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ip_route.json'), 'r',
              encoding='utf-8') as f:
        ubuntu_18_4_ip_route_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ip_route.json'), 'r',
              encoding='utf-8') as f:
        centos_7_7_ip_route_json = json.loads(f.read())

    def test_ip_route_nodata(self):
        """
        Test  'ip_route' with no data
        """
        self.assertEqual(jc.parsers.ip_route.parse('', quiet=True), [])

    def test_ip_route_ubuntu_18_4(self):
        """
        Test 'ip_route' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.ip_route.parse(self.ubuntu_18_4_ip_route, quiet=True),
                         self.ubuntu_18_4_ip_route_json)

    def test_ip_route_centos_7_7(self):
        """
        Test 'history' on Centos 7.7
        """
        self.assertEqual(jc.parsers.ip_route.parse(self.centos_7_7_ip_route, quiet=True),
                         self.centos_7_7_ip_route_json)


if __name__ == '__main__':
    unittest.main()
