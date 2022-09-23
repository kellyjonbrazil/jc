import os
import unittest
import json
import jc.parsers.cef

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/cef.out'), 'r', encoding='utf-8') as f:
        cef = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/cef.json'), 'r', encoding='utf-8') as f:
        cef_json = json.loads(f.read())


    def test_cef_nodata(self):
        """
        Test 'cef' with no data
        """
        self.assertEqual(jc.parsers.cef.parse('', quiet=True), [])

    def test_cef_sample(self):
        """
        Test with sample cef log
        """
        self.assertEqual(jc.parsers.cef.parse(self.cef, quiet=True), self.cef_json)


if __name__ == '__main__':
    unittest.main()
