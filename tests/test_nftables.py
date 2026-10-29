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

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/nftables--wrapped-set-elements.out'), 'r', encoding='utf-8') as f:
        generic_nftables_wrapped_set_elements = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/nftables--wrapped-set-elements.json'), 'r', encoding='utf-8') as f:
        generic_nftables_wrapped_set_elements_json = json.loads(f.read())

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

    def test_nftables_chain_header_fields(self):
        """
        Test 'nftables' chain header priority, devices, and handle: the
        priority ends at the first `;` after it and is null when no `;`
        follows it
        """
        cases = {
            'type filter hook input priority filter; policy drop;': ('filter', [], 'drop'),
            'type filter hook input priority filter - 10; policy drop;': ('filter - 10', [], 'drop'),
            'type filter hook input priority   0;': ('0', [], None),
            'type filter hook input priority 0': (None, [], None),
            'type filter hook input; priority 0': (None, [], None),
            'type filter hook input priority priority 0; policy drop;': ('priority 0', [], 'drop'),
            'type filter hook input ' + 'priority ' * 200 + '0': (None, [], None),
            'type filter hook ingress device eth0 priority 0;': ('0', ['eth0'], None),
            'type filter hook ingress device = "eth0" priority 0;': ('0', ['eth0'], None),
            'type filter hook ingress devices   =   { "eth0", "eth1" } priority 0;': ('0', ['eth0', 'eth1'], None)
        }

        for header, expected in cases.items():
            with self.subTest(header):
                data = 'table ip t {\n\tchain c {\n\t\t' + header + '    # handle 9\n\t}\n}\n'
                chain = jc.parse('nftables', data, quiet=True)[0]['chains'][0]
                self.assertEqual((chain['priority'], chain['devices'], chain['policy']), expected)

    def test_nftables_rule_blank_run(self):
        """
        Test 'nftables' keeps a long run of blanks inside a rule and still
        finds the trailing handle
        """
        rule = 'accept comment "a' + ' ' * 5000 + 'b"'
        data = 'table ip t {\n\tchain c {\n\t\t' + rule + ' # handle 5\n\t\tdrop' + ' ' * 5000 + 'x\n\t}\n}\n'
        rules = jc.parse('nftables', data, quiet=True)[0]['chains'][0]['rules']
        self.assertEqual([(r['rule'], r['handle']) for r in rules], [(rule, 5), ('drop' + ' ' * 5000 + 'x', None)])

    def test_nftables_wrapped_set_elements(self):
        """
        Test 'nftables' with a set whose elements wrap over many lines and
        rules with counters inside braces
        """
        self.assertEqual(jc.parse('nftables', self.generic_nftables_wrapped_set_elements, quiet=True), self.generic_nftables_wrapped_set_elements_json)

    def test_nftables_wrapped_statement_handle(self):
        """
        Test 'nftables' keeps the handle of a statement that wraps over more
        lines than a block opener can, and of a closing brace
        """
        lines = ''.join(f'\t\t\t{i},\n' for i in range(20))
        data = 'table ip t { # handle 1\n\tset s {\n\t\ttype integer\n\t\telements = { 0,\n' + lines + '\t\t\t99 } # handle 2\n\t} # handle 3\n}\n'
        table = jc.parse('nftables', data, quiet=True)[0]
        self.assertEqual(table['handle'], 1)
        self.assertEqual(table['sets'][0]['elements'], ['0'] + [str(i) for i in range(20)] + ['99'])

    def test_nftables_wrapped_closing_brace_handle(self):
        """
        Test 'nftables' with a closing brace whose handle comment wraps
        """
        data = 'table ip t {\n\tchain c {\n\t\taccept\n\t} #\nhandle\n5\n}\n'
        table = jc.parse('nftables', data, quiet=True)[0]
        self.assertEqual([r['rule'] for r in table['chains'][0]['rules']], ['accept'])

    def test_nftables_line_break_in_quoted_string(self):
        """
        Test 'nftables' with line-break characters inside a quoted comment
        """
        for sep in ('\n', '\r\n', '\r', '\x0b', '\x0c', '\x1c', '\x85', ' ', ' '):
            with self.subTest(sep=repr(sep)):
                comment = 'web' + sep + '}' + sep + 'chain unused { # handle 7' + sep + 'comment '
                data = ('table inet filter { # handle 1\n\tchain input { # handle 1\n'
                        '\t\ttype filter hook input priority filter; policy drop;\n'
                        '\t\ttcp dport 443 accept comment "' + comment + '" # handle 4\n'
                        '\t\ttcp dport 22 accept # handle 5\n\t}\n}\n')
                chains = jc.parse('nftables', data, quiet=True)[0]['chains']
                self.assertEqual([c['name'] for c in chains], ['input'])
                self.assertEqual([r['handle'] for r in chains[0]['rules']], [4, 5])
                self.assertEqual(chains[0]['rules'][0]['rule'], 'tcp dport 443 accept comment "' + comment + '"')

    def test_nftables_unterminated_quoted_string_warns(self):
        """
        Test 'nftables' warns when the input ends inside a quoted string
        """
        for data in ('table ip t {\n\tchain c {\n\t\taccept comment "x\n\t}\n}\n',
                     'table ip t {\n}\ncomment "x\n'):
            with self.subTest(data=data):
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr):
                    result = jc.parse('nftables', data)
                self.assertEqual(result[0]['name'], 't')
                self.assertIn('Some input was skipped', stderr.getvalue())

    def test_nftables_quoted_device_with_brace(self):
        """
        Test 'nftables' with a quoted device name that contains '}'
        """
        data = (
            'table netdev t {\n'
            '\tchain c1 {\n'
            '\t\ttype filter hook ingress devices = { "a}b", "eth0" } priority filter; policy accept;\n'
            '\t}\n'
            '\n'
            '\tchain c2 {\n'
            '\t\ttype filter hook ingress device "a}b" priority filter; policy accept;\n'
            '\t}\n'
            '}\n'
        )
        chains = jc.parse('nftables', data, quiet=True)[0]['chains']
        self.assertEqual([(x['name'], x['devices']) for x in chains], [('c1', ['a}b', 'eth0']), ('c2', ['a}b'])])
        self.assertEqual([(x['priority'], x['policy']) for x in chains], [('filter', 'accept'), ('filter', 'accept')])


if __name__ == '__main__':
    unittest.main()
