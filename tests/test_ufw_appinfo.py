import os
import json
import unittest
import jc.parsers.ufw_appinfo

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ufw-appinfo-all.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_04_ufw_appinfo_all = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ufw-appinfo-test.out'), 'r', encoding='utf-8') as f:
        generic_ufw_appinfo_test = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ufw-appinfo-test2.out'), 'r', encoding='utf-8') as f:
        generic_ufw_appinfo_test2 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ufw-appinfo-test3.out'), 'r', encoding='utf-8') as f:
        generic_ufw_appinfo_test3 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ufw-appinfo-msn.out'), 'r', encoding='utf-8') as f:
        generic_ufw_appinfo_msn = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ufw-appinfo-multiline-description.out'), 'r', encoding='utf-8') as f:
        generic_ufw_appinfo_multiline_description = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ufw-appinfo-all.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_04_ufw_appinfo_all_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ufw-appinfo-test.json'), 'r', encoding='utf-8') as f:
        generic_ufw_appinfo_test_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ufw-appinfo-test2.json'), 'r', encoding='utf-8') as f:
        generic_ufw_appinfo_test2_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ufw-appinfo-test3.json'), 'r', encoding='utf-8') as f:
        generic_ufw_appinfo_test3_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ufw-appinfo-msn.json'), 'r', encoding='utf-8') as f:
        generic_ufw_appinfo_msn_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ufw-appinfo-multiline-description.json'), 'r', encoding='utf-8') as f:
        generic_ufw_appinfo_multiline_description_json = json.loads(f.read())


    def test_ufw_appinfo_nodata(self):
        """
        Test 'ufw_appinfo' with no data
        """
        self.assertEqual(jc.parsers.ufw_appinfo.parse('', quiet=True), [])

    def test_ufw_appinfo_ubuntu_18_04_all(self):
        """
        Test 'ufw app info all' on Ubuntu 18.04
        """
        self.assertEqual(jc.parsers.ufw_appinfo.parse(self.ubuntu_18_04_ufw_appinfo_all, quiet=True), self.ubuntu_18_04_ufw_appinfo_all_json)

    def test_ufw_appinfo_generic_test(self):
        """
        Test 'ufw app info [application]' sample
        """
        self.assertEqual(jc.parsers.ufw_appinfo.parse(self.generic_ufw_appinfo_test, quiet=True), self.generic_ufw_appinfo_test_json)

    def test_ufw_appinfo_generic_test2(self):
        """
        Test 'ufw app info [application]' sample
        """
        self.assertEqual(jc.parsers.ufw_appinfo.parse(self.generic_ufw_appinfo_test2, quiet=True), self.generic_ufw_appinfo_test2_json)

    def test_ufw_appinfo_generic_test3(self):
        """
        Test 'ufw app info [application]' sample
        """
        self.assertEqual(jc.parsers.ufw_appinfo.parse(self.generic_ufw_appinfo_test3, quiet=True), self.generic_ufw_appinfo_test3_json)

    def test_ufw_appinfo_generic_msn(self):
        """
        Test 'ufw app info MSN' sample
        """
        self.assertEqual(jc.parsers.ufw_appinfo.parse(self.generic_ufw_appinfo_msn, quiet=True), self.generic_ufw_appinfo_msn_json)

    def test_ufw_appinfo_generic_multiline_description(self):
        """
        Test 'ufw app info all' with mult-line description field
        """
        self.assertEqual(jc.parsers.ufw_appinfo.parse(self.generic_ufw_appinfo_multiline_description, quiet=True), self.generic_ufw_appinfo_multiline_description_json)


if __name__ == '__main__':
    unittest.main()
