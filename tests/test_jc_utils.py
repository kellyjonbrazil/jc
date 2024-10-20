import sys
import unittest
import jc.utils


class MyTests(unittest.TestCase):

    def test_utils_timestamp(self):
        # naive timestamps created in PDT
        datetime_map = {
            # C locale format conversion, or date cli command in C locale with non-UTC tz
            'Tue Mar 23 16:12:11 2021': {'string': 'Tue Mar 23 16:12:11 2021', 'format': 1000, 'naive': 1616541131, 'utc': None},
            'Tue Mar 23 16:12:11 IST 2021': {'string': 'Tue Mar 23 16:12:11 IST 2021', 'format': 1000, 'naive': 1616541131, 'utc': None},
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

            self.assertEqual(ts_dict, expected_output)

    def test_utils_convert_to_int(self):
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

    def test_utils_convert_to_bool(self):
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
        io_map = {
            '1 KB': 1024,
            '1.5 GB': 1610612736
        }

        for input_string, expected_output in io_map.items():
            self.assertEqual(jc.utils.convert_size_to_int(input_string, binary=True), expected_output)


    def test_utils_convert_size_to_int_posix_mode(self):
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


    def test_utils_has_data_nodata(self):
        self.assertFalse(jc.utils.has_data('     \n      '))


    def test_utils_has_data_withdata(self):
        self.assertTrue(jc.utils.has_data('     \n  abcd    \n    '))


    def test_utils_input_type_check_wrong(self):
        self.assertRaises(TypeError, jc.utils.input_type_check, ['abc'])


    def test_utils_input_type_check_correct(self):
        self.assertEqual(jc.utils.input_type_check('abc'), None)


    def test_utils_line_slice_string_positive_slice(self):
        data = '''line1
line2
line3
line4
'''
        expected = 'line2\nline3'
        self.assertEqual(jc.utils.line_slice(data, 1, 3), expected)


    def test_utils_line_slice_string_negative_slice(self):
        data = '''line1
line2
line3
line4
'''
        expected = 'line2\nline3'
        self.assertEqual(jc.utils.line_slice(data, 1, -1), expected)


    def test_utils_line_slice_iter_positive_slice(self):
        data = [
            'line1',
            'line2',
            'line3',
            'line4'
        ]
        expected = ['line2', 'line3']
        self.assertEqual(list(jc.utils.line_slice(data, 1, 3)), expected)


    def test_utils_line_slice_iter_negative_slice(self):
        data = [
            'line1',
            'line2',
            'line3',
            'line4'
        ]
        expected = ['line2', 'line3']
        self.assertEqual(list(jc.utils.line_slice(data, 1, -1)), expected)

    def test_utils_line_slice_string_blank_lines(self):
        data = '''line1
line2

line4
line5
'''
        expected = 'line2\n\nline4'
        self.assertEqual(jc.utils.line_slice(data, 1, 4), expected)

    def test_utils_line_slice_iter_positive_blank_lines(self):
        data = [
            'line1',
            'line2',
            '',
            'line4',
            'line5'
        ]
        expected = ['line2', '', 'line4']
        self.assertEqual(list(jc.utils.line_slice(data, 1, 4)), expected)

    def test_remove_quotes(self):
        for char in ["'", '"']:
            with self.subTest(f'Quote character: {char}'):
                data = f'{char}this is a test{char}'
                expected = 'this is a test'
                self.assertEqual(jc.utils.remove_quotes(data), expected)

    def test_normalize_key(self):
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
