import os
import unittest
import jc.parsers.ls

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ls.out'), 'r') as f:
            self.centos_7_7_ls = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ls.out'), 'r') as f:
            self.ubuntu_18_4_ls = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ls-al.out'), 'r') as f:
            self.centos_7_7_ls_al = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ls-al.out'), 'r') as f:
            self.ubuntu_18_4_ls_al = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ls-alh.out'), 'r') as f:
            self.centos_7_7_ls_alh = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ls-alh.out'), 'r') as f:
            self.ubuntu_18_4_ls_alh = f.read()

    def test_ls_centos_7_7(self):
        """
        Test plain 'ls /' on Centos 7.7
        """
        self.assertEqual(jc.parsers.ls.parse(self.centos_7_7_ls)[1]['filename'], 'boot')

    def test_ls_ubuntu_18_4(self):
        """
        Test plain 'ls /' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.ls.parse(self.ubuntu_18_4_ls)[1]['filename'], 'boot')

    def test_ls_al_centos_7_7(self):
        """
        Test 'ls -al /' on Centos 7.7
        """
        self.assertEqual(jc.parsers.ls.parse(self.centos_7_7_ls_al)[2], {'filename': 'bin',
                                                                         'link_to': 'usr/bin',
                                                                         'flags': 'lrwxrwxrwx.',
                                                                         'links': '1',
                                                                         'owner': 'root',
                                                                         'group': 'root',
                                                                         'size': '7',
                                                                         'date': 'Aug 15 10:53'})

    def test_ls_al_ubuntu_18_4(self):
        """
        Test 'ls -al /' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.ls.parse(self.ubuntu_18_4_ls_al)[4], {'filename': 'cdrom',
                                                                          'flags': 'drwxr-xr-x',
                                                                          'links': '2',
                                                                          'owner': 'root',
                                                                          'group': 'root',
                                                                          'size': '4096',
                                                                          'date': 'Aug 12 17:21'})

    def test_ls_alh_centos_7_7(self):
        """
        Test 'ls -alh /' on Centos 7.7
        """
        self.assertEqual(jc.parsers.ls.parse(self.centos_7_7_ls_alh)[5], {'filename': 'etc',
                                                                          'flags': 'drwxr-xr-x.',
                                                                          'links': '78',
                                                                          'owner': 'root',
                                                                          'group': 'root',
                                                                          'size': '8.0K',
                                                                          'date': 'Oct 25 18:47'})

    def test_ls_alh_ubuntu_18_4(self):
        """
        Test 'ls -alh /' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.ls.parse(self.ubuntu_18_4_ls_alh)[7], {'filename': 'home',
                                                                           'flags': 'drwxr-xr-x',
                                                                           'links': '3',
                                                                           'owner': 'root',
                                                                           'group': 'root',
                                                                           'size': '4.0K',
                                                                           'date': 'Aug 12 17:24'})


if __name__ == '__main__':
    unittest.main()
