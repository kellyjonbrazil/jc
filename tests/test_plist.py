import os
import unittest
import json
import jc.parsers.plist

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/plist-garageband-info.plist'), 'rb') as f:
        generic_garageband = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/plist-safari-info.plist'), 'r', encoding='utf-8') as f:
        generic_safari = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/plist-alltypes.plist'), 'r', encoding='utf-8') as f:
        generic_alltypes = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/plist-alltypes-bin.plist'), 'rb') as f:
        generic_alltypes_bin = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/plist-garageband-info.json'), 'r', encoding='utf-8') as f:
        generic_garageband_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/plist-safari-info.json'), 'r', encoding='utf-8') as f:
        generic_safari_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/plist-alltypes.json'), 'r', encoding='utf-8') as f:
        generic_alltypes_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/plist-alltypes-bin.json'), 'r', encoding='utf-8') as f:
        generic_alltypes_bin_json = json.loads(f.read())


    def test_plist_nodata(self):
        """
        Test 'plist' with no data
        """
        self.assertEqual(jc.parsers.plist.parse('', quiet=True), {})


    def test_plist_binary(self):
        """
        Test binary plist file (garage band)
        """
        self.assertEqual(jc.parsers.plist.parse(self.generic_garageband, quiet=True), self.generic_garageband_json)


    def test_plist_xml(self):
        """
        Test XML plist file (safari)
        """
        self.assertEqual(jc.parsers.plist.parse(self.generic_safari, quiet=True), self.generic_safari_json)


    def test_plist_xml_alltypes(self):
        """
        Test XML plist file with all object types
        """
        self.assertEqual(jc.parsers.plist.parse(self.generic_alltypes, quiet=True), self.generic_alltypes_json)


    def test_plist_bin_alltypes(self):
        """
        Test binary plist file with all object types
        """
        self.assertEqual(jc.parsers.plist.parse(self.generic_alltypes_bin, quiet=True), self.generic_alltypes_bin_json)


if __name__ == '__main__':
    unittest.main()
