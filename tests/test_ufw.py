import os
import json
import unittest
import jc.parsers.ufw

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ufw.out'), 'r', encoding='utf-8') as f:
            self.generic_ufw = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ufw-numbered.out'), 'r', encoding='utf-8') as f:
            self.generic_ufw_numbered = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ufw-inactive.out'), 'r', encoding='utf-8') as f:
            self.generic_ufw_inactive = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ufw.json'), 'r', encoding='utf-8') as f:
            self.generic_ufw_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ufw-numbered.json'), 'r', encoding='utf-8') as f:
            self.generic_ufw_numbered_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ufw-inactive.json'), 'r', encoding='utf-8') as f:
            self.generic_ufw_inactive_json = json.loads(f.read())

    def test_ufw_nodata(self):
        """
        Test 'ufw' with no data
        """
        self.assertEqual(jc.parsers.ufw.parse('', quiet=True), {})

    def test_ufw_verbose(self):
        """
        Test 'ufw status verbose' sample
        """
        self.assertEqual(jc.parsers.ufw.parse(self.generic_ufw, quiet=True), self.generic_ufw_json)

    def test_ufw_verbose_numbered(self):
        """
        Test 'ufw status verbose numbered' sample
        """
        self.assertEqual(jc.parsers.ufw.parse(self.generic_ufw_numbered, quiet=True), self.generic_ufw_numbered_json)

    def test_ufw_inactive(self):
        """
        Test 'ufw status' when firewall is inactive
        """
        self.assertEqual(jc.parsers.ufw.parse(self.generic_ufw_inactive, quiet=True), self.generic_ufw_inactive_json)


if __name__ == '__main__':
    unittest.main()
