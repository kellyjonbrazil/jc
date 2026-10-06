import math
import unittest

from jc.parsers import prometheus


PROMETHEUS_DATA = '''# HELP http_requests The total number of HTTP requests.\n\
# TYPE http_requests counter\n\
http_requests_total{method="post",code="200"} 1027 1395066363000\n\
http_requests_total{method="post",code="400"} 3\n'''

OPENMETRICS_DATA = '''# HELP request_duration_seconds Request duration\\nmeasured in seconds.\n\
# TYPE request_duration_seconds histogram\n\
# UNIT request_duration_seconds seconds\n\
request_duration_seconds_bucket{le="0.5",path="/api\\nitems"} 12 # {trace_id="abc\\"123"} 0.42 1.7\n\
request_duration_seconds_sum 1.25e1\n\
temperature NaN\n\
# EOF\n'''


class PrometheusParserTests(unittest.TestCase):

    def test_prometheus_samples_and_family_metadata(self):
        parsed = prometheus.parse(PROMETHEUS_DATA)

        self.assertEqual(len(parsed), 2)
        self.assertEqual(parsed[0], {
            'name': 'http_requests_total',
            'labels': {'method': 'post', 'code': '200'},
            'value': 1027,
            'timestamp': 1395066363000,
            'help': 'The total number of HTTP requests.',
            'type': 'counter'
        })
        self.assertEqual(parsed[1]['value'], 3)
        self.assertEqual(parsed[1]['type'], 'counter')

    def test_openmetrics_exemplar_unit_and_special_value(self):
        parsed = prometheus.parse(OPENMETRICS_DATA)

        self.assertEqual(parsed[0]['labels'], {
            'le': '0.5',
            'path': '/api\nitems'
        })
        self.assertEqual(parsed[0]['help'],
                         'Request duration\nmeasured in seconds.')
        self.assertEqual(parsed[0]['type'], 'histogram')
        self.assertEqual(parsed[0]['unit'], 'seconds')
        self.assertEqual(parsed[0]['exemplar'], {
            'labels': {'trace_id': 'abc"123'},
            'value': 0.42,
            'timestamp': 1.7
        })
        self.assertEqual(parsed[1]['value'], 12.5)
        self.assertEqual(parsed[2]['value'], 'NaN')

    def test_raw_mode_preserves_numbers_as_strings(self):
        parsed = prometheus.parse('metric 1.25 1234\n', raw=True)

        self.assertEqual(parsed, [{
            'name': 'metric',
            'labels': {},
            'value': '1.25',
            'timestamp': '1234'
        }])

    def test_bytes_and_infinity(self):
        parsed = prometheus.parse(b'metric +Inf\n')

        self.assertEqual(parsed[0]['value'], '+Inf')
        self.assertFalse(isinstance(parsed[0]['value'], float) and
                         math.isinf(parsed[0]['value']))

    def test_empty_input(self):
        self.assertEqual(prometheus.parse(''), [])

    def test_malformed_label_reports_line_number(self):
        with self.assertRaisesRegex(ValueError, r'^line 2: invalid label set$'):
            prometheus.parse('# comment\nmetric{label=no_quotes} 1\n')

    def test_duplicate_label_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'duplicate label: status'):
            prometheus.parse('metric{status="ok",status="bad"} 1\n')


if __name__ == '__main__':
    unittest.main()
