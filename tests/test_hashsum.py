import os
import unittest
import json
import jc.parsers.hashsum

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/md5sum.out'), 'r', encoding='utf-8') as f:
        centos_7_7_md5sum = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/sha256sum.out'), 'r', encoding='utf-8') as f:
        centos_7_7_sha256sum = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/sha384sum.out'), 'r', encoding='utf-8') as f:
        centos_7_7_sha384sum = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/shasum-portable.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_04_shasum_portable = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-24.04/sha256sum-binary.out'), 'r', encoding='utf-8') as f:
        ubuntu_24_04_sha256sum_binary = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-24.04/shasum-universal-bits.out'), 'r', encoding='utf-8') as f:
        ubuntu_24_04_shasum_universal_bits = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/md5.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_md5 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/shasum.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_shasum = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/sha256sum-line-separator.out'), 'r', encoding='utf-8') as f:
        generic_sha256sum_line_separator = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/md5sum.json'), 'r', encoding='utf-8') as f:
        centos_7_7_md5sum_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/md5sum-raw.json'), 'r', encoding='utf-8') as f:
        centos_7_7_md5sum_raw_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/sha256sum.json'), 'r', encoding='utf-8') as f:
        centos_7_7_sha256sum_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/sha256sum-raw.json'), 'r', encoding='utf-8') as f:
        centos_7_7_sha256sum_raw_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/sha384sum.json'), 'r', encoding='utf-8') as f:
        centos_7_7_sha384sum_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/sha384sum-raw.json'), 'r', encoding='utf-8') as f:
        centos_7_7_sha384sum_raw_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/shasum-portable.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_04_shasum_portable_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/shasum-portable-raw.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_04_shasum_portable_raw_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-24.04/sha256sum-binary.json'), 'r', encoding='utf-8') as f:
        ubuntu_24_04_sha256sum_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-24.04/sha256sum-binary-raw.json'), 'r', encoding='utf-8') as f:
        ubuntu_24_04_sha256sum_raw_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-24.04/shasum-universal-bits.json'), 'r', encoding='utf-8') as f:
        ubuntu_24_04_shasum_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-24.04/shasum-universal-bits-raw.json'), 'r', encoding='utf-8') as f:
        ubuntu_24_04_shasum_raw_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/md5.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_md5_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/md5-raw.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_md5_raw_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/sha256sum-escaped-filenames.out'), 'r', encoding='utf-8') as f:
        generic_sha256sum_escaped_filenames = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/sha256sum-escaped-filenames.json'), 'r', encoding='utf-8') as f:
        generic_sha256sum_escaped_filenames_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/md5sum-tag-escaped-filenames.out'), 'r', encoding='utf-8') as f:
        generic_md5sum_tag_escaped_filenames = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/md5sum-tag-escaped-filenames.json'), 'r', encoding='utf-8') as f:
        generic_md5sum_tag_escaped_filenames_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/shasum.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_shasum_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/shasum-raw.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_shasum_raw_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/sha256sum-line-separator.json'), 'r', encoding='utf-8') as f:
        generic_sha256sum_line_separator_json = json.loads(f.read())


    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/hashsum-bsd-style.out'), 'r', encoding='utf-8') as f:
        generic_hashsum_bsd_style = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/hashsum-bsd-style.json'), 'r', encoding='utf-8') as f:
        generic_hashsum_bsd_style_json = json.loads(f.read())

    def test_hashsum_nodata(self):
        """
        Test 'hashsum' parser with no data
        """
        self.assertEqual(jc.parsers.hashsum.parse('', quiet=True), [])

    def test_md5sum_centos_7_7(self):
        """
        Test 'md5sum' on Centos 7.7
        """
        self.assertEqual(jc.parsers.hashsum.parse(self.centos_7_7_md5sum, quiet=True), self.centos_7_7_md5sum_json)

    def test_md5sum_centos_7_7_raw(self):
        """
        Test 'md5sum' on Centos 7.7, raw output
        """
        self.assertEqual(
            jc.parsers.hashsum.parse(self.centos_7_7_md5sum, quiet=True, raw=True),
            self.centos_7_7_md5sum_raw_json)

    def test_sha256sum_centos_7_7(self):
        """
        Test 'sha256sum' on Centos 7.7
        """
        self.assertEqual(jc.parsers.hashsum.parse(self.centos_7_7_sha256sum, quiet=True), self.centos_7_7_sha256sum_json)

    def test_sha256sum_centos_7_7_raw(self):
        """
        Test 'sha256sum' on Centos 7.7, raw output
        """
        self.assertEqual(
            jc.parsers.hashsum.parse(self.centos_7_7_sha256sum, quiet=True, raw=True),
            self.centos_7_7_sha256sum_raw_json)

    def test_sha384sum_centos_7_7(self):
        """
        Test 'sha384sum' on Centos 7.7
        """
        self.assertEqual(jc.parsers.hashsum.parse(self.centos_7_7_sha384sum, quiet=True), self.centos_7_7_sha384sum_json)

    def test_sha384sum_centos_7_7_raw(self):
        """
        Test 'sha384sum' on Centos 7.7, raw output
        """
        self.assertEqual(jc.parsers.hashsum.parse(
            self.centos_7_7_sha384sum, quiet=True, raw=True),
            self.centos_7_7_sha384sum_raw_json)

    def test_sha256sum_ubuntu_18_04_unsupported_mode(self):
        """
        Test 'sha256sum' on Ubuntu 18.04, portable mode (no friendly name)
        """
        self.assertEqual(jc.parsers.hashsum.parse(
            self.ubuntu_18_04_shasum_portable, quiet=True),
            self.ubuntu_18_04_shasum_portable_json)

    def test_sha256sum_ubuntu_18_04_unsupported_mode_raw(self):
        """
        Test 'sha256sum' on Ubuntu 18.04, portable mode (no friendly name), raw output
        """
        self.assertEqual(jc.parsers.hashsum.parse(
            self.ubuntu_18_04_shasum_portable, quiet=True, raw=True),
            self.ubuntu_18_04_shasum_portable_raw_json)

    def test_sha256sum_ubuntu_24_04_binary(self):
        """
        Test 'sha256sum' on Ubuntu 24.04, binary mode
        """
        self.assertEqual(jc.parsers.hashsum.parse(self.ubuntu_24_04_sha256sum_binary, quiet=True), self.ubuntu_24_04_sha256sum_json)

    def test_sha256sum_ubuntu_24_04_binary_raw(self):
        """
        Test 'sha256sum' on Ubuntu 24.04, binary mode, raw output
        """
        self.assertEqual(jc.parsers.hashsum.parse(
            self.ubuntu_24_04_sha256sum_binary, quiet=True, raw=True),
            self.ubuntu_24_04_sha256sum_raw_json)

    def test_shasum_ubuntu_24_04_universal_bits(self):
        """
        Test 'shasum' on Ubuntu 24.04, universal and bits modes
        """
        self.assertEqual(jc.parsers.hashsum.parse(self.ubuntu_24_04_shasum_universal_bits, quiet=True), self.ubuntu_24_04_shasum_json)

    def test_shasum_ubuntu_24_04_raw(self):
        """
        Test 'shasum' on Ubuntu 24.04, universal and bits modes, raw output
        """
        self.assertEqual(
            jc.parsers.hashsum.parse(self.ubuntu_24_04_shasum_universal_bits, quiet=True, raw=True),
            self.ubuntu_24_04_shasum_raw_json)

    def test_md5_osx_10_14_6(self):
        """
        Test 'md5' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.hashsum.parse(self.osx_10_14_6_md5, quiet=True), self.osx_10_14_6_md5_json)

    def test_md5_osx_10_14_6_raw(self):
        """
        Test 'md5' on OSX 10.14.6, raw output
        """
        self.assertEqual(
            jc.parsers.hashsum.parse(self.osx_10_14_6_md5, quiet=True, raw=True),
            self.osx_10_14_6_md5_raw_json)

    def test_shasum_osx_10_14_6(self):
        """
        Test 'shasum' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.hashsum.parse(self.osx_10_14_6_shasum, quiet=True), self.osx_10_14_6_shasum_json)

    def test_shasum_osx_10_14_6_raw(self):
        """
        Test 'shasum' on OSX 10.14.6, raw output
        """
        self.assertEqual(
            jc.parsers.hashsum.parse(self.osx_10_14_6_shasum, quiet=True, raw=True),
            self.osx_10_14_6_shasum_raw_json)

    def test_sha256sum_line_separator(self):
        """
        Test 'sha256sum' with a filename containing U+2028 (LINE SEPARATOR):
        the line must stay a single record
        """
        self.assertEqual(jc.parsers.hashsum.parse(self.generic_sha256sum_line_separator, quiet=True), self.generic_sha256sum_line_separator_json)

    def test_hashsum_bsd_style(self):
        """
        Test 'md5' and 'shasum' BSD style output with parentheses and equals signs in file names
        """
        self.assertEqual(jc.parsers.hashsum.parse(self.generic_hashsum_bsd_style, quiet=True), self.generic_hashsum_bsd_style_json)

    def test_sha256sum_escaped_filenames(self):
        """
        Test 'sha256sum' with backslash, newline and carriage return in file names
        """
        self.assertEqual(jc.parsers.hashsum.parse(self.generic_sha256sum_escaped_filenames, quiet=True), self.generic_sha256sum_escaped_filenames_json)

    def test_md5sum_tag_escaped_filenames(self):
        """
        Test 'md5sum --tag' with backslash, newline and carriage return in file names
        """
        self.assertEqual(jc.parsers.hashsum.parse(self.generic_md5sum_tag_escaped_filenames, quiet=True), self.generic_md5sum_tag_escaped_filenames_json)

    def test_md5sum_binary_escaped_filename_raw(self):
        """
        Test 'md5sum -b' with an escaped file name, raw output
        """
        data = ('\\d41d8cd98f00b204e9800998ecf8427e *back\\\\slash\\n\n'
                'd41d8cd98f00b204e9800998ecf8427e *plain\\n\n')
        expected = [
            {'filename': 'back\\slash\n', 'mode': '*', 'hash': 'd41d8cd98f00b204e9800998ecf8427e'},
            {'filename': 'plain\\n', 'mode': '*', 'hash': 'd41d8cd98f00b204e9800998ecf8427e'}
        ]
        self.assertEqual(jc.parsers.hashsum.parse(data, raw=True, quiet=True), expected)

    def test_hashsum_escaped_invalid_line(self):
        """
        Test 'hashsum' still rejects an invalid line that starts with a backslash
        """
        with self.assertRaisesRegex(ValueError, r'Invalid line format: "\\not a hash"'):
            jc.parsers.hashsum.parse('\\not a hash\n', quiet=True)


if __name__ == '__main__':
    unittest.main()
