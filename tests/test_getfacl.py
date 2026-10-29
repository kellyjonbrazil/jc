import unittest
import os
import sys
sys.path.append(os.getcwd())
from tests import utils_for_test as test_utils
sys.path.pop()
import jc.parsers.getfacl


class MyTests(unittest.TestCase):

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

    def test_getfacl_escaped_names_raw(self):
        """
        Test 'getfacl' decodes escaped names in raw output
        """
        data = ('# file: Q1\\\\report\\012.txt\n'
                '# owner: CORP\\\\alice\n'
                '# group: CORP\\\\domain\\040users\n'
                'user::rw-\n'
                'group:CORP\\\\domain\\040admins:rw-\n')
        expected = [
            {'file': 'Q1\\report\n.txt', 'owner': 'CORP\\alice', 'group': 'CORP\\domain users', 'flags': None, 'type': 'user', 'name': None, 'permissions': 'rw-', 'effective': None, 'default': False},
            {'file': 'Q1\\report\n.txt', 'owner': 'CORP\\alice', 'group': 'CORP\\domain users', 'flags': None, 'type': 'group', 'name': 'CORP\\domain admins', 'permissions': 'rw-', 'effective': None, 'default': False}
        ]
        self.assertEqual(jc.parsers.getfacl.parse(data, raw=True, quiet=True), expected)

    def test_getfacl_octal_escapes_per_field(self):
        """
        Test 'getfacl' decodes only the octal escapes getfacl writes for each field
        """
        data = ('# file: a\\040b\\011c\n'
                '# owner: d\\072e\\040f\n'
                '# group: g\\054h\n'
                'user:i\\072j\\054k\\055l:r--\n')
        expected = [{'file': 'a\\040b\\011c', 'owner': 'd\\072e f', 'group': 'g\\054h', 'flags': None, 'type': 'user', 'name': 'i:j,k\\055l', 'permissions': 'r--', 'effective': None, 'default': False}]
        self.assertEqual(jc.parsers.getfacl.parse(data, quiet=True), expected)


if __name__ == '__main__':
    unittest.main()
