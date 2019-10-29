import os
import unittest
import jc.parsers.ps

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ps-ef.out'), 'r') as f:
            self.centos_7_7_ps_ef = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ps-ef.out'), 'r') as f:
            self.ubuntu_18_4_ps_ef = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ps-axu.out'), 'r') as f:
            self.centos_7_7_ps_axu = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ps-axu.out'), 'r') as f:
            self.ubuntu_18_4_ps_axu = f.read()

    def test_ps_ef_centos_7_7(self):
        """
        Test 'ps -ef' on Centos 7.7
        """
        self.assertEqual(jc.parsers.ps.parse(self.centos_7_7_ps_ef)[25], {'uid': 'root',
                                                                          'pid': '33',
                                                                          'ppid': '2',
                                                                          'c': '0',
                                                                          'stime': 'Oct25',
                                                                          'tty': '?',
                                                                          'time': '00:00:00',
                                                                          'cmd': '[crypto]'})

    def test_ps_ef_ubuntu_18_4(self):
        """
        Test 'ps -ef' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.ps.parse(self.ubuntu_18_4_ps_ef)[30], {'uid': 'root',
                                                                           'pid': '36',
                                                                           'ppid': '2',
                                                                           'c': '0',
                                                                           'stime': 'Oct26',
                                                                           'tty': '?',
                                                                           'time': '00:00:00',
                                                                           'cmd': '[ecryptfs-kthrea]'})

    def test_ps_axu_centos_7_7(self):
        """
        Test 'ps axu' on Centos 7.7
        """
        self.assertEqual(jc.parsers.ps.parse(self.centos_7_7_ps_axu)[13], {'user': 'root',
                                                                           'pid': '16',
                                                                           'cpu_percent': '0.0',
                                                                           'mem_percent': '0.0',
                                                                           'vsz': '0',
                                                                           'rss': '0',
                                                                           'tty': '?',
                                                                           'stat': 'S<',
                                                                           'start': 'Oct25',
                                                                           'time': '0:00',
                                                                           'command': '[writeback]'})

    def test_ps_axu_ubuntu_18_4(self):
        """
        Test 'ps axu' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.ps.parse(self.ubuntu_18_4_ps_axu)[40], {'user': 'root',
                                                                            'pid': '170',
                                                                            'cpu_percent': '0.0',
                                                                            'mem_percent': '0.0',
                                                                            'vsz': '0',
                                                                            'rss': '0',
                                                                            'tty': '?',
                                                                            'stat': 'I<',
                                                                            'start': 'Oct26',
                                                                            'time': '0:00',
                                                                            'command': '[mpt_poll_0]'})


if __name__ == '__main__':
    unittest.main()
