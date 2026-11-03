import unittest
from jc.exceptions import ParseError, LibraryNotInstalled


class MyTests(unittest.TestCase):

    def test_short_message_unchanged(self):
        """
        Test that a short one-line message is returned as it is
        """
        e = ParseError('Not date data')
        self.assertEqual(e.short_message, 'Not date data')
        self.assertEqual(str(e), 'Not date data')

    def test_short_message_exactly_500(self):
        """
        Test that a 500 character message is not cut
        """
        msg = 'x' * 500
        self.assertEqual(ParseError(msg).short_message, msg)

    def test_short_message_long(self):
        """
        Test that a message longer than 500 characters is cut to 500 and str() keeps it whole
        """
        msg = 'Unable to parse line: ' + 'a' * 1000
        e = ParseError(msg)
        self.assertEqual(e.short_message, msg[:500] + '...')
        self.assertEqual(str(e), msg)

    def test_short_message_multiline(self):
        """
        Test that only the first line of a multi-line message is kept
        """
        msg = 'Unable to parse date: line one\nline two\nline three'
        e = ParseError(msg)
        self.assertEqual(e.short_message, 'Unable to parse date: line one ...')
        self.assertEqual(str(e), msg)

    def test_short_message_crlf(self):
        """
        Test that a CRLF line ending does not leave a CR in the first line
        """
        self.assertEqual(ParseError('first\r\nsecond').short_message, 'first ...')

    def test_short_message_leading_newline(self):
        """
        Test that a message starting with a newline uses the first line with text
        """
        self.assertEqual(ParseError('\nNot date data').short_message, 'Not date data')

    def test_short_message_long_multiline(self):
        """
        Test that a long first line of a multi-line message is cut to 500 characters
        """
        e = ParseError('b' * 800 + '\nsecond')
        self.assertEqual(e.short_message, 'b' * 500 + '...')

    def test_short_message_no_args(self):
        """
        Test a ParseError raised without a message
        """
        self.assertEqual(ParseError().short_message, '')

    def test_short_message_args_unchanged(self):
        """
        Test that the exception args are not changed
        """
        e = ParseError('a\nb')
        _ = e.short_message
        self.assertEqual(e.args, ('a\nb',))

    def test_library_not_installed_has_no_short_message(self):
        """
        Test that LibraryNotInstalled is unchanged (the CLI falls back to str(e))
        """
        self.assertFalse(hasattr(LibraryNotInstalled('x'), 'short_message'))


if __name__ == '__main__':
    unittest.main()
