import os
import json
import unittest
import jc.parsers.stat

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/stat.out'), 'r') as f:
            self.centos_7_7_stat = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/stat.out'), 'r') as f:
            self.ubuntu_18_4_stat = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/stat.json'), 'r') as f:
            self.centos_7_7_stat_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/stat.json'), 'r') as f:
            self.ubuntu_18_4_stat_json = json.loads(f.read())

    def test_stat_centos_7_7(self):
        """
        Test 'stat /bin/*' on Centos 7.7
        """
        self.assertEqual(jc.parsers.stat.parse(self.centos_7_7_stat, quiet=True), self.centos_7_7_stat_json)

    def test_stat_ubuntu_18_4(self):
        """
        Test 'stat /bin/*' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.stat.parse(self.ubuntu_18_4_stat, quiet=True), self.ubuntu_18_4_stat_json)


if __name__ == '__main__':
    unittest.main()
