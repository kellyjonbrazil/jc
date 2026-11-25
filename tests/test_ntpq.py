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

    def test_ntpq_p_space_in_refid(self):
        """
        Test 'ntpq -p' with a space in the refid and a blank line
        """
        data = (
            '     remote           refid      st t when poll reach   delay   offset  jitter\n'
            '==============================================================================\n'
            '*time.x.net      .GPS 1.          1 u   10   64  377    0.5   -1.0   0.2\n'
            ' pool.ntp.org    10.1.2.3         2 u    -   64    1   93.0   -0.8   2.8\n'
            '\n'
            '+a.b             10.0.0.1         3 u   20   64    7    1.5    0.5   0.1\n'
        )
        result = jc.parsers.ntpq.parse(data, quiet=True)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], {
            'remote': 'time.x.net', 'refid': '.GPS 1.', 'st': 1, 't': 'u', 'when': 10,
            'poll': 64, 'reach': 377, 'delay': 0.5, 'offset': -1.0, 'jitter': 0.2, 'state': '*'
        })
        self.assertEqual(result[1]['remote'], 'pool.ntp.org')
        self.assertEqual(result[1]['refid'], '10.1.2.3')
        self.assertIsNone(result[1]['state'])
        self.assertIsNone(result[1]['when'])
        self.assertEqual(result[2]['remote'], 'a.b')
        self.assertEqual(result[2]['jitter'], 0.1)


if __name__ == '__main__':
    unittest.main()
