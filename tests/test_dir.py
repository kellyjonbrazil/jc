import os
import json
import unittest
import jc.parsers.dir

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/windows-10/dir.out'),
                  'r', encoding='utf-8') as f:
            self.windows_10_dir = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/windows-10/dir.json'),
                  'r', encoding='utf-8') as f:
            self.windows_10_dir_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/windows-10/dir-ODTC.out'),
                  'r', encoding='utf-8') as f:
            self.windows_10_dir_ODTC = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/windows-10/dir-ODTC.json'),
                  'r', encoding='utf-8') as f:
            self.windows_10_dir_ODTC_json = json.loads(f.read())

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/windows-10/dir-C.out'),
                  'r', encoding='utf-8') as f:
            self.windows_10_dir_C = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/windows-10/dir-Q.out'),
                  'r', encoding='utf-8') as f:
            self.windows_10_dir_Q = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/windows-10/dir-Q.json'),
                  'r', encoding='utf-8') as f:
            self.windows_10_dir_Q_json = json.loads(f.read())

    def test_dir_error(self):
        self.assertEqual(jc.parsers.dir.parse("Access is denied.", quiet=True), [])

    def test_dir_empty(self):
        self.assertEqual(jc.parsers.dir.parse("", quiet=True), [])

    def test_dir_windows_10(self):
        self.assertEqual(jc.parsers.dir.parse(self.windows_10_dir, quiet=True),
                         self.windows_10_dir_json)

    def test_dir_windows_10_ODTC(self):
        self.assertEqual(jc.parsers.dir.parse(self.windows_10_dir_ODTC, quiet=True),
                         self.windows_10_dir_ODTC_json)

    def test_dir_windows_10_C(self):
        self.assertEqual(jc.parsers.dir.parse(self.windows_10_dir_C, quiet=True),
                         self.windows_10_dir_json)

    def test_dir_windows_10_Q(self):
        self.assertEqual(jc.parsers.dir.parse(self.windows_10_dir_Q, quiet=True),
                         self.windows_10_dir_Q_json)


if __name__ == '__main__':
    unittest.main()
