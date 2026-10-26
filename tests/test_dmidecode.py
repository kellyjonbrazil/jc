import os
import json
import unittest
from jc.exceptions import ParseError
import jc.parsers.dmidecode

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # new input/output fixtures
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/dmidecode-multiple-descriptions.out'), 'r', encoding='utf-8') as f:
        generic_dmidecode_multiple_descriptions = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/dmidecode-multiple-descriptions.json'), 'r', encoding='utf-8') as f:
        generic_dmidecode_multiple_descriptions_json = json.loads(f.read())

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/dmidecode.out'), 'r', encoding='utf-8') as f:
        centos_7_7_dmidecode = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/dmidecode.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_dmidecode = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/fedora32/dmidecode.out'), 'r', encoding='utf-8') as f:
        fedora32_dmidecode = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/dmidecode.json'), 'r', encoding='utf-8') as f:
        centos_7_7_dmidecode_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/dmidecode.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_dmidecode_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/fedora32/dmidecode.json'), 'r', encoding='utf-8') as f:
        fedora32_dmidecode_json = json.loads(f.read())


    def test_dmidecode_nodata(self):
        """
        Test 'dmidecode' with no data
        """
        self.assertEqual(jc.parsers.dmidecode.parse('', quiet=True), [])

    def test_dmidecode_centos_7_7(self):
        """
        Test 'dmidecode' on Centos 7.7
        """
        self.assertEqual(jc.parsers.dmidecode.parse(self.centos_7_7_dmidecode, quiet=True), self.centos_7_7_dmidecode_json)

    def test_dmidecode_ubuntu_18_4(self):
        """
        Test 'dmidecode' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.dmidecode.parse(self.ubuntu_18_4_dmidecode, quiet=True), self.ubuntu_18_4_dmidecode_json)

    def test_dmidecode_fedora32(self):
        """
        Test 'dmidecode' on Fedora 32
        """
        self.assertEqual(jc.parsers.dmidecode.parse(self.fedora32_dmidecode, quiet=True), self.fedora32_dmidecode_json)

    def test_dmidecode_multiple_descriptions(self):
        """
        Test 'dmidecode' with many descriptions under a single handle
        """
        self.assertEqual(jc.parsers.dmidecode.parse(self.generic_dmidecode_multiple_descriptions, quiet=True), self.generic_dmidecode_multiple_descriptions_json)

    def test_dmidecode_malformed_handle(self):
        """
        Test 'dmidecode' with malformed Handle lines (raises ParseError)
        """
        handles = [
            'Handle 0x1, DMI type 0, 24 bytes',
            'Handle 0xZZZZ, DMI type 0, 24 bytes',
            'Handle 0x0000 DMI type 0, 24 bytes',
            'Handle 0x0000, DMI type -1, 24 bytes',
            'Handle 0x0000, DMI type 0, 24 bytes bytes',
            'Handle ' + 'x' * 5000 + ' a b c d bytes'
        ]

        for handle in handles:
            with self.subTest(handle[:60]):
                data = 'Getting SMBIOS data from sysfs.\n\n' + handle + '\nBIOS Information\n\tVendor: Acme\n\nBIOS Language\n'
                with self.assertRaises(ParseError):
                    jc.parsers.dmidecode.parse(data, quiet=True)

    def test_dmidecode_handle_fields(self):
        """
        Test 'dmidecode' handle, type, and bytes fields, including repeated
        descriptions under the same handle
        """
        data = 'Getting SMBIOS data from sysfs.\n\nHandle 0x00aB, DMI type 11, 5 bytes\nOEM Strings\n\tString 1: a\nSecond Description\n\tString 2: b\n\n'
        expected = [
            {'handle': '0x00aB', 'type': 11, 'bytes': 5, 'description': 'OEM Strings', 'values': {'string_1': 'a'}},
            {'handle': '0x00aB', 'type': 11, 'bytes': 5, 'description': 'Second Description', 'values': {'string_2': 'b'}}
        ]
        self.assertEqual(jc.parsers.dmidecode.parse(data, quiet=True), expected)


if __name__ == '__main__':
    unittest.main()
