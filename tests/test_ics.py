import contextlib
import io
import os
import unittest
import json
import jc.parsers.ics

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ics-test.ics'), 'r', encoding='utf-8') as f:
        generic_ics_test = f.read()

    # newline='' keeps the CRLF line endings of the fixture
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ics-crlf.ics'), 'r', encoding='utf-8', newline='') as f:
        generic_ics_crlf = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ics-google-shape.ics'), 'r', encoding='utf-8') as f:
        generic_ics_google = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ics-outlook-shape.ics'), 'r', encoding='utf-8') as f:
        generic_ics_outlook = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ics-test.json'), 'r', encoding='utf-8') as f:
        generic_ics_test_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ics-test-raw.json'), 'r', encoding='utf-8') as f:
        generic_ics_test_raw_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ics-crlf.json'), 'r', encoding='utf-8') as f:
        generic_ics_crlf_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ics-crlf-raw.json'), 'r', encoding='utf-8') as f:
        generic_ics_crlf_raw_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ics-google-shape.json'), 'r', encoding='utf-8') as f:
        generic_ics_google_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ics-outlook-shape.json'), 'r', encoding='utf-8') as f:
        generic_ics_outlook_json = json.loads(f.read())


    def test_ics_nodata(self):
        """
        Test the ics parser with no data
        """
        self.assertEqual(jc.parsers.ics.parse('', quiet=True), [])


    def test_ics_test(self):
        """
        Test the test ics file
        """
        self.assertEqual(
            jc.parsers.ics.parse(self.generic_ics_test, quiet=True),
            self.generic_ics_test_json
        )


    def test_ics_test_raw(self):
        """
        Test the test ics file with raw=True
        """
        self.assertEqual(
            jc.parsers.ics.parse(self.generic_ics_test, raw=True, quiet=True),
            self.generic_ics_test_raw_json
        )


    def test_ics_crlf(self):
        """
        Test CRLF line endings, a tab continuation and a quoted parameter
        """
        self.assertEqual(
            jc.parsers.ics.parse(self.generic_ics_crlf, quiet=True),
            self.generic_ics_crlf_json
        )


    def test_ics_crlf_raw(self):
        """
        Test CRLF line endings with raw=True: the DATE value is not normalized
        """
        self.assertEqual(
            jc.parsers.ics.parse(self.generic_ics_crlf, raw=True, quiet=True),
            self.generic_ics_crlf_raw_json
        )


    def test_ics_google_shape(self):
        """
        Test a fixture reconstructed from a Google Calendar export: a line
        folded at 75 octets, a folded ATTENDEE, X- and calendar-level X-WR-
        properties, and a duration alarm
        """
        self.assertEqual(
            jc.parsers.ics.parse(self.generic_ics_google, quiet=True),
            self.generic_ics_google_json
        )


    def test_ics_outlook_shape(self):
        """
        Test a fixture reconstructed from an Outlook export: a line folded at
        75 octets right before a `\n` escape (so the continuation line starts
        with the escape), LANGUAGE parameters, CLASS, PRIORITY and
        X-MICROSOFT- properties
        """
        self.assertEqual(
            jc.parsers.ics.parse(self.generic_ics_outlook, quiet=True),
            self.generic_ics_outlook_json
        )


    def test_ics_tzid_floating_and_utc(self):
        """
        Test that a TZID value, a floating value and a UTC value are kept apart
        """
        result = jc.parsers.ics.parse(
            'BEGIN:VEVENT\n'
            'DTSTART;TZID=America/New_York:20261015T090000\n'
            'DTEND:20261015T090000\n'
            'DTSTAMP:20261015T090000Z\n'
            'END:VEVENT\n',
            quiet=True
        )

        self.assertEqual(result[0]['dtstart'], '2026-10-15T09:00:00')
        self.assertEqual(result[0]['dtstart_tzid'], 'America/New_York')
        self.assertEqual(result[0]['dtend'], '2026-10-15T09:00:00')
        self.assertNotIn('dtend_tzid', result[0])
        self.assertEqual(result[0]['dtstamp'], '2026-10-15T09:00:00Z')


    def test_ics_recurrence_id(self):
        """
        Test that RECURRENCE-ID is read, normalized and keeps its TZID
        """
        result = jc.parsers.ics.parse(
            'BEGIN:VEVENT\n'
            'UID:42\n'
            'RECURRENCE-ID;TZID=Europe/Rome:20261022T090000\n'
            'END:VEVENT\n',
            quiet=True
        )

        self.assertEqual(result[0]['recurrence_id'], '2026-10-22T09:00:00')
        self.assertEqual(result[0]['recurrence_id_tzid'], 'Europe/Rome')


    def test_ics_vtodo_fields(self):
        """
        Test COMPLETED, PRIORITY and PERCENT-COMPLETE on a VTODO
        """
        result = jc.parsers.ics.parse(
            'BEGIN:VTODO\n'
            'UID:7\n'
            'COMPLETED:20261014T120000Z\n'
            'PRIORITY:5\n'
            'PERCENT-COMPLETE:40\n'
            'END:VTODO\n',
            quiet=True
        )

        self.assertEqual(result[0]['completed'], '2026-10-14T12:00:00Z')
        self.assertEqual(result[0]['priority'], 5)
        self.assertEqual(result[0]['percent_complete'], 40)


    def test_ics_alarm_trigger(self):
        """
        Test that an absolute TRIGGER is normalized while a duration is not
        """
        result = jc.parsers.ics.parse(
            'BEGIN:VEVENT\n'
            'UID:42\n'
            'BEGIN:VALARM\n'
            'ACTION:DISPLAY\n'
            'TRIGGER;VALUE=DATE-TIME:20261015T080000Z\n'
            'END:VALARM\n'
            'BEGIN:VALARM\n'
            'ACTION:DISPLAY\n'
            'TRIGGER:-PT15M\n'
            'END:VALARM\n'
            'END:VEVENT\n',
            quiet=True
        )

        self.assertEqual(result[0]['alarms'][0]['trigger'], '2026-10-15T08:00:00Z')
        self.assertEqual(result[0]['alarms'][1]['trigger'], '-PT15M')


    def test_ics_unterminated_component_warns(self):
        """
        Test that a component without an END is reported and dropped
        """
        data = 'BEGIN:VCALENDAR\nBEGIN:VEVENT\nUID:42\nSUMMARY:Truncated\n'

        with contextlib.redirect_stderr(io.StringIO()) as err:
            result = jc.parsers.ics.parse(data)

        self.assertEqual(result, [])
        self.assertIn('Unterminated BEGIN:VEVENT', err.getvalue())


    def test_ics_mismatched_end_warns(self):
        """
        Test that an END that does not match the open BEGIN is reported, and
        that the component it names is still read
        """
        data = (
            'BEGIN:VCALENDAR\n'
            'BEGIN:VEVENT\n'
            'UID:42\n'
            'BEGIN:VALARM\n'
            'ACTION:DISPLAY\n'
            'END:VEVENT\n'
            'END:VCALENDAR\n'
        )

        with contextlib.redirect_stderr(io.StringIO()) as err:
            result = jc.parsers.ics.parse(data)

        self.assertEqual(result[0]['uid'], '42')
        self.assertEqual(result[0]['alarms'][0]['action'], 'DISPLAY')
        self.assertIn('does not match the open BEGIN:VALARM', err.getvalue())


    def test_ics_end_without_begin_warns(self):
        """
        Test that an END with no open component of that kind is reported
        """
        with contextlib.redirect_stderr(io.StringIO()) as err:
            result = jc.parsers.ics.parse('BEGIN:VEVENT\nUID:42\nEND:VCALENDAR\nEND:VEVENT\n')

        self.assertEqual(result[0]['uid'], '42')
        self.assertIn('END:VCALENDAR without a matching BEGIN', err.getvalue())


    def test_ics_component_left_open_by_a_mismatch_warns(self):
        """
        Test that a component left open by a mismatched END is dropped like
        any unterminated component, and named in its own warning
        """
        data = (
            'BEGIN:VEVENT\n'
            'UID:42\n'
            'BEGIN:VTODO\n'
            'UID:9\n'
            'END:VEVENT\n'
        )

        with contextlib.redirect_stderr(io.StringIO()) as err:
            result = jc.parsers.ics.parse(data)

        self.assertEqual([component['uid'] for component in result], ['42'])
        self.assertIn('does not match the open BEGIN:VTODO', err.getvalue())
        self.assertIn('Unterminated BEGIN:VTODO', err.getvalue())


    def test_ics_line_without_colon_warns(self):
        """
        Test that a line without a property/value separator is reported
        """
        data = 'BEGIN:VEVENT\nSUMMARY missing the colon\nUID:42\nEND:VEVENT\n'

        with contextlib.redirect_stderr(io.StringIO()) as err:
            result = jc.parsers.ics.parse(data)

        self.assertEqual(result[0]['uid'], '42')
        self.assertNotIn('summary', result[0])
        self.assertIn('no property/value separator', err.getvalue())


    def test_ics_valid_input_does_not_warn(self):
        """
        Test that the VTIMEZONE block and the VCALENDAR properties do not warn
        """
        with contextlib.redirect_stderr(io.StringIO()) as err:
            jc.parsers.ics.parse(self.generic_ics_test)

        self.assertEqual(err.getvalue(), '')


    def test_ics_quiet_suppresses_warnings(self):
        """
        Test that quiet=True suppresses the warning messages
        """
        data = 'BEGIN:VEVENT\nSUMMARY missing the colon\nEND:VEVENT\n'

        with contextlib.redirect_stderr(io.StringIO()) as err:
            jc.parsers.ics.parse(data, quiet=True)

        self.assertEqual(err.getvalue(), '')


if __name__ == '__main__':
    unittest.main()
