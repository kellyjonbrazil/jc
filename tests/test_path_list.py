import unittest
import jc.parsers.path_list
import os
import sys
sys.path.append(os.getcwd())
from tests import utils_for_test as test_utils
sys.path.pop()


class MyTests(unittest.TestCase):

    def test_path_list_nodata(self):
        """
        Test 'path_list' with no data
        """
        test_utils.run_no_data(self, __file__, [])

    def test_path_list_all_fixtures(self):
        """
        Test 'path_list' with various logs
        """
        test_utils.run_all_fixtures(self, __file__)

    def test_path_list_blank_and_empty_entries(self):
        """
        Test 'path_list' with whitespace-only input and empty entries
        """
        self.assertEqual(jc.parsers.path_list.parse('   \n', quiet=True), [])
        self.assertEqual(jc.parsers.path_list.parse('', quiet=True), [])
        self.assertEqual(len(jc.parsers.path_list.parse('/a::/b', quiet=True)), 3)

    def test_path_list_empty_entry_is_current_directory(self):
        """
        Test 'path_list' with empty entries, which mean the current directory
        """
        for data in ('/usr/bin::/bin', '/usr/bin::/bin\n'):
            result = jc.parsers.path_list.parse(data, quiet=True)
            self.assertEqual([r['path'] for r in result], ['/usr/bin', '.', '/bin'])

        result = jc.parsers.path_list.parse(':/bin\n', quiet=True)
        self.assertEqual([r['path'] for r in result], ['.', '/bin'])

        result = jc.parsers.path_list.parse('/bin:\n', quiet=True)
        self.assertEqual([r['path'] for r in result], ['/bin', '.'])
        self.assertEqual(result[1], {'path': '.', 'parent': '.', 'filename': '', 'stem': '', 'extension': '', 'path_list': []})

        result = jc.parsers.path_list.parse('C:\\a;;D:\\b\n', quiet=True)
        self.assertEqual([r['path'] for r in result], ['C:\\a', '.', 'D:\\b'])

    def test_path_list_whitespace_only_entry(self):
        """
        Test 'path_list' with a whitespace-only entry, which is a valid directory name
        """
        result = jc.parsers.path_list.parse('a: :b', quiet=True)
        self.assertEqual(result[1], {'path': ' ', 'parent': '.', 'filename': ' ', 'stem': ' ', 'extension': '', 'path_list': [' ']})
        self.assertEqual([r['path'] for r in result], ['a', ' ', 'b'])

        result = jc.parsers.path_list.parse('C:\\a; ;D:\\b', quiet=True)
        self.assertEqual([r['path'] for r in result], ['C:\\a', ' ', 'D:\\b'])
        self.assertEqual(result[1]['filename'], ' ')


if __name__ == '__main__':
    unittest.main()
