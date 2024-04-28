import os
import json
import unittest
import jc.parsers.upower

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/upower-i.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_upower_i = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/upower-d.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_upower_d = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/upower-d-clocale.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_upower_d_clocale = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/upower-i-utc.out'), 'r', encoding='utf-8') as f:
        generic_upower_i_utc = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/upower-i-non-utc.out'), 'r', encoding='utf-8') as f:
        generic_upower_i_non_utc = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/upower-i-c-locale.out'), 'r', encoding='utf-8') as f:
        generic_upower_i_c_locale = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/upower-i.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_upower_i_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/upower-d.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_upower_d_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/upower-d-clocale.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_upower_d_clocale_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/upower-i-utc.json'), 'r', encoding='utf-8') as f:
        generic_upower_i_utc_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/upower-i-non-utc.json'), 'r', encoding='utf-8') as f:
        generic_upower_i_non_utc_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/upower-i-c-locale.json'), 'r', encoding='utf-8') as f:
        generic_upower_i_c_locale_json = json.loads(f.read())


    def test_upower_nodata(self):
        """
        Test 'upower' with no data
        """
        self.assertEqual(jc.parsers.upower.parse('', quiet=True), [])

    def test_upower_i_ubuntu_18_4(self):
        """
        Test 'upower -i' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.upower.parse(self.ubuntu_18_4_upower_i, quiet=True), self.ubuntu_18_4_upower_i_json)

    def test_upower_d_ubuntu_18_4(self):
        """
        Test 'upower -d' on Ubuntu 18.4 using LANG=en_US.UTF-8
        """
        self.assertEqual(jc.parsers.upower.parse(self.ubuntu_18_4_upower_d, quiet=True), self.ubuntu_18_4_upower_d_json)

    def test_upower_d_clocale_ubuntu_18_4(self):
        """
        Test 'upower -d' on Ubuntu 18.4 using LANG=C
        """
        self.assertEqual(jc.parsers.upower.parse(self.ubuntu_18_4_upower_d, quiet=True), self.ubuntu_18_4_upower_d_json)

    def test_upower_i_utc_generic(self):
        """
        Test 'upower -i' with utc time output
        """
        self.assertEqual(jc.parsers.upower.parse(self.generic_upower_i_utc, quiet=True), self.generic_upower_i_utc_json)

    def test_upower_i_non_utc_generic(self):
        """
        Test 'upower -i' with non-utc time output
        """
        self.assertEqual(jc.parsers.upower.parse(self.generic_upower_i_non_utc, quiet=True), self.generic_upower_i_non_utc_json)

    def test_upower_i_c_locale(self):
        """
        Test 'upower -i' with LANG=C time output
        """
        self.assertEqual(jc.parsers.upower.parse(self.generic_upower_i_c_locale, quiet=True), self.generic_upower_i_c_locale_json)


if __name__ == '__main__':
    unittest.main()
