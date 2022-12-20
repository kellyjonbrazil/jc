import os
import json
import unittest
import jc.parsers.iwconfig

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class iwconfigTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, 'fixtures/ubuntu-20.10/iwconfig.out'), 'r', encoding='utf-8') as f:
        ubuntu_20_10_iwconfig= f.read()

    # output
    with open(os.path.join(THIS_DIR, 'fixtures/ubuntu-20.10/iwconfig.json'), 'r', encoding='utf-8') as f:
        ubuntu_20_10_iwconfig_json= json.loads(f.read())

    with open(os.path.join(THIS_DIR, 'fixtures/ubuntu-20.10/iwconfig-raw.json'), 'r', encoding='utf-8') as f:
        ubuntu_20_10_iwconfig_raw_json= json.loads(f.read())


    def test_iwconfig_nodata(self):
        """
        Test 'iwconfig' with no data
        """
        self.assertEqual(jc.parsers.iwconfig.parse('', quiet=True), [])

    def test_iwconfig_ubuntu_20_04(self):
        """
        Test 'iwconfig' raw on Ubuntu 20.10
        """
        self.assertEqual(jc.parsers.iwconfig.parse(self.ubuntu_20_10_iwconfig, quiet=True, raw=True), self.ubuntu_20_10_iwconfig_raw_json)

    def test_iwconfig_ubuntu_20_04(self):
        """
        Test 'iwconfig' on Ubuntu 20.10
        """
        self.assertEqual(jc.parsers.iwconfig.parse(self.ubuntu_20_10_iwconfig, quiet=True), self.ubuntu_20_10_iwconfig_json)

if __name__ == '__main__':
    unittest.main()
