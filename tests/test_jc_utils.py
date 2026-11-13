import sys
import io
import os
import contextlib
import locale
import unittest
from unittest import mock
import jc.utils
from jc.exceptions import ParseError


class MyTests(unittest.TestCase):

    def test_utils_timestamp(self):
        """
        Test timestamp conversion of known date formats
        """
        # naive timestamps created in PDT
        datetime_map = {
            # C locale format conversion, or date cli command in C locale with non-UTC tz
            'Tue Mar 23 16:12:11 2021': {'string': 'Tue Mar 23 16:12:11 2021', 'format': 1000, 'naive': 1616541131, 'utc': None},
            'Tue Mar 23 16:12:11 IST 2021': {'string': 'Tue Mar 23 16:12:11 IST 2021', 'format': 1000, 'naive': 1616541131, 'utc': None},
            # date cli command in a locale that prints a 12-hour clock (#748).
            # The tz abbreviation is stripped before any format is tried, so these
            # reach strptime as 'Thu Sep 10 11:10:44 AM 2026' and need the 12-hour
            # twin of 1000. PM is asserted too: without %p the hour is read as 11.
            'Thu Sep 10 11:10:44 AM EEST 2026': {'string': 'Thu Sep 10 11:10:44 AM EEST 2026', 'format': 1200, 'naive': 1789063844, 'utc': None},
            'Thu Sep 10 11:10:44 PM EEST 2026': {'string': 'Thu Sep 10 11:10:44 PM EEST 2026', 'format': 1200, 'naive': 1789107044, 'utc': None},
            'Thu Sep 10 11:10:44 AM 2026': {'string': 'Thu Sep 10 11:10:44 AM 2026', 'format': 1200, 'naive': 1789063844, 'utc': None},
            # Git date output
            'Thu Mar 5 09:17:40 2020 -0800': {'string': 'Thu Mar 5 09:17:40 2020 -0800', 'format': 1100, 'naive': 1583428660, 'utc': None},
            # ISO Format with UTC (found in syslog 5424)
            '2003-10-11T22:14:15.003Z': {'string': '2003-10-11T22:14:15.003Z', 'format': 1300, 'naive': 1065935655, 'utc': 1065910455},
            # ISO Format without TZ (found in syslog 5424)
            '2003-10-11T22:14:15.003': {'string': '2003-10-11T22:14:15.003', 'format': 1310, 'naive': 1065935655, 'utc': None},
            # CEF Format with UTC
            'Nov 08 2022 12:30:00.111 UTC': {'string': 'Nov 08 2022 12:30:00.111 UTC', 'format': 1400, 'naive': 1667939400, 'utc': 1667910600},
            # CEF Format without TZ
            'Nov 08 2022 12:30:00.111': {'string': 'Nov 08 2022 12:30:00.111', 'format': 1410, 'naive': 1667939400, 'utc': None},
            # CEF Format with UTC without microseconds
            'Nov 08 2022 12:30:00 UTC': {'string': 'Nov 08 2022 12:30:00 UTC', 'format': 1420, 'naive': 1667939400, 'utc': 1667910600},
            # CEF Format without TZ or microseconds
            'Nov 08 2022 12:30:00': {'string': 'Nov 08 2022 12:30:00', 'format': 1430, 'naive': 1667939400, 'utc': None},
            # en_US.UTF-8 local format (found in who cli output)
            '2021-03-23 00:14': {'string': '2021-03-23 00:14', 'format': 1500, 'naive': 1616483640, 'utc': None},
            # Windows english format (found in dir cli output)
            '12/07/2019 02:09 AM': {'string': '12/07/2019 02:09 AM', 'format': 1600, 'naive': 1575713340, 'utc': None},
            # Windows english format wint non-UTC tz (found in systeminfo cli output)
            '3/22/2021, 1:15:51 PM (UTC-0600)': {'string': '3/22/2021, 1:15:51 PM (UTC-0600)', 'format': 1700, 'naive': 1616444151, 'utc': None},
            # Windows english format with UTC tz (found in systeminfo cli output)
            '3/22/2021, 1:15:51 PM (UTC)': {'string': '3/22/2021, 1:15:51 PM (UTC)', 'format': 1705, 'naive': 1616444151, 'utc': 1616418951},
            # Windows english format with UTC tz in long-form (found in systeminfo cli output)
            '3/22/2021, 1:15:51 PM (Coordinated Universal Time)': {'string': '3/22/2021, 1:15:51 PM (Coordinated Universal Time)', 'format': 1705, 'naive': 1616444151, 'utc': 1616418951},
            # Windows english format with UTC tz (found in systeminfo cli output)
            '3/22/2021, 1:15:51 PM (UTC+0000)': {'string': '3/22/2021, 1:15:51 PM (UTC+0000)', 'format': 1710, 'naive': 1616444151, 'utc': 1616418951},
            # Windows ipconfig cli output format
            'Thursday, June 22, 2023 10:39:04 AM': {'string': 'Thursday, June 22, 2023 10:39:04 AM', 'format': 1720, 'naive': 1687455544, 'utc': None},
            # Google Big Table format with no timezone:
            '2000/01/01-01:00:00.000000': {'string': '2000/01/01-01:00:00.000000', 'format': 1750, 'naive': 946717200, 'utc': None},
            # Google Big Table format with timezone:
            '2000/01/01-01:00:00.000000+00:00': {'string': '2000/01/01-01:00:00.000000+00:00', 'format': 1755, 'naive': 946717200, 'utc': 946688400},
            # certbot format with timezone:
            '2023-05-11 01:33:10+00:00': {'string': '2023-05-11 01:33:10+00:00', 'format': 1760, 'naive': 1683793990, 'utc': 1683768790},
            # Common Log Format
            '10/Oct/2000:13:55:36 -0700': {'string': '10/Oct/2000:13:55:36 -0700', 'format': 1800, 'naive': 971211336, 'utc': None},
            '10/Oct/2000:13:55:36 -0000': {'string': '10/Oct/2000:13:55:36 -0000', 'format': 1800, 'naive': 971211336, 'utc': 971186136},
            # en_US.UTF-8 local format (found in upower cli output)
            'Tue 23 Mar 2021 04:12:11 PM UTC': {'string': 'Tue 23 Mar 2021 04:12:11 PM UTC', 'format': 2000, 'naive': 1616541131, 'utc': 1616515931},
            # en_US.UTF-8 local format with non-UTC tz (found in upower cli output)
            'Tue 23 Mar 2021 04:12:11 PM IST': {'string': 'Tue 23 Mar 2021 04:12:11 PM IST', 'format': 3000, 'naive': 1616541131, 'utc': None},
            # HTTP header time format (always GMT so assume UTC)
            'Wed, 31 Jan 2024 00:39:28 GMT': {'string': 'Wed, 31 Jan 2024 00:39:28 GMT', 'format': 3500, 'naive': 1706690368, 'utc': 1706661568},
            # European local format (found in upower cli output)
            'Tuesday 01 October 2019 12:50:41 PM UTC': {'string': 'Tuesday 01 October 2019 12:50:41 PM UTC', 'format': 4000, 'naive': 1569959441, 'utc': 1569934241},
            # European local format with non-UTC tz (found in upower cli output)
            'Tuesday 01 October 2019 12:50:41 PM IST': {'string': 'Tuesday 01 October 2019 12:50:41 PM IST', 'format': 5000, 'naive': 1569959441, 'utc': None},
            # date cli command in en_US.UTF-8 format
            'Wed Mar 24 06:16:19 PM UTC 2021': {'string': 'Wed Mar 24 06:16:19 PM UTC 2021', 'format': 6000, 'naive': 1616634979, 'utc': 1616609779},
            # date cli command in C locale format
            'Wed Mar 24 11:11:30 UTC 2021': {'string': 'Wed Mar 24 11:11:30 UTC 2021', 'format': 7000, 'naive': 1616609490, 'utc': 1616584290},
            # C locale format (found in stat cli output - OSX)
            'Mar 29 11:49:05 2021': {'string': 'Mar 29 11:49:05 2021', 'format': 7100, 'naive': 1617043745, 'utc': None},
            # C local format (found in stat cli output - linux) non-UTC tz
            '2019-08-13 18:13:43.555604315 -0400': {'string': '2019-08-13 18:13:43.555604315 -0400', 'format': 7200, 'naive': 1565745223, 'utc': None},
            # C local format (found in stat cli output - linux) UTC
            '2019-08-13 18:13:43.555604315 -0000': {'string': '2019-08-13 18:13:43.555604315 -0000', 'format': 7200, 'naive': 1565745223, 'utc': 1565720023},
            # C locale format with non-UTC tz (found in modified vmstat cli output)
            '2021-09-16 20:32:28 PDT': {'string': '2021-09-16 20:32:28 PDT', 'format': 7250, 'naive': 1631849548, 'utc': None},
            # C locale format (found in modified vmstat cli output)
            '2021-09-16 20:32:28 UTC': {'string': '2021-09-16 20:32:28 UTC', 'format': 7255, 'naive': 1631849548, 'utc': 1631824348},
            # C locale format (found in timedatectl cli output)
            'Wed 2020-03-11 00:53:21 UTC': {'string': 'Wed 2020-03-11 00:53:21 UTC', 'format': 7300, 'naive': 1583913201, 'utc': 1583888001},
            # test with None input
            None: {'string': None, 'format': None, 'naive': None, 'utc': None}
        }

        # fixup for change in behavior after python 3.6:
        # Changed in version 3.7: When the %z directive is provided to the strptime() method,
        # the UTC offsets can have a colon as a separator between hours, minutes and seconds.
        # For example, '+01:00:00' will be parsed as an offset of one hour. In addition,
        # providing 'Z' is identical to '+00:00'.
        if sys.version_info < (3, 7, 0):
            del datetime_map['2000/01/01-01:00:00.000000+00:00']

        for input_string, expected_output in datetime_map.items():
            ts = jc.utils.timestamp(input_string)
            ts_dict = {
                'string': ts.string,
                'format': ts.format,
                'naive': ts.naive,
                'utc': ts.utc
            }

            try:
                self.assertEqual(ts_dict, expected_output)
            except AssertionError:
                # fixup for behavior change in python 3.15
                format_changes = {7250: 1760}
                if sys.version_info >= (3, 15, 0) and expected_output['format'] in format_changes:
                    expected_output['format'] = format_changes[expected_output['format']]
                    self.assertEqual(ts_dict, expected_output)
                else:
                    raise

    def test_utils_convert_to_int(self):
        """
        Test converting values to integers
        """
        io_map = {
            None: None,
            True: 1,
            False: 0,
            '': None,
            '0': 0,
            '1': 1,
            '-1': -1,
            '0.0': 0,
            '0.1': 0,
            '0.6': 0,
            '-0.1': 0,
            '-0.6': 0,
            0: 0,
            1: 1,
            -1: -1,
            0.0: 0,
            0.1: 0,
            0.6: 0,
            -0.1: 0,
            -0.6: 0
        }

        for input_string, expected_output in io_map.items():
            self.assertEqual(jc.utils.convert_to_int(input_string), expected_output)

    def test_utils_convert_to_float(self):
        """
        Test converting values to floats
        """
        io_map = {
            None: None,
            True: 1.0,
            False: 0.0,
            '': None,
            '0': 0.0,
            '1': 1.0,
            '-1': -1.0,
            '0.0': 0.0,
            '0.1': 0.1,
            '0.6': 0.6,
            '-0.1': -0.1,
            '-0.6': -0.6,
            0: 0.0,
            1: 1.0,
            -1: -1.0,
            0.0: 0.0,
            0.1: 0.1,
            0.6: 0.6,
            -0.1: -0.1,
            -0.6: -0.6
        }

        for input_string, expected_output in io_map.items():
            self.assertEqual(jc.utils.convert_to_float(input_string), expected_output)

    def test_utils_convert_to_int_non_finite(self):
        """
        Test converting inf, nan and very long digit strings to integers
        """
        self.assertIsNone(jc.utils.convert_to_int(float('inf')))
        self.assertIsNone(jc.utils.convert_to_int(float('-inf')))
        self.assertIsNone(jc.utils.convert_to_int(float('nan')))
        self.assertEqual(jc.utils.convert_to_int('9' * 400), 10**400 - 1)
        # above the int() digit limit of Python 3.11+ this used to raise
        # OverflowError. Older Pythons have no limit and return the number.
        self.assertIn(jc.utils.convert_to_int('9' * 5000), (None, 10**5000 - 1))

    def test_utils_convert_to_float_non_finite(self):
        """
        Test converting inf, nan and numbers too large for a float to floats
        """
        self.assertIsNone(jc.utils.convert_to_float(float('inf')))
        self.assertIsNone(jc.utils.convert_to_float(float('-inf')))
        self.assertIsNone(jc.utils.convert_to_float(float('nan')))
        self.assertIsNone(jc.utils.convert_to_float(10**400))
        self.assertIsNone(jc.utils.convert_to_float('9' * 310))
        self.assertIsNone(jc.utils.convert_to_float('-' + '9' * 310))
        self.assertEqual(jc.utils.convert_to_float('9' * 300), float('9' * 300))
        self.assertTrue(jc.utils.convert_to_bool('9' * 310))

    def test_utils_convert_to_bool(self):
        """
        Test converting values to booleans
        """
        io_map = {
            None: False,
            True: True,
            False: False,
            '': False,
            '0': False,
            '1': True,
            '-1': True,
            '0.0': False,
            '0.1': True,
            '-0.1': True,
            '*': True,
            'true': True,
            'True': True,
            'false': False,
            'False': False,
            'Y': True,
            'y': True,
            'Yes': True,
            'n': False,
            'N': False,
            'No': False,
            0: False,
            1: True,
            -1: True,
            0.0: False,
            0.1: True,
            -0.1: True,
        }

        for input_string, expected_output in io_map.items():
            self.assertEqual(jc.utils.convert_to_bool(input_string), expected_output)


    def test_utils_convert_size_to_int(self):
        """
        Test converting size strings to integers
        """
        io_map = {
            '42': 42,
            '13b': 13,
            '5 bytes': 5,
            '1 KB': 1000,
            '1 kilobyte': 1000,
            '1 KiB': 1024,
            '1.5 GB': 1500000000
        }

        for input_string, expected_output in io_map.items():
            self.assertEqual(jc.utils.convert_size_to_int(input_string), expected_output)


    def test_utils_convert_size_to_int_binary_true(self):
        """
        Test converting size strings to integers with binary units
        """
        io_map = {
            '1 KB': 1024,
            '1.5 GB': 1610612736
        }

        for input_string, expected_output in io_map.items():
            self.assertEqual(jc.utils.convert_size_to_int(input_string, binary=True), expected_output)


    def test_utils_convert_size_to_int_posix_mode(self):
        """
        Test converting size strings to integers in POSIX mode
        """
        io_map = {
            '1 K': 1024,
            '1 KiB': 1024,
            '1 KB': 1000,
            '1.5 G': 1610612736,
            '1.5 GiB': 1610612736,
            '1.5 GB': 1500000000
        }

        for input_string, expected_output in io_map.items():
            self.assertEqual(jc.utils.convert_size_to_int(input_string, posix_mode=True), expected_output)


    def test_utils_convert_size_to_int_decimal_bias(self):
        """
        Test converting size strings to integers with decimal bias
        """
        io_map = {
            '1 K': 1000,
            '1 Ki': 1000,
            '1 KiB': 1024,
            '1.5 G': 1500000000,
            '1.5 Gi': 1500000000,
            '1.5 GiB': 1610612736
        }

        for input_string, expected_output in io_map.items():
            self.assertEqual(jc.utils.convert_size_to_int(input_string, decimal_bias=True), expected_output)


    def test_utils_timestamp_non_date_strings(self):
        """
        Test 'timestamp' with strings that have no digits or are very long
        """
        no_match = (None, None, None, None)
        before = jc.utils.timestamp._parse_dt.cache_info().currsize

        for input_string in ('hello world', 'never', 'n/a', 'x' * 20000, 'ab1 ' * 5000):
            ts = jc.utils.timestamp(input_string)
            self.assertEqual((ts.format, ts.naive, ts.utc, ts.iso), no_match)
            self.assertEqual(ts.string, input_string)

        self.assertEqual(jc.utils.timestamp._parse_dt.cache_info().currsize, before)

    def test_utils_timestamp_long_strings_that_normalize_short(self):
        """
        Test 'timestamp' with long strings that are short after normalization
        """
        ts = jc.utils.timestamp('Wed Mar 24 11:11:30 ' + 'EST ' * 40 + '2021')
        self.assertEqual((ts.format, ts.iso), (1000, '2021-03-24T11:11:30'))

        ts = jc.utils.timestamp('2019-08-13 18:13:43.555604315' + '1' * 200 + ' -0400')
        self.assertEqual((ts.format, ts.iso), (7200, '2019-08-13T18:13:43.555604'))

        ts = jc.utils.timestamp('2021-03-23' + ' ' * 200 + '00:14')
        self.assertEqual((ts.format, ts.iso), (1500, '2021-03-23T00:14:00'))

    def test_utils_timestamp_does_not_change_locale(self):
        """
        Test that timestamp conversion restores the original LC_TIME locale
        """
        # jc.utils.timestamp sets LC_TIME while trying date formats. It should
        # always restore the original LC_TIME, on both success and failure.
        original = locale.setlocale(locale.LC_TIME)

        try:
            # find a locale that differs from the environment locale, since
            # some timestamp formats use the environment locale ('')
            environment = locale.setlocale(locale.LC_TIME, '')
            test_locale = None

            for candidate in ('C', 'en_US.utf8', 'de_DE.utf8', 'fr_FR.utf8'):
                if candidate == environment:
                    continue
                try:
                    test_locale = locale.setlocale(locale.LC_TIME, candidate)
                    break
                except locale.Error:
                    continue

            if test_locale is None:
                self.skipTest('no alternate LC_TIME locale available for testing')

            # failed parse
            jc.utils.timestamp('not a parsable timestamp at all', format_hint=(1000,))
            self.assertEqual(locale.setlocale(locale.LC_TIME), test_locale)

            # successful parse
            self.assertIsNotNone(jc.utils.timestamp('Tue Mar 23 16:12:11 2021', format_hint=(1000,)).naive)
            self.assertEqual(locale.setlocale(locale.LC_TIME), test_locale)

        finally:
            locale.setlocale(locale.LC_TIME, original)


    def test_utils_has_data_nodata(self):
        """
        Test has_data with only whitespace
        """
        self.assertFalse(jc.utils.has_data('     \n      '))


    def test_utils_has_data_withdata(self):
        """
        Test has_data with data
        """
        self.assertTrue(jc.utils.has_data('     \n  abcd    \n    '))


    def test_utils_input_type_check_wrong(self):
        """
        Test that input_type_check raises TypeError for input that is not a string
        """
        self.assertRaises(TypeError, jc.utils.input_type_check, ['abc'])


    def test_utils_input_type_check_correct(self):
        """
        Test input_type_check with a string
        """
        self.assertEqual(jc.utils.input_type_check('abc'), None)


    def test_utils_splitlines(self):
        """
        Test that splitlines splits only on LF and CRLF
        """
        data = 'line1\nline2\r\nline3\u2028still line3\rstill line3\x0cstill line3\n'
        expected = ['line1', 'line2', 'line3\u2028still line3\rstill line3\x0cstill line3']
        self.assertEqual(jc.utils.splitlines(data), expected)


    def test_utils_splitlines_keepends(self):
        """
        Test splitlines with keepends
        """
        data = 'line1\nline2\r\nline3\u2028still line3'
        expected = ['line1\n', 'line2\r\n', 'line3\u2028still line3']
        self.assertEqual(jc.utils.splitlines(data, keepends=True), expected)


    def test_utils_splitlines_other_separators_stay_in_line(self):
        """
        Test that splitlines keeps other line-break characters in the line
        """
        for sep in ('\x0b', '\x0c', '\x1c', '\x1d', '\x1e', '\x85', '\u2028', '\u2029'):
            data = 'a' + sep + 'b\nc\n'
            self.assertEqual(jc.utils.splitlines(data), ['a' + sep + 'b', 'c'])
            self.assertEqual(jc.utils.splitlines(data, split_cr=True), ['a' + sep + 'b', 'c'])


    def test_utils_splitlines_same_as_str_splitlines(self):
        """
        Test that splitlines matches str.splitlines() for input with only LF and CRLF line endings
        """
        for data in ('', '\n', 'a', 'a\n', 'a\n\nb', 'a\r\n\r\nb\r\n', '\n\na\n\n'):
            for keepends in (False, True):
                self.assertEqual(jc.utils.splitlines(data, keepends=keepends), data.splitlines(keepends))
                self.assertEqual(jc.utils.splitlines(data, keepends=keepends, split_cr=True), data.splitlines(keepends))


    def test_utils_splitlines_split_cr(self):
        """
        Test splitlines with split_cr, which also splits on a lone CR
        """
        data = 'line1\rline2\r\nline3\nline4\u2028still line4\x0cstill line4\r'
        expected = ['line1', 'line2', 'line3', 'line4\u2028still line4\x0cstill line4']
        self.assertEqual(jc.utils.splitlines(data, split_cr=True), expected)


    def test_utils_splitlines_split_cr_keepends(self):
        """
        Test splitlines with split_cr and keepends
        """
        data = 'line1\rline2\r\nline3\nline4\u2028still line4'
        expected = ['line1\r', 'line2\r\n', 'line3\n', 'line4\u2028still line4']
        self.assertEqual(jc.utils.splitlines(data, keepends=True, split_cr=True), expected)


    def test_utils_splitlines_split_cr_blank_lines(self):
        """
        Test splitlines with split_cr and blank lines
        """
        data = 'a\r\rb\r\n\r\nc\r'
        self.assertEqual(jc.utils.splitlines(data, split_cr=True), ['a', '', 'b', '', 'c'])


    def test_utils_line_slice_string_positive_slice(self):
        """
        Test line_slice of a string with a positive start and end
        """
        data = '''line1
line2
line3
line4
'''
        expected = 'line2\nline3'
        self.assertEqual(jc.utils.line_slice(data, 1, 3), expected)


    def test_utils_line_slice_string_negative_slice(self):
        """
        Test line_slice of a string with a negative end
        """
        data = '''line1
line2
line3
line4
'''
        expected = 'line2\nline3'
        self.assertEqual(jc.utils.line_slice(data, 1, -1), expected)


    def test_utils_line_slice_iter_positive_slice(self):
        """
        Test line_slice of an iterable with a positive start and end
        """
        data = [
            'line1',
            'line2',
            'line3',
            'line4'
        ]
        expected = ['line2', 'line3']
        self.assertEqual(list(jc.utils.line_slice(data, 1, 3)), expected)


    def test_utils_line_slice_iter_negative_slice(self):
        """
        Test line_slice of an iterable with a negative end
        """
        data = [
            'line1',
            'line2',
            'line3',
            'line4'
        ]
        expected = ['line2', 'line3']
        self.assertEqual(list(jc.utils.line_slice(data, 1, -1)), expected)

    def test_utils_line_slice_string_blank_lines(self):
        """
        Test line_slice of a string with blank lines
        """
        data = '''line1
line2

line4
line5
'''
        expected = 'line2\n\nline4'
        self.assertEqual(jc.utils.line_slice(data, 1, 4), expected)

    def test_utils_line_slice_iter_positive_blank_lines(self):
        """
        Test line_slice of an iterable with blank lines
        """
        data = [
            'line1',
            'line2',
            '',
            'line4',
            'line5'
        ]
        expected = ['line2', '', 'line4']
        self.assertEqual(list(jc.utils.line_slice(data, 1, 4)), expected)

    def test_utils_line_slice_string_lone_cr(self):
        """
        Test that line_slice of a string counts lines at LF and CRLF only
        """
        data = 'a\rb\nc\r\nd\ne'
        self.assertEqual(jc.utils.line_slice(data, 1, 3), 'c\nd')
        self.assertEqual(jc.utils.line_slice(data, 0, 2), 'a\rb\nc')
        self.assertEqual(jc.utils.line_slice(data, -2, None), 'd\ne')

    def test_remove_quotes(self):
        """
        Test removing single and double quotes around a string
        """
        for char in ["'", '"']:
            with self.subTest(f'Quote character: {char}'):
                data = f'{char}this is a test{char}'
                expected = 'this is a test'
                self.assertEqual(jc.utils.remove_quotes(data), expected)

    def test_normalize_key(self):
        """
        Test normalizing key names
        """
        io_map = {
            'This is @ crazy  Key!!': 'this_is_crazy_key',
            'Simple': 'simple',
            'CamelCase': 'camelcase',
            '^Complex-Key*': '_complex_key'
        }

        for data, expected in io_map.items():
            with self.subTest(f'Original key: {data}'):
                self.assertEqual(jc.utils.normalize_key(data), expected)


    # need to mock shutil.get_terminal_size().columns or add a column parameter to test
    def test_utils_expansion_limit(self):
        """
        Test the output size limit for an input size
        """
        self.assertEqual(jc.utils.expansion_limit(0), 50000000)
        self.assertEqual(jc.utils.expansion_limit(1000), 51000000)

    def test_utils_expansion_check_small(self):
        """
        Test expansion_check with small data
        """
        data = {'a': [1, 2.5, None, True, False, 'x' * 100], 'b': {'c': 'd'}, 'e': []}
        self.assertIsNone(jc.utils.expansion_check(data, 0))
        self.assertIsNone(jc.utils.expansion_check('x' * 1000, 0))
        self.assertIsNone(jc.utils.expansion_check([], 0))

    def test_utils_expansion_check_shared_references(self):
        """
        Test that expansion_check counts a shared object once per reference
        """
        # one 1 MB list referenced many times is counted once per reference
        shared = ['x' * 998] * 1000      # 1,001,001 characters of JSON
        self.assertIsNone(jc.utils.expansion_check([shared] * 40, 100))
        self.assertRaises(ParseError, jc.utils.expansion_check, [shared] * 60, 100)
        self.assertRaises(ParseError, jc.utils.expansion_check, {'a': [shared] * 60}, 100)

    def test_utils_expansion_check_nested_references(self):
        """
        Test expansion_check with nested shared references
        """
        node = ['x']
        for _ in range(30):
            node = [node, node]
        self.assertRaises(ParseError, jc.utils.expansion_check, node, 1000)

    def test_utils_expansion_check_boundary(self):
        """
        Test expansion_check at the size limit
        """
        # each item of `shared` is '"' + 998 x's + '"' plus a separator
        shared = ['x' * 998] * 1000
        shared_size = 2 + 1000 * 1000 + 999
        items = 50
        input_size = 100
        limit = jc.utils.expansion_limit(input_size)
        # [shared, shared, ..., "ppp...p"]
        base_size = 2 + items * shared_size + items + 2
        pad = 'p' * (limit - base_size)
        data = [shared] * items + [pad]
        self.assertIsNone(jc.utils.expansion_check(data, input_size))
        data = [shared] * items + [pad + 'p']
        self.assertRaises(ParseError, jc.utils.expansion_check, data, input_size)

    def test_utils_expansion_check_circular(self):
        """
        Test expansion_check with a circular reference
        """
        data = [1, 2]
        data.append(data)
        self.assertIsNone(jc.utils.expansion_check(data, 0))

    def test_utils_xml_defaults_check(self):
        """
        Test xml_defaults_check with documents under the limit
        """
        doc = '<!DOCTYPE a [<!ATTLIST b x CDATA "1" y CDATA #IMPLIED>]><a>' + '<b/>' * 100 + '</a>'
        self.assertIsNone(jc.utils.xml_defaults_check(doc))
        self.assertIsNone(jc.utils.xml_defaults_check(doc.encode()))
        self.assertIsNone(jc.utils.xml_defaults_check('<a><b x="1"/></a>'))
        self.assertIsNone(jc.utils.xml_defaults_check('<!DOCTYPE a [<!ATTLIST b x CDATA "1">]><a><b>'))

    def test_utils_xml_defaults_check_limit(self):
        """
        Test that xml_defaults_check raises ParseError when attribute defaults exceed the limit
        """
        doc = '<!DOCTYPE a [<!ATTLIST b x CDATA "' + 'v' * 100000 + '">]><a>' + '<b/>' * 2000 + '</a>'
        self.assertRaises(ParseError, jc.utils.xml_defaults_check, doc)
        self.assertRaises(ParseError, jc.utils.xml_defaults_check, doc.encode())
        # attributes given in the document are not defaulted
        doc = '<!DOCTYPE a [<!ATTLIST b x CDATA "' + 'v' * 100000 + '">]><a>' + '<b x=""/>' * 2000 + '</a>'
        self.assertIsNone(jc.utils.xml_defaults_check(doc))

    def _stderr_of(self, func, message_lines):
        f = io.StringIO()
        with mock.patch.dict(os.environ, {'COLUMNS': '80'}), \
             mock.patch.object(jc.utils, 'CLI_QUIET', False), \
             contextlib.redirect_stderr(f):
            func(message_lines)
        return f.getvalue()

    def test_utils_warning_message_control_chars(self):
        """
        Test that warning messages show control characters as escapes
        """
        msg = ['Unparsable line found: a\x1b]0;b\x07c\x1b[2Jd\x9be\x7ff\x00g\rh', 'x\x85y']
        expected = ('jc:  Warning - Unparsable line found: a\\x1b]0;b\\x07c\\x1b[2Jd\\x9be\\x7ff\\x00g\\x0dh\n'
                    '               x\\x85y\n')
        self.assertEqual(expected, self._stderr_of(jc.utils.warning_message, msg))

    def test_utils_error_message_control_chars(self):
        """
        Test that error messages show control characters as escapes
        """
        msg = ['Parser issue with swapon:', 'ParseError: bad line \x1b[1;31mred\x1b[0m']
        expected = ('jc:  Error - Parser issue with swapon:\n'
                    '             ParseError: bad line \\x1b[1;31mred\\x1b[0m\n')
        self.assertEqual(expected, self._stderr_of(jc.utils.error_message, msg))

    def test_utils_warning_message_printable_unchanged(self):
        """
        Test that warning messages keep tabs, newlines and printable characters
        """
        msg = ['tab\there caf\u00e9 \u2603 \u00a0 \u4e2d\u6587', 'new\nline']
        expected = ('jc:  Warning - tab      here caf\u00e9 \u2603 \u00a0 \u4e2d\u6587\n'
                    '               new line\n')
        self.assertEqual(expected, self._stderr_of(jc.utils.warning_message, msg))

    def test_utils_warning_message_long_line_shortened(self):
        """
        Test that warning messages shorten very long lines
        """
        word = 'a@' + 'b' * 1000000
        out = self._stderr_of(jc.utils.warning_message, ['Invalid email address found: ' + word])
        self.assertTrue(out.startswith('jc:  Warning - Invalid email address found: a@bbb'))
        self.assertTrue(' '.join(out.split()).endswith('... (1000031 characters)'))
        self.assertLess(len(out), 6000)

    def test_utils_unquote_git_path(self):
        """
        Test unquote_git_path with git C-quoted and unquoted paths
        """
        cases = {
            'plain/file.txt': 'plain/file.txt',
            '"d\\303\\251ploy.yml"': 'd\u00e9ploy.yml',
            '"a\\"b"': 'a"b',
            '"back\\\\slash"': 'back\\slash',
            '"tab\\there"': 'tab\there',
            '"new\\nline"': 'new\nline',
            '"\\a\\b\\f\\r\\v"': '\a\b\f\r\v',
            '"bad\\377.txt"': 'bad\\xff.txt',
            '"\\346\\227\\245.txt"': '\u65e5.txt',
            '"keep \u00e9\\t"': 'keep \u00e9\t',
            '"\\q"': '\\q',
            '""': '',
            '"': '"',
            '"unterminated': '"unterminated',
            'x => y': 'x => y',
            '"p q/d\\303\\251.txt" => p q/f.txt': 'p q/d\u00e9.txt => p q/f.txt',
            'a => "b\\"c"': 'a => b"c',
            '"a" => "b\\tc"': 'a => b\tc',
            '"a\\" => \\"b"': 'a" => "b'
        }

        for quoted, expected in cases.items():
            with self.subTest(quoted):
                self.assertEqual(jc.utils.unquote_git_path(quoted), expected)

    def test_utils_error_message_long_line_shortened(self):
        """
        Test that error messages shorten very long lines
        """
        out = self._stderr_of(jc.utils.error_message, ['first', 'x' * 100000])
        self.assertTrue(' '.join(out.split()).endswith('... (100000 characters)'))
        self.assertLess(len(out), 6000)

    def test_utils_warning_message_line_at_limit_unchanged(self):
        """
        Test that warning messages keep a line at the length limit
        """
        line = 'y' * jc.utils._MAX_MESSAGE_LINE_LENGTH
        out = self._stderr_of(jc.utils.warning_message, ['first', line])
        self.assertNotIn('...', out)
        self.assertEqual(len(line), out.count('y'))

    def test_utils_unescape_backslashes_octal(self):
        """
        Test unescape_backslashes decoding every octal escape like libmount
        """
        cases = {
            'plain/path': 'plain/path',
            '/mnt/my\\040disk': '/mnt/my disk',
            'rw,\\145xec,\\163uid': 'rw,exec,suid',
            'a\\011b\\012c\\134d': 'a\tb\nc\\d',
            'caf\\303\\251': 'café',
            'bad\\377': 'bad\\xff',
            'mask\\777': 'mask\\xff',
            'x\\\\040y': 'x\\ y',
            'short\\12': 'short\\12',
            'not\\089octal': 'not\\089octal',
            'end\\': 'end\\',
            'nul\\000kept': 'nul\x00kept',
            '\\040\\040': '  ',
            '\\041a\\042': '!a"'
        }

        for escaped, expected in cases.items():
            with self.subTest(escaped):
                self.assertEqual(jc.utils.unescape_backslashes(escaped), expected)

    def test_utils_unescape_backslashes_variants(self):
        """
        Test unescape_backslashes with a limited octal set and extra escapes
        """
        acl = (' \t\n\r', {'\\': '\\'})
        md5sum = ('', {'\\': '\\', 'n': '\n', 'r': '\r'})
        cases = [
            ('CORP\\\\domain\\040users', acl, 'CORP\\domain users'),
            ('\\\\040x', acl, '\\040x'),
            ('a\\\\\\\\b', acl, 'a\\\\b'),
            ('tab\\011name\\012', acl, 'tab\tname\n'),
            ('dash\\055kept', acl, 'dash\\055kept'),
            ('caf\\303\\251', acl, 'caf\\303\\251'),
            ('end\\', acl, 'end\\'),
            ('back\\\\slash', md5sum, 'back\\slash'),
            ('line\\nfeed\\r', md5sum, 'line\nfeed\r'),
            ('\\\\n', md5sum, '\\n'),
            ('octal\\040kept\\t', md5sum, 'octal\\040kept\\t')
        ]

        for escaped, (octal_chars, escapes), expected in cases:
            with self.subTest(escaped):
                self.assertEqual(
                    jc.utils.unescape_backslashes(escaped, octal_chars, escapes),
                    expected)

    # def test_utils_warning_message(self):
    #     msg = [
    #         'this is a long first line that will be wrapped yada yada yada yada yada yada yada.',
    #         'this is a second long line that will be wrapped yada yada yada yada yada yada yada yada yada.',
    #         'this is a third long line that will be wrapped yada yada yada yada yada yada yada yada yada.'
    #     ]

    #     expected = '''jc:  Warning - this is a long first line that will be wrapped yada yada yada
    #            yada yada yada yada.
    #            this is a second long line that will be wrapped yada yada yada
    #                yada yada yada yada yada yada.
    #            this is a third long line that will be wrapped yada yada yada
    #                yada yada yada yada yada yada.'''

    #     f = io.StringIO()
    #     with contextlib.redirect_stderr(f):
    #         jc.utils.warning_message(msg)

    #     self.assertEqual(f.getvalue(), expected + '\n')



if __name__ == '__main__':
    unittest.main()
