import unittest
import jc.utils


class MyTests(unittest.TestCase):
    def test_utils_parse_datetime_to_timestamp(self):

        # naive timestamps created in PDT
        datetime_map = {
            # C locale format conversion, or date cli command in C locale with non-UTC tz
            'Tue Mar 23 16:12:11 2021': {'format': 1000, 'timestamp_naive': 1616541131, 'timestamp_utc': None},
            'Tue Mar 23 16:12:11 IST 2021': {'format': 1000, 'timestamp_naive': 1616541131, 'timestamp_utc': None},
            # en_US.UTF-8 local format (found in upower cli output)
            'Tue 23 Mar 2021 04:12:11 PM UTC': {'format': 2000, 'timestamp_naive': 1616541131, 'timestamp_utc': 1616515931},
            # en_US.UTF-8 local format with non-UTC tz (found in upower cli output)
            'Tue 23 Mar 2021 04:12:11 PM IST': {'format': 3000, 'timestamp_naive': 1616541131, 'timestamp_utc': None},
            # European local format (found in upower cli output)
            'Tuesday 01 October 2019 12:50:41 PM UTC': {'format': 4000, 'timestamp_naive': 1569959441, 'timestamp_utc': 1569934241},
            # European local format with non-UTC tz (found in upower cli output)
            'Tuesday 01 October 2019 12:50:41 PM IST': {'format': 5000, 'timestamp_naive': 1569959441, 'timestamp_utc': None},
            # date cli command in en_US.UTF-8 format
            'Wed Mar 24 06:16:19 PM UTC 2021': {'format': 6000, 'timestamp_naive': 1616634979, 'timestamp_utc': 1616609779},
            # date cli command in C locale format
            'Wed Mar 24 11:11:30 UTC 2021': {'format': 7000, 'timestamp_naive': 1616609490, 'timestamp_utc': 1616584290},
            # C locale format (found in stat cli output - OSX)
            'Mar 29 11:49:05 2021': {'format': 7100, 'timestamp_naive': 1617043745, 'timestamp_utc': None},
            # C local format (found in stat cli output - linux) non-UTC tz
            '2019-08-13 18:13:43.555604315 -0400': {'format': 7200, 'timestamp_naive': 1565745223, 'timestamp_utc': None},
            # C local format (found in stat cli output - linux) UTC
            '2019-08-13 18:13:43.555604315 -0000': {'format': 7200, 'timestamp_naive': 1565745223, 'timestamp_utc': 1565720023}
        }

        for input_string, expected_output in datetime_map.items():
            self.assertEqual(jc.utils.parse_datetime_to_timestamp(input_string), expected_output)
