import unittest
import os
import sys
sys.path.append(os.getcwd())
from tests import utils_for_test as test_utils
sys.path.pop()
import jc.parsers.pacman

# Execute these steps for standard tests:
# - Save this file as `test_{parser_name}.py` since the helper methods extract parser names from the filename.
# - Organize fixtures in `tests/fixtures` for optimal structure.
# - Format fixtures as follows (using double dashes):
#     - `{parser_name}--{some_test_description}.out` for command output.
#     - `{parser_name}--{some_test_description}.json` for expected JSON after parsing.

class MyTests(unittest.TestCase):

    def test_pacman_nodata(self):
        """
        Test 'pacman' with no data
        """
        test_utils.run_no_data(self, __file__, [])

    def test_pacman_all_fixtures(self):
        """
        Test 'pacman' with various fixtures
        """
        test_utils.run_all_fixtures(self, __file__)

    def test_pacman_wrapped_fields_after_empty_multiline_field(self):
        """
        Test 'pacman' with wrapped fields after a multiline field that is None
        """
        data = (
            'Name            : coolprompt\n'
            'Version         : 1.0-1\n'
            'Required By     : None\n'
            'Optional For    : coolprompt-themes\n'
            '                  coolprompt-extras\n'
            'Backup Files    : None\n'
            '\n'
            'Name            : zstd\n'
            'Version         : 1.5.6-1\n'
            'Description     : Zstandard - Fast real-time\n'
            '                  compression algorithm\n'
            'Optional Deps   : None\n'
            'Depends On      : glibc  gcc-libs\n'
            '                  zlib  xz\n'
            '                  lz4\n'
        )
        expected = [
            {
                'name': 'coolprompt',
                'version': '1.0-1',
                'optional_for': ['coolprompt-themes', 'coolprompt-extras']
            },
            {
                'name': 'zstd',
                'version': '1.5.6-1',
                'description': 'Zstandard - Fast real-time compression algorithm',
                'depends_on': ['glibc', 'gcc-libs', 'zlib', 'xz', 'lz4']
            }
        ]
        self.assertEqual(jc.parsers.pacman.parse(data, quiet=True), expected)


if __name__ == '__main__':
    unittest.main()
