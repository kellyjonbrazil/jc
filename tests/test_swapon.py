import os
import unittest
import json
from typing import Dict
from jc.parsers.swapon import parse

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class Swapon(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            "swapon_all": ("fixtures/generic/swapon-all-v1.out", "fixtures/generic/swapon-all-v1.json"),
            "swapon_all_v2": ("fixtures/generic/swapon-all-v2.out", "fixtures/generic/swapon-all-v2.json"),
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), "r", encoding="utf-8") as a, open(
                os.path.join(THIS_DIR, filepaths[1]), "r", encoding="utf-8"
            ) as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())

    def test_swapon_nodata(self):
        """
        Test 'swapon' with no data
        """
        self.assertEqual(parse('', quiet=True), [])

    def test_swapon_all(self):
        """
        Test 'swapon --output-all'
        """
        self.assertEqual(parse(self.f_in["swapon_all"], quiet=True), self.f_json["swapon_all"])

    def test_swapon_all_v2(self):
        """
        Test 'swapon --output-all'
        """
        self.assertEqual(parse(self.f_in["swapon_all_v2"], quiet=True), self.f_json["swapon_all_v2"])


if __name__ == "__main__":
    unittest.main()
