import os
import json
import unittest
import jc.parsers.history

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/history.out'), 'r') as f:
            self.centos_7_7_history = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/history.out'), 'r') as f:
            self.ubuntu_18_4_history = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/history.json'), 'r') as f:
            self.centos_7_7_history_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/history.json'), 'r') as f:
            self.ubuntu_18_4_history_json = json.loads(f.read())

    def test_history_centos_7_7(self):
        """
        Test 'history' on Centos 7.7
        """
        self.assertEqual(jc.parsers.history.parse(self.centos_7_7_history, quiet=True), self.centos_7_7_history_json)

    def test_history_ubuntu_18_4(self):
        """
        Test 'history' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.history.parse(self.ubuntu_18_4_history, quiet=True), self.ubuntu_18_4_history_json)


if __name__ == '__main__':
    unittest.main()
