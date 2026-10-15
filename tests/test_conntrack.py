import contextlib
import io
import os
import sys
import unittest
sys.path.append(os.getcwd())
from tests import utils_for_test as test_utils
sys.path.pop()
import jc


class MyTests(unittest.TestCase):

    def test_conntrack_nodata(self):
        """
        Test 'conntrack' with no data
        """
        test_utils.run_no_data(self, __file__, [])

    def test_conntrack_all_fixtures(self):
        """
        Test 'conntrack' with various fixtures
        """
        test_utils.run_all_fixtures(self, __file__)

    def test_conntrack_unparsable_line_warns(self):
        """
        Test 'conntrack' warns with the offending line when a line can't be
        parsed
        """
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            result = jc.parse('conntrack', 'this is not conntrack output\n')

        self.assertEqual(result, [])
        self.assertIn(
            'Unparsable line found: this is not conntrack output',
            stderr.getvalue()
        )

    def test_conntrack_malformed_fixture_warns(self):
        """
        Test 'conntrack' warns once for each unparsable line in the malformed
        fixture, and not for its summary line
        """
        base_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(base_dir, 'fixtures/generic/conntrack--malformed.out'),
                  encoding='utf-8') as f:
            data = f.read()

        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            result = jc.parse('conntrack', data)

        self.assertEqual(len(result), 2)
        self.assertEqual(stderr.getvalue().count('Unparsable line found'), 4)

    def test_conntrack_summary_line_does_not_warn(self):
        """
        Test 'conntrack' skips the `flow entries/events have been shown`
        summary line silently
        """
        summaries = (
            'conntrack v1.4.9 (conntrack-tools): 2 flow entries have been shown.\n',
            'conntrack v1.4.9 (conntrack-tools): 3 flow events have been shown.\n'
        )

        for summary in summaries:
            with self.subTest(summary):
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr):
                    result = jc.parse('conntrack', summary)

                self.assertEqual(result, [])
                self.assertNotIn('Unparsable line found', stderr.getvalue())

    def test_conntrack_valid_fixture_does_not_warn(self):
        """
        Test 'conntrack' doesn't warn on valid output that carries the summary
        line
        """
        base_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(base_dir, 'fixtures/generic/conntrack--list.out'),
                  encoding='utf-8') as f:
            data = f.read()

        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            result = jc.parse('conntrack', data)

        self.assertEqual(len(result), 6)
        self.assertNotIn('Unparsable line found', stderr.getvalue())

    def test_conntrack_quiet_suppresses_warning(self):
        """
        Test 'conntrack' suppresses the unparsable line warning when quiet is
        set
        """
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            result = jc.parse('conntrack', 'this is not conntrack output\n', quiet=True)

        self.assertEqual(result, [])
        self.assertEqual(stderr.getvalue(), '')


if __name__ == '__main__':
    unittest.main()
