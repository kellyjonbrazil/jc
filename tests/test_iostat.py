import os
import unittest
import json
import jc.parsers.iostat
from jc.exceptions import ParseError

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # new input fixtures
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/iostat-linux-stray-line.out'), 'r', encoding='utf-8') as f:
        generic_iostat_stray_line = f.read()

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iostat.out'), 'r', encoding='utf-8') as f:
        centos_7_7_iostat = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iostat-m.out'), 'r', encoding='utf-8') as f:
        centos_7_7_iostat_m = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iostat-x.out'), 'r', encoding='utf-8') as f:
        centos_7_7_iostat_x = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iostat-mx.out'), 'r', encoding='utf-8') as f:
        centos_7_7_iostat_mx = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iostat-1.out'), 'r', encoding='utf-8') as f:
        centos_7_7_iostat_1 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/iostat.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_iostat = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/iostat-m.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_iostat_m = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/iostat-x.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_iostat_x = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/iostat-mx.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_iostat_mx = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/iostat-1.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_iostat_1 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.10/iostat.out'), 'r', encoding='utf-8') as f:
        ubuntu_20_10_iostat = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.10/iostat-m.out'), 'r', encoding='utf-8') as f:
        ubuntu_20_10_iostat_m = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.10/iostat-x.out'), 'r', encoding='utf-8') as f:
        ubuntu_20_10_iostat_x = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.10/iostat-mx.out'), 'r', encoding='utf-8') as f:
        ubuntu_20_10_iostat_mx = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iostat.json'), 'r', encoding='utf-8') as f:
        centos_7_7_iostat_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iostat-m.json'), 'r', encoding='utf-8') as f:
        centos_7_7_iostat_m_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iostat-x.json'), 'r', encoding='utf-8') as f:
        centos_7_7_iostat_x_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iostat-mx.json'), 'r', encoding='utf-8') as f:
        centos_7_7_iostat_mx_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iostat-1.json'), 'r', encoding='utf-8') as f:
        centos_7_7_iostat_1_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/iostat.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_iostat_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/iostat-m.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_iostat_m_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/iostat-x.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_iostat_x_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/iostat-mx.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_iostat_mx_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/iostat-1.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_iostat_1_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.10/iostat.json'), 'r', encoding='utf-8') as f:
        ubuntu_20_10_iostat_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.10/iostat-m.json'), 'r', encoding='utf-8') as f:
        ubuntu_20_10_iostat_m_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.10/iostat-x.json'), 'r', encoding='utf-8') as f:
        ubuntu_20_10_iostat_x_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.10/iostat-mx.json'), 'r', encoding='utf-8') as f:
        ubuntu_20_10_iostat_mx_json = json.loads(f.read())


    def test_iostat_nodata(self):
        """
        Test 'iostat' with no data
        """
        self.assertEqual(jc.parsers.iostat.parse('', quiet=True), [])

    def test_iostat_centos_7_7(self):
        """
        Test 'iostat' on Centos 7.7
        """
        self.assertEqual(jc.parsers.iostat.parse(self.centos_7_7_iostat, quiet=True), self.centos_7_7_iostat_json)

    def test_iostat_m_centos_7_7(self):
        """
        Test 'iostat -m' on Centos 7.7
        """
        self.assertEqual(jc.parsers.iostat.parse(self.centos_7_7_iostat_m, quiet=True), self.centos_7_7_iostat_m_json)

    def test_iostat_x_centos_7_7(self):
        """
        Test 'iostat -x' on Centos 7.7
        """
        self.assertEqual(jc.parsers.iostat.parse(self.centos_7_7_iostat_x, quiet=True), self.centos_7_7_iostat_x_json)

    def test_iostat_mx_centos_7_7(self):
        """
        Test 'iostat -mx' on Centos 7.7
        """
        self.assertEqual(jc.parsers.iostat.parse(self.centos_7_7_iostat_mx, quiet=True), self.centos_7_7_iostat_mx_json)

    def test_iostat_1_centos_7_7(self):
        """
        Test 'iostat 1 3' on Centos 7.7
        """
        self.assertEqual(jc.parsers.iostat.parse(self.centos_7_7_iostat_1, quiet=True), self.centos_7_7_iostat_1_json)

    def test_iostat_ubuntu_18_4(self):
        """
        Test 'iostat' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.iostat.parse(self.ubuntu_18_4_iostat, quiet=True), self.ubuntu_18_4_iostat_json)

    def test_iostat_m_ubuntu_18_4(self):
        """
        Test 'iostat -m' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.iostat.parse(self.ubuntu_18_4_iostat_m, quiet=True), self.ubuntu_18_4_iostat_m_json)

    def test_iostat_x_ubuntu_18_4(self):
        """
        Test 'iostat -x' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.iostat.parse(self.ubuntu_18_4_iostat_x, quiet=True), self.ubuntu_18_4_iostat_x_json)

    def test_iostat_mx_ubuntu_18_4(self):
        """
        Test 'iostat -mx' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.iostat.parse(self.ubuntu_18_4_iostat_mx, quiet=True), self.ubuntu_18_4_iostat_mx_json)

    def test_iostat_1_ubuntu_18_4(self):
        """
        Test 'iostat 1 3' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.iostat.parse(self.ubuntu_18_4_iostat_1, quiet=True), self.ubuntu_18_4_iostat_1_json)

    def test_iostat_ubuntu_20_10(self):
        """
        Test 'iostat' on Ubuntu 20.10
        """
        self.assertEqual(jc.parsers.iostat.parse(self.ubuntu_20_10_iostat, quiet=True), self.ubuntu_20_10_iostat_json)

    def test_iostat_m_ubuntu_20_10(self):
        """
        Test 'iostat -m' on Ubuntu 20.10
        """
        self.assertEqual(jc.parsers.iostat.parse(self.ubuntu_20_10_iostat_m, quiet=True), self.ubuntu_20_10_iostat_m_json)

    def test_iostat_x_ubuntu_20_10(self):
        """
        Test 'iostat -x' on Ubuntu 20.10
        """
        self.assertEqual(jc.parsers.iostat.parse(self.ubuntu_20_10_iostat_x, quiet=True), self.ubuntu_20_10_iostat_x_json)

    def test_iostat_mx_ubuntu_20_10(self):
        """
        Test 'iostat -mx' on Ubuntu 20.10
        """
        self.assertEqual(jc.parsers.iostat.parse(self.ubuntu_20_10_iostat_mx, quiet=True), self.ubuntu_20_10_iostat_mx_json)


    def test_iostat_stray_line(self):
        """
        Test 'iostat' with a line that is not iostat data inside a table. Should raise ParseError
        """
        self.assertRaises(ParseError, jc.parsers.iostat.parse, self.generic_iostat_stray_line, quiet=True)

    def test_iostat_ragged_rows(self):
        """
        Test 'iostat' rows with fewer or more fields than the header. Each should raise ParseError
        """
        for bad in ('sda 1.5', 'sdb 2.5 3.5 4.5', 'random'):
            self.assertRaises(ParseError, jc.parsers.iostat.parse, 'Device: r/s w/s\n' + bad, quiet=True)

    def test_iostat_whitespace_only_line(self):
        """
        Test 'iostat' with whitespace-only lines inside a table. They are skipped like blank lines
        """
        data = 'Device: r/s w/s\nsda 1.5 2.5\n   \n\t\nsdb 3.5 4.5\n'
        self.assertEqual([d['device'] for d in jc.parsers.iostat.parse(data, quiet=True)], ['sda', 'sdb'])


if __name__ == '__main__':
    unittest.main()
