import unittest
import os
import sys
import jc.parsers.ldd
sys.path.append(os.getcwd())
from tests import utils_for_test as test_utils
sys.path.pop()


class MyTests(unittest.TestCase):

    def test_ldd_nodata(self):
        """
        Test 'ldd' with no data
        """
        test_utils.run_no_data(self, __file__, [])

    def test_ldd_all_fixtures(self):
        """
        Test 'ldd' with various fixtures
        """
        test_utils.run_all_fixtures(self, __file__)

    def test_ldd_spaces_in_names(self):
        """
        Test 'ldd' with spaces in file, library and path names
        """
        data = (
            'bin/my tool:\n'
            '\tlibselinux.so.1 => /tmp/vendor libs/libselinux.so.1 (0x00007f0cbe2ef000)\n'
            '\t/opt/My App/ld linux.so.2 (0x00007f0cbe359000)\n'
            '\n'
            '\tVersion information:\n'
            '\tbin/my tool:\n'
            '\t\tmy lib.so.2 (MY_1.0) => /opt/My App/my lib.so.2\n'
            'second tool:\n'
            '\tlibc.so.6 => /lib64/libc.so.6 (0x00007f0cbe0e7000)\n'
        )
        result = jc.parsers.ldd.parse(data, quiet=True)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['file'], 'bin/my tool')
        self.assertEqual(result[0]['dependencies'], [
            {'name': 'libselinux.so.1', 'path': '/tmp/vendor libs/libselinux.so.1', 'address': '0x00007f0cbe2ef000'},
            {'name': '/opt/My App/ld linux.so.2', 'path': None, 'address': '0x00007f0cbe359000'}
        ])
        self.assertEqual(result[0]['version_info'], [
            {'for': 'bin/my tool', 'requires': [
                {'name': 'my lib.so.2', 'version': 'MY_1.0', 'path': '/opt/My App/my lib.so.2'}
            ]}
        ])
        self.assertEqual(result[1]['file'], 'second tool')
        self.assertEqual(result[1]['dependencies'], [
            {'name': 'libc.so.6', 'path': '/lib64/libc.so.6', 'address': '0x00007f0cbe0e7000'}
        ])


if __name__ == '__main__':
    unittest.main()
