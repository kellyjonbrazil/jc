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

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ics-test.json'), 'r', encoding='utf-8') as f:
        generic_ics_test_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ics-test-raw.json'), 'r', encoding='utf-8') as f:
        generic_ics_test_raw_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ics-crlf.json'), 'r', encoding='utf-8') as f:
        generic_ics_crlf_json = json.loads(f.read())


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


if __name__ == '__main__':
    unittest.main()
