import os
import json
import unittest
import jc.parsers.efibootmgr

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/opensuse-leap-15.5/efibootmgr-v.out'), 'r', encoding='utf-8') as f:
        opensuse_leap_15_5_efibootmgr_v = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/opensuse-leap-15.5/efibootmgr.out'), 'r', encoding='utf-8') as f:
        opensuse_leap_15_5_efibootmgr = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/opensuse-leap-15.5/efibootmgr-v.json'), 'r', encoding='utf-8') as f:
        opensuse_leap_15_5_efibootmgr_json_v = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/opensuse-leap-15.5/efibootmgr.json'), 'r', encoding='utf-8') as f:
        opensuse_leap_15_5_efibootmgr_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/efibootmgr-label-with-key.out'), 'r', encoding='utf-8') as f:
        generic_efibootmgr_label_with_key = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/efibootmgr-label-with-key.json'), 'r', encoding='utf-8') as f:
        generic_efibootmgr_label_with_key_json = json.loads(f.read())

    def test_efibootmgr_nodata(self):
        """
        Test 'efibootmgr' with no data
        """
        self.assertEqual(jc.parsers.efibootmgr.parse('', quiet=True), {})

    def test_efibootmgr_v_opensuse_leap_15_5(self):
        """
        Test 'efibootmgr -v' on Opensuse Leap 15.5
        """
        self.assertEqual(jc.parsers.efibootmgr.parse(self.opensuse_leap_15_5_efibootmgr_v, quiet=True), self.opensuse_leap_15_5_efibootmgr_json_v)

    def test_efibootmgr_opensuse_leap_15_5(self):
        """
        Test 'efibootmgr' on Opensuse Leap 15.5
        """
        self.assertEqual(jc.parsers.efibootmgr.parse(self.opensuse_leap_15_5_efibootmgr, quiet=True), self.opensuse_leap_15_5_efibootmgr_json)

    def test_efibootmgr_label_with_key(self):
        """
        Test 'efibootmgr' with boot entry labels that contain other key names
        """
        self.assertEqual(jc.parsers.efibootmgr.parse(self.generic_efibootmgr_label_with_key, quiet=True), self.generic_efibootmgr_label_with_key_json)


if __name__ == '__main__':
    unittest.main()
