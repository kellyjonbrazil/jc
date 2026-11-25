import unittest
import os
import sys
sys.path.append(os.getcwd())
from tests import utils_for_test as test_utils
sys.path.pop()
import jc.parsers.prometheus
from jc.exceptions import ParseError


class MyTests(unittest.TestCase):

    def test_prometheus_nodata(self):
        """
        Test 'prometheus' with no data
        """
        test_utils.run_no_data(self, __file__, [])

    def test_prometheus_all_fixtures(self):
        """
        Test 'prometheus' with various fixtures
        """
        test_utils.run_all_fixtures(self, __file__)

    def test_prometheus_metadata(self):
        """
        Test 'prometheus' HELP and TYPE lines with a quoted metric name, and a
        sample name that only looks like it belongs to a metric family
        """
        data = (
            '# HELP "my.dotted.metric" A metric with a dotted name.\n'
            '# TYPE "my.dotted.metric" gauge\n'
            '{"my.dotted.metric"} 1\n'
            '# TYPE foo gauge\n'
            'foo 1\n'
            'foo_total 2\n'
        )
        result = jc.parsers.prometheus.parse(data, quiet=True)
        self.assertEqual([(x['name'], x['type'], x['help']) for x in result], [
            ('my.dotted.metric', 'gauge', 'A metric with a dotted name.'),
            ('foo', 'gauge', None),
            ('foo_total', None, None)
        ])

    def test_prometheus_invalid_lines(self):
        """
        Test 'prometheus' with lines that are not valid samples
        """
        for line in ['foo', 'foo 1 2 3', 'foo{a="1",a="2"} 1', 'foo{a=1} 1', 'foo{a="1" 1', '{"name"} 1 # x 1', '"name" 1']:
            with self.subTest(line=line):
                with self.assertRaises(ParseError):
                    jc.parsers.prometheus.parse(line, quiet=True)


if __name__ == '__main__':
    unittest.main()
