import os
import unittest
import jc.parsers.free

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/free.out'), 'r') as f:
            self.centos_7_7_free = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/free.out'), 'r') as f:
            self.ubuntu_18_4_free = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/free-h.out'), 'r') as f:
            self.centos_7_7_free_h = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/free-h.out'), 'r') as f:
            self.ubuntu_18_4_free_h = f.read()

    def test_free_centos_7_7(self):
        """
        Test 'free' on Centos 7.7
        """
        self.assertEqual(jc.parsers.free.parse(self.centos_7_7_free)[1], {'type': 'Swap',
                                                                          'total': '2097148',
                                                                          'used': '0',
                                                                          'free': '2097148'})

    def test_free_ubuntu_18_4(self):
        """
        Test 'free' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.free.parse(self.ubuntu_18_4_free)[0], {'type': 'Mem',
                                                                           'total': '2017300',
                                                                           'used': '242740',
                                                                           'free': '478228',
                                                                           'shared': '1196',
                                                                           'buff_cache': '1296332',
                                                                           'available': '1585920'})

    def test_free_h_centos_7_7(self):
        """
        Test 'free -h' on Centos 7.7
        """
        self.assertEqual(jc.parsers.free.parse(self.centos_7_7_free_h)[0], {'type': 'Mem',
                                                                            'total': '3.7G',
                                                                            'used': '217M',
                                                                            'free': '3.2G',
                                                                            'shared': '11M',
                                                                            'buff_cache': '267M',
                                                                            'available': '3.2G'})

    def test_free_h_ubuntu_18_4(self):
        """
        Test 'free -h' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.free.parse(self.ubuntu_18_4_free_h)[1], {'type': 'Swap',
                                                                             'total': '2.0G',
                                                                             'used': '268K',
                                                                             'free': '2.0G'})


if __name__ == '__main__':
    unittest.main()
