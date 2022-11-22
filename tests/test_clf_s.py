import os
import json
import unittest
from typing import Dict
from jc.parsers.clf_s import parse

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

# To create streaming output use:
# $ cat clf.out | jc --clf-s | jello -c > clf-streaming.json


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'clf_s': (
                'fixtures/generic/common-log-format.log',
                'fixtures/generic/common-log-format-streaming.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_clf_s_nodata(self):
        """
        Test 'clf-s' with no data
        """
        self.assertEqual(list(parse([], quiet=True)), [])


    def test_clf_s_centos_7_7(self):
        """
        Test 'clf-s' with various logs
        """
        self.assertEqual(
            list(parse(self.f_in['clf_s'].splitlines(), quiet=True)),
            self.f_json['clf_s']
        )


if __name__ == '__main__':
    unittest.main()
