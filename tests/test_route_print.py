import os
import unittest
import json
from typing import Dict
from jc.parsers.route_print import parse

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'windows_xp_route_print': (
                'fixtures/windows/windows-xp/route_print.out',
                'fixtures/windows/windows-xp/route_print.json'),
            'windows_7_route_print': (
                'fixtures/windows/windows-7/route_print.out',
                'fixtures/windows/windows-7/route_print.json'),
            'windows_2008_route_print': (
                'fixtures/windows/windows-2008/route_print.out',
                'fixtures/windows/windows-2008/route_print.json'),
            'windows_2016_route_print': (
                'fixtures/windows/windows-2016/route_print.out',
                'fixtures/windows/windows-2016/route_print.json'),
            'windows_10_route_print': (
                'fixtures/windows/windows-10/route_print.out',
                'fixtures/windows/windows-10/route_print.json'),
            'windows_11_route_print': (
                'fixtures/windows/windows-11/route_print.out',
                'fixtures/windows/windows-11/route_print.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_route_print_nodata(self):
        """
        Test 'route_print' with no data
        """
        self.assertEqual(parse('', quiet=True), {})


    def test_route_print_windows_xp(self):
        """
        Test 'route_print' on Windows XP
        """
        self.assertEqual(
            parse(self.f_in['windows_xp_route_print'], quiet=True),
            self.f_json['windows_xp_route_print']
        )

    def test_route_print_windows_7(self):
        """
        Test 'route_print' on Windows 7
        """
        self.assertEqual(
            parse(self.f_in['windows_7_route_print'], quiet=True),
            self.f_json['windows_7_route_print']
        )

    def test_route_print_windows_2008(self):
        """
        Test 'route_print' on Windows 2008
        """
        self.assertEqual(
            parse(self.f_in['windows_2008_route_print'], quiet=True),
            self.f_json['windows_2008_route_print']
        )

    def test_route_print_windows_2016(self):
        """
        Test 'route_print' on Windows 2016
        """
        self.assertEqual(
            parse(self.f_in['windows_2016_route_print'], quiet=True),
            self.f_json['windows_2016_route_print']
        )

    def test_route_print_windows_10(self):
        """
        Test 'route_print' on Windows 10
        """
        self.assertEqual(
            parse(self.f_in['windows_10_route_print'], quiet=True),
            self.f_json['windows_10_route_print']
        )

    def test_route_print_windows_11(self):
        """
        Test 'route_print' on Windows 11
        """
        self.assertEqual(
            parse(self.f_in['windows_11_route_print'], quiet=True),
            self.f_json['windows_11_route_print']
        )


if __name__ == '__main__':
    unittest.main()
