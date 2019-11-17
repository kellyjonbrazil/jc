import os
import json
import unittest
import jc.parsers.systemctl_lj

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        # with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/systemctl-lj.out'), 'r') as f:
        #     self.centos_7_7_systemctl_lj = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/systemctl-lj.out'), 'r') as f:
            self.ubuntu_18_4_systemctl_lj = f.read()

        # output
        # with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/systemctl-lj.json'), 'r') as f:
        #     self.centos_7_7_systemctl_lj_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/systemctl-lj.json'), 'r') as f:
            self.ubuntu_18_4_systemctl_lj_json = json.loads(f.read())

    # def test_systemctl_lj_centos_7_7(self):
    #     """
    #     Test 'systemctl -a list-jobs' on Centos 7.7
    #     """
    #     self.assertEqual(jc.parsers.systemctl_lj.parse(self.centos_7_7_systemctl_lj, quiet=True), self.centos_7_7_systemctl_lj_json)

    def test_systemctl_lj_ubuntu_18_4(self):
        """
        Test 'systemctl -a list-jobs' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.systemctl_lj.parse(self.ubuntu_18_4_systemctl_lj, quiet=True), self.ubuntu_18_4_systemctl_lj_json)


if __name__ == '__main__':
    unittest.main()
