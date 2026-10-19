import io
import json
import os
import sys
import unittest
from contextlib import redirect_stderr
sys.path.append(os.getcwd())
from tests import utils_for_test as test_utils
import jc
sys.path.pop()


THIS_DIR = os.path.dirname(os.path.abspath(__file__))
FIXTURES = os.path.join(THIS_DIR, 'fixtures', 'generic')


def _fixture(name):
    with open(os.path.join(FIXTURES, name), 'r', encoding='utf-8') as f:
        return f.read()


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
        result = jc.parse('tnsnames', _fixture('tnsnames--alias-list.out'), quiet=True)

        self.assertEqual(result[0]['name'], 'ORCL')
        self.assertEqual(result[0]['aliases'], ['ORCL', 'ORCL.WORLD'])
        self.assertEqual(
            result[0]['description']['address_list'][0]['address'],
            [{'protocol': 'tcp', 'host': 'orcl1-svr', 'port': 1521}]
        )

    def test_tnsnames_source_route_hop_order(self):
        """
        Test that `hops` keeps the address order from the file, including
        addresses inside a nested ADDRESS_LIST, and that it is added when
        SOURCE_ROUTE comes after the addresses
        """
        result = jc.parse('tnsnames', _fixture('tnsnames--source-route.out'), quiet=True)

        self.assertEqual(
            [hop['host'] for hop in result[0]['description']['hops']],
            ['hop1', 'hop2', 'hop3']
        )
        self.assertEqual(
            [hop['host'] for hop in result[1]['description']['hops']],
            ['hop1', 'hop2a', 'hop2b', 'hop3']
        )

        # `hops` is only added when source_route is present
        self.assertNotIn('hops', result[0]['description']['address_list'][0])

    def test_tnsnames_address_list_is_always_a_list(self):
        """
        Test that a single ADDRESS_LIST and two ADDRESS_LISTs under one
        DESCRIPTION both give an `address_list` list
        """
        two = jc.parse('tnsnames', _fixture('tnsnames--two-address-lists.out'), quiet=True)
        one = jc.parse('tnsnames', _fixture('tnsnames--alias-list.out'), quiet=True)

        self.assertIsInstance(two[0]['description']['address_list'], list)
        self.assertEqual(len(two[0]['description']['address_list']), 2)
        self.assertIsInstance(one[0]['description']['address_list'], list)
        self.assertEqual(len(one[0]['description']['address_list']), 1)

    def test_tnsnames_raw_keeps_numbers_as_strings(self):
        """
        Test that raw output matches the processed output except that numeric
        parameters stay strings
        """
        result = jc.parse('tnsnames', _fixture('tnsnames--multi-entry.out'), quiet=True, raw=True)

        self.assertEqual(result, json.loads(_fixture('tnsnames-multi-entry-raw.json')))
        self.assertEqual(result[0]['description']['address_list'][0]['address'][0]['port'], '1521')
        self.assertEqual(
            result[0]['description']['connect_data']['failover_mode']['retries'], '180'
        )

    def test_tnsnames_non_numeric_port_and_quoted_hash(self):
        """
        Test that a non-numeric PORT and a numeric-looking SID stay strings and
        that a `#` inside quotation marks is kept in the value
        """
        result = jc.parse('tnsnames', _fixture('tnsnames--types.out'), quiet=True)

        self.assertEqual(result[0]['description']['address'][0]['port'], '1521X')
        self.assertEqual(result[0]['description']['connect_data']['sid'], '12345')
        self.assertEqual(
            result[0]['description']['connect_data']['service_name'],
            'types#1.example.com'
        )

    def test_tnsnames_top_level_scalar(self):
        """
        Test that a top-level scalar that is not IFILE is skipped with a
        warning instead of becoming a key named after the input
        """
        stderr = io.StringIO()

        with redirect_stderr(stderr):
            result = jc.parse('tnsnames', _fixture('tnsnames--top-level-scalar.out'))

        self.assertEqual(result, json.loads(_fixture('tnsnames--top-level-scalar.json')))
        self.assertNotIn('scalar_line', json.dumps(result))
        self.assertNotIn('h:1521/svc', json.dumps(result))
        self.assertIn('Skipped top-level scalar', stderr.getvalue())

        quiet_stderr = io.StringIO()

        with redirect_stderr(quiet_stderr):
            jc.parse('tnsnames', _fixture('tnsnames--top-level-scalar.out'), quiet=True)

        self.assertEqual(quiet_stderr.getvalue(), '')

    def test_tnsnames_malformed_warns(self):
        """
        Test that a truncated file still returns what it parsed and warns that
        a container was not closed
        """
        stderr = io.StringIO()

        with redirect_stderr(stderr):
            result = jc.parse('tnsnames', _fixture('tnsnames--malformed.out'))

        self.assertEqual(result, json.loads(_fixture('tnsnames--malformed.json')))
        self.assertIn('was not closed', stderr.getvalue())

    def test_tnsnames_plain_text_warns(self):
        """
        Test that input that is not a tnsnames file gives an empty list and a
        warning
        """
        stderr = io.StringIO()

        with redirect_stderr(stderr):
            result = jc.parse('tnsnames', 'this is not a tnsnames file\n')

        self.assertEqual(result, [])
        self.assertIn('Skipped input', stderr.getvalue())

    def test_tnsnames_netca_generated_file(self):
        """
        Test a tnsnames.ora generated by Oracle's netca, captured from
        markddrake/YADAMU---Yet-Another-DAta-Migration-Utility
        (docker/regressionTests/tnsnames.ora)
        """
        result = jc.parse('tnsnames', _fixture('tnsnames--netca.out'), quiet=True)

        self.assertEqual(len(result), 11)
        self.assertEqual(result[0]['name'], 'ORACL01')
        self.assertEqual(result[0]['description']['address'][0]['host'], 'ORACLE-DB1')
        self.assertEqual(result[0]['description']['connect_data']['service_name'], 'PDB19300')


if __name__ == '__main__':
    unittest.main()
