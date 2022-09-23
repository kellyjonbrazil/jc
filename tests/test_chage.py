import os
import unittest
import json
import jc.parsers.chage

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/chage.out'), 'r', encoding='utf-8') as f:
        centos_7_7_chage = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/chage.json'), 'r', encoding='utf-8') as f:
        centos_7_7_chage_json = json.loads(f.read())


    def test_chage_nodata(self):
        """
        Test 'chage' with no data
        """
        self.assertEqual(jc.parsers.chage.parse('', quiet=True), {})

    def test_chage_centos_7_7(self):
        """
        Test 'chage' on Centos 7.7
        """
        self.assertEqual(jc.parsers.chage.parse(self.centos_7_7_chage, quiet=True), self.centos_7_7_chage_json)


if __name__ == '__main__':
    unittest.main()
