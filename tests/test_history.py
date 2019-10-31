import os
import unittest
import jc.parsers.history

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/history.out'), 'r') as f:
            self.centos_7_7_history = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/history.out'), 'r') as f:
            self.ubuntu_18_4_history = f.read()

    def test_history_centos_7_7(self):
        """
        Test 'history' on Centos 7.7
        """
        self.assertEqual(jc.parsers.history.parse(self.centos_7_7_history)['n658'], 'cat testing ')

    def test_history_ubuntu_18_4(self):
        """
        Test 'history' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.history.parse(self.ubuntu_18_4_history)['n214'], 'netstat -lp | jc --netstat')


if __name__ == '__main__':
    unittest.main()
