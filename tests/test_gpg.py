import os
import unittest
import json
import jc.parsers.gpg

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/gpg.out'), 'r', encoding='utf-8') as f:
        gpg = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/gpg.json'), 'r', encoding='utf-8') as f:
        gpg_json = json.loads(f.read())


    def test_gpg_nodata(self):
        """
        Test 'gpg' with no data
        """
        self.assertEqual(jc.parsers.gpg.parse('', quiet=True), [])

    def test_gpg(self):
        """
        Test 'gpg --with-colons --list-keys --with-fingerprint --with-fingerprint wk@gnupg.org'
        """
        self.assertEqual(jc.parsers.gpg.parse(self.gpg, quiet=True), self.gpg_json)


if __name__ == '__main__':
    unittest.main()
