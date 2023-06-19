import os
import unittest
import json
import jc.parsers.srt

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/srt-attack_of_the_clones.srt'), 'r', encoding='utf-8') as f:
        generic_attack_of_the_clones = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/srt-complex.srt'), 'r', encoding='utf-8') as f:
        generic_complex = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/srt-attack_of_the_clones_raw.json'), 'r', encoding='utf-8') as f:
        generic_attack_of_the_clones_raw_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/srt-attack_of_the_clones.json'), 'r', encoding='utf-8') as f:
        generic_attack_of_the_clones_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/srt-complex.json'), 'r', encoding='utf-8') as f:
        generic_complex_json = json.loads(f.read())

    def test_srt_nodata(self):
        """
        Test srt parser with no data
        """
        self.assertEqual(jc.parsers.srt.parse('', quiet=True), [])

    def test_srt_nodata_r(self):
        """
        Test srt parser with no data and raw output
        """
        self.assertEqual(jc.parsers.srt.parse('', raw=True, quiet=True), [])

    def test_srt_attack_of_the_clones_raw(self):
        """
        Test the attack of the clones srt file without post processing
        """
        self.assertEqual(jc.parsers.srt.parse(self.generic_attack_of_the_clones, raw=True, quiet=True), self.generic_attack_of_the_clones_raw_json)

    def test_srt_attack_of_the_clones(self):
        """
        Test the attack of the clones srt file
        """
        self.assertEqual(jc.parsers.srt.parse(self.generic_attack_of_the_clones, quiet=True), self.generic_attack_of_the_clones_json)

    def test_srt_complex(self):
        """
        Test a complex srt file
        """
        self.assertEqual(jc.parsers.srt.parse(self.generic_complex, quiet=True), self.generic_complex_json)

if __name__ == '__main__':
    unittest.main()
