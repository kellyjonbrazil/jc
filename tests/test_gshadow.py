import os
import json
import unittest
import jc.parsers.gshadow

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/gshadow.out'), 'r') as f:
            self.centos_7_7_gshadow = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/gshadow.out'), 'r') as f:
            self.ubuntu_18_4_gshadow = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/gshadow.json'), 'r') as f:
            self.centos_7_7_gshadow_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/gshadow.json'), 'r') as f:
            self.ubuntu_18_4_gshadow_json = json.loads(f.read())

    def test_gshadow_centos_7_7(self):
        """
        Test 'cat /etc/gshadow' on Centos 7.7
        """
        self.assertEqual(jc.parsers.gshadow.parse(self.centos_7_7_gshadow, quiet=True), self.centos_7_7_gshadow_json)

    def test_gshadow_ubuntu_18_4(self):
        """
        Test 'cat /etc/gshadow' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.gshadow.parse(self.ubuntu_18_4_gshadow, quiet=True), self.ubuntu_18_4_gshadow_json)


if __name__ == '__main__':
    unittest.main()
