import os
import unittest
import json
import jc.parsers.ini

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ini-test.ini'), 'r') as f:
            self.generic_ini_test = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ini-iptelserver.ini'), 'r') as f:
            self.generic_ini_iptelserver = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ini-test.json'), 'r') as f:
            self.generic_ini_test_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ini-iptelserver.json'), 'r') as f:
            self.generic_ini_iptelserver_json = json.loads(f.read())

    def test_ini_test(self):
        """
        Test the test ini file
        """
        self.assertEqual(jc.parsers.ini.parse(self.generic_ini_test, quiet=True), self.generic_ini_test_json)

    def test_ini_iptelserver(self):
        """
        Test the iptelserver ini file
        """
        self.assertEqual(jc.parsers.ini.parse(self.generic_ini_iptelserver, quiet=True), self.generic_ini_iptelserver_json)


if __name__ == '__main__':
    unittest.main()
