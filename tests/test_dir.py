import os
import json
import unittest
import jc.parsers.dir

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/windows-10/dir.out'),
                'r', encoding='utf-8') as f:
        windows_10_dir = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/windows-10/dir.json'),
                'r', encoding='utf-8') as f:
        windows_10_dir_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/windows-10/dir-ODTC.out'),
                'r', encoding='utf-8') as f:
        windows_10_dir_ODTC = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/windows-10/dir-ODTC.json'),
                'r', encoding='utf-8') as f:
        windows_10_dir_ODTC_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/windows-10/dir-C.out'),
                'r', encoding='utf-8') as f:
        windows_10_dir_C = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/windows-10/dir-mix.out'),
                'r', encoding='utf-8') as f:
        windows_10_dir_mix = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/windows-10/dir-mix.json'),
                'r', encoding='utf-8') as f:
        windows_10_dir_mix_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/windows-10/dir-files.out'),
                'r', encoding='utf-8') as f:
        windows_10_dir_files = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/windows-10/dir-files.json'),
                'r', encoding='utf-8') as f:
        windows_10_dir_files_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/windows-10/dir-dirs.out'),
                'r', encoding='utf-8') as f:
        windows_10_dir_dirs = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/windows-10/dir-dirs.json'),
                'r', encoding='utf-8') as f:
        windows_10_dir_dirs_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/windows-10/dir-S.out'),
                'r', encoding='utf-8') as f:
        windows_10_dir_S = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/windows-10/dir-S.json'),
                'r', encoding='utf-8') as f:
        windows_10_dir_S_json = json.loads(f.read())


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

    def test_dir_windows_10_mix(self):
        self.assertEqual(jc.parsers.dir.parse(self.windows_10_dir_mix, quiet=True),
                         self.windows_10_dir_mix_json)

    def test_dir_windows_10_files(self):
        self.assertEqual(jc.parsers.dir.parse(self.windows_10_dir_files, quiet=True),
                         self.windows_10_dir_files_json)

    def test_dir_windows_10_dirs(self):
        self.assertEqual(jc.parsers.dir.parse(self.windows_10_dir_dirs, quiet=True),
                         self.windows_10_dir_dirs_json)

    def test_dir_windows_10_S(self):
        self.assertEqual(jc.parsers.dir.parse(self.windows_10_dir_S, quiet=True),
                         self.windows_10_dir_S_json)

    def test_dir_drive_letter_preserved(self):
        """
        Test that a drive letter at the start of the Directory path is preserved.
        lstrip(" Directory of ") incorrectly strips the leading 'D' from 'D:\\...',
        because lstrip strips individual characters, not a literal prefix string.
        Regression test for https://github.com/kellyjonbrazil/jc/issues/687.
        """
        data = (
            ' Volume in drive D has no label.\r\n'
            ' Volume Serial Number is 1234-5678\r\n'
            '\r\n'
            ' Directory of D:\\Users\\testuser\r\n'
            '\r\n'
            '03/24/2021  03:15 PM    <DIR>          .\r\n'
            '03/24/2021  03:15 PM    <DIR>          ..\r\n'
        )
        result = jc.parsers.dir.parse(data, quiet=True)
        self.assertEqual(result[0]['parent'], 'D:\\Users\\testuser')


if __name__ == '__main__':
    unittest.main()
