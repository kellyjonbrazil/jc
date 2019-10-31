import os
import unittest
import jc.parsers.mount

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/mount.out'), 'r') as f:
            self.centos_7_7_mount = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/mount.out'), 'r') as f:
            self.ubuntu_18_4_mount = f.read()

    def test_mount_centos_7_7(self):
        """
        Test 'mount' on Centos 7.7
        """
        self.assertEqual(jc.parsers.mount.parse(self.centos_7_7_mount)[5], {'filesystem': 'devpts',
                                                                            'mount_point': '/dev/pts',
                                                                            'type': 'devpts',
                                                                            'access': ['rw',
                                                                                       'nosuid',
                                                                                       'noexec',
                                                                                       'relatime',
                                                                                       'seclabel',
                                                                                       'gid=5',
                                                                                       'mode=620',
                                                                                       'ptmxmode=000']})

    def test_mount_ubuntu_18_4(self):
        """
        Test 'mount' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.mount.parse(self.ubuntu_18_4_mount)[9], {'filesystem': 'tmpfs',
                                                                             'mount_point': '/sys/fs/cgroup',
                                                                             'type': 'tmpfs',
                                                                             'access': ['ro',
                                                                                        'nosuid',
                                                                                        'nodev',
                                                                                        'noexec',
                                                                                        'mode=755']})


if __name__ == '__main__':
    unittest.main()
