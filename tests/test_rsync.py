import os
import unittest
import json
import jc.parsers.rsync

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/rsync-i.out'), 'r', encoding='utf-8') as f:
            self.centos_7_7_rsync_i = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/rsync-i.out'), 'r', encoding='utf-8') as f:
            self.generic_rsync_i = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/rsync-ivvv.out'), 'r', encoding='utf-8') as f:
            self.centos_7_7_rsync_ivvv = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/rsync-i-logfile.out'), 'r', encoding='utf-8') as f:
            self.centos_7_7_rsync_i_logfile = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/rsync-i-v-logfile.out'), 'r', encoding='utf-8') as f:
            self.centos_7_7_rsync_i_v_logfile = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/rsync-i-vv-logfile.out'), 'r', encoding='utf-8') as f:
            self.centos_7_7_rsync_i_vv_logfile = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/rsync-i-vvv-logfile.out'), 'r', encoding='utf-8') as f:
            self.centos_7_7_rsync_i_vvv_logfile = f.read()

        

        # with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/rsync.out'), 'r', encoding='utf-8') as f:
        #     self.ubuntu_18_4_rsync = f.read()



        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/rsync-i.json'), 'r', encoding='utf-8') as f:
            self.centos_7_7_rsync_i_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/rsync-i.json'), 'r', encoding='utf-8') as f:
            self.generic_rsync_i_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/rsync-ivvv.json'), 'r', encoding='utf-8') as f:
            self.centos_7_7_rsync_ivvv_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/rsync-i-logfile.json'), 'r', encoding='utf-8') as f:
            self.centos_7_7_rsync_i_logfile_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/rsync-i-v-logfile.json'), 'r', encoding='utf-8') as f:
            self.centos_7_7_rsync_i_v_logfile_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/rsync-i-vv-logfile.json'), 'r', encoding='utf-8') as f:
            self.centos_7_7_rsync_i_vv_logfile_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/rsync-i-vvv-logfile.json'), 'r', encoding='utf-8') as f:
            self.centos_7_7_rsync_i_vvv_logfile_json = json.loads(f.read())

        # with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/rsync.json'), 'r', encoding='utf-8') as f:
        #     self.ubuntu_18_4_rsync_json = json.loads(f.read())



    def test_rsync_nodata(self):
        """
        Test 'rsync' with no data
        """
        self.assertEqual(jc.parsers.rsync.parse('', quiet=True), [])

    def test_rsync_centos_7_7_rsync_i(self):
        """
        Test 'rsync -i' on Centos 7.7
        """
        self.assertEqual(jc.parsers.rsync.parse(self.centos_7_7_rsync_i, quiet=True), self.centos_7_7_rsync_i_json)

    def test_rsync_generic_rsync_i(self):
        """
        Test 'rsync -i'
        """
        self.assertEqual(jc.parsers.rsync.parse(self.generic_rsync_i, quiet=True), self.generic_rsync_i_json)

    def test_rsync_centos_7_7_rsync_ivvv(self):
        """
        Test 'rsync -ivvv' on Centos 7.7
        """
        self.assertEqual(jc.parsers.rsync.parse(self.centos_7_7_rsync_ivvv, quiet=True), self.centos_7_7_rsync_ivvv_json)

    def test_rsync_centos_7_7_rsync_i_logfile(self):
        """
        Test 'rsync -i --log-file=xxx' on Centos 7.7
        """
        self.assertEqual(jc.parsers.rsync.parse(self.centos_7_7_rsync_i_logfile, quiet=True), self.centos_7_7_rsync_i_logfile_json)

    def test_rsync_centos_7_7_rsync_i_v_logfile(self):
        """
        Test 'rsync -iv --log-file=xxx' on Centos 7.7
        """
        self.assertEqual(jc.parsers.rsync.parse(self.centos_7_7_rsync_i_v_logfile, quiet=True), self.centos_7_7_rsync_i_v_logfile_json)

    def test_rsync_centos_7_7_rsync_i_vv_logfile(self):
        """
        Test 'rsync -ivv --log-file=xxx' on Centos 7.7
        """
        self.assertEqual(jc.parsers.rsync.parse(self.centos_7_7_rsync_i_vv_logfile, quiet=True), self.centos_7_7_rsync_i_vv_logfile_json)

    def test_rsync_centos_7_7_rsync_i_vvv_logfile(self):
        """
        Test 'rsync -ivvv --log-file=xxx' on Centos 7.7
        """
        self.assertEqual(jc.parsers.rsync.parse(self.centos_7_7_rsync_i_vvv_logfile, quiet=True), self.centos_7_7_rsync_i_vvv_logfile_json)

    # def test_rsync_ubuntu_18_4(self):
    #     """
    #     Test 'rsync' on Ubuntu 18.4
    #     """
    #     self.assertEqual(jc.parsers.rsync.parse(self.ubuntu_18_4_rsync, quiet=True), self.ubuntu_18_4_rsync_json)



if __name__ == '__main__':
    unittest.main()
