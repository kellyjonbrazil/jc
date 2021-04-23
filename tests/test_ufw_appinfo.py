import os
import json
import unittest
import jc.parsers.ufw_appinfo

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ufw-appinfo-test.out'), 'r', encoding='utf-8') as f:
            self.generic_ufw_appinfo_test = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ufw-appinfo-test2.out'), 'r', encoding='utf-8') as f:
            self.generic_ufw_appinfo_test2 = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ufw-appinfo-test3.out'), 'r', encoding='utf-8') as f:
            self.generic_ufw_appinfo_test3 = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ufw-appinfo-msn.out'), 'r', encoding='utf-8') as f:
            self.generic_ufw_appinfo_msn = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ufw-appinfo-test.json'), 'r', encoding='utf-8') as f:
            self.generic_ufw_appinfo_test_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ufw-appinfo-test2.json'), 'r', encoding='utf-8') as f:
            self.generic_ufw_appinfo_test2_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ufw-appinfo-test3.json'), 'r', encoding='utf-8') as f:
            self.generic_ufw_appinfo_test3_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ufw-appinfo-msn.json'), 'r', encoding='utf-8') as f:
            self.generic_ufw_appinfo_msn_json = json.loads(f.read())

    def test_ufw_appinfo_nodata(self):
        """
        Test 'ufw_appinfo' with no data
        """
        self.assertEqual(jc.parsers.ufw_appinfo.parse('', quiet=True), {})

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


if __name__ == '__main__':
    unittest.main()
