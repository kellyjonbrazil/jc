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

    def test_dir_drive_letter_d(self):
        """
        Test that the D: drive letter is not stripped from the parent path.
        Regression test: lstrip(" Directory of ") strips any char in the set
        {' ','D','i','r','e','c','t','o','y','f'}, which incorrectly removes
        the 'D' from 'D:\\'.
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


    def test_dir_line_separator(self):
        """
        Test 'dir' with a line-break character other than LF inside a field
        """
        data = ' Directory of C:\\Shared\r\n\r\n03/24/2021  03:15 PM                 0 a.txt\u2028 Directory of other\r\n03/24/2021  03:16 PM            54,784 payroll.xlsx\r\n'
        result = jc.parsers.dir.parse(data, quiet=True)
        self.assertEqual(len(result), 2)
        self.assertEqual([x['parent'] for x in result], ['C:\\Shared', 'C:\\Shared'])
        self.assertEqual(result[0]['size'], 0)
        self.assertEqual(result[1]['filename'], 'payroll.xlsx')

    def test_dir_filename_whitespace(self):
        """
        Test that leading and repeated spaces in file and directory names are kept
        """
        data = (' Directory of C:\\Shared\n\n'
                '01/01/1999  12:00 AM       999,999,999 file  name.txt\n'
                '03/24/2021  03:15 PM                 0 file name.txt\n'
                '03/24/2021  03:15 PM             1,088  lead.txt\n'
                '03/24/2021  03:15 PM    <DIR>           lead dir\n'
                '03/24/2021  03:15 PM    <DIR>          a  b\n')
        result = jc.parsers.dir.parse(data, raw=True, quiet=True)
        self.assertEqual([r['filename'] for r in result], ['file  name.txt', 'file name.txt', ' lead.txt', ' lead dir', 'a  b'])
        self.assertEqual([r['size'] for r in result], ['999,999,999', '0', '1,088', None, None])
        self.assertEqual([r['dir'] for r in result], [False, False, False, True, True])

    def test_dir_junction_symlink(self):
        """
        Test <JUNCTION>, <SYMLINKD>, and <SYMLINK> rows
        """
        data = (' Directory of C:\\Shared\n\n'
                '03/24/2021  03:15 PM    <JUNCTION>     my  link [C:\\Target]\n'
                '03/24/2021  03:15 PM    <SYMLINKD>     sdir [C:\\Other]\n'
                '03/24/2021  03:15 PM    <SYMLINK>      f.txt [g.txt]\n')
        result = jc.parsers.dir.parse(data, raw=True, quiet=True)
        self.assertEqual([r['filename'] for r in result], ['my  link [C:\\Target]', 'sdir [C:\\Other]', 'f.txt [g.txt]'])
        self.assertEqual([r['size'] for r in result], ['<JUNCTION>', '<SYMLINKD>', '<SYMLINK>'])
        self.assertEqual(result[0]['parent'], 'C:\\Shared')


if __name__ == '__main__':
    unittest.main()
