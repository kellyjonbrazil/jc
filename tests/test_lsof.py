import os
import unittest
import jc.parsers.lsof

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/lsof.out'), 'r') as f:
            self.centos_7_7_lsof = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/lsof.out'), 'r') as f:
            self.ubuntu_18_4_lsof = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/lsof-sudo.out'), 'r') as f:
            self.centos_7_7_lsof_sudo = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/lsof-sudo.out'), 'r') as f:
            self.ubuntu_18_4_lsof_sudo = f.read()

    def test_lsof_centos_7_7(self):
        """
        Test 'lsof' on Centos 7.7
        """
        self.assertEqual(jc.parsers.lsof.parse(self.centos_7_7_lsof)[155], {'command': 'scsi_eh_0',
                                                                            'pid': '291',
                                                                            'tid': None,
                                                                            'user': 'root',
                                                                            'fd': 'NOFD',
                                                                            'type': None,
                                                                            'device': None,
                                                                            'size_off': None,
                                                                            'node': None,
                                                                            'name': '/proc/291/fd (opendir: Permission denied)'})

    def test_lsof_ubuntu_18_4(self):
        """
        Test 'lsof' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.lsof.parse(self.ubuntu_18_4_lsof)[341], {'command': 'scsi_tmf_',
                                                                             'pid': '246',
                                                                             'tid': None,
                                                                             'user': 'root',
                                                                             'fd': 'rtd',
                                                                             'type': 'unknown',
                                                                             'device': None,
                                                                             'size_off': None,
                                                                             'node': None,
                                                                             'name': '/proc/246/root (readlink: Permission denied)'})

    def test_lsof_sudo_centos_7_7(self):
        """
        Test 'sudo lsof' on Centos 7.7
        """
        self.assertEqual(jc.parsers.lsof.parse(self.centos_7_7_lsof_sudo)[500], {'command': 'dbus-daem',
                                                                                 'pid': '778',
                                                                                 'tid': None,
                                                                                 'user': 'dbus',
                                                                                 'fd': '6u',
                                                                                 'type': 'netlink',
                                                                                 'device': None,
                                                                                 'size_off': '0t0',
                                                                                 'node': '17854',
                                                                                 'name': 'SELINUX'})

    def test_lsof_sudo_ubuntu_18_4(self):
        """
        Test 'sudo lsof' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.lsof.parse(self.ubuntu_18_4_lsof_sudo)[782], {'command': 'vmtoolsd',
                                                                                  'pid': '680',
                                                                                  'tid': None,
                                                                                  'user': 'root',
                                                                                  'fd': '4u',
                                                                                  'type': 'a_inode',
                                                                                  'device': '0,13',
                                                                                  'size_off': '0',
                                                                                  'node': '10717',
                                                                                  'name': '[eventfd]'})


if __name__ == '__main__':
    unittest.main()
