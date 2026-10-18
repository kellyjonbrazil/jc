import contextlib
import io
import json
import os
import sys
import unittest
sys.path.append(os.getcwd())
from tests import utils_for_test as test_utils
sys.path.pop()
import jc


class MyTests(unittest.TestCase):

    def test_nftables_nodata(self):
        """
        Test 'nftables' with no data
        """
        test_utils.run_no_data(self, __file__, [])

    def test_nftables_all_fixtures(self):
        """
        Test 'nftables' with various fixtures
        """
        test_utils.run_all_fixtures(self, __file__)

    def test_nftables_malformed_warns(self):
        """
        Test 'nftables' warns about skipped input and still returns the tables
        it could parse
        """
        base_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(base_dir, 'fixtures/generic/nftables--malformed.out'), encoding='utf-8') as f:
            data = f.read()
        with open(os.path.join(base_dir, 'fixtures/generic/nftables--malformed.json'), encoding='utf-8') as f:
            expected = json.loads(f.read())

        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            result = jc.parse('nftables', data)

        self.assertEqual(result, expected)
        self.assertIn('Some input was skipped', stderr.getvalue())

    def test_nftables_skipped_input_warns(self):
        """
        Test 'nftables' warns for plain text, a chain outside any table, and an
        unclosed block
        """
        empty_cases = {
            'plain text': 'not nft output at all\n',
            'chain outside a table': 'chain orphan {\n\ttcp dport 80 accept\n}\n'
        }

        for name, data in empty_cases.items():
            with self.subTest(name):
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr):
                    result = jc.parse('nftables', data)

                self.assertEqual(result, [])
                self.assertIn('Some input was skipped', stderr.getvalue())

        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            jc.parse('nftables', 'table inet broken {\n\tchain input {\n\t\ttcp dport 22 accept\n')

        self.assertIn('Some input was skipped', stderr.getvalue())

        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            jc.parse('nftables', 'not nft output at all\n', quiet=True)

        self.assertEqual(stderr.getvalue(), '')

    def test_nftables_rule_counters(self):
        """
        Test 'nftables' pulls inline rule counters into their own fields and
        ignores counter-like text in quoted strings, named counter references,
        and counters inside braces
        """
        data = (
            'table inet filter {\n'
            '\tchain input {\n'
            '\t\ttcp dport 8080 counter packets 12 bytes 720 accept\n'
            '\t\ttcp dport 22 accept\n'
            '\t\taccept comment "counter packets 1 bytes 2"\n'
            '\t\ttcp dport 443 counter name "https" accept\n'
            '\t\tadd @seen { ip saddr counter packets 3 bytes 4 } accept\n'
            '\t}\n'
            '}\n'
        )
        expected = [(12, 720), (None, None), (None, None), (None, None), (None, None)]

        rules = jc.parse('nftables', data, quiet=True)[0]['chains'][0]['rules']
        self.assertEqual([(r['counter_packets'], r['counter_bytes']) for r in rules], expected)
        self.assertEqual(rules[0]['rule'], 'tcp dport 8080 counter packets 12 bytes 720 accept')

        raw_rules = jc.parse('nftables', data, raw=True, quiet=True)[0]['chains'][0]['rules']
        self.assertEqual((raw_rules[0]['counter_packets'], raw_rules[0]['counter_bytes']), ('12', '720'))


if __name__ == '__main__':
    unittest.main()
