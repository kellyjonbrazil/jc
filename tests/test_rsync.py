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

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/rsync-i-stats.out'), 'r', encoding='utf-8') as f:
        generic_rsync_i_stats = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/rsync-i-delete.out'), 'r', encoding='utf-8') as f:
        generic_rsync_i_delete = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/rsync-i-delete-logfile.out'), 'r', encoding='utf-8') as f:
        generic_rsync_i_delete_logfile = f.read()

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

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/rsync-i-stats.json'), 'r', encoding='utf-8') as f:
        generic_rsync_i_stats_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/rsync-i-delete.json'), 'r', encoding='utf-8') as f:
        generic_rsync_i_delete_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/rsync-i-delete-logfile.json'), 'r', encoding='utf-8') as f:
        generic_rsync_i_delete_logfile_json = json.loads(f.read())


    def test_rsync_line_separators(self):
        """
        Test 'rsync' with line-break characters other than LF in a file name
        """
        data = '>f+++++++++ some/a\rb\x0bc\x0cd\x1ce\x1df\x1eg\x85h\u2028i\u2029j.txt\n.f....og..x some/dir/b.txt\n'
        result = jc.parsers.rsync.parse(data, quiet=True)
        self.assertEqual(result[0]['files'][0]['filename'], 'some/a\rb\x0bc\x0cd\x1ce\x1df\x1eg\x85h\u2028i\u2029j.txt')
        self.assertEqual(result[0]['files'][1]['filename'], 'some/dir/b.txt')

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

    def test_rsync_logfile_run_without_file_lines(self):
        """
        Test 'rsync' log file with a run that has a summary but no file lines
        """
        data = (
            '2022/01/28 03:53:52 [9190] building file list\n'
            '2022/01/28 03:53:52 [9190] >f+++++++++ a.txt\n'
            '2022/01/28 03:53:52 [9190] sent 1,713 bytes  received 507 bytes  total size 235\n'
            '2022/01/28 03:55:00 [9198] building file list\n'
            '2022/01/28 03:55:00 [9198] sent 120 bytes  received 12 bytes  total size 235\n'
        )
        result = jc.parsers.rsync.parse(data, quiet=True)
        self.assertEqual(len(result), 2)
        self.assertEqual([x['filename'] for x in result[0]['files']], ['a.txt'])
        self.assertEqual(result[0]['summary']['process'], 9190)
        self.assertEqual(result[0]['summary']['sent'], 1713)
        self.assertEqual(result[1]['files'], [])
        self.assertEqual(result[1]['summary']['process'], 9198)
        self.assertEqual(result[1]['summary']['sent'], 120)
        self.assertEqual(result[1]['summary']['received'], 12)

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

    def test_rsync_with_stats(self):
        """
        Test 'rsync -i --stats' or 'rsync -i --info=stats[1-3]'
        """
        self.assertEqual(jc.parsers.rsync.parse(self.generic_rsync_i_stats, quiet=True), self.generic_rsync_i_stats_json)

    def test_rsync_i_delete(self):
        """
        Test 'rsync -i --delete' with deleted files
        """
        self.assertEqual(jc.parsers.rsync.parse(self.generic_rsync_i_delete, quiet=True), self.generic_rsync_i_delete_json)

    def test_rsync_i_delete_logfile(self):
        """
        Test 'rsync -i --delete --log-file' with deleted files in two runs
        """
        self.assertEqual(jc.parsers.rsync.parse(self.generic_rsync_i_delete_logfile, quiet=True), self.generic_rsync_i_delete_logfile_json)

    def test_rsync_logfile_skipping_message(self):
        """
        Test 'rsync --log-file' with a "*** Skipping" message, which is not a file
        """
        data = (
            '2022/01/28 03:53:52 [9190] *** Skipping any contents from this failed directory ***\n'
            '2022/01/28 03:53:52 [9190] *deleting   old/stale.conf\n'
        )
        result = jc.parsers.rsync.parse(data, quiet=True)
        self.assertEqual([x['filename'] for x in result[0]['files']], ['old/stale.conf'])
        self.assertEqual(result[0]['files'][0]['metadata'], '*deleting')
        self.assertEqual(result[0]['files'][0]['update_type'], 'message')


if __name__ == '__main__':
    unittest.main()
