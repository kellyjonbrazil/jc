import unittest
import jc.streaming


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


    def test_add_jc_meta_ignore_exceptions_by_position(self):
        """
        Test add_jc_meta with ignore_exceptions passed by keyword, by
        position, through **kwargs, and left at its default
        """
        @jc.streaming.add_jc_meta
        def parse(data, raw=False, quiet=False, ignore_exceptions=False):
            yield {'a': data}

        @jc.streaming.add_jc_meta
        def parse_kwargs(data, **kwargs):
            yield {'a': data}

        success = {'a': 1, '_jc_meta': {'success': True}}
        self.assertEqual(list(parse(1, ignore_exceptions=True)), [success])
        self.assertEqual(list(parse(1, False, False, True)), [success])
        self.assertEqual(list(parse(1, False, False, False)), [{'a': 1}])
        self.assertEqual(list(parse(1, False, True)), [{'a': 1}])
        self.assertEqual(list(parse(1)), [{'a': 1}])
        self.assertEqual(list(parse_kwargs(1, ignore_exceptions=True)), [success])
        self.assertEqual(list(parse_kwargs(1)), [{'a': 1}])


if __name__ == '__main__':
    unittest.main()
