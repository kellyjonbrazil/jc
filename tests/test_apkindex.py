import os
import unittest
import json
from typing import Dict
from jc.parsers.apkindex import parse

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class Apkindex(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}
    f_raw: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            "normal": ("fixtures/generic/apkindex", "fixtures/generic/apkindex.json", "fixtures/generic/apkindex.raw.json"),
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), "r", encoding="utf-8") as a, open(
                os.path.join(THIS_DIR, filepaths[1]), "r", encoding="utf-8"
            ) as b, open(
                os.path.join(THIS_DIR, filepaths[1]), "r", encoding="utf-8"
            ) as c:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())
                cls.f_raw[file] = json.loads(c.read())

    def test_apkindex(self):
        """
        Test 'apkindex'
        """
        f = "normal"
        self.assertEqual(parse(self.f_in[f], quiet=True), self.f_json[f])

if __name__ == "__main__":
    unittest.main()
