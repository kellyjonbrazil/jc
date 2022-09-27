import os
import unittest
import json
import jc.parsers.hash

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/hash.out'), 'r', encoding='utf-8') as f:
        centos_7_7_hash = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/hash.json'), 'r', encoding='utf-8') as f:
        centos_7_7_hash_json = json.loads(f.read())


    def test_hash_nodata(self):
        """
        Test 'hash' parser with no data
        """
        self.assertEqual(jc.parsers.hash.parse('', quiet=True), [])

    def test_hash_centos_7_7(self):
        """
        Test 'hash' on Centos 7.7
        """
        self.assertEqual(jc.parsers.hash.parse(self.centos_7_7_hash, quiet=True), self.centos_7_7_hash_json)


if __name__ == '__main__':
    unittest.main()
