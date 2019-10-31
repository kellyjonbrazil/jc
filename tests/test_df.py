import os
import unittest
import jc.parsers.df

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/df.out'), 'r') as f:
            self.centos_7_7_df = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/df.out'), 'r') as f:
            self.ubuntu_18_4_df = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/df-h.out'), 'r') as f:
            self.centos_7_7_df_h = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/df-h.out'), 'r') as f:
            self.ubuntu_18_4_df_h = f.read()

    def test_df_centos_7_7(self):
        """
        Test plain 'df' on Centos 7.7
        """
        self.assertEqual(jc.parsers.df.parse(self.centos_7_7_df)[2], {'filesystem': 'tmpfs',
                                                                      '1k-blocks': '1930664',
                                                                      'used': '11832',
                                                                      'available': '1918832',
                                                                      'use_percent': '1%',
                                                                      'mounted': '/run'})

    def test_df_ubuntu_18_4(self):
        """
        Test plain 'df' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.df.parse(self.ubuntu_18_4_df)[6], {'filesystem': '/dev/loop0',
                                                                       '1k-blocks': '55936',
                                                                       'used': '55936',
                                                                       'available': '0',
                                                                       'use_percent': '100%',
                                                                       'mounted': '/snap/core18/1223'})

    def test_df_h_centos_7_7(self):
        """
        Test plain 'df -h' on Centos 7.7
        """
        self.assertEqual(jc.parsers.df.parse(self.centos_7_7_df_h)[4], {'filesystem': '/dev/mapper/centos-root',
                                                                        'size': '17G',
                                                                        'used': '1.8G',
                                                                        'avail': '16G',
                                                                        'use_percent': '11%',
                                                                        'mounted': '/'})

    def test_df_h_ubuntu_18_4(self):
        """
        Test plain 'df -h' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.df.parse(self.ubuntu_18_4_df_h)[3], {'filesystem': 'tmpfs',
                                                                         'size': '986M',
                                                                         'used': '0',
                                                                         'avail': '986M',
                                                                         'use_percent': '0%',
                                                                         'mounted': '/dev/shm'})


if __name__ == '__main__':
    unittest.main()
