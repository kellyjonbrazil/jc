import contextlib
import io
import os
import json
import unittest
from typing import Dict
from unittest import mock
from jc.exceptions import ParseError
from jc.parsers.nfsiostat_s import parse

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

# The input fixtures are shared with the nfsiostat parser tests. The
# expected streaming output is the same list of mount objects that the
# nfsiostat parser returns, one item per mount block.


def _parse_capturing_stderr(data, quiet=False, ignore_exceptions=False):
    # skip the platform compatibility warning so only parser warnings are seen
    with mock.patch('jc.utils.compatibility'), \
         contextlib.redirect_stderr(io.StringIO()) as err:
        result = list(parse(data, quiet=quiet, ignore_exceptions=ignore_exceptions))
    return result, err.getvalue()


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'attr': (
                'fixtures/generic/nfsiostat--attr.out',
                'fixtures/generic/nfsiostat_s--attr.json'),
            'dir': (
                'fixtures/generic/nfsiostat--dir.out',
                'fixtures/generic/nfsiostat_s--dir.json'),
            'interval_count': (
                'fixtures/generic/nfsiostat--interval-count.out',
                'fixtures/generic/nfsiostat_s--interval-count.json'),
            'interval_count_ignore_exceptions': (
                'fixtures/generic/nfsiostat--interval-count.out',
                'fixtures/generic/nfsiostat_s--interval-count-ignore-exceptions.json'),
            'malformed_ignore_exceptions': (
                'fixtures/generic/nfsiostat--malformed.out',
                'fixtures/generic/nfsiostat_s--malformed-ignore-exceptions.json'),
            'no_errors_column': (
                'fixtures/generic/nfsiostat--no-errors-column.out',
                'fixtures/generic/nfsiostat_s--no-errors-column.json'),
            'page': (
                'fixtures/generic/nfsiostat--page.out',
                'fixtures/generic/nfsiostat_s--page.json'),
            'two_mounts': (
                'fixtures/generic/nfsiostat--two-mounts.out',
                'fixtures/generic/nfsiostat_s--two-mounts.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())

        with open(os.path.join(THIS_DIR, 'fixtures/generic/nfsiostat--no-mounts.out'), 'r', encoding='utf-8') as f:
            cls.no_mounts = f.read()


    def test_nfsiostat_s_nodata(self):
        """
        Test 'nfsiostat' with no data
        """
        self.assertEqual(list(parse([], quiet=True)), [])

    def test_nfsiostat_s_unparsable(self):
        """
        Test non-nfsiostat data (raises ParseError)
        """
        g = parse(['not nfsiostat data', 'not nfsiostat data'], quiet=True)
        with self.assertRaises(ParseError):
            list(g)

    def test_nfsiostat_s_ignore_exceptions_error(self):
        """
        Test non-nfsiostat data with the ignore_exceptions option
        """
        expected = [{'_jc_meta': {'success': False, 'error': 'ParseError: Not nfsiostat data', 'line': 'not nfsiostat data'}}]
        self.assertEqual(list(parse(['not nfsiostat data'], quiet=True, ignore_exceptions=True)), expected)

    def test_nfsiostat_s_ignore_exceptions_success(self):
        """
        Test 'nfsiostat' with an interval and count and the ignore_exceptions option
        """
        self.assertEqual(
            list(parse(self.f_in['interval_count_ignore_exceptions'].splitlines(), quiet=True, ignore_exceptions=True)),
            self.f_json['interval_count_ignore_exceptions']
        )

    def test_nfsiostat_s_interval_count(self):
        """
        Test 'nfsiostat' with an interval and count
        """
        self.assertEqual(
            list(parse(self.f_in['interval_count'].splitlines(), quiet=True)),
            self.f_json['interval_count']
        )

    def test_nfsiostat_s_two_mounts(self):
        """
        Test 'nfsiostat' with two mounts
        """
        self.assertEqual(
            list(parse(self.f_in['two_mounts'].splitlines(), quiet=True)),
            self.f_json['two_mounts']
        )

    def test_nfsiostat_s_attr(self):
        """
        Test 'nfsiostat -a'
        """
        self.assertEqual(
            list(parse(self.f_in['attr'].splitlines(), quiet=True)),
            self.f_json['attr']
        )

    def test_nfsiostat_s_dir(self):
        """
        Test 'nfsiostat -d'
        """
        self.assertEqual(
            list(parse(self.f_in['dir'].splitlines(), quiet=True)),
            self.f_json['dir']
        )

    def test_nfsiostat_s_page(self):
        """
        Test 'nfsiostat -p'
        """
        self.assertEqual(
            list(parse(self.f_in['page'].splitlines(), quiet=True)),
            self.f_json['page']
        )

    def test_nfsiostat_s_no_errors_column(self):
        """
        Test 'nfsiostat' on a kernel without per-operation error counts
        """
        self.assertEqual(
            list(parse(self.f_in['no_errors_column'].splitlines(), quiet=True)),
            self.f_json['no_errors_column']
        )

    def test_nfsiostat_s_no_mounts(self):
        """
        Test 'nfsiostat' with "No NFS mount points were found" yields nothing
        """
        result, stderr = _parse_capturing_stderr(self.no_mounts.splitlines())
        self.assertEqual(result, [])
        self.assertEqual(stderr, '')

    def test_nfsiostat_s_malformed_raises(self):
        """
        Test 'nfsiostat' with an unparseable values line (raises ParseError)
        """
        g = parse(self.f_in['malformed_ignore_exceptions'].splitlines(), quiet=True)
        with self.assertRaises(ParseError):
            list(g)

    def test_nfsiostat_s_malformed_ignore_exceptions(self):
        """
        Test 'nfsiostat' with unparseable values lines and the ignore_exceptions option
        """
        self.assertEqual(
            list(parse(self.f_in['malformed_ignore_exceptions'].splitlines(), quiet=True, ignore_exceptions=True)),
            self.f_json['malformed_ignore_exceptions']
        )

    def test_nfsiostat_s_malformed_warns(self):
        """
        Test 'nfsiostat' warns about skipped tables and incomplete mount blocks
        """
        _, stderr = _parse_capturing_stderr(self.f_in['malformed_ignore_exceptions'].splitlines(), ignore_exceptions=True)
        self.assertIn('/home: skipping unknown operation table: commit', stderr)
        self.assertIn('/mnt/archive: no operation statistics found', stderr)

    def test_nfsiostat_s_malformed_quiet(self):
        """
        Test 'nfsiostat' prints nothing with quiet=True
        """
        _, stderr = _parse_capturing_stderr(self.f_in['malformed_ignore_exceptions'].splitlines(), quiet=True, ignore_exceptions=True)
        self.assertEqual(stderr, '')

    def test_nfsiostat_s_missing_values_line_warns(self):
        """
        Test 'nfsiostat' warns when a header line is not followed by its values line
        """
        data = [
            '192.168.1.10:/export/home mounted on /home:',
            '           ops/s       rpc bklog',
            '192.168.1.11:/export/data mounted on /data:',
            '           ops/s       rpc bklog',
            '           1.000           0.000',
            'read:              ops/s            kB/s           kB/op         retrans    avg RTT (ms)    avg exe (ms)  avg queue (ms)',
            '                   0.008           7.942         980.310        2 (0.3%)           6.000           6.300           0.300'
        ]
        result, stderr = _parse_capturing_stderr(data)
        self.assertEqual([item['mount'] for item in result], ['/home', '/data'])
        self.assertIn('/home: missing the values line after a header line', stderr)

    def test_nfsiostat_s_mount_header_followed_by_op_header_warns(self):
        """
        Test 'nfsiostat' warns when the "ops/s rpc bklog" header is followed by an operation header
        """
        data = [
            '192.168.1.10:/export/home mounted on /home:',
            '           ops/s       rpc bklog',
            'read:              ops/s            kB/s           kB/op         retrans    avg RTT (ms)    avg exe (ms)  avg queue (ms)',
            '                   0.008           7.942         980.310        2 (0.3%)           6.000           6.300           0.300'
        ]
        result, stderr = _parse_capturing_stderr(data)
        self.assertNotIn('ops_sec', result[0])
        self.assertIn('read', result[0])
        self.assertEqual(stderr.count('/home: missing the values line after a header line'), 1)

    def test_nfsiostat_s_op_header_followed_by_op_header_warns(self):
        """
        Test 'nfsiostat' warns when an operation header is followed by another operation header
        """
        data = [
            '192.168.1.10:/export/home mounted on /home:',
            '           ops/s       rpc bklog',
            '           2.110           0.000',
            'read:              ops/s            kB/s           kB/op         retrans    avg RTT (ms)    avg exe (ms)  avg queue (ms)',
            'write:             ops/s            kB/s           kB/op         retrans    avg RTT (ms)    avg exe (ms)  avg queue (ms)',
            '                   0.002           2.371        1024.176        0 (0.0%)          10.000          10.200           0.100'
        ]
        result, stderr = _parse_capturing_stderr(data)
        self.assertNotIn('read', result[0])
        self.assertIn('write', result[0])
        self.assertEqual(stderr.count('/home: missing the values line after a header line'), 1)

    def test_nfsiostat_s_summary_lines_do_not_warn(self):
        """
        Test 'nfsiostat' does not warn about the -a, -d, and -p summary lines
        """
        for name in ('attr', 'dir', 'page'):
            with self.subTest(fixture=name):
                _, stderr = _parse_capturing_stderr(self.f_in[name].splitlines())
                self.assertEqual(stderr, '')

    def test_nfsiostat_s_yields_each_mount_when_its_block_ends(self):
        """
        Test 'nfsiostat' outputs a mount as soon as the next mount header is read
        """
        lines = self.f_in['interval_count'].splitlines()
        second_header = next(i for i, line in enumerate(lines)
                             if i > 0 and line.endswith(' mounted on /mnt/archive:'))
        consumed = []

        def source():
            for line in lines:
                consumed.append(line)
                yield line

        first = next(parse(source(), quiet=True))
        self.assertEqual(first['mount'], '/home')
        self.assertEqual(len(consumed), second_header + 1)


if __name__ == '__main__':
    unittest.main()
