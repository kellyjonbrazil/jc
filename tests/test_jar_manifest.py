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

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/rhel-8/MANIFEST.MF.json'), 'r', encoding='utf-8') as f:
        rhel_8_manifest_mf_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/rhel-8/MANIFEST.MF.MULTI.json'), 'r', encoding='utf-8') as f:
        rhel_8_manifest_mf_multi_json = json.loads(f.read())


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


if __name__ == '__main__':
    unittest.main()
