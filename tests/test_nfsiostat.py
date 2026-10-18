import unittest
import contextlib
import io
import os
import sys
from unittest import mock
sys.path.append(os.getcwd())
from tests import utils_for_test as test_utils
sys.path.pop()

import jc.parsers.nfsiostat

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def _parse_capturing_stderr(data, quiet=False):
    # skip the platform compatibility warning so only parser warnings are seen
    with mock.patch('jc.utils.compatibility'), \
         contextlib.redirect_stderr(io.StringIO()) as err:
        result = jc.parsers.nfsiostat.parse(data, quiet=quiet)
    return result, err.getvalue()


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/nfsiostat--malformed.out'), 'r', encoding='utf-8') as f:
        generic_nfsiostat_malformed = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/nfsiostat--attr.out'), 'r', encoding='utf-8') as f:
        generic_nfsiostat_attr = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/nfsiostat--dir.out'), 'r', encoding='utf-8') as f:
        generic_nfsiostat_dir = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/nfsiostat--page.out'), 'r', encoding='utf-8') as f:
        generic_nfsiostat_page = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/nfsiostat--no-mounts.out'), 'r', encoding='utf-8') as f:
        generic_nfsiostat_no_mounts = f.read()

    def test_nfsiostat_nodata(self):
        """
        Test 'nfsiostat' with no data
        """
        test_utils.run_no_data(self, __file__, [])

    def test_nfsiostat_all_fixtures(self):
        """
        Test 'nfsiostat' with various fixtures
        """
        test_utils.run_all_fixtures(self, __file__)

    def test_nfsiostat_malformed_warns(self):
        """
        Test 'nfsiostat' warns about lines it can't parse
        """
        _, stderr = _parse_capturing_stderr(self.generic_nfsiostat_malformed)
        self.assertIn('/home: unexpected number of fields: 2.110', stderr)
        self.assertIn('/home: skipping unknown operation table: commit', stderr)
        self.assertIn('/home: could not parse write values', stderr)
        self.assertIn('/mnt/archive: no operation statistics found', stderr)

    def test_nfsiostat_unknown_operation_not_a_key(self):
        """
        Test 'nfsiostat' does not turn an unknown table name into a key
        """
        result, _ = _parse_capturing_stderr(self.generic_nfsiostat_malformed)
        self.assertNotIn('commit', result[0])
        self.assertIn('read', result[0])

    def test_nfsiostat_summary_lines_do_not_warn(self):
        """
        Test 'nfsiostat' does not warn about the -a, -d, and -p summary lines
        """
        for name, data in (('attr', self.generic_nfsiostat_attr),
                           ('dir', self.generic_nfsiostat_dir),
                           ('page', self.generic_nfsiostat_page)):
            with self.subTest(fixture=name):
                _, stderr = _parse_capturing_stderr(data)
                self.assertEqual(stderr, '')

    def test_nfsiostat_malformed_quiet(self):
        """
        Test 'nfsiostat' prints nothing with quiet=True
        """
        _, stderr = _parse_capturing_stderr(self.generic_nfsiostat_malformed, quiet=True)
        self.assertEqual(stderr, '')

    def test_nfsiostat_missing_values_line_warns(self):
        """
        Test 'nfsiostat' warns when a header line is followed by a mount header
        """
        data = '\n'.join([
            '192.168.1.10:/export/home mounted on /home:',
            '           ops/s       rpc bklog',
            '192.168.1.11:/export/data mounted on /data:',
            '           ops/s       rpc bklog',
            '           1.000           0.000',
            'read:              ops/s            kB/s           kB/op         retrans    avg RTT (ms)    avg exe (ms)  avg queue (ms)',
            '                   0.008           7.942         980.310        2 (0.3%)           6.000           6.300           0.300'
        ])
        result, stderr = _parse_capturing_stderr(data)
        self.assertEqual([item['mount'] for item in result], ['/home', '/data'])
        self.assertIn('/home: missing the values line after a header line', stderr)

    def test_nfsiostat_mount_header_followed_by_op_header_warns(self):
        """
        Test 'nfsiostat' warns when the "ops/s rpc bklog" header is followed by an operation header
        """
        data = '\n'.join([
            '192.168.1.10:/export/home mounted on /home:',
            '           ops/s       rpc bklog',
            'read:              ops/s            kB/s           kB/op         retrans    avg RTT (ms)    avg exe (ms)  avg queue (ms)',
            '                   0.008           7.942         980.310        2 (0.3%)           6.000           6.300           0.300'
        ])
        result, stderr = _parse_capturing_stderr(data)
        self.assertNotIn('ops_sec', result[0])
        self.assertIn('read', result[0])
        self.assertEqual(stderr.count('/home: missing the values line after a header line'), 1)

    def test_nfsiostat_op_header_followed_by_op_header_warns(self):
        """
        Test 'nfsiostat' warns when an operation header is followed by another operation header
        """
        data = '\n'.join([
            '192.168.1.10:/export/home mounted on /home:',
            '           ops/s       rpc bklog',
            '           2.110           0.000',
            'read:              ops/s            kB/s           kB/op         retrans    avg RTT (ms)    avg exe (ms)  avg queue (ms)',
            'write:             ops/s            kB/s           kB/op         retrans    avg RTT (ms)    avg exe (ms)  avg queue (ms)',
            '                   0.002           2.371        1024.176        0 (0.0%)          10.000          10.200           0.100'
        ])
        result, stderr = _parse_capturing_stderr(data)
        self.assertNotIn('read', result[0])
        self.assertIn('write', result[0])
        self.assertEqual(stderr.count('/home: missing the values line after a header line'), 1)

    def test_nfsiostat_no_mount_blocks_warns(self):
        """
        Test 'nfsiostat' warns when the input has no mount blocks
        """
        result, stderr = _parse_capturing_stderr('Usage: iostat [ options ] [ <interval> [ <count> ] ]\n')
        self.assertEqual(result, [])
        self.assertIn('No NFS mount blocks found', stderr)

    def test_nfsiostat_no_mounts_message_does_not_warn(self):
        """
        Test 'nfsiostat' returns [] without a warning for "No NFS mount points were found"
        """
        result, stderr = _parse_capturing_stderr(self.generic_nfsiostat_no_mounts)
        self.assertEqual(result, [])
        self.assertEqual(stderr, '')


if __name__ == '__main__':
    unittest.main()
