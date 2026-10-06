import unittest
import os
import sys
sys.path.append(os.getcwd())
from tests import utils_for_test as test_utils
import jc
sys.path.pop()


class MyTests(unittest.TestCase):

    def test_tnsnames_nodata(self):
        """
        Test 'tnsnames' with no data
        """
        test_utils.run_no_data(self, __file__, [])

    def test_tnsnames_all_fixtures(self):
        """
        Test 'tnsnames' with various fixtures
        """
        test_utils.run_all_fixtures(self, __file__)

    def test_tnsnames_alias_list(self):
        """
        Test that a comma-separated alias list keeps every name and that a
        single-address ADDRESS_LIST still gives an `address` list
        """
        fixture = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'fixtures/generic/tnsnames--alias-list.out'
        )

        with open(fixture, 'r', encoding='utf-8') as f:
            result = jc.parse('tnsnames', f.read(), quiet=True)

        self.assertEqual(result[0]['name'], 'ORCL')
        self.assertEqual(result[0]['aliases'], ['ORCL', 'ORCL.WORLD'])
        self.assertEqual(
            result[0]['description']['address_list']['address'],
            [{'protocol': 'tcp', 'host': 'orcl1-svr', 'port': 1521}]
        )


if __name__ == '__main__':
    unittest.main()
