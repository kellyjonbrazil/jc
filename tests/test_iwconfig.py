import os
import json
import unittest
import jc.parsers.iwconfig

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class iwconfigTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, 'fixtures/generic/iwconfig.out'), 'r', encoding='utf-8') as f:
        iwconfig_output = f.read()

    with open(os.path.join(THIS_DIR, 'fixtures/generic/iwconfig-many.out'), 'r', encoding='utf-8') as f:
        iwconfig_many_output = f.read()

    with open(os.path.join(THIS_DIR, 'fixtures/generic/iwconfig-space-dash-ssid.out'), 'r', encoding='utf-8') as f:
        iwconfig_space_dash_ssid = f.read()

    with open(os.path.join(THIS_DIR, 'fixtures/generic/iwconfig-essid-variants.out'), 'r', encoding='utf-8') as f:
        iwconfig_essid_variants = f.read()

    # output
    with open(os.path.join(THIS_DIR, 'fixtures/generic/iwconfig.json'), 'r', encoding='utf-8') as f:
        iwconfig_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, 'fixtures/generic/iwconfig-raw.json'), 'r', encoding='utf-8') as f:
        iwconfig_raw_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, 'fixtures/generic/iwconfig-many.json'), 'r', encoding='utf-8') as f:
        iwconfig_many_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, 'fixtures/generic/iwconfig-space-dash-ssid.json'), 'r', encoding='utf-8') as f:
        iwconfig_space_dash_ssid_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, 'fixtures/generic/iwconfig-essid-variants.json'), 'r', encoding='utf-8') as f:
        iwconfig_essid_variants_json = json.loads(f.read())


    def test_iwconfig_line_separators(self):
        """
        Test 'iwconfig' with line-break characters other than LF in an ESSID
        """
        data = 'wlp5s0    IEEE 802.11  ESSID:"BLa\rb\x0bc\x0cd\x1ce\x1df\x1eg\x85h\u2028i\u2029j"  \n          Mode:Managed  Frequency:5.18 GHz  Access Point: E6:63:DA:16:50:BF   \n'
        result = jc.parsers.iwconfig.parse(data, quiet=True)
        self.assertEqual(result[0]['essid'], 'BLa\rb\x0bc\x0cd\x1ce\x1df\x1eg\x85h\u2028i\u2029j')
        self.assertEqual(result[0]['mode'], 'Managed')

    def test_iwconfig_nodata(self):
        """
        Test 'iwconfig' with no data
        """
        self.assertEqual(jc.parsers.iwconfig.parse('', quiet=True), [])

    def test_iwconfig_raw(self):
        """
        Test 'iwconfig' raw
        """
        self.assertEqual(jc.parsers.iwconfig.parse(self.iwconfig_output, quiet=True, raw=True), self.iwconfig_raw_json)

    def test_iwconfig(self):
        """
        Test 'iwconfig'
        """
        self.assertEqual(jc.parsers.iwconfig.parse(self.iwconfig_output, quiet=True), self.iwconfig_json)

    def test_iwconfig_many(self):
        """
        Test 'iwconfig' many interface
        """
        self.assertEqual(jc.parsers.iwconfig.parse(self.iwconfig_many_output, quiet=True), self.iwconfig_many_json)

    def test_iwconfig_space_dash_ssid(self):
        """
        Test 'iwconfig' many spaces and dashes in the SSID
        """
        self.assertEqual(jc.parsers.iwconfig.parse(self.iwconfig_space_dash_ssid, quiet=True), self.iwconfig_space_dash_ssid_json)

    def test_iwconfig_essid_variants(self):
        """
        Test 'iwconfig' with non-ASCII, off/any and Monitor mode interface lines
        """
        self.assertEqual(jc.parsers.iwconfig.parse(self.iwconfig_essid_variants, quiet=True), self.iwconfig_essid_variants_json)

    def test_iwconfig_essid_non_ascii_two_interfaces(self):
        """
        Test 'iwconfig' with a non-ASCII ESSID followed by another interface
        """
        data = (
            'wlan0     IEEE 802.11  ESSID:"caf\u00e9"  \n'
            '          Mode:Managed  Frequency:5.18 GHz\n'
            'wlan1     IEEE 802.11  ESSID:"other"  \n'
            '          Mode:Managed  Frequency:2.412 GHz\n'
        )
        result = jc.parsers.iwconfig.parse(data, quiet=True)
        self.assertEqual([(x['name'], x['essid'], x['frequency']) for x in result], [('wlan0', 'caf\u00e9', 5.18), ('wlan1', 'other', 2.412)])


if __name__ == '__main__':
    unittest.main()
