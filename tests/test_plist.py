import os
import unittest
import json
import plistlib
from datetime import datetime
import tempfile
from unittest import mock
import jc.parsers.plist
from jc.exceptions import ParseError

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

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/plist-nextstep.plist'), 'rb') as f:
        nextstep = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/plist-nextstep2.plist'), 'rb') as f:
        nextstep2 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/plist-shared-refs-bin.plist'), 'rb') as f:
        shared_refs_bin = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/plist-garageband-info.json'), 'r', encoding='utf-8') as f:
        generic_garageband_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/plist-safari-info.json'), 'r', encoding='utf-8') as f:
        generic_safari_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/plist-alltypes.json'), 'r', encoding='utf-8') as f:
        generic_alltypes_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/plist-alltypes-bin.json'), 'r', encoding='utf-8') as f:
        generic_alltypes_bin_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/plist-nextstep.json'), 'r', encoding='utf-8') as f:
        nextstep_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/plist-nextstep2.json'), 'r', encoding='utf-8') as f:
        nextstep2_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/plist-shared-refs-bin.json'), 'r', encoding='utf-8') as f:
        shared_refs_bin_json = json.loads(f.read())


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


    def test_plist_nextstep(self):
        """
        Test NeXTSTEP style plist file
        """
        self.assertEqual(jc.parsers.plist.parse(self.nextstep, quiet=True), self.nextstep_json)

    def test_plist_nextstep2(self):
        """
        Test NeXTSTEP style plist file simple
        """
        self.assertEqual(jc.parsers.plist.parse(self.nextstep2, quiet=True), self.nextstep2_json)

    def test_plist_bin_shared_refs(self):
        """
        Test binary plist file with objects referenced more than once
        """
        self.assertEqual(jc.parsers.plist.parse(self.shared_refs_bin, quiet=True), self.shared_refs_bin_json)

    def test_plist_bin_shared_array_expansion_limit(self):
        """
        Test binary plist with nested shared arrays that expand far beyond the input size
        """
        node = ['x']
        for _ in range(10):
            node = [node] * 10
        data = plistlib.dumps({'a': node}, fmt=plistlib.FMT_BINARY)
        self.assertRaises(ParseError, jc.parsers.plist.parse, data, quiet=True)

    def test_plist_bin_shared_data_expansion_limit(self):
        """
        Test binary plist with one data value referenced by many keys
        """
        data = plistlib.dumps(dict.fromkeys(map(str, range(4000)), b'\xaa' * 50000), fmt=plistlib.FMT_BINARY)
        self.assertRaises(ParseError, jc.parsers.plist.parse, data, quiet=True)

    def test_plist_bin_circular_reference(self):
        """
        Test binary plist with an array that contains itself
        """
        # header, one array object holding a reference to itself, offset table, trailer
        data = b'bplist00' + bytes([0xA1, 0x00, 0x08]) + bytes(6) + bytes([1, 1]) \
            + (1).to_bytes(8, 'big') + (0).to_bytes(8, 'big') + (10).to_bytes(8, 'big')
        self.assertRaises(ParseError, jc.parsers.plist.parse, data, quiet=True)

    def test_plist_xml_dtd_defaults(self):
        """
        Test XML plist with attribute default values declared in its DTD
        """
        data = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<!DOCTYPE plist [<!ATTLIST plist version CDATA "1.0"><!ATTLIST string lang CDATA "en">]>\n'
            '<plist><dict><key>Name</key><string>Example</string>'
            '<key>Items</key><array><string>a</string><integer>3</integer><true/></array></dict></plist>\n'
        )
        expected = {'Name': 'Example', 'Items': ['a', 3, True]}
        self.assertEqual(jc.parsers.plist.parse(data, quiet=True), expected)

    def test_plist_xml_dtd_defaults_expansion_limit(self):
        """
        Test XML plist with a long attribute default value applied to many elements
        """
        data = (
            '<?xml version="1.0"?><!DOCTYPE plist [<!ATTLIST true x CDATA "' + 'v' * 100000 + '">]>'
            '<plist><array>' + '<true/>' * 2000 + '</array></plist>'
        )
        self.assertRaises(ParseError, jc.parsers.plist.parse, data, quiet=True)


    def test_plist_nextstep_temp_file_removed(self):
        """
        Test that the temporary file used for NeXTSTEP input is removed
        after both a successful and a failed parse
        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            with mock.patch.object(tempfile, 'tempdir', tmp_dir):
                jc.parsers.plist.parse(self.nextstep, quiet=True)
                self.assertEqual([], os.listdir(tmp_dir))

                with self.assertRaises(Exception):
                    jc.parsers.plist.parse('{', quiet=True)
                self.assertEqual([], os.listdir(tmp_dir))

    def test_plist_existing_iso_key(self):
        """
        Test 'plist' with a key that has the same name as a generated _iso key
        """
        data = {
            'built': datetime(1979, 5, 27, 7, 32, 0),
            'built_iso': 'my own value',
            'nested': {'when_iso': 5, 'when': datetime(2020, 1, 1, 0, 0, 0)},
            'other': datetime(2021, 1, 1, 0, 0, 0)
        }
        result = jc.parsers.plist.parse(plistlib.dumps(data), quiet=True)
        self.assertEqual(result['built_iso'], 'my own value')
        self.assertEqual(result['nested']['when_iso'], 5)
        self.assertIsInstance(result['nested']['when'], int)
        self.assertEqual(result['other_iso'], '2021-01-01T00:00:00')


if __name__ == '__main__':
    unittest.main()
