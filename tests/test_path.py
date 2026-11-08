import unittest
import os
import sys
sys.path.append(os.getcwd())
from tests import utils_for_test as test_utils
sys.path.pop()

class MyTests(unittest.TestCase):

    def test_path_nodata(self):
        """
        Test 'path' with no data
        """
        test_utils.run_no_data(self, __file__, {})

    def test_path_all_fixtures(self):
        """
        Test 'path' with various logs
        """
        test_utils.run_all_fixtures(self, __file__)

    def test_path_windows_crlf(self):
        """
        Test 'path' with Windows path terminated by CRLF (#897)
        """
        import jc
        p = "C:\\work\\report.txt"
        for ending in ("", chr(10), chr(13) + chr(10)):
            data = p + ending
            res = jc.parse("path", data)
            self.assertEqual(res["filename"], "report.txt")
            self.assertEqual(res["extension"], "txt")
            self.assertEqual(res["path"], p)


if __name__ == '__main__':
    unittest.main()
