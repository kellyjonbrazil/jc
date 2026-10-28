import os
import unittest
import json
import jc.parsers.iw_scan

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iw-scan0.out'), 'r', encoding='utf-8') as f:
        centos_7_7_iw_scan0 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iw-scan1.out'), 'r', encoding='utf-8') as f:
        centos_7_7_iw_scan1 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iw-scan2.out'), 'r', encoding='utf-8') as f:
        centos_7_7_iw_scan2 = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iw-scan0.json'), 'r', encoding='utf-8') as f:
        centos_7_7_iw_scan0_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iw-scan1.json'), 'r', encoding='utf-8') as f:
        centos_7_7_iw_scan1_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iw-scan2.json'), 'r', encoding='utf-8') as f:
        centos_7_7_iw_scan2_json = json.loads(f.read())


    def test_iw_scan_nodata(self):
        """
        Test 'iw_scan' parser with no data
        """
        self.assertEqual(jc.parsers.iw_scan.parse('', quiet=True), [])

    def test_iw_scan0_centos_7_7(self):
        """
        Test 'iw_scan' on Centos 7.7
        """
        self.assertEqual(jc.parsers.iw_scan.parse(self.centos_7_7_iw_scan0, quiet=True), self.centos_7_7_iw_scan0_json)

    def test_iw_scan1_centos_7_7(self):
        """
        Test 'iw_scan' on Centos 7.7
        """
        self.assertEqual(jc.parsers.iw_scan.parse(self.centos_7_7_iw_scan1, quiet=True), self.centos_7_7_iw_scan1_json)

    def test_iw_scan2_centos_7_7(self):
        """
        Test 'iw_scan' on Centos 7.7
        """
        self.assertEqual(jc.parsers.iw_scan.parse(self.centos_7_7_iw_scan2, quiet=True), self.centos_7_7_iw_scan2_json)

    def test_iw_scan_non_finite_values(self):
        """
        Test 'iw dev wlan0 scan' with an SSID of inf and a WPS model of nan:
        the text is kept
        """
        data = (
            'BSS 00:19:a9:cd:c6:80 (on wlan0)\n'
            '\tfreq: 2412\n'
            '\tsignal: -45.00 dBm\n'
            '\tSSID: inf\n'
            '\tSupported rates: 1.0* 5.5 Infinity \n'
            '\tWPS:\t * Version: 1.0\n'
            '\t\t * Model: nan\n'
        )
        result = jc.parsers.iw_scan.parse(data, quiet=True)
        self.assertEqual(result[0]['ssid'], 'inf')
        self.assertEqual(result[0]['model'], 'nan')
        self.assertEqual(result[0]['freq'], 2412)
        self.assertEqual(result[0]['signal_dbm'], -45.0)
        self.assertEqual(result[0]['supported_rates'], [1.0, 5.5, 'Infinity'])
        self.assertEqual(result[0]['selected_rates'], [1.0])


if __name__ == '__main__':
    unittest.main()
