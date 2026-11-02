import unittest
import os
import sys
sys.path.append(os.getcwd())
from tests import utils_for_test as test_utils
sys.path.pop()
import jc

# Execute these steps for standard tests:
# - Save this file as `test_{parser_name}.py` since the helper methods extract parser names from the filename.
# - Organize fixtures in `tests/fixtures` for optimal structure.
# - Format fixtures as follows (using double dashes):
#     - `{parser_name}--{some_test_description}.out` for command output.
#     - `{parser_name}--{some_test_description}.json` for expected JSON after parsing.

class MyTests(unittest.TestCase):

    def test_apt_cache_show_nodata(self):
        """
        Test 'apt_cache_show' with no data
        """
        test_utils.run_no_data(self, __file__, [])

    def test_apt_cache_show_all_fixtures(self):
        """
        Test 'apt_cache_show' with various fixtures
        """
        test_utils.run_all_fixtures(self, __file__)

    def test_apt_cache_show_continuation_after_description(self):
        """
        Test 'apt_cache_show' with an indented continuation line of a field after Description-en
        """
        data = (
            'Package: a\n'
            'Description-en: short text\n'
            ' long text\n'
            'Description-md5: 00000000000000000000000000000000\n'
            'Tag: admin::boot, role::program,\n'
            ' works-with::software:running\n'
            'Section: admin\n'
        )
        result = jc.parse('apt_cache_show', data, quiet=True)
        self.assertEqual(result[0]['description'], 'short text  long text')
        self.assertEqual(result[0]['description_md5'], '00000000000000000000000000000000')
        self.assertEqual(result[0]['section'], 'admin')


if __name__ == '__main__':
    unittest.main()
