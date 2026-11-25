import unittest
import jc.streaming
from jc.exceptions import ParseError


class MyTests(unittest.TestCase):

    def test_streaming_input_type_check_wrong(self):
        self.assertRaises(TypeError, jc.streaming.streaming_input_type_check, 'abc')


    def test_streaming_input_type_check_correct(self):
        self.assertEqual(jc.streaming.streaming_input_type_check(['abc']), None)


    def test_streaming_line_input_type_check_wrong(self):
        self.assertRaises(TypeError, jc.streaming.streaming_line_input_type_check, ['abc'])


    def test_streaming_line_input_type_check_correct(self):
        self.assertEqual(jc.streaming.streaming_line_input_type_check('abc'), None)


    def test_stream_success_ignore_exceptions_true(self):
        self.assertEqual(jc.streaming.stream_success({}, True), {'_jc_meta': {'success': True}})


    def test_stream_success_ignore_exceptions_false(self):
        self.assertEqual(jc.streaming.stream_success({}, False), {})


    def test_stream_error(self):
        self.assertEqual(jc.streaming.stream_error(
            TypeError, 'this is a test'),
            {
                '_jc_meta':
                    {
                        'success': False,
                        'error': 'type: <class \'TypeError\'>',
                        'line': 'this is a test'
                    }
            }
        )


    def test_stream_error_parse_error_short_message(self):
        """
        Test that a long or multi-line ParseError message is shortened in _jc_meta
        """
        msg = 'Unable to parse line: ' + 'a' * 1000 + '\nsecond line'
        self.assertEqual(jc.streaming.stream_error(
            ParseError(msg), 'this is a test'),
            {
                '_jc_meta':
                    {
                        'success': False,
                        'error': 'ParseError: ' + msg[:500] + '...',
                        'line': 'this is a test'
                    }
            }
        )


    def test_stream_error_other_exception_full_message(self):
        """
        Test that exceptions other than ParseError keep their full message in _jc_meta
        """
        msg = 'b' * 1000
        self.assertEqual(
            jc.streaming.stream_error(ValueError(msg), 'x')['_jc_meta']['error'],
            'ValueError: ' + msg
        )


    def test_raise_or_yield_ignore_exceptions(self):
        self.assertEqual(jc.streaming.raise_or_yield(
            True, TypeError, 'this is a test'),
            (TypeError, 'this is a test')
        )


    def test_raise_or_yield_ignore_exceptions_false(self):
        self.assertRaises(
            TypeError,
            jc.streaming.raise_or_yield,
            False, TypeError, 'this is a test'
        )


if __name__ == '__main__':
    unittest.main()
