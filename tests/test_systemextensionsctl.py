import unittest
import os
import sys
sys.path.append(os.getcwd())
from tests import utils_for_test as test_utils
sys.path.pop()
import jc.parsers.systemextensionsctl
from jc.exceptions import ParseError


class MyTests(unittest.TestCase):

    def test_systemextensionsctl_nodata(self):
        """
        Test 'systemextensionsctl' with no data
        """
        test_utils.run_no_data(self, __file__, [])

    def test_systemextensionsctl_all_fixtures(self):
        """
        Test 'systemextensionsctl' with various fixtures
        """
        test_utils.run_all_fixtures(self, __file__)

    def test_systemextensionsctl_raw(self):
        """
        Test 'systemextensionsctl list' raw output keeps the enabled and active
        markers and the '-' team ID
        """
        with open('tests/fixtures/generic/systemextensionsctl--list-team-id-dash.out', 'r', encoding='utf-8') as f:
            data = f.read()
        result = jc.parsers.systemextensionsctl.parse(data, raw=True, quiet=True)
        self.assertEqual([(x['enabled'], x['active'], x['team_id']) for x in result],
                         [('*', '*', 'G43BCU2T37'), ('*', '*', '-')])

    def test_systemextensionsctl_invalid_line(self):
        """
        Test 'systemextensionsctl list' with lines that are not extension rows
        """
        header = '1 extension(s)\n--- com.apple.system_extension.driver_extension\nenabled\tactive\tteamID\tbundleID (version)\tname\t[state]\n'
        for line in ['*\t*\tG43BCU2T37\torg.example.ext (1.0)\tExt\t[activated enabled]',
                     '*    *    G43BCU2T37    org.example.ext (1.0/1)    Ext    [activated enabled]']:
            with self.subTest(line=line):
                with self.assertRaises(ParseError):
                    jc.parsers.systemextensionsctl.parse(header + line + '\n', quiet=True)


if __name__ == '__main__':
    unittest.main()
