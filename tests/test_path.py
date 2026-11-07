import unittest
import os
import sys
import jc
sys.path.append(os.getcwd())
from tests import utils_for_test as test_utils
sys.path.pop()

class MyTests(unittest.TestCase):

    def test_path_nodata(self):
        """
        Test 'path' with no data
        """
        test_utils.run_no_data(self, __file__, {})

    def test_path_windows_crlf(self):
        """Remove the line ending, not part of the Windows filename."""
        expected = {
            'path': r'C:\work\report.txt',
            'parent': r'C:\work',
            'filename': 'report.txt',
            'stem': 'report',
            'extension': 'txt',
            'path_list': ['C:\\', 'work', 'report.txt'],
        }
        for raw in (False, True):
            with self.subTest(raw=raw):
                self.assertEqual(
                    jc.parse('path', 'C:\\work\\report.txt\r\n',
                             raw=raw, quiet=True),
                    expected,
                )

    def test_path_windows_line_endings(self):
        """Keep the supported Windows forms consistent across line endings."""
        paths = (
            r'C:\work\report.txt',
            'C:/work/report.txt',
            r'\\server\share\report.txt',
            r'work\report.txt',
        )
        for path in paths:
            for raw in (False, True):
                expected = jc.parse('path', path, raw=raw, quiet=True)
                for ending in ('', '\n', '\r\n'):
                    with self.subTest(path=path, raw=raw, ending=ending):
                        self.assertEqual(
                            jc.parse('path', path + ending,
                                     raw=raw, quiet=True),
                            expected,
                        )

    def test_path_posix_filename_characters(self):
        """Do not discard literal CR or whitespace from POSIX filenames."""
        filenames = (
            'report.txt\r',
            're\rport.txt',
            ' report.txt ',
            're\tport.txt',
            'report.txt\u00a0',
        )
        for filename in filenames:
            path = '/tmp/' + filename
            for raw in (False, True):
                for ending in ('', '\n'):
                    with self.subTest(path=path, raw=raw, ending=ending):
                        parsed = jc.parse('path', path + ending,
                                          raw=raw, quiet=True)
                        self.assertEqual(parsed['filename'], filename)
                        self.assertEqual(parsed['path'], path)

    def test_path_all_fixtures(self):
        """
        Test 'path' with various logs
        """
        test_utils.run_all_fixtures(self, __file__)


if __name__ == '__main__':
    unittest.main()
