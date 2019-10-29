import os
import unittest
import jc.parsers.jobs

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/jobs.out'), 'r') as f:
            self.centos_7_7_jobs = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/jobs.out'), 'r') as f:
            self.ubuntu_18_4_jobs = f.read()

    def test_jobs_centos_7_7(self):
        """
        Test 'jobs' on Centos 7.7
        """
        self.assertEqual(jc.parsers.jobs.parse(self.centos_7_7_jobs)[3], {'job_number': '4',
                                                                          'history': 'current',
                                                                          'status': 'Running',
                                                                          'command': 'sleep 14 &'})

    def test_jobs_ubuntu_18_4(self):
        """
        Test 'jobs' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.jobs.parse(self.ubuntu_18_4_jobs)[2], {'job_number': '3',
                                                                           'history': 'previous',
                                                                           'status': 'Running',
                                                                           'command': 'sleep 13 &'})


if __name__ == '__main__':
    unittest.main()
