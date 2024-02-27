import os
import unittest
import json
import jc.parsers.rsync

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/rsync-i.out'), 'r', encoding='utf-8') as f:
        centos_7_7_rsync_i = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/rsync-i.out'), 'r', encoding='utf-8') as f:
        generic_rsync_i = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/rsync-ivvv.out'), 'r', encoding='utf-8') as f:
        centos_7_7_rsync_ivvv = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/rsync-i-vvv.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_rsync_ivvv = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/rsync-ivvv-nochange.out'), 'r', encoding='utf-8') as f:
        centos_7_7_rsync_ivvv_nochange = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/rsync-i-vvv-nochange.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_rsync_ivvv_nochange = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/rsync-i-logfile.out'), 'r', encoding='utf-8') as f:
        centos_7_7_rsync_i_logfile = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/rsync-i-v-logfile.out'), 'r', encoding='utf-8') as f:
        centos_7_7_rsync_i_v_logfile = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/rsync-i-vv-logfile.out'), 'r', encoding='utf-8') as f:
        centos_7_7_rsync_i_vv_logfile = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/rsync-i-vvv-logfile.out'), 'r', encoding='utf-8') as f:
        centos_7_7_rsync_i_vvv_logfile = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/rsync-i-vvv-logfile-nochange.out'), 'r', encoding='utf-8') as f:
        centos_7_7_rsync_i_vvv_logfile_nochange = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/rsync-i-vvv-logfile-nochange.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_rsync_i_vvv_logfile_nochange = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/rsync-i.json'), 'r', encoding='utf-8') as f:
        centos_7_7_rsync_i_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/rsync-i.json'), 'r', encoding='utf-8') as f:
        generic_rsync_i_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/rsync-ivvv.json'), 'r', encoding='utf-8') as f:
        centos_7_7_rsync_ivvv_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/rsync-i-vvv.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_rsync_ivvv_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/rsync-ivvv-nochange.json'), 'r', encoding='utf-8') as f:
        centos_7_7_rsync_ivvv_nochange_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/rsync-i-vvv-nochange.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_rsync_ivvv_nochange_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/rsync-i-logfile.json'), 'r', encoding='utf-8') as f:
        centos_7_7_rsync_i_logfile_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/rsync-i-v-logfile.json'), 'r', encoding='utf-8') as f:
        centos_7_7_rsync_i_v_logfile_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/rsync-i-vv-logfile.json'), 'r', encoding='utf-8') as f:
        centos_7_7_rsync_i_vv_logfile_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/rsync-i-vvv-logfile.json'), 'r', encoding='utf-8') as f:
        centos_7_7_rsync_i_vvv_logfile_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/rsync-i-vvv-logfile-nochange.json'), 'r', encoding='utf-8') as f:
        centos_7_7_rsync_i_vvv_logfile_nochange_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/rsync-i-vvv-logfile-nochange.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_rsync_i_vvv_logfile_nochange_json = json.loads(f.read())


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

    def test_rsync_osx_10_14_6_rsync_ivvv(self):
        """
        Test 'rsync -ivvv' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.rsync.parse(self.osx_10_14_6_rsync_ivvv, quiet=True), self.osx_10_14_6_rsync_ivvv_json)

    def test_rsync_osx_10_14_6_rsync_ivvv_nochange(self):
        """
        Test 'rsync -ivvv' on OSX 10.14.6 with no file changes
        """
        self.assertEqual(jc.parsers.rsync.parse(self.osx_10_14_6_rsync_ivvv_nochange, quiet=True), self.osx_10_14_6_rsync_ivvv_nochange_json)

    def test_rsync_centos_7_7_rsync_ivvv_nochange(self):
        """
        Test 'rsync -ivvv' on Centos 7.7 with no file changes
        """
        self.assertEqual(jc.parsers.rsync.parse(self.centos_7_7_rsync_ivvv_nochange, quiet=True), self.centos_7_7_rsync_ivvv_nochange_json)

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

    def test_rsync_centos_7_7_rsync_i_vvv_logfile_nochange(self):
        """
        Test 'rsync -ivvv --log-file=xxx' on Centos 7.7 with no file changes
        """
        self.assertEqual(jc.parsers.rsync.parse(self.centos_7_7_rsync_i_vvv_logfile_nochange, quiet=True), self.centos_7_7_rsync_i_vvv_logfile_nochange_json)

    def test_rsync_osx_10_14_6_rsync_i_vvv_logfile_nochange(self):
        """
        Test 'rsync -ivvv --log-file=xxx' on OSX 10.14.6 with no file changes
        """
        self.assertEqual(jc.parsers.rsync.parse(self.osx_10_14_6_rsync_i_vvv_logfile_nochange, quiet=True), self.osx_10_14_6_rsync_i_vvv_logfile_nochange_json)

    def test_rsync_simple_summary(self):
        """
        Test 'rsync avh' output with a simple summary
        """
        data = '''sending incremental file list

sent 8.71M bytes  received 29.88K bytes  10.99K bytes/sec
total size is 221.79G  speedup is 25,388.23
'''
        expected = [{"summary":{"sent":8710000,"received":29880,"bytes_sec":10990.0,"total_size":221790000000,"speedup":25388.23},"files":[]}]
        self.assertEqual(jc.parsers.rsync.parse(data, quiet=True), expected)


if __name__ == '__main__':
    unittest.main()
