import unittest
import json
import jc.parsers.timestamp


class MyTests(unittest.TestCase):

    def test_timestamp_nodata(self):
        """
        Test 'timestamp' with no data
        """
        self.assertEqual(jc.parsers.timestamp.parse('', quiet=True), {})

    def test_10_digit_timestamp(self):
        """
        Test 10 digit timestamp string
        """
        data = r'1658599410'
        expected = json.loads(r"""{"naive":{"year":2022,"month":"Jul","month_num":7,"day":23,"weekday":"Sat","weekday_num":6,"hour":11,"hour_24":11,"minute":3,"second":30,"period":"AM","day_of_year":204,"week_of_year":29,"iso":"2022-07-23T11:03:30"},"utc":{"year":2022,"month":"Jul","month_num":7,"day":23,"weekday":"Sat","weekday_num":6,"hour":6,"hour_24":18,"minute":3,"second":30,"period":"PM","utc_offset":"+0000","day_of_year":204,"week_of_year":29,"iso":"2022-07-23T18:03:30+00:00"}}""")
        self.assertEqual(jc.parsers.timestamp.parse(data, quiet=True), expected)

    def test_13_digit_timestamp(self):
        """
        Test 13 digit timestamp string (with milliseconds)
        """
        data = r'1658604427154'
        expected = json.loads(r"""{"naive":{"year":2022,"month":"Jul","month_num":7,"day":23,"weekday":"Sat","weekday_num":6,"hour":12,"hour_24":12,"minute":27,"second":7,"period":"PM","day_of_year":204,"week_of_year":29,"iso":"2022-07-23T12:27:07"},"utc":{"year":2022,"month":"Jul","month_num":7,"day":23,"weekday":"Sat","weekday_num":6,"hour":7,"hour_24":19,"minute":27,"second":7,"period":"PM","utc_offset":"+0000","day_of_year":204,"week_of_year":29,"iso":"2022-07-23T19:27:07+00:00"}}""")
        self.assertEqual(jc.parsers.timestamp.parse(data, quiet=True), expected)


if __name__ == '__main__':
    unittest.main()
