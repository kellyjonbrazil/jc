import os
import unittest
import jc.parsers.uptime

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/uptime.out'), 'r') as f:
            self.centos_7_7_uptime = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/uptime.out'), 'r') as f:
            self.ubuntu_18_4_uptime = f.read()

    def test_uptime_centos_7_7(self):
        """
        Test 'uptime' on Centos 7.7
        """
        self.assertEqual(jc.parsers.uptime.parse(self.centos_7_7_uptime), {'time': '10:25:20',
                                                                           'uptime': '16:03',
                                                                           'users': '2',
                                                                           'load_1m': '0.00',
                                                                           'load_5m': '0.01',
                                                                           'load_15m': '0.05'})

    def test_uptime_ubuntu_18_4(self):
        """
        Test 'uptime' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.uptime.parse(self.ubuntu_18_4_uptime), {'time': '19:43:06',
                                                                            'uptime': '2 days, 19:32',
                                                                            'users': '2',
                                                                            'load_1m': '0.00',
                                                                            'load_5m': '0.00',
                                                                            'load_15m': '0.00'})


if __name__ == '__main__':
    unittest.main()
