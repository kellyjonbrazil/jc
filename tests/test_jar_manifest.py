import os
import unittest
import json
import jc.parsers.jar_manifest

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/rhel-8/MANIFEST.MF.out'), 'r', encoding='utf-8') as f:
        rhel_8_manifest_mf = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/rhel-8/MANIFEST.MF.MULTI.out'), 'r', encoding='utf-8') as f:
        rhel_8_manifest_mf_multi = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/jar-manifest-continuations.out'), 'r', encoding='utf-8') as f:
        generic_continuations = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/rhel-8/MANIFEST.MF.json'), 'r', encoding='utf-8') as f:
        rhel_8_manifest_mf_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/rhel-8/MANIFEST.MF.MULTI.json'), 'r', encoding='utf-8') as f:
        rhel_8_manifest_mf_multi_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/jar-manifest-continuations.json'), 'r', encoding='utf-8') as f:
        generic_continuations_json = json.loads(f.read())


    def test_jar_manifest_nodata(self):
        """
        Test 'jar_manifest' parser with no data
        """
        self.assertEqual(jc.parsers.jar_manifest.parse('', quiet=True), [])

    def test_jar_manifest_rhel_8(self):
        """
        Test 'cat MANIFEST.MF | jc --jar_manifest'
        """
        self.assertEqual(jc.parsers.jar_manifest.parse(self.rhel_8_manifest_mf, quiet=True), self.rhel_8_manifest_mf_json)

    def test_jar_manifest_multi_rhel_8(self):
        """
        Test 'unzip -c apache-log4j-2.16.0-bin/log4j-core-2.16.0.jar META-INF/MANIFEST.MF | jc --jar_manifest'
        """
        self.assertEqual(jc.parsers.jar_manifest.parse(self.rhel_8_manifest_mf_multi, quiet=True), self.rhel_8_manifest_mf_multi_json)


    def test_jar_manifest_line_separator(self):
        """
        Test 'jar_manifest' with a line-break character other than LF inside a field
        """
        data = 'Manifest-Version: 1.0\r\nMain-Class: com.example.app.Launcher\r\nImplementation-Title: Reporting Service\u2028Main-Class: org.example.app.Main\r\nImplementation-Version: 1.4.2\r\n\r\n'
        result = jc.parsers.jar_manifest.parse(data, quiet=True)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['Main_Class'], 'com.example.app.Launcher')
        self.assertEqual(result[0]['Implementation_Title'], 'Reporting Service\u2028Main-Class: org.example.app.Main')

    def test_jar_manifest_cr_line_endings(self):
        """
        Test 'jar_manifest' with CR-only line endings
        """
        data = 'Manifest-Version: 1.0\rMain-Class: com.example.Main\rCreated-By: 1.8\r\rName: a/b.class\rSHA-256-Digest: abc\r'
        expected = [{'Manifest_Version': '1.0', 'Main_Class': 'com.example.Main', 'Created_By': '1.8'}, {'Name': 'a/b.class', 'SHA_256_Digest': 'abc'}]
        self.assertEqual(jc.parsers.jar_manifest.parse(data, quiet=True), expected)

    def test_jar_manifest_continuations_fixture(self):
        """
        Test 'jar_manifest' with continuation lines of one, two and three lines and an unzip header
        """
        self.assertEqual(jc.parsers.jar_manifest.parse(self.generic_continuations, quiet=True), self.generic_continuations_json)

    def test_jar_manifest_single_continuation(self):
        """
        Test 'jar_manifest' with a single continuation line followed by another folded attribute
        """
        data = 'A: x\n y\nB: p\n q\n r\nC: z\n'
        self.assertEqual(jc.parsers.jar_manifest.parse(data, quiet=True), [{'A': 'xy', 'B': 'pqr', 'C': 'z'}])

    def test_jar_manifest_last_attribute_two_continuations(self):
        """
        Test 'jar_manifest' with a value folded over three lines at the end of a section
        """
        data = 'Manifest-Version: 1.0\nPremain-Class: com.example.ag\n ent.Premain\n Agent\n\nName: a\nB: c\n d\n e\n'
        expected = [{'Manifest_Version': '1.0', 'Premain_Class': 'com.example.agent.PremainAgent'}, {'Name': 'a', 'B': 'cde'}]
        self.assertEqual(jc.parsers.jar_manifest.parse(data, quiet=True), expected)

    def test_jar_manifest_continuation_keeps_inner_spaces(self):
        """
        Test 'jar_manifest' removes only the one leading space of a continuation line
        """
        data = 'Bundle-Description: Hello \n  wide  world\n'
        self.assertEqual(jc.parsers.jar_manifest.parse(data, quiet=True), [{'Bundle_Description': 'Hello  wide  world'}])

    def test_jar_manifest_continuation_looks_like_unzip_line(self):
        """
        Test 'jar_manifest' with continuation text that looks like the unzip inflating line
        """
        data = 'Manifest-Version: 1.0\nMain-Class: com.example.Main\nBundle-Description: abc\n  inflating: META-INF/MANIFEST.MF\n def\n\n'
        expected = [{'Manifest_Version': '1.0', 'Main_Class': 'com.example.Main', 'Bundle_Description': 'abc inflating: META-INF/MANIFEST.MFdef'}]
        self.assertEqual(jc.parsers.jar_manifest.parse(data, quiet=True), expected)

    def test_jar_manifest_unzip_extracting_line(self):
        """
        Test 'jar_manifest' with the unzip header of a manifest that is stored without compression
        """
        data = 'Archive:  a.jar\n extracting: META-INF/MANIFEST.MF\nManifest-Version: 1.0\n'
        self.assertEqual(jc.parsers.jar_manifest.parse(data, quiet=True), [{'Archive': 'a.jar', 'Manifest_Version': '1.0'}])

    def test_jar_manifest_many_continuations(self):
        """
        Test 'jar_manifest' with a value folded over many short lines
        """
        data = 'Manifest-Version: 1.0\nClass-Path: a\n' + ' ab\n' * 20000 + 'Created-By: 1.8\n'
        result = jc.parsers.jar_manifest.parse(data, quiet=True)
        self.assertEqual(result, [{'Manifest_Version': '1.0', 'Class_Path': 'a' + 'ab' * 20000, 'Created_By': '1.8'}])

    def test_jar_manifest_unzip_archive_attribute(self):
        """
        Test 'jar_manifest' with unzip output where a manifest has an Archive attribute
        """
        data = (
            'Archive:  reporting-core-1.4.2.jar\n'
            '  inflating: META-INF/MANIFEST.MF    \n'
            'Manifest-Version: 1.0\n'
            'Main-Class: org.example.app.Main\n'
            '\n'
            '\n'
            'Archive:  upload-7f3a.jar\n'
            ' extracting: META-INF/MANIFEST.MF    \n'
            'Manifest-Version: 1.0\n'
            'Main-Class: com.example.Other\n'
            'Archive: reporting-core-1.4.2.jar\n'
            '\n'
        )
        expected = [
            {'Archive': 'reporting-core-1.4.2.jar', 'Manifest_Version': '1.0', 'Main_Class': 'org.example.app.Main'},
            {'Archive': 'upload-7f3a.jar', 'Manifest_Version': '1.0', 'Main_Class': 'com.example.Other'}
        ]
        self.assertEqual(jc.parsers.jar_manifest.parse(data, quiet=True), expected)

    def test_jar_manifest_archive_attribute_without_unzip(self):
        """
        Test 'jar_manifest' with an Archive attribute in a manifest that is not unzip output
        """
        data = 'Manifest-Version: 1.0\nArchive: a.jar\n'
        self.assertEqual(jc.parsers.jar_manifest.parse(data, quiet=True), [{'Manifest_Version': '1.0', 'Archive': 'a.jar'}])

    def test_jar_manifest_keys_differ_in_dash_and_underscore(self):
        """
        Test 'jar_manifest' with attribute names that only differ in "-" and "_"
        """
        data = 'Manifest-Version: 1.0\nMain-Class: com.example.Main\nMain_Class: com.example.Other\nX-Y: 1\nX-Y: 2\n'
        expected = [{'Manifest_Version': '1.0', 'Main_Class': 'com.example.Main', 'X_Y': '2'}]
        self.assertEqual(jc.parsers.jar_manifest.parse(data, quiet=True), expected)

    def test_jar_manifest_value_ends_like_unzip_summary(self):
        """
        Test 'jar_manifest' with a last attribute that ends like the unzip summary line
        """
        data = 'Manifest-Version: 1.0\nMain-Class: org.example.app.Main\nClass-Path: lib/plugin.jar archives were successfully processed.'
        expected = [{'Manifest_Version': '1.0', 'Main_Class': 'org.example.app.Main', 'Class_Path': 'lib/plugin.jar archives were successfully processed.'}]
        self.assertEqual(jc.parsers.jar_manifest.parse(data, quiet=True), expected)

    def test_jar_manifest_unzip_summary_line(self):
        """
        Test 'jar_manifest' with the unzip summary line after several archives
        """
        data = self.rhel_8_manifest_mf_multi + '3 archives were successfully processed.\n'
        self.assertEqual(jc.parsers.jar_manifest.parse(data, quiet=True), self.rhel_8_manifest_mf_multi_json)


if __name__ == '__main__':
    unittest.main()
