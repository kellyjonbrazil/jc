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

FIXTURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures/generic')


def _read_fixture(name):
    with open(os.path.join(FIXTURES_DIR, name), 'r', encoding='utf-8') as f:
        return f.read()


def _parse_capturing_stderr(data, quiet=False):
    # skip the platform compatibility warning so only parser warnings are seen
    with mock.patch('jc.utils.compatibility'), \
         contextlib.redirect_stderr(io.StringIO()) as err:
        result = jc.parsers.nfsiostat.parse(data, quiet=quiet)
    return result, err.getvalue()


class MyTests(unittest.TestCase):

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
        _, stderr = _parse_capturing_stderr(_read_fixture('nfsiostat--malformed.out'))
        self.assertIn('/home: unexpected number of fields: 2.110', stderr)
        self.assertIn('/home: skipping unknown operation table: commit', stderr)
        self.assertIn('/home: could not parse write values', stderr)
        self.assertIn('/mnt/archive: no operation statistics found', stderr)

    def test_nfsiostat_unknown_operation_not_a_key(self):
        """
        Test 'nfsiostat' does not turn an unknown table name into a key
        """
        result, _ = _parse_capturing_stderr(_read_fixture('nfsiostat--malformed.out'))
        self.assertNotIn('commit', result[0])
        self.assertIn('read', result[0])

    def test_nfsiostat_summary_lines_do_not_warn(self):
        """
        Test 'nfsiostat' does not warn about the -a, -d, and -p summary lines
        """
        for name in ('nfsiostat--attr.out', 'nfsiostat--dir.out', 'nfsiostat--page.out'):
            with self.subTest(fixture=name):
                _, stderr = _parse_capturing_stderr(_read_fixture(name))
                self.assertEqual(stderr, '')

    def test_nfsiostat_malformed_quiet(self):
        """
        Test 'nfsiostat' prints nothing with quiet=True
        """
        _, stderr = _parse_capturing_stderr(_read_fixture('nfsiostat--malformed.out'), quiet=True)
        self.assertEqual(stderr, '')


if __name__ == '__main__':
    unittest.main()
