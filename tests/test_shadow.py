import os
import json
import unittest
import jc.parsers.shadow

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/shadow.out'), 'r', encoding='utf-8') as f:
            self.centos_7_7_shadow = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/shadow.out'), 'r', encoding='utf-8') as f:
            self.ubuntu_18_4_shadow = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/shadow.json'), 'r', encoding='utf-8') as f:
            self.centos_7_7_shadow_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/shadow.json'), 'r', encoding='utf-8') as f:
            self.ubuntu_18_4_shadow_json = json.loads(f.read())

    def test_shadow_centos_7_7(self):
        """
        Test 'cat /etc/shadow' on Centos 7.7
        """
        self.assertEqual(jc.parsers.shadow.parse(self.centos_7_7_shadow, quiet=True), self.centos_7_7_shadow_json)

    def test_shadow_ubuntu_18_4(self):
        """
        Test 'cat /etc/shadow' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.shadow.parse(self.ubuntu_18_4_shadow, quiet=True), self.ubuntu_18_4_shadow_json)


if __name__ == '__main__':
    unittest.main()
