import unittest
import os
import sys
sys.path.append(os.getcwd())
from tests import utils_for_test as test_utils
sys.path.pop()
import jc.parsers.getfacl


class MyTests(unittest.TestCase):

    def test_getfacl_line_separators(self):
        """
        Test 'getfacl' with line-break characters other than LF in a file name
        """
        data = '# file: a\rb\x0bc\x0cd\x1ce\x1df\x1eg\x85h\u2028i\u2029j\n# owner: alice\n# group: staff\nuser::rw-\n'
        result = jc.parsers.getfacl.parse(data, quiet=True)
        self.assertEqual(result[0]['file'], 'a\rb\x0bc\x0cd\x1ce\x1df\x1eg\x85h\u2028i\u2029j')
        self.assertEqual(result[0]['owner'], 'alice')

    def test_getfacl_nodata(self):
        """
        Test 'getfacl' with no data
        """
        test_utils.run_no_data(self, __file__, [])

    def test_getfacl_all_fixtures(self):
        """
        Test 'getfacl' with various fixtures
        """
        test_utils.run_all_fixtures(self, __file__)


if __name__ == '__main__':
    unittest.main()
