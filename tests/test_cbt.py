import os
import unittest
from jc.exceptions import ParseError
import jc.parsers.cbt

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def test_cbt_nodata(self):
        """
        Test 'cbt' with no data
        """
        self.assertEqual(jc.parsers.cbt.parse('', quiet=True), [])

    def test_cbt_single_row(self):
        """
        Test 'cbt' with a single row
        """
        input = '''
----------------------------------------
foo
  foo:bar                                  @ 1970/01/01-01:00:00.000000
    "baz"
        '''
        expected = [
            {
                "key": "foo",
                "cells": {
                    "foo": {
                        "bar": "baz"
                    }
                }
            }
        ]
        self.assertEqual(jc.parsers.cbt.parse(input, quiet=True), expected)

    def test_cbt_multiple_column_families(self):
        """
        Test 'cbt' with multiple column families
        """
        input = '''
----------------------------------------
foo
  foo:bar1                                 @ 1970/01/01-01:00:00.000000
    "baz1"
  foo:bar2                                 @ 1970/01/01-01:00:00.000000
    "baz2"
  bat:bar                                  @ 1970/01/01-01:00:00.000000
    "baz"
            '''
        expected = [
            {
                "key": "foo",
                "cells": {
                    "foo": {
                        "bar1": "baz1",
                        "bar2": "baz2",
                    },
                    "bat": {
                        "bar": "baz"
                    }
                }
            }
        ]
        self.assertEqual(jc.parsers.cbt.parse(input, quiet=True), expected)

    def test_cbt_multiple_rows(self):
        """
        Test 'cbt' with multiple rows
        """
        input = '''
----------------------------------------
foo
  foo:bar                                  @ 1970/01/01-01:00:00.000000
    "baz1"
----------------------------------------
bar
  foo:bar                                  @ 1970/01/01-01:00:00.000000
    "baz2"
            '''
        expected = [
            {
                "key": "foo",
                "cells": {
                    "foo": {
                        "bar": "baz1",
                    }
                }
            },
            {
                "key": "bar",
                "cells": {
                    "foo": {
                        "bar": "baz2",
                    }
                }
            }
        ]
        self.assertEqual(jc.parsers.cbt.parse(input, quiet=True), expected)

    def test_cbt_multiple_rows_raw(self):
        """
        Test 'cbt' with multiple rows raw
        """
        input = '''
----------------------------------------
foo
  foo:bar                                  @ 1970/01/01-01:00:00.000000
    "baz1"
----------------------------------------
bar
  foo:bar                                  @ 1970/01/01-01:00:00.000000
    "baz2"
            '''
        expected = [
            {
                "key": "foo",
                "cells": [
                    {
                        "column_family": "foo",
                        "column": "bar",
                        "timestamp": "1970-01-01T01:00:00",
                        "value": "baz1",
                    }
                ]
            },
            {
                "key": "bar",
                "cells": [
                    {
                        "column_family": "foo",
                        "column": "bar",
                        "timestamp": "1970-01-01T01:00:00",
                        "value": "baz2",
                    }
                ]
            }
        ]
        self.assertEqual(jc.parsers.cbt.parse(input, quiet=True, raw=True), expected)


if __name__ == '__main__':
    unittest.main()
