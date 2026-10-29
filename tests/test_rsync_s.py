import os
import json
import unittest
import jc.parsers.rsync_s

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


# To create streaming output use:
# $ cat rsync.out | jc --rsync-s | jello -c > rsync-streaming.json


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

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/rsync-i-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_rsync_i_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/rsync-i-streaming.json'), 'r', encoding='utf-8') as f:
        generic_rsync_i_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/rsync-ivvv-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_rsync_ivvv_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/rsync-i-vvv-streaming.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_rsync_ivvv_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/rsync-ivvv-nochange-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_rsync_ivvv_nochange_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/rsync-i-vvv-nochange-streaming.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_rsync_ivvv_nochange_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/rsync-i-logfile-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_rsync_i_logfile_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/rsync-i-v-logfile-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_rsync_i_v_logfile_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/rsync-i-vv-logfile-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_rsync_i_vv_logfile_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/rsync-i-vvv-logfile-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_rsync_i_vvv_logfile_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/rsync-i-vvv-logfile-nochange-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_rsync_i_vvv_logfile_nochange_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/rsync-i-vvv-logfile-nochange-streaming.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_rsync_i_vvv_logfile_nochange_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/rsync-i-stats-streaming.json'), 'r', encoding='utf-8') as f:
        generic_rsync_i_stats_streaming_json = json.loads(f.read())


    def test_rsync_s_nodata(self):
        """
        Test 'rsync' with no data
        """
        self.assertEqual(list(jc.parsers.rsync_s.parse([], quiet=True)), [])

    def test_rsync_s_i_centos_7_7(self):
        """
        Test 'rsync -i' on Centos 7.7
        """
        self.assertEqual(list(jc.parsers.rsync_s.parse(self.centos_7_7_rsync_i.splitlines(), quiet=True)), self.centos_7_7_rsync_i_streaming_json)

    def test_rsync_s_logfile_run_without_file_lines(self):
        """
        Test 'rsync_s' log file with a run that has a summary but no file lines
        """
        data = [
            '2022/01/28 03:53:52 [9190] building file list',
            '2022/01/28 03:53:52 [9190] >f+++++++++ a.txt',
            '2022/01/28 03:53:52 [9190] sent 1,713 bytes  received 507 bytes  total size 235',
            '2022/01/28 03:55:00 [9198] building file list',
            '2022/01/28 03:55:00 [9198] sent 120 bytes  received 12 bytes  total size 235'
        ]
        result = list(jc.parsers.rsync_s.parse(data, quiet=True))
        self.assertEqual([(x['type'], x['process']) for x in result],
                         [('file', 9190), ('summary', 9190), ('summary', 9198)])
        self.assertEqual(result[0]['filename'], 'a.txt')
        self.assertEqual(result[1]['sent'], 1713)
        self.assertEqual(result[2]['sent'], 120)
        self.assertEqual(result[2]['received'], 12)

    def test_rsync_s_i_generic(self):
        """
        Test 'rsync -i'
        """
        self.assertEqual(list(jc.parsers.rsync_s.parse(self.generic_rsync_i.splitlines(), quiet=True)), self.generic_rsync_i_streaming_json)

    def test_rsync_s_ivvv_centos_7_7(self):
        """
        Test 'rsync -ivvv' on Centos 7.7
        """
        self.assertEqual(list(jc.parsers.rsync_s.parse(self.centos_7_7_rsync_ivvv.splitlines(), quiet=True)), self.centos_7_7_rsync_ivvv_streaming_json)

    def test_rsync_s_ivvv_osx_10_14_6(self):
        """
        Test 'rsync -ivvv' on OSX 10.14.6
        """
        self.assertEqual(list(jc.parsers.rsync_s.parse(self.osx_10_14_6_rsync_ivvv.splitlines(), quiet=True)), self.osx_10_14_6_rsync_ivvv_streaming_json)

    def test_rsync_s_ivvv_nochange_centos_7_7(self):
        """
        Test 'rsync -ivvv' on Centos 7.7 with no file changes
        """
        self.assertEqual(list(jc.parsers.rsync_s.parse(self.centos_7_7_rsync_ivvv_nochange.splitlines(), quiet=True)), self.centos_7_7_rsync_ivvv_nochange_streaming_json)

    def test_rsync_s_ivvv_nochange_osx_10_14_6(self):
        """
        Test 'rsync -ivvv' on OSX 10.14.6 with no file changes
        """
        self.assertEqual(list(jc.parsers.rsync_s.parse(self.osx_10_14_6_rsync_ivvv_nochange.splitlines(), quiet=True)), self.osx_10_14_6_rsync_ivvv_nochange_streaming_json)

    def test_rsync_s_i_logfile_centos_7_7(self):
        """
        Test 'rsync -i --logfile=xxx' on Centos 7.7
        """
        self.assertEqual(list(jc.parsers.rsync_s.parse(self.centos_7_7_rsync_i_logfile.splitlines(), quiet=True)), self.centos_7_7_rsync_i_logfile_streaming_json)

    def test_rsync_s_i_v_logfile_centos_7_7(self):
        """
        Test 'rsync -iv --logfile=xxx' on Centos 7.7
        """
        self.assertEqual(list(jc.parsers.rsync_s.parse(self.centos_7_7_rsync_i_v_logfile.splitlines(), quiet=True)), self.centos_7_7_rsync_i_v_logfile_streaming_json)

    def test_rsync_s_i_vv_logfile_centos_7_7(self):
        """
        Test 'rsync -ivv --logfile=xxx' on Centos 7.7
        """
        self.assertEqual(list(jc.parsers.rsync_s.parse(self.centos_7_7_rsync_i_vv_logfile.splitlines(), quiet=True)), self.centos_7_7_rsync_i_vv_logfile_streaming_json)

    def test_rsync_s_i_vvv_logfile_centos_7_7(self):
        """
        Test 'rsync -ivvv --logfile=xxx' on Centos 7.7
        """
        self.assertEqual(list(jc.parsers.rsync_s.parse(self.centos_7_7_rsync_i_vvv_logfile.splitlines(), quiet=True)), self.centos_7_7_rsync_i_vvv_logfile_streaming_json)

    def test_rsync_s_i_vvv_logfile_nochange_centos_7_7(self):
        """
        Test 'rsync -ivvv --logfile=xxx' on Centos 7.7 with no file changes
        """
        self.assertEqual(list(jc.parsers.rsync_s.parse(self.centos_7_7_rsync_i_vvv_logfile_nochange.splitlines(), quiet=True)), self.centos_7_7_rsync_i_vvv_logfile_nochange_streaming_json)

    def test_rsync_s_i_vvv_logfile_nochange_osx_10_14_6(self):
        """
        Test 'rsync -ivvv --logfile=xxx' on OSX 10.14.6 with no file changes
        """
        self.assertEqual(list(jc.parsers.rsync_s.parse(self.osx_10_14_6_rsync_i_vvv_logfile_nochange.splitlines(), quiet=True)), self.osx_10_14_6_rsync_i_vvv_logfile_nochange_streaming_json)

    def test_rsync_s_simple_summary(self):
        """
        Test 'rsync avh' output with a simple summary
        """
        data = '''sending incremental file list

sent 8.71M bytes  received 29.88K bytes  10.99K bytes/sec
total size is 221.79G  speedup is 25,388.23
'''
        expected = [{"type":"summary","sent":8710000,"received":29880,"bytes_sec":10990.0,"total_size":221790000000,"speedup":25388.23}]
        self.assertEqual(list(jc.parsers.rsync_s.parse(data.splitlines(), quiet=True)), expected)

    def test_rsync_s_i_stats(self):
        """
        Test 'rsync -i --stats' or 'rsync -i --info=stats[1-3]'
        """
        self.assertEqual(list(jc.parsers.rsync_s.parse(self.generic_rsync_i_stats.splitlines(), quiet=True)), self.generic_rsync_i_stats_streaming_json)


    def test_rsync_s_crlf_lines(self):
        """
        Test rsync with CRLF line endings, split on LF or with line endings kept
        """
        crlf_data = self.centos_7_7_rsync_i.replace('\n', '\r\n')
        self.assertEqual(list(jc.parsers.rsync_s.parse(crlf_data.split('\n'), quiet=True)), self.centos_7_7_rsync_i_streaming_json)
        self.assertEqual(list(jc.parsers.rsync_s.parse(crlf_data.splitlines(keepends=True), quiet=True)), self.centos_7_7_rsync_i_streaming_json)


if __name__ == '__main__':
    unittest.main()
