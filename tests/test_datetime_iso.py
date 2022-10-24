import unittest
import json
import jc.parsers.datetime_iso


class MyTests(unittest.TestCase):
    def test_datetime_iso_nodata(self):
        """
        Test 'datetime_iso' with no data
        """
        self.assertEqual(jc.parsers.datetime_iso.parse('', quiet=True), {})


    def test_datetime_iso_z(self):
        """
        Test ISO datetime string with Z timezone
        """
        data = r'2007-04-05T14:30Z'
        expected = json.loads(r'''{"year":2007,"month":"Apr","month_num":4,"day":5,"weekday":"Thu","weekday_num":4,"hour":2,"hour_24":14,"minute":30,"second":0,"microsecond":0,"period":"PM","utc_offset":"+0000","day_of_year":95,"week_of_year":14,"iso":"2007-04-05T14:30:00+00:00","timestamp":1175783400}''')
        self.assertEqual(jc.parsers.datetime_iso.parse(data, quiet=True), expected)


    def test_datetime_iso_microseconds(self):
        """
        Test ISO datetime string with Z timezone
        """
        data = r'2007-04-05T14:30.555Z'
        expected = json.loads(r'''{"year":2007,"month":"Apr","month_num":4,"day":5,"weekday":"Thu","weekday_num":4,"hour":2,"hour_24":14,"minute":0,"second":30,"microsecond":555000,"period":"PM","utc_offset":"+0000","day_of_year":95,"week_of_year":14,"iso":"2007-04-05T14:00:30.555000+00:00","timestamp":1175781630}''')
        self.assertEqual(jc.parsers.datetime_iso.parse(data, quiet=True), expected)


    def test_datetime_iso_plus_offset(self):
        """
        Test ISO datetime string with + offset
        """
        data = r'2007-04-05T14:30+03:30'
        expected = json.loads(r'''{"year":2007,"month":"Apr","month_num":4,"day":5,"weekday":"Thu","weekday_num":4,"hour":2,"hour_24":14,"minute":30,"second":0,"microsecond":0,"period":"PM","utc_offset":"+0330","day_of_year":95,"week_of_year":14,"iso":"2007-04-05T14:30:00+03:30","timestamp":1175770800}''')
        self.assertEqual(jc.parsers.datetime_iso.parse(data, quiet=True), expected)


    def test_datetime_iso_negative_offset(self):
        """
        Test ISO datetime string with - offset
        """
        data = r'2007-04-05T14:30-03:30'
        expected = json.loads(r'''{"year":2007,"month":"Apr","month_num":4,"day":5,"weekday":"Thu","weekday_num":4,"hour":2,"hour_24":14,"minute":30,"second":0,"microsecond":0,"period":"PM","utc_offset":"-0330","day_of_year":95,"week_of_year":14,"iso":"2007-04-05T14:30:00-03:30","timestamp":1175796000}''')
        self.assertEqual(jc.parsers.datetime_iso.parse(data, quiet=True), expected)


    def test_datetime_iso_nocolon_offset(self):
        """
        Test ISO datetime string with no colon offset
        """
        data = r'2007-04-05T14:30+0300'
        expected = json.loads(r'''{"year":2007,"month":"Apr","month_num":4,"day":5,"weekday":"Thu","weekday_num":4,"hour":2,"hour_24":14,"minute":30,"second":0,"microsecond":0,"period":"PM","utc_offset":"+0300","day_of_year":95,"week_of_year":14,"iso":"2007-04-05T14:30:00+03:00","timestamp":1175772600}''')
        self.assertEqual(jc.parsers.datetime_iso.parse(data, quiet=True), expected)


if __name__ == '__main__':
    unittest.main()
