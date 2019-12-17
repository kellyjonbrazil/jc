import os
import json
import unittest
import jc.parsers.pip_show

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/pip-show.out'), 'r') as f:
            self.centos_7_7_pip_show = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/pip-show.out'), 'r') as f:
            self.ubuntu_18_4_pip_show = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/pip-show.out'), 'r') as f:
            self.osx_10_11_6_pip_show = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/pip-show.out'), 'r') as f:
            self.osx_10_14_6_pip_show = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/pip-show.json'), 'r') as f:
            self.centos_7_7_pip_show_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/pip-show.json'), 'r') as f:
            self.ubuntu_18_4_pip_show_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/pip-show.json'), 'r') as f:
            self.osx_10_11_6_pip_show_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/pip-show.json'), 'r') as f:
            self.osx_10_14_6_pip_show_json = json.loads(f.read())

    def test_pip_show_centos_7_7(self):
        """
        Test 'pip show' on Centos 7.7
        """
        self.assertEqual(jc.parsers.pip_show.parse(self.centos_7_7_pip_show, quiet=True), self.centos_7_7_pip_show_json)

    def test_pip_show_ubuntu_18_4(self):
        """
        Test 'pip show' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.pip_show.parse(self.ubuntu_18_4_pip_show, quiet=True), self.ubuntu_18_4_pip_show_json)

    def test_pip_show_osx_10_11_6(self):
        """
        Test 'pip show' on OSX 10.11.6
        """
        self.assertEqual(jc.parsers.pip_show.parse(self.osx_10_11_6_pip_show, quiet=True), self.osx_10_11_6_pip_show_json)

    def test_pip_show_osx_10_14_6(self):
        """
        Test 'pip show' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.pip_show.parse(self.osx_10_14_6_pip_show, quiet=True), self.osx_10_14_6_pip_show_json)


if __name__ == '__main__':
    unittest.main()
