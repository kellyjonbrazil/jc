import os
import json
import unittest
import jc.parsers.netrc

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/netrc.out'), 'r', encoding='utf-8') as f:
        netrc = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/netrc.json'), 'r', encoding='utf-8') as f:
        netrc_json = json.loads(f.read())

    def test_netrc_nodata(self):
        """
        Test 'netrc' with no data
        """
        self.assertEqual(jc.parsers.netrc.parse('', quiet=True), [])

    def test_netrc(self):
        """
        Test a '.netrc' file with:

        - a one-keyword-per-line machine block
        - a machine block written entirely on one line
        - a default block (the bare 'default' keyword, no value)
        - a macdef block whose body is terminated by a blank line
        - a macdef block whose body is terminated by EOF instead of a
          blank line
        - a leading comment line, which should be silently ignored
        """
        self.assertEqual(jc.parsers.netrc.parse(self.netrc, quiet=True), self.netrc_json)


if __name__ == '__main__':
    unittest.main()
