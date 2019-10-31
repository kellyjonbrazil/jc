import os
import unittest
import jc.parsers.w

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/w.out'), 'r') as f:
            self.centos_7_7_w = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/w.out'), 'r') as f:
            self.ubuntu_18_4_w = f.read()

    def test_w_centos_7_7(self):
        """
        Test 'w' on Centos 7.7
        """
        self.assertEqual(jc.parsers.w.parse(self.centos_7_7_w)[1], {'user': 'kbrazil',
                                                                    'tty': 'pts/0',
                                                                    'from': '192.168.71.1',
                                                                    'login_at': '09:53',
                                                                    'idle': '8.00s',
                                                                    'jcpu': '0.10s',
                                                                    'pcpu': '0.00s',
                                                                    'what': 'w'})

    def test_w_ubuntu_18_4(self):
        """
        Test 'w' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.w.parse(self.ubuntu_18_4_w)[1], {'user': 'kbrazil',
                                                                     'tty': 'pts/0',
                                                                     'from': '192.168.71.1',
                                                                     'login_at': 'Thu22',
                                                                     'idle': '10.00s',
                                                                     'jcpu': '0.17s',
                                                                     'pcpu': '0.00s',
                                                                     'what': 'w'})


if __name__ == '__main__':
    unittest.main()
