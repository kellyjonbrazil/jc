import os
import json
import unittest
import jc.parsers.jobs

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/jobs.out'), 'r') as f:
            self.centos_7_7_jobs = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/jobs.out'), 'r') as f:
            self.ubuntu_18_4_jobs = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/jobs.json'), 'r') as f:
            self.centos_7_7_jobs_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/jobs.json'), 'r') as f:
            self.ubuntu_18_4_jobs_json = json.loads(f.read())

    def test_jobs_centos_7_7(self):
        """
        Test 'jobs' on Centos 7.7
        """
        self.assertEqual(jc.parsers.jobs.parse(self.centos_7_7_jobs, quiet=True), self.centos_7_7_jobs_json)

    def test_jobs_ubuntu_18_4(self):
        """
        Test 'jobs' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.jobs.parse(self.ubuntu_18_4_jobs, quiet=True), self.ubuntu_18_4_jobs_json)


if __name__ == '__main__':
    unittest.main()
