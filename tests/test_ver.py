import unittest
from jc.parsers.ver import parse


class MyTests(unittest.TestCase):

    def test_ver_nodata(self):
        """
        Test 'ver' with no data
        """
        self.assertEqual(parse('', quiet=True), {})


    def test_ver_strict_strings(self):
        strict_strings = {
            '0.4': {'major': 0, 'minor': 4, 'patch': 0, 'prerelease': None, 'prerelease_num': None, 'strict': True},
            '0.4.0': {'major': 0, 'minor': 4, 'patch': 0, 'prerelease': None, 'prerelease_num': None, 'strict': True},
            '0.4.1': {'major': 0, 'minor': 4, 'patch': 1, 'prerelease': None, 'prerelease_num': None, 'strict': True},
            '0.5a1': {'major': 0, 'minor': 5, 'patch': 0, 'prerelease': 'a', 'prerelease_num': 1, 'strict': True},
            '0.5b3': {'major': 0, 'minor': 5, 'patch': 0, 'prerelease': 'b', 'prerelease_num': 3, 'strict': True},
            '0.5': {'major': 0, 'minor': 5, 'patch': 0, 'prerelease': None, 'prerelease_num': None, 'strict': True},
            '0.9.6': {'major': 0, 'minor': 9, 'patch': 6, 'prerelease': None, 'prerelease_num': None, 'strict': True},
            '1.0': {'major': 1, 'minor': 0, 'patch': 0, 'prerelease': None, 'prerelease_num': None, 'strict': True},
            '1.0.4a3': {'major': 1, 'minor': 0, 'patch': 4, 'prerelease': 'a', 'prerelease_num': 3, 'strict': True},
            '1.0.4b1': {'major': 1, 'minor': 0, 'patch': 4, 'prerelease': 'b', 'prerelease_num': 1, 'strict': True},
            '1.0.4': {'major': 1, 'minor': 0, 'patch': 4, 'prerelease': None, 'prerelease_num': None, 'strict': True}
        }

        for ver_string, expected in strict_strings.items():
            self.assertEqual(parse(ver_string, quiet=True), expected)

    def test_ver_loose_strings(self):
        loose_strings = {
            '1': {'components': [1], 'strict': False},
            '2.7.2.2': {'components': [2, 7, 2, 2], 'strict': False},
            '1.3.a4': {'components': [1, 3, 'a', 4], 'strict': False},
            '1.3pl1': {'components': [1, 3, 'pl', 1], 'strict': False},
            '1.3c4': {'components': [1, 3, 'c', 4], 'strict': False}
        }

        for ver_string, expected in loose_strings.items():
            self.assertEqual(parse(ver_string, quiet=True), expected)

if __name__ == '__main__':
    unittest.main()
