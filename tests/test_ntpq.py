import os
import unittest
import json
import jc.parsers.ntpq

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ntpq-p.out'), 'r', encoding='utf-8') as f:
        centos_7_7_ntpq_p = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ntpq-p.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ntpq_p = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ntpq-pn.out'), 'r', encoding='utf-8') as f:
        centos_7_7_ntpq_pn = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ntpq-pn.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ntpq_pn = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ntpq-p2.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ntpq_p2 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/ntpq-p.out'), 'r', encoding='utf-8') as f:
        freebsd12_ntpq_p = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ntpq-p.json'), 'r', encoding='utf-8') as f:
        centos_7_7_ntpq_p_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ntpq-p.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ntpq_p_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ntpq-pn.json'), 'r', encoding='utf-8') as f:
        centos_7_7_ntpq_pn_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ntpq-pn.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ntpq_pn_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ntpq-p2.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ntpq_p2_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/ntpq-p.json'), 'r', encoding='utf-8') as f:
        freebsd12_ntpq_p_json = json.loads(f.read())


    def test_ntpq_p_nodata(self):
        """
        Test 'ntpq -p' with no data
        """
        self.assertEqual(jc.parsers.ntpq.parse('', quiet=True), [])

    def test_ntpq_p_centos_7_7(self):
        """
        Test 'ntpq -p' on Centos 7.7
        """
        self.assertEqual(jc.parsers.ntpq.parse(self.centos_7_7_ntpq_p, quiet=True), self.centos_7_7_ntpq_p_json)

    def test_ntpq_p_ubuntu_18_4(self):
        """
        Test 'ntpq -p' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.ntpq.parse(self.ubuntu_18_4_ntpq_p, quiet=True), self.ubuntu_18_4_ntpq_p_json)

    def test_ntpq_pn_centos_7_7(self):
        """
        Test 'ntpq -pn' on Centos 7.7
        """
        self.assertEqual(jc.parsers.ntpq.parse(self.centos_7_7_ntpq_pn, quiet=True), self.centos_7_7_ntpq_pn_json)

    def test_ntpq_pn_ubuntu_18_4(self):
        """
        Test 'ntpq -pn' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.ntpq.parse(self.ubuntu_18_4_ntpq_pn, quiet=True), self.ubuntu_18_4_ntpq_pn_json)

    def test_ntpq_p2_ubuntu_18_4(self):
        """
        Test 'ntpq -p' with ip data with spaces on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.ntpq.parse(self.ubuntu_18_4_ntpq_p2, quiet=True), self.ubuntu_18_4_ntpq_p2_json)

    def test_ntpq_p_freebsd12(self):
        """
        Test 'ntpq -p' on FreeBSD12
        """
        self.assertEqual(jc.parsers.ntpq.parse(self.freebsd12_ntpq_p, quiet=True), self.freebsd12_ntpq_p_json)


if __name__ == '__main__':
    unittest.main()
