import os
import unittest
import json
import jc.parsers.find

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/find.out'), 'r', encoding='utf-8') as f:
        centos_7_7_find = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/find.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_find = f.read()

    #output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/find.json'), 'r', encoding='utf-8') as f:
        centos_7_7_find_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/find.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_find_json = json.loads(f.read())

    def test_find_nodata(self):
        """
        Test 'find' with no data
        """
        self.assertEqual(jc.parsers.find.parse('', quiet=True), [])

    def test_find_centos_7_7(self):
        """
        Test 'find' on Centos 7.7
        """
        self.assertEqual(jc.parsers.find.parse(self.centos_7_7_find, quiet=True), self.centos_7_7_find_json)

    def test_find_ubuntu_18_4(self):
        """
        Test 'find' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.find.parse(self.ubuntu_18_4_find, quiet=True), self.ubuntu_18_4_find_json)

if __name__ == '__main__':
    unittest.main()