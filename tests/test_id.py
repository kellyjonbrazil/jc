import os
import json
import unittest
import jc.parsers.id

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/id.out'), 'r') as f:
            self.centos_7_7_id = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/id.out'), 'r') as f:
            self.osx_10_14_6_id = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/id.json'), 'r') as f:
            self.centos_7_7_id_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/id.json'), 'r') as f:
            self.osx_10_14_6_id_json = json.loads(f.read())

    def test_id_centos_7_7(self):
        """
        Test 'id' on Centos 7.7
        """
        self.assertEqual(jc.parsers.id.parse(self.centos_7_7_id, quiet=True), self.centos_7_7_id_json)

    def test_id_osx_10_14_6(self):
        """
        Test 'id' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.id.parse(self.osx_10_14_6_id, quiet=True), self.osx_10_14_6_id_json)


if __name__ == '__main__':
    unittest.main()
